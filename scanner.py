# scanner.py
import pandas as pd
import numpy as np
from config import ORBConfig
from data_feed import get_prev_close, get_intraday_data, compute_orb
from typing import List, Dict

def compute_gap_pct(open_price: float, prev_close: float) -> float:
    if prev_close is None or prev_close == 0:
        return 0.0
    return ((open_price - prev_close) / prev_close) * 100

def determine_signal(current_price: float, orb_high: float, orb_low: float) -> str:
    """Classify current price position relative to ORB."""
    if current_price > orb_high:
        return "LONG"
    elif current_price < orb_low:
        return "SHORT"
    else:
        # Check proximity: within 0.5% of boundary = WATCH, deep inside = INSIDE
        range_size = orb_high - orb_low
        from_high = (orb_high - current_price) / range_size
        from_low = (current_price - orb_low) / range_size
        if from_high < 0.3 or from_low < 0.3:
            return "WATCH"
        return "INSIDE"

def compute_rr(signal: str, current_price: float, orb_high: float,
               orb_low: float, stop_buffer_pct: float = 0.3,
               target_multiplier: float = 2.0) -> tuple:
    """Compute entry, stop, target and R:R ratio."""
    buf = stop_buffer_pct / 100

    if signal == "LONG":
        entry = orb_high * 1.001         # small breakout buffer
        stop = orb_low * (1 - buf)
        risk = entry - stop
        target = entry + (risk * target_multiplier)
    elif signal == "SHORT":
        entry = orb_low * 0.999
        stop = orb_high * (1 + buf)
        risk = stop - entry
        target = entry - (risk * target_multiplier)
    else:
        # WATCH: compute hypothetical breakout R:R
        entry = orb_high * 1.001
        stop = orb_low * (1 - buf)
        risk = entry - stop
        target = entry + (risk * target_multiplier)

    if risk <= 0:
        rr = 0.0
    else:
        actual_risk = abs(entry - stop)
        actual_reward = abs(target - entry)
        rr = round(actual_reward / actual_risk, 1) if actual_risk > 0 else 0.0

    return round(entry, 2), round(stop, 2), round(target, 2), rr

def compute_vol_x(volume: int, avg_volume: int) -> float:
    """Volume multiplier vs average."""
    if avg_volume == 0:
        return 0.0
    return round(volume / avg_volume, 1)

def scan_symbol(symbol: str, config: ORBConfig) -> dict | None:
    """Run full ORB scan on a single symbol. Returns result dict or None."""
    import yfinance as yf

    df = get_intraday_data(symbol, interval="1m")
    if df.empty:
        return None

    orb = compute_orb(df, config.orb_window_minutes)
    if orb is None:
        return None

    prev_close = get_prev_close(symbol)
    if prev_close is None:
        return None

    gap_pct = compute_gap_pct(orb["open_price"], prev_close)
    chg_pct = ((orb["current_price"] - prev_close) / prev_close) * 100

    # Apply filters
    if orb["volume"] < config.min_volume:
        return None
    if abs(gap_pct) < config.min_gap_pct:
        return None
    if orb["orb_range_pct"] > config.max_range_pct:
        return None

    signal = determine_signal(orb["current_price"], orb["orb_high"], orb["orb_low"])
    entry, stop, target, rr = compute_rr(
        signal, orb["current_price"], orb["orb_high"], orb["orb_low"],
        config.stop_buffer_pct, config.target_multiplier
    )

    # Average volume from 5-day data
    try:
        hist = yf.Ticker(symbol).history(period="10d", interval="1d")
        avg_vol = int(hist["Volume"].mean()) if not hist.empty else orb["volume"]
    except Exception:
        avg_vol = orb["volume"]

    vol_x = compute_vol_x(orb["volume"], avg_vol)

    clean_symbol = symbol.replace(".NS", "").replace(".BO", "")

    return {
        "symbol": clean_symbol,
        "price": orb["current_price"],
        "chg_pct": round(chg_pct, 2),
        "gap_pct": round(gap_pct, 2),
        "orb_high": orb["orb_high"],
        "orb_low": orb["orb_low"],
        "range_pct": round(orb["orb_range_pct"], 2),
        "signal": signal,
        "volume": orb["volume"],
        "vol_x": vol_x,
        "rr": rr,
        "entry": entry,
        "stop": stop,
        "target": target,
        "prev_close": prev_close,
    }

def run_scan(config: ORBConfig) -> List[Dict]:
    """Scan all configured symbols and return filtered results."""
    results = []
    for symbol in config.symbols[:config.max_symbols]:
        result = scan_symbol(symbol, config)
        if result:
            results.append(result)
    return results
