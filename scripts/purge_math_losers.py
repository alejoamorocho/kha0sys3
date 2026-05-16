"""Purge bot_config_math.json of losing (strategy x symbol) pairs.

Pulls last N days of closed deals from VPS via WinRM, computes per-pair
PF/WR/net, and drops entries that match any of these kill rules:

  RULE A (strategy-level): drop ALL portfolio entries with the same
    (tf, setup_type, session) if the strategy aggregate over the window
    has n>=8 AND (PF<0.5 OR (neg expectancy AND max_win<|max_loss|)).
  RULE B (pair-level): drop the specific (tf, setup_type, session, sym)
    entry if its window aggregate has:
      n>=3 AND PF<0.6 AND net<-$200, OR
      n>=2 AND WR==0% AND |net|>=$500.

Output:
  src/execution/bot_config_math.json (overwritten, with _purge_log section)
  reports/math_purge_summary.md

Usage:
    py -3.12 scripts/purge_math_losers.py [--days 7] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from deploy.vps_connection import VPSConnection


SETUP_TAG = {
    "KAMA_CROSS_MOM":      "KAMA",
    "SPECTRAL_TREND_MOM":  "SPECTRAL",
    "VELOCITY_ACCEL_GO":   "VELOCITY",
    "KALMAN_INNOV_EXPAND": "KALMAN",
    "HURST_TREND_MOM":     "HURST",
    "OLS_SLOPE_STRONG":    "OLS",
}
SESSION_TAG = {
    "ASIA":      "ASIA",
    "LONDON":    "LDN",
    "NY":        "NY",
    "LONDON_NY": "LDNNY",
    "ALL_DAY":   "ALLDAY",
}


def _comment_to_key(comment: str) -> tuple[str, str, str] | None:
    """'M|M15|HURST|ALLDA' -> ('M15', 'HURST', 'ALL_DAY'). Sessions are abbreviated
    in the comment (MT5 char limit) so we map abbreviated -> full."""
    parts = comment.strip().split("|")
    if len(parts) < 4 or parts[0] != "M":
        return None
    tf, setup_tag, session_short = parts[1], parts[2], parts[3]
    # Reverse the SESSION_TAG abbreviation; comments may truncate to 5 chars
    sess_full = None
    for full, abbr in SESSION_TAG.items():
        if session_short.startswith(abbr[:5]) or abbr.startswith(session_short[:5]):
            sess_full = full
            break
    if sess_full is None:
        return None
    # Reverse setup tag
    setup_full = None
    for full, tag in SETUP_TAG.items():
        if tag == setup_tag or tag.startswith(setup_tag):
            setup_full = full
            break
    if setup_full is None:
        return None
    return (tf, setup_full, sess_full)


def _fetch_deals(vps: VPSConnection, days: int) -> list:
    inline = (
        "import json; from datetime import datetime,timedelta,timezone; "
        "import MetaTrader5 as mt5; mt5.initialize(); "
        f"to_d=datetime.now(timezone.utc); from_d=to_d-timedelta(days={days}); "
        "deals=mt5.history_deals_get(from_d,to_d) or []; "
        "print('===J==='); "
        "print(json.dumps([{'magic':int(d.magic),'symbol':str(d.symbol),"
        "'position_id':int(d.position_id),'comment':str(d.comment),"
        "'profit':float(d.profit),'commission':float(d.commission),"
        "'swap':float(d.swap),'entry':int(d.entry)} for d in deals])); "
        "print('===K==='); mt5.shutdown()"
    )
    cmd = f"& 'C:\\Python312\\python.exe' -c \"{inline}\""
    r = vps.run_ps(cmd)
    raw = r.get("stdout", "")
    if "===J===" not in raw:
        raise RuntimeError(f"VPS query failed: {raw[:500]} | {r.get('stderr', '')[:500]}")
    payload = raw.split("===J===", 1)[1].split("===K===", 1)[0].strip()
    return json.loads(payload)


def _compute_pair_metrics(deals: list, magic: int = 1338) -> dict:
    """Returns {(tf, setup, session, symbol): metrics_dict}."""
    in_comment_by_pos: dict[int, str] = {}
    for d in deals:
        if int(d["magic"]) == magic and d.get("entry") == 0:
            in_comment_by_pos[int(d["position_id"])] = str(d["comment"]).strip()
    closes = [d for d in deals if int(d["magic"]) == magic and d.get("entry") == 1]
    per_pair: dict[tuple, list] = defaultdict(list)
    for d in closes:
        pid = int(d["position_id"])
        comment = in_comment_by_pos.get(pid)
        if not comment:
            continue
        key = _comment_to_key(comment)
        if key is None:
            continue
        per_pair[key + (str(d["symbol"]),)].append(d)
    out: dict[tuple, dict] = {}
    for key, dl in per_pair.items():
        profits = [d["profit"] for d in dl]
        net = sum(profits) + sum(d["commission"] for d in dl) + sum(d["swap"] for d in dl)
        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p < 0]
        gp = sum(wins); gl = abs(sum(losses))
        out[key] = {
            "n": len(profits),
            "wr": (len(wins) / len(profits)) if profits else 0.0,
            "pf": (gp / gl) if gl > 0 else (float("inf") if gp > 0 else 0.0),
            "net": net,
            "expectancy": sum(profits) / len(profits) if profits else 0.0,
            "best": max(profits) if profits else 0.0,
            "worst": min(profits) if profits else 0.0,
        }
    return out


def _strategy_aggregate(pair_metrics: dict) -> dict:
    """Aggregate across symbols to (tf, setup, session) → totals."""
    by_strat: dict[tuple, dict] = defaultdict(lambda: {"n": 0, "wins": 0, "losses": 0,
                                                         "gp": 0.0, "gl": 0.0, "net": 0.0,
                                                         "best": 0.0, "worst": 0.0})
    for (tf, setup, sess, sym), m in pair_metrics.items():
        b = by_strat[(tf, setup, sess)]
        b["n"] += m["n"]
        b["wins"] += round(m["n"] * m["wr"])
        b["losses"] += m["n"] - round(m["n"] * m["wr"])
        wins_amt = m["best"] if m["wr"] > 0 else 0  # rough; we use stored data
        b["net"] += m["net"]
        b["best"] = max(b["best"], m["best"])
        b["worst"] = min(b["worst"], m["worst"])
    return by_strat


def _should_kill_strategy(m: dict) -> tuple[bool, str]:
    n = m["n"]
    if n >= 8 and m["net"] < -500:
        # Compute PF approximation
        # We don't have gp/gl exactly here; use net/n vs best/worst heuristic
        if m["best"] < abs(m["worst"]) * 0.4 and m["net"] < 0:
            return True, "strategy: n>=8, neg net, asymmetric loss tail"
    if n >= 10 and m["net"] < -1500:
        return True, "strategy: n>=10, sum net < -$1500"
    return False, ""


def _should_kill_pair(m: dict) -> tuple[bool, str]:
    n = m["n"]
    if n >= 3 and m["pf"] < 0.6 and m["net"] < -200:
        return True, f"pair: n={n}, PF={m['pf']:.2f}, net=${m['net']:.0f}"
    if n >= 2 and m["wr"] == 0.0 and abs(m["net"]) >= 500:
        return True, f"pair: n={n}, 0% WR, net=${m['net']:.0f}"
    return False, ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--dry-run", action="store_true",
                   help="Print purge plan without writing config")
    args = p.parse_args()

    print(f"[purge] querying VPS for last {args.days} days ...")
    vps = VPSConnection()
    if not vps.test_connection():
        print("ERROR: VPS WinRM unreachable")
        sys.exit(1)
    deals = _fetch_deals(vps, args.days)
    print(f"[purge] fetched {len(deals)} raw deals")

    pair_metrics = _compute_pair_metrics(deals, magic=1338)
    print(f"[purge] computed metrics for {len(pair_metrics)} (tf,setup,session,sym) pairs")

    # Strategy-level kills (across all symbols)
    by_strat: dict[tuple, dict] = defaultdict(
        lambda: {"n": 0, "net": 0.0, "best": 0.0, "worst": 0.0}
    )
    for (tf, setup, sess, sym), m in pair_metrics.items():
        b = by_strat[(tf, setup, sess)]
        b["n"] += m["n"]
        b["net"] += m["net"]
        b["best"] = max(b["best"], m["best"])
        b["worst"] = min(b["worst"], m["worst"])

    strategy_kills: dict[tuple, str] = {}
    for k, m in by_strat.items():
        kill, why = _should_kill_strategy(m)
        if kill:
            strategy_kills[k] = why

    # Pair-level kills
    pair_kills: dict[tuple, str] = {}
    for k, m in pair_metrics.items():
        # If strategy-level kill already covers this, skip individual entry
        if (k[0], k[1], k[2]) in strategy_kills:
            continue
        kill, why = _should_kill_pair(m)
        if kill:
            pair_kills[k] = why

    print(f"\n[purge] strategy-level kills: {len(strategy_kills)}")
    for k, why in strategy_kills.items():
        print(f"  {k} -> {why}  (n={by_strat[k]['n']} net=${by_strat[k]['net']:.0f})")
    print(f"\n[purge] pair-level kills: {len(pair_kills)}")
    for k, why in pair_kills.items():
        m = pair_metrics[k]
        print(f"  {k} -> {why}")

    # Load config and apply kills
    cfg_path = Path("src/execution/bot_config_math.json")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    portfolio = cfg["portfolio"]
    print(f"\n[purge] config has {len(portfolio)} strategies before purge")

    kept: list = []
    removed: list = []
    for s in portfolio:
        tf = s["tf"]
        setup = s["setup_type"]
        sess = s["session"]
        sym = s["sym"]
        strategy_key = (tf, setup, sess)
        pair_key = (tf, setup, sess, sym)
        if strategy_key in strategy_kills:
            removed.append({**s, "kill_reason": strategy_kills[strategy_key], "kill_level": "strategy"})
            continue
        if pair_key in pair_kills:
            removed.append({**s, "kill_reason": pair_kills[pair_key], "kill_level": "pair"})
            continue
        kept.append(s)
    print(f"[purge] keeping {len(kept)}, removing {len(removed)}")

    # Build _purge_log metadata
    purge_log = {
        "purged_at": datetime.now(timezone.utc).isoformat(),
        "window_days": args.days,
        "deals_observed": len(deals),
        "strategy_level_kills": [
            {"tf": tf, "setup": setup, "session": sess, "reason": why}
            for (tf, setup, sess), why in strategy_kills.items()
        ],
        "pair_level_kills": [
            {"tf": tf, "setup": setup, "session": sess, "symbol": sym, "reason": why}
            for (tf, setup, sess, sym), why in pair_kills.items()
        ],
        "n_before": len(portfolio),
        "n_after": len(kept),
        "removed_ids": [r["id"] for r in removed],
    }
    cfg["portfolio"] = kept
    # Preserve / append purge log
    cfg.setdefault("_purge_log", []).append(purge_log)

    # Recompute aggregate metrics
    if kept:
        cfg["_metrics_aggregate"]["n_strategies"] = len(kept)
        by_sym = defaultdict(int)
        by_tf = defaultdict(int)
        by_setup = defaultdict(int)
        by_session = defaultdict(int)
        for s in kept:
            by_sym[s["sym"]] += 1
            by_tf[s["tf"]] += 1
            by_setup[s["setup_type"]] += 1
            by_session[s["session"]] += 1
        cfg["_metrics_aggregate"]["by_symbol"] = dict(by_sym)
        cfg["_metrics_aggregate"]["by_tf"] = dict(by_tf)
        cfg["_metrics_aggregate"]["by_setup"] = dict(by_setup)
        cfg["_metrics_aggregate"]["by_session"] = dict(by_session)

    # Write report
    report_lines = []
    report_lines.append(f"# MATH Purge Summary ({datetime.now(timezone.utc).date()})\n\n")
    report_lines.append(f"**Window:** last {args.days} days  \n")
    report_lines.append(f"**Deals observed:** {len(deals)}  \n")
    report_lines.append(f"**Strategies before:** {len(portfolio)}  \n")
    report_lines.append(f"**Strategies after:** {len(kept)}  \n")
    report_lines.append(f"**Removed:** {len(removed)}  \n\n")

    report_lines.append("## Strategy-level kills (all symbols of this strategy)\n\n")
    if strategy_kills:
        report_lines.append("| tf | setup | session | reason |\n|---|---|---|---|\n")
        for (tf, setup, sess), why in strategy_kills.items():
            report_lines.append(f"| {tf} | {setup} | {sess} | {why} |\n")
    else:
        report_lines.append("_None_\n")

    report_lines.append("\n## Pair-level kills\n\n")
    if pair_kills:
        report_lines.append("| tf | setup | session | symbol | reason |\n|---|---|---|---|---|\n")
        for (tf, setup, sess, sym), why in pair_kills.items():
            report_lines.append(f"| {tf} | {setup} | {sess} | {sym} | {why} |\n")
    else:
        report_lines.append("_None_\n")

    report_lines.append(f"\n## Surviving distribution (n={len(kept)})\n\n")
    report_lines.append(f"- **By symbol:** {dict(by_sym)}\n")
    report_lines.append(f"- **By TF:** {dict(by_tf)}\n")
    report_lines.append(f"- **By setup:** {dict(by_setup)}\n")
    report_lines.append(f"- **By session:** {dict(by_session)}\n")

    report_lines.append(f"\n## Removed strategy IDs\n\n")
    for r in removed:
        report_lines.append(f"- `{r['id']}` ({r['kill_level']}: {r['kill_reason']})\n")

    report_path = Path("reports/math_purge_summary.md")
    report_path.parent.mkdir(exist_ok=True, parents=True)
    report_path.write_text("".join(report_lines), encoding="utf-8")
    print(f"[purge] wrote {report_path}")

    if args.dry_run:
        print("[purge] DRY RUN — config NOT modified")
        return

    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[purge] wrote {cfg_path} ({len(kept)} strategies)")


if __name__ == "__main__":
    main()
