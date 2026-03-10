# main.py
import time
from datetime import datetime
import pytz

from config import CONFIG
from scanner import run_scan
from scorer import score_all
from trade_plan import generate_trade_plan
from display import console, render_header, render_table, render_trade_plan

IST = pytz.timezone("Asia/Kolkata")

def main():
    console.clear()
    scan_start = datetime.now(IST)
    scan_time_str = scan_start.strftime("%H:%M:%S")

    console.print(f"\n[dim]Scanning {len(CONFIG.symbols)} symbols... please wait.[/]\n")

    # 1. Scan
    raw_results = run_scan(CONFIG)

    # 2. Score & sort
    scored = score_all(raw_results)

    # 3. Summary stats
    total = len(CONFIG.symbols)
    passed = len(scored)
    long_c  = sum(1 for r in scored if r["signal"] == "LONG")
    short_c = sum(1 for r in scored if r["signal"] == "SHORT")
    watch_c = sum(1 for r in scored if r["signal"] == "WATCH")
    inside_c = sum(1 for r in scored if r["signal"] == "INSIDE")
    avg_range = sum(r["range_pct"] for r in scored) / passed if passed else 0

    # 4. Render
    console.clear()
    render_header(CONFIG, scan_time_str, total, passed,
                  long_c, short_c, watch_c, inside_c, avg_range)
    render_table(scored)

    # 5. Top trade plan
    if scored:
        top = scored[0]
        plan = generate_trade_plan(top)
        render_trade_plan(plan)

    console.print(f"\n[dim]Next scan in 60 seconds... (Ctrl+C to exit)[/]")

if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(60)    # Auto-refresh every 60 seconds
    except KeyboardInterrupt:
        console.print("\n[bold red]Scanner stopped.[/]")
