# trade_plan.py
from typing import Dict

def generate_trade_plan(result: Dict) -> Dict:
    """
    Build a complete deterministic trade plan from scanned result.
    """
    signal = result["signal"]
    price = result["price"]
    orb_high = result["orb_high"]
    orb_low = result["orb_low"]
    orb_range = orb_high - orb_low

    # Position within ORB (0% = at low, 100% = at high, >100% = breakout)
    if orb_range > 0:
        position_pct = ((price - orb_low) / orb_range) * 100
    else:
        position_pct = 50.0

    risk_pct = abs((result["entry"] - result["stop"]) / result["entry"]) * 100

    plan = {
        "symbol": result["symbol"],
        "signal": signal,
        "score": result.get("score", 0),
        "current_price": price,
        "gap_pct": result["gap_pct"],
        "chg_pct": result["chg_pct"],
        "orb_high": orb_high,
        "orb_low": orb_low,
        "range_pct": result["range_pct"],
        "entry": result["entry"],
        "stop": result["stop"],
        "target": result["target"],
        "rr": result["rr"],
        "risk_pct": round(risk_pct, 2),
        "position_pct": round(position_pct, 1),
        "volume": result["volume"],
        "vol_x": result["vol_x"],
    }

    return plan
