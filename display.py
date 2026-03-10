# display.py (FULL MODIFIED VERSION - only score_bar + table column fixed)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich import box
from rich.style import Style
from datetime import datetime
import pytz
from typing import List, Dict

console = Console()
IST = pytz.timezone("Asia/Kolkata")

SIGNAL_STYLES = {
    "LONG":   ("▲ LONG",   "bold green"),
    "SHORT":  ("▼ SHORT",  "bold red"),
    "WATCH":  ("◆ WATCH",  "bold yellow"),
    "INSIDE": ("⇌ INSIDE", "bold cyan"),
}

def fmt_price(val: float) -> str:
    return f"₹{val:,.2f}"

def fmt_pct(val: float) -> str:
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.2f}%"

def score_bar(score: int, width: int = 8) -> str:
    """Render score as compact bar + number - FIXED VERSION."""
    filled = int((score / 100) * (width - 2))  # Reserve 2 chars for number
    bar_chars = "█" * filled + "░" * (width - 2 - filled)
    
    color = "green" if score >= 60 else "yellow" if score >= 40 else "red"
    num_style = "bold white"
    
    return f"[{color}]{bar_chars}[/{color}][{num_style}]{score:2d}[/{num_style}]"

def render_header(config, scan_time: str, total: int, passed: int,
                  long_c: int, short_c: int, watch_c: int, inside_c: int,
                  avg_range: float):
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

    header_text = (
        f"[bold cyan]ORB[/] [dim]SCREENER[/]\n"
        f"[bold white]Opening Range Breakout — {config.orb_window_minutes}-Min Strategy[/]\n"
        f"[dim]{config.market} Markets[/]"
    )
    console.print(Panel(header_text, border_style="cyan", width=70))

    config_text = (
        f"[bold]CONFIG[/]\n"
        f"  Market      : [cyan]{config.market}[/]\n"
        f"  ORB Range   : [cyan]{config.orb_window_minutes} minutes[/]\n"
        f"  Min Volume  : [cyan]{config.min_volume:,}[/]\n"
        f"  Min Gap     : [cyan]{config.min_gap_pct}%[/]\n"
        f"  Max Range   : [cyan]{config.max_range_pct}%[/]\n"
        f"  Symbols     : [cyan]{config.max_symbols} stocks[/]"
    )
    console.print(Panel(config_text, border_style="dim white", width=70))

    console.print(
        f"\n[bold cyan]ORB SCANNER — {now}[/]  [dim]|[/]  "
        f"[white]{total} symbols scanned[/]"
    )
    console.print(f"[dim]Scan complete. {passed} symbols passed filters.[/]\n")

    summary = (
        f"[bold]SCAN SUMMARY   {scan_time}[/]\n\n"
        f"Total Passed : [white]{passed}[/]   |   "
        f"[green]▲ Long: {long_c}[/]   |   "
        f"[red]▼ Short: {short_c}[/]   |   "
        f"[yellow]◆ Watch: {watch_c}[/]   |   "
        f"[cyan]⇌ Inside: {inside_c}[/]\n"
        f"Avg ORB Range : [white]{avg_range:.2f}%[/]   |   "
        f"ORB Window : [cyan]{config.orb_window_minutes} min[/]"
    )
    console.print(Panel(summary, border_style="dim white", width=70))

def render_table(results: List[Dict]):
    table = Table(
        box=box.SIMPLE_HEAD,
        border_style="dim white",
        header_style="bold white on black",
        show_lines=False,
        pad_edge=True,
        width=120
    )

    cols = [
        ("SYMBOL",   "left",  "bold white"),
        ("PRICE",    "right", "white"),
        ("CHG%",     "right", "white"),
        ("GAP%",     "right", "white"),
        ("ORB-H",    "right", "green"),
        ("ORB-L",    "right", "red"),
        ("RANGE%",   "right", "white"),
        ("SIGNAL",   "left",  "white"),
        ("VOL",      "right", "white"),
        ("VOL-X",    "right", "white"),
        ("R:R",      "right", "white"),
        ("SCORE",    "center", "white"),  # FIXED: center + width control
    ]
    for col, justify, style in cols[:-1]:  # All except SCORE
        table.add_column(col, justify=justify, style=style, no_wrap=True)
    
    # FIXED SCORE COLUMN
    table.add_column("SCORE", justify="center", style="white", width=10, no_wrap=True)

    def fmt_vol(v: int) -> str:
        if v >= 1_00_00_000:
            return f"{v/1_00_00_000:.1f}Cr"
        elif v >= 1_00_000:
            return f"{v/1_00_000:.1f}L"
        return f"{v:,}"

    for r in results:
        sig_text, sig_style = SIGNAL_STYLES.get(r["signal"], ("?", "white"))
        chg_style = "green" if r["chg_pct"] >= 0 else "red"
        gap_style = "green" if r["gap_pct"] >= 0 else "red"
        rr_style = "bold green" if r["rr"] >= 3 else ("yellow" if r["rr"] >= 2 else "red")

        table.add_row(
            Text(r["symbol"], style="bold white"),
            fmt_price(r["price"]),
            Text(fmt_pct(r["chg_pct"]), style=chg_style),
            Text(fmt_pct(r["gap_pct"]), style=gap_style),
            Text(fmt_price(r["orb_high"]), style="green"),
            Text(fmt_price(r["orb_low"]), style="red"),
            f"{r['range_pct']:.2f}%",
            Text(sig_text, style=sig_style),
            fmt_vol(r["volume"]),
            f"{r['vol_x']}×",
            Text(f"{r['rr']}:1", style=rr_style),
            score_bar(r["score"]),  # FIXED: Perfect "████ 87" format
        )

    console.print(table)

def render_trade_plan(plan: Dict):
    sig_text, sig_style = SIGNAL_STYLES.get(plan["signal"], ("?", "white"))

    # Position visualizer bar
    pos = min(max(plan["position_pct"], 0), 200)
    bar_width = 20
    if pos <= 100:
        filled = int((pos / 100) * bar_width)
        bar = "·" * filled + "◆" + "·" * (bar_width - filled - 1)
    else:
        bar = "·" * bar_width + "◆"

    header = (
        f"[bold green]●[/] [bold white]{plan['symbol']}[/]  "
        f"[{sig_style}]{sig_text}[/]  "
        f"[dim]\\[Score: {plan['score']}/100][/]"
    )

    body = (
        f"\n[bold]Current Price :[/] [white]{fmt_price(plan['current_price'])}[/]   "
        f"Gap: [{'green' if plan['gap_pct']>=0 else 'red'}]{fmt_pct(plan['gap_pct'])}[/]   "
        f"Change: [{'green' if plan['chg_pct']>=0 else 'red'}]{fmt_pct(plan['chg_pct'])}[/]\n"
        f"[bold]ORB High :[/] [green]{fmt_price(plan['orb_high'])}[/]   "
        f"[bold]ORB Low:[/] [red]{fmt_price(plan['orb_low'])}[/]   "
        f"Range: [white]{plan['range_pct']:.2f}%[/]\n"
        f"[bold]Position     :[/] [dim]|{bar}[/] [white]({plan['position_pct']:.0f}%)[/]\n\n"
        f"[bold green]Entry  → {fmt_price(plan['entry'])}[/]\n"
        f"[bold red]Stop   → {fmt_price(plan['stop'])}[/]  "
        f"[dim]({plan['risk_pct']:.2f}% risk)[/]\n"
        f"[bold cyan]Target → {fmt_price(plan['target'])}[/]  "
        f"[dim](R:R {plan['rr']}:1)[/]"
    )

    console.print(Panel(
        header + body,
        title="[bold]TOP SETUP — TRADE PLAN[/]",
        border_style="green",
        width=70
    ))
