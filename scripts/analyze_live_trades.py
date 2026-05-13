"""Pull live MT5 deal history for magic=1338 and analyze per-strategy.

Run on VPS via WinRM (deploy/vps_connection.py).
Output:
  reports/Live_Strategy_Analysis.md  (per strategy metrics)
  reports/live_strategy_trades.parquet
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


REMOTE_SCRIPT = r"""
import MetaTrader5 as mt5, json, sys
from datetime import datetime, timezone, timedelta
mt5.initialize()
MAGIC = 1338

# Pull last 60 days of deals
end = datetime.now(timezone.utc)
start = end - timedelta(days=60)

deals = mt5.history_deals_get(start, end) or []
math_deals = [d for d in deals if getattr(d, 'magic', 0) == MAGIC]

# Group by position_id (each trade has open + close deal)
positions = {}
for d in math_deals:
    pid = d.position_id
    if pid not in positions:
        positions[pid] = {
            'position_id': pid,
            'symbol': d.symbol,
            'comment_open': '',
            'comment_close': '',
            'open_time': None, 'open_price': None,
            'close_time': None, 'close_price': None,
            'volume': 0.0,
            'profit_usd': 0.0,
            'swap': 0.0,
            'commission': 0.0,
            'direction': None,
        }
    rec = positions[pid]
    # entry=0 = IN, entry=1 = OUT
    if d.entry == 0:
        rec['comment_open'] = d.comment or ''
        rec['open_time'] = int(d.time)
        rec['open_price'] = float(d.price)
        rec['volume'] = float(d.volume)
        rec['direction'] = 'BUY' if d.type == 0 else 'SELL'
    elif d.entry == 1:
        rec['comment_close'] = d.comment or ''
        rec['close_time'] = int(d.time)
        rec['close_price'] = float(d.price)
        rec['profit_usd'] += float(d.profit)
        rec['swap'] += float(d.swap)
        rec['commission'] += float(d.commission)
    else:
        # entry=2 (correction) or other
        rec['profit_usd'] += float(d.profit)

# Also include the comments from ALL deals (some commissions land separately)
for d in math_deals:
    pid = d.position_id
    if pid in positions:
        positions[pid]['profit_usd'] += float(d.profit) if d.entry == 2 else 0
        positions[pid]['swap'] += float(d.swap) if d.entry == 2 else 0
        positions[pid]['commission'] += float(d.commission) if d.entry == 2 else 0

# Also pull current open positions
open_pos = mt5.positions_get() or []
math_open = [p for p in open_pos if p.magic == MAGIC]
open_list = []
for p in math_open:
    open_list.append({
        'ticket': p.ticket, 'symbol': p.symbol,
        'comment': p.comment or '',
        'time': int(p.time), 'price_open': float(p.price_open),
        'volume': float(p.volume), 'profit': float(p.profit),
        'direction': 'BUY' if p.type == 0 else 'SELL',
    })

# Account info
acct = mt5.account_info()
acct_dict = {
    'login': acct.login if acct else 0,
    'balance': float(acct.balance) if acct else 0,
    'equity': float(acct.equity) if acct else 0,
    'currency': acct.currency if acct else '',
} if acct else {}

out = {
    'pulled_at_utc': end.isoformat(),
    'window_start_utc': start.isoformat(),
    'magic': MAGIC,
    'account': acct_dict,
    'closed_positions': list(positions.values()),
    'open_positions': open_list,
}
sys.stdout.write(json.dumps(out, default=str))
mt5.shutdown()
"""


def parse_comment(comment: str) -> dict:
    """Comment format: M|<TF>|<SETUP_TAG>|<SESSION_TAG>"""
    parts = (comment or "").split("|")
    if len(parts) >= 4 and parts[0] == "M":
        return {"tf": parts[1], "setup_tag": parts[2], "session_tag": parts[3]}
    return {"tf": "?", "setup_tag": "?", "session_tag": "?"}


def main():
    sys.path.insert(0, ".")
    from deploy.vps_connection import VPSConnection
    vps = VPSConnection()

    print("Pulling MT5 deal history from VPS...")
    # Write a temp .py file via WinRM and execute it
    remote_path = r"C:\Proyectos\kha0sys3\_tmp_live_trades.py"
    import base64
    b64 = base64.b64encode(REMOTE_SCRIPT.encode("utf-8")).decode("ascii")
    # Use two-step approach: write base64 string to file, then decode it server-side
    chunks = [b64[i:i+1000] for i in range(0, len(b64), 1000)]
    vps.run_ps(rf"Remove-Item -Force '{remote_path}.b64' -ErrorAction SilentlyContinue")
    for i, ck in enumerate(chunks):
        op = ">>" if i > 0 else ">"
        vps.run_ps(f"'{ck}' {op} '{remote_path}.b64'")
    decode_cmd = (
        f"$b64 = Get-Content '{remote_path}.b64' -Raw; "
        f"$b64 = $b64 -replace '`r`n','' -replace ' ',''; "
        f"$bytes = [Convert]::FromBase64String($b64); "
        f"[IO.File]::WriteAllBytes('{remote_path}', $bytes); "
        f"Write-Output (Test-Path '{remote_path}')"
    )
    r2 = vps.run_ps(decode_cmd)
    print(f"Remote script created: {r2['stdout'].strip()}")
    r = vps.run_ps(rf"cd 'C:\Proyectos\kha0sys3'; C:\Python312\python.exe '{remote_path}'")
    vps.run_ps(f"Remove-Item -Force '{remote_path}','{remote_path}.b64' -ErrorAction SilentlyContinue")

    stdout = r["stdout"]
    if not stdout.strip():
        print("ERR: no data")
        print("STDERR:", r["stderr"][:500])
        return
    try:
        data = json.loads(stdout)
    except Exception as e:
        # Try to find JSON line in output
        for line in stdout.splitlines():
            try:
                data = json.loads(line)
                break
            except Exception:
                continue
        else:
            print("ERR parse JSON:", e)
            print("STDOUT:", stdout[:500])
            return

    closed = data.get("closed_positions", [])
    openp = data.get("open_positions", [])
    acct = data.get("account", {})
    print(f"Window: {data.get('window_start_utc')} -> {data.get('pulled_at_utc')}")
    print(f"Account: login={acct.get('login')} balance=${acct.get('balance', 0):.2f}")
    print(f"Closed positions: {len(closed)}  Open positions: {len(openp)}")

    # Load bot config for expectations
    cfg_path = Path("src/execution/bot_config_math.json")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    portfolio = cfg["portfolio"]

    # Build (sym, tf, setup, session) → strategy lookup. Symbol uses broker name.
    by_key = {}
    for p in portfolio:
        # Comment uses SHORT setup tag e.g. KAMA / SPECTRAL / VELOCITY / KALMAN / HURST / OLS
        SETUP_TAG = {
            "KAMA_CROSS_MOM": "KAMA",
            "SPECTRAL_TREND_MOM": "SPECTRAL",
            "VELOCITY_ACCEL_GO": "VELOCITY",
            "KALMAN_INNOV_EXPAND": "KALMAN",
            "HURST_TREND_MOM": "HURST",
            "OLS_SLOPE_STRONG": "OLS",
        }
        SESSION_TAG = {"ASIA": "ASIA", "LONDON": "LDN", "NY": "NY",
                       "LONDON_NY": "LDNNY", "ALL_DAY": "ALLDAY"}
        key = (p["sym"], p["tf"], SETUP_TAG.get(p["setup_type"], "?"),
               SESSION_TAG.get(p["session"], "?"))
        by_key[key] = p

    # Aggregate trades per strategy
    agg = defaultdict(lambda: {
        "n": 0, "wins": 0, "losses": 0,
        "gross_profit_usd": 0.0, "gross_loss_usd": 0.0,
        "net_profit_usd": 0.0,
        "swap_usd": 0.0, "commission_usd": 0.0,
        "first_trade": None, "last_trade": None,
    })

    import polars as pl
    rows_for_parquet = []

    for d in closed:
        c = parse_comment(d.get("comment_open") or d.get("comment_close"))
        key = (d["symbol"], c["tf"], c["setup_tag"], c["session_tag"])
        s = agg[key]
        s["n"] += 1
        profit_total = d.get("profit_usd", 0.0) + d.get("swap", 0.0) + d.get("commission", 0.0)
        if profit_total > 0:
            s["wins"] += 1
            s["gross_profit_usd"] += profit_total
        else:
            s["losses"] += 1
            s["gross_loss_usd"] += -profit_total  # store as positive abs
        s["net_profit_usd"] += profit_total
        s["swap_usd"] += d.get("swap", 0.0)
        s["commission_usd"] += d.get("commission", 0.0)
        t_open = d.get("open_time")
        if t_open:
            s["first_trade"] = min(s["first_trade"] or t_open, t_open)
            s["last_trade"] = max(s["last_trade"] or t_open, t_open)
        # Also save trade-level row
        rows_for_parquet.append({
            **{"strategy_key": f"{d['symbol']}|{c['tf']}|{c['setup_tag']}|{c['session_tag']}"},
            "position_id": d.get("position_id"),
            "symbol": d["symbol"], "tf": c["tf"], "setup_tag": c["setup_tag"],
            "session_tag": c["session_tag"], "direction": d.get("direction"),
            "volume": d.get("volume", 0),
            "open_time": d.get("open_time"), "close_time": d.get("close_time"),
            "open_price": d.get("open_price"), "close_price": d.get("close_price"),
            "profit_usd": d.get("profit_usd", 0),
            "swap_usd": d.get("swap", 0), "commission_usd": d.get("commission", 0),
            "net_usd": profit_total,
        })

    # Compose dataframe
    rows_strat = []
    for k, s in agg.items():
        broker_sym, tf, setup_tag, session_tag = k
        cfg_entry = by_key.get(k)
        wr = s["wins"] / s["n"] if s["n"] else 0.0
        pf = s["gross_profit_usd"] / s["gross_loss_usd"] if s["gross_loss_usd"] > 0 else float("inf")
        avg_net = s["net_profit_usd"] / s["n"] if s["n"] else 0
        first_t = datetime.fromtimestamp(s["first_trade"], tz=timezone.utc).isoformat() if s["first_trade"] else "-"
        last_t = datetime.fromtimestamp(s["last_trade"], tz=timezone.utc).isoformat() if s["last_trade"] else "-"
        rows_strat.append({
            "symbol": broker_sym, "tf": tf, "setup_tag": setup_tag,
            "session_tag": session_tag,
            "in_config": cfg_entry is not None,
            "strategy_id": (cfg_entry or {}).get("id", "-"),
            "expected_wr": (cfg_entry or {}).get("expected_wr", None),
            "expected_pf": (cfg_entry or {}).get("expected_pf", None),
            "expected_pf_oos": (cfg_entry or {}).get("expected_pf_oos", None),
            "robustness": (cfg_entry or {}).get("robustness_label", "?"),
            "n_trades": s["n"], "wins": s["wins"], "losses": s["losses"],
            "win_rate": wr, "pf": pf, "avg_net_usd": avg_net,
            "gross_profit_usd": s["gross_profit_usd"],
            "gross_loss_usd": s["gross_loss_usd"],
            "net_profit_usd": s["net_profit_usd"],
            "swap_usd": s["swap_usd"], "commission_usd": s["commission_usd"],
            "first_trade_utc": first_t, "last_trade_utc": last_t,
        })

    df = pl.DataFrame(rows_strat).sort("n_trades", descending=True)
    df.write_parquet("reports/live_strategy_analysis.parquet")
    if rows_for_parquet:
        pl.DataFrame(rows_for_parquet).write_parquet("reports/live_strategy_trades.parquet")
    print(f"\nWrote {len(df)} strategy aggregates")

    # Stats
    total_n = sum(r["n_trades"] for r in rows_strat)
    total_net = sum(r["net_profit_usd"] for r in rows_strat)
    total_wins = sum(r["wins"] for r in rows_strat)
    print(f"\n=== AGGREGATE LIVE (60 days) ===")
    print(f"Total closed trades: {total_n}")
    print(f"Total wins: {total_wins} ({100*total_wins/max(total_n,1):.1f}%)")
    print(f"Total net P&L: ${total_net:+.2f}")
    print(f"Open positions: {len(openp)}")
    print(f"\n=== STRATEGIES THAT TRADED ===")
    print(f"Distinct strategies in deal stream: {len(df)}")
    print(f"In config (recognized): {len(df.filter(pl.col('in_config')))} / {len(df)}")
    print(f"NOT in current config (likely from K3-97 deploy): "
          f"{len(df.filter(~pl.col('in_config')))}")
    print(f"\nConfigured strategies WITHOUT trades: "
          f"{len(portfolio) - len(df.filter(pl.col('in_config')))}/{len(portfolio)}")

    # Markdown report
    md = ["# Live Strategy Analysis — MT5 deal history (60 days)",
          f"",
          f"Pulled at {data['pulled_at_utc']}",
          f"Account: login={acct.get('login')} balance=${acct.get('balance', 0):.2f} {acct.get('currency','')}",
          f"Window: {data['window_start_utc']} → {data['pulled_at_utc']}",
          "",
          "## Summary",
          f"- Total closed trades: **{total_n}**",
          f"- Total wins: **{total_wins}** ({100*total_wins/max(total_n,1):.1f}%)",
          f"- Total net P&L: **${total_net:+.2f}**",
          f"- Open positions now: {len(openp)}",
          f"- Distinct strategies that fired trades: {len(df)}",
          f"- Of those, in current K3M1-75 config: {len(df.filter(pl.col('in_config')))}",
          f"- K3M1-75 strategies that have NOT fired yet: "
          f"{len(portfolio) - len(df.filter(pl.col('in_config')))}/{len(portfolio)}",
          "",
          "## Por TF (signal timeframe)",
          "",
          "| TF | n strats | n trades | wins | WR | Net USD |",
          "|---|---|---|---|---|---|"]
    for tfv in ["M1", "M15", "H1", "H4", "?"]:
        sub = df.filter(pl.col("tf") == tfv)
        if len(sub) == 0: continue
        nt = int(sub["n_trades"].sum())
        w = int(sub["wins"].sum())
        nv = float(sub["net_profit_usd"].sum())
        wr = 100 * w / max(nt, 1)
        md.append(f"| **{tfv}** | {len(sub)} | {nt} | {w} | {wr:.1f}% | ${nv:+.2f} |")

    md += ["", "## Por setup", "",
           "| Setup | n strats | n trades | WR | Net USD |",
           "|---|---|---|---|---|"]
    for r in df.group_by("setup_tag").agg([
        pl.len().alias("n_strats"),
        pl.col("n_trades").sum().alias("nt"),
        pl.col("wins").sum().alias("w"),
        pl.col("net_profit_usd").sum().alias("nv"),
    ]).sort("nt", descending=True).iter_rows(named=True):
        wr = 100 * r["w"] / max(r["nt"], 1)
        md.append(f"| {r['setup_tag']} | {r['n_strats']} | {r['nt']} | {wr:.1f}% | ${r['nv']:+.2f} |")

    md += ["", "## Per-strategy detail (ranked by trades)", "",
           "| Symbol | TF | Setup | Sess | In cfg | Robust | n | WR | PF | Net USD | Expected PF OOS |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in df.iter_rows(named=True):
        pf_str = f"{r['pf']:.2f}" if r["pf"] != float("inf") else "inf"
        ev_pf = r["expected_pf_oos"]
        ev_pf_str = f"{ev_pf:.2f}" if ev_pf is not None else "-"
        cfg_str = "✓" if r["in_config"] else "✗ (legacy)"
        md.append(f"| {r['symbol']} | {r['tf']} | {r['setup_tag']} | "
                  f"{r['session_tag']} | {cfg_str} | {r['robustness']} | "
                  f"{r['n_trades']} | {r['win_rate']*100:.1f}% | {pf_str} | "
                  f"${r['net_profit_usd']:+.2f} | {ev_pf_str} |")

    md += ["", "## K3M1-75 strategies WITHOUT live activity (cold)",
           "", "These haven't fired since deploy — either session not active yet, "
           "or signal condition hasn't met.", "",
           "| ID | Symbol | TF | Setup | Sess | Robust | Expected tpy |",
           "|---|---|---|---|---|---|---|"]
    # Find configured strategies with no trades
    SETUP_TAG = {
        "KAMA_CROSS_MOM": "KAMA", "SPECTRAL_TREND_MOM": "SPECTRAL",
        "VELOCITY_ACCEL_GO": "VELOCITY", "KALMAN_INNOV_EXPAND": "KALMAN",
        "HURST_TREND_MOM": "HURST", "OLS_SLOPE_STRONG": "OLS",
    }
    SESSION_TAG = {"ASIA": "ASIA", "LONDON": "LDN", "NY": "NY",
                   "LONDON_NY": "LDNNY", "ALL_DAY": "ALLDAY"}
    traded_keys = set()
    for r in df.iter_rows(named=True):
        traded_keys.add((r["symbol"], r["tf"], r["setup_tag"], r["session_tag"]))
    cold = []
    for p in portfolio:
        key = (p["sym"], p["tf"], SETUP_TAG.get(p["setup_type"], "?"),
               SESSION_TAG.get(p["session"], "?"))
        if key not in traded_keys:
            cold.append(p)
    for p in sorted(cold, key=lambda x: x["sym"]):
        md.append(f"| {p['id']} | {p['sym']} | {p['tf']} | {p['setup_type']} | "
                  f"{p['session']} | {p.get('robustness_label','?')} | "
                  f"{p.get('expected_trades_per_year', 0):.0f} |")

    Path("reports/Live_Strategy_Analysis.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nReport: reports/Live_Strategy_Analysis.md")
    print(f"Parquets: reports/live_strategy_analysis.parquet, reports/live_strategy_trades.parquet")


if __name__ == "__main__":
    main()
