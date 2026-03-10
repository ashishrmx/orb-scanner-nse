# config.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class ORBConfig:
    market: str = "NSE"
    orb_window_minutes: int = 15          # Opening range window
    min_volume: int = 500_000             # Min volume filter
    min_gap_pct: float = 0.3              # Min gap % to qualify
    max_range_pct: float = 5.0            # Max ORB range % filter
    risk_reward_min: float = 1.5          # Minimum R:R for signal
    stop_buffer_pct: float = 0.3          # % below ORB low for stop
    target_multiplier: float = 2.0        # R:R target multiplier
    max_symbols: int = 50

    # NSE F&O / large cap watchlist
    symbols: List[str] = field(default_factory=lambda: [
        "TATASTEEL.NS", "NTPC.NS", "HINDUNILVR.NS", "BANKBARODA.NS",
        "RELIANCE.NS", "M&M.NS", "LT.NS", "HDFCBANK.NS", "KOTAKBANK.NS",
        "CANBK.NS", "IOC.NS", "BAJFINANCE.NS", "PNB.NS", "ONGC.NS",
        "ICICIBANK.NS", "ADANIPORTS.NS", "COALINDIA.NS", "SBIN.NS",
        "INFY.NS", "TCS.NS", "WIPRO.NS", "AXISBANK.NS", "POWERGRID.NS",
        "BPCL.NS", "GAIL.NS", "HEROMOTOCO.NS", "EICHERMOT.NS",
        "DIVISLAB.NS", "DRREDDY.NS", "CIPLA.NS", "SUNPHARMA.NS",
        "TITAN.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS",
        "PIDILITIND.NS", "ULTRACEMCO.NS", "SHREECEM.NS", "GRASIM.NS",
        "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS",
        "BHARTIARTL.NS", "TECHM.NS", "HCLTECH.NS", "UPL.NS", "SRF.NS", 
        "TATACONSUM.NS"
    ])

CONFIG = ORBConfig()
