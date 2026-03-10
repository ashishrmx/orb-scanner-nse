# scorer.py
from typing import Dict, List

# Weights that drive the score (must sum to 100)
WEIGHTS = {
    "rr_score":      30,   # R:R quality
    "vol_score":     25,   # Volume velocity
    "gap_score":     20,   # Gap magnitude / quality
    "range_score":   15,   # Tight ORB range (tighter = better)
    "signal_score":  10,   # Confirmed breakout vs watch vs inside
}

def score_symbol(result: Dict) -> int:
    """
    Deterministic scoring 0–100.
    Higher score = higher quality setup.
    """
    score = 0

    # 1. R:R Score (0–30)
    rr = result.get("rr", 0)
    if rr >= 4:
        score += 30
    elif rr >= 3:
        score += 24
    elif rr >= 2:
        score += 18
    elif rr >= 1.5:
        score += 10
    else:
        score += 0

    # 2. Volume Velocity (0–25)
    vol_x = result.get("vol_x", 0)
    if vol_x >= 2.0:
        score += 25
    elif vol_x >= 1.5:
        score += 20
    elif vol_x >= 1.0:
        score += 14
    elif vol_x >= 0.7:
        score += 8
    else:
        score += 0

    # 3. Gap Score (0–20): moderate gaps (0.5–2%) are ideal
    gap = abs(result.get("gap_pct", 0))
    if 0.5 <= gap <= 2.0:
        score += 20
    elif gap > 2.0:
        score += 10   # Large gap = potential exhaustion
    elif gap >= 0.3:
        score += 13
    else:
        score += 0

    # 4. Range Score (0–15): tighter range = better structure
    rng = result.get("range_pct", 5)
    if rng <= 0.75:
        score += 15
    elif rng <= 1.25:
        score += 12
    elif rng <= 2.0:
        score += 8
    elif rng <= 3.5:
        score += 4
    else:
        score += 0

    # 5. Signal Score (0–10)
    sig = result.get("signal", "INSIDE")
    signal_map = {"LONG": 10, "SHORT": 10, "WATCH": 5, "INSIDE": 0}
    score += signal_map.get(sig, 0)

    return min(score, 100)

def score_all(results: List[Dict]) -> List[Dict]:
    """Attach scores and sort by score descending."""
    for r in results:
        r["score"] = score_symbol(r)
    return sorted(results, key=lambda x: x["score"], reverse=True)
