# data_feed.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")

def get_prev_close(symbol: str) -> float:
    """Fetch previous day's closing price."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", interval="1d")
        if len(hist) >= 2:
            return float(hist["Close"].iloc[-2])
        return float(hist["Close"].iloc[-1])
    except Exception:
        return None

def get_intraday_data(symbol: str, interval: str = "1m") -> pd.DataFrame:
    """Fetch today's intraday 1-min OHLCV data."""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval=interval)
        if df.empty:
            return pd.DataFrame()
        df.index = df.index.tz_convert(IST)
        return df
    except Exception:
        return pd.DataFrame()

def compute_orb(df: pd.DataFrame, orb_minutes: int = 15) -> dict:
    """
    Extract the Opening Range (first N minutes after 9:15 AM IST).
    Returns orb_high, orb_low, orb_range_pct, open_price, current_price, volume.
    """
    if df.empty:
        return None

    market_open = df.index[0].replace(hour=9, minute=15, second=0, microsecond=0)
    orb_end = market_open + timedelta(minutes=orb_minutes)

    orb_data = df[df.index <= orb_end]
    if orb_data.empty:
        return None

    orb_high = float(orb_data["High"].max())
    orb_low = float(orb_data["Low"].min())
    open_price = float(orb_data["Open"].iloc[0])
    current_price = float(df["Close"].iloc[-1])
    total_volume = int(df["Volume"].sum())
    orb_range_pct = ((orb_high - orb_low) / orb_low) * 100

    return {
        "orb_high": orb_high,
        "orb_low": orb_low,
        "open_price": open_price,
        "current_price": current_price,
        "volume": total_volume,
        "orb_range_pct": orb_range_pct,
    }
