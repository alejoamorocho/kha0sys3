"""Live performance breakdown of the CURRENT portfolio (post profit-purge).

Purge/deploy of the profit-only portfolio: 2026-06-09 ~19:41 UTC (commit
780b791/a4a835c). This report filters closed trades to that window so the
numbers reflect what is live NOW, not the purged legacy strategies.

Breakdown by bot, symbol, strategy (comment) and session/hour. ASCII only.
deal.time is server time (UTC+3); we subtract 3h to display real UTC.
Run on the VPS where MT5 is connected.
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict

mt5.initialize()
MAGICS = {1338: "MATH", 1339: "SWING", 1340: "ORB", 8338: "AMO8"}
SRV_OFF = timedelta(hours=3)  # broker server = UTC+3

PURGE_UTC = datetime(2026, 6, 9, 20, 0, tzinfo=timezone.utc)
now = datetime.now(timezone.utc)
cutoff_srv_epoch = (PURGE_UTC + SRV_OFF).timestamp()
days = (now - PURGE_UTC).total_seconds() / 86400.0

# Query a wide window, then filter precisely by entry epoch.
frm = now - timedelta(days=14)
deals = mt5.history_deals_get(frm + SRV_OFF, now + SRV_OFF) or []

positions = {}
for d in deals:
    if d.magic not in MAGICS:
        continue
    if d.entry == 0:
        positions[d.position_id] = {"ent": d, "exits": []}
    elif d.position_id in positions:
        positions[d.position_id]["exits"].append(d)

trades = []
for pid, pp in positions.items():
    if not pp["exits"]:
        continue
    e = pp["ent"]
    if e.time < cutoff_srv_epoch:      # pre-purge -> skip
        continue
    pnl = sum(x.profit + x.commission + x.swap for x in pp["exits"]) + e.commission + e.swap
    cmt = (e.comment or "").strip()
    parts = cmt.split("|")
    # session / hour label per bot
    if e.magic == 1338 and len(parts) >= 4:
        sess = parts[3]                # MATH encodes session (ASIA/LDN/NY/...)
    elif e.magic in (1339, 1340) and len(parts) >= 2:
        sess = parts[1]                # ORB encodes open window (07h30m...)
    else:
        sess = "OR"
    utc_open = datetime.utcfromtimestamp(e.time) - SRV_OFF
    trades.append({
        "magic": e.magic, "bot": MAGICS[e.magic], "sym": e.symbol,
        "cmt": cmt, "strat": cmt.split("]")[0][:30], "pnl": pnl,
        "sess": sess, "hour": utc_open.hour,
        "type": "BUY" if e.type == 0 else "SELL",
    })


def stats(ts):
    pnls = [t["pnl"] for t in ts]
    n = len(pnls)
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    ws, ls = sum(wins), abs(sum(losses))
    pf = (ws / ls) if ls > 0 else (float("inf") if ws > 0 else 0.0)
    return {
        "n": n, "wr": (len(wins) / n if n else 0), "pf": pf,
        "tot": sum(pnls), "avg": (sum(pnls) / n if n else 0),
        "best": max(pnls) if pnls else 0, "worst": min(pnls) if pnls else 0,
    }


def agg(ts, keyfn):
    g = defaultdict(list)
    for t in ts:
        g[keyfn(t)].append(t)
    rows = [(k, stats(v)) for k, v in g.items()]
    rows.sort(key=lambda r: -r[1]["tot"])
    return rows


def pf_s(pf):
    return "INF" if pf == float("inf") else f"{pf:.2f}"


def mark(tot):
    return "+" if tot > 0 else ("." if tot == 0 else "x")


print("=" * 78)
print(f"  PORTAFOLIO ACTUAL (post-purga) — desde {PURGE_UTC:%Y-%m-%d %H:%M} UTC  (~{days:.1f} dias)")
print("=" * 78)
g = stats(trades)
print(f"  TOTAL: {g['n']} trades   WR={g['wr']*100:.1f}%   PF={pf_s(g['pf'])}   NETO=${g['tot']:+,.2f}")
print()
print("  -- POR BOT --")
print(f"  {'bot':<7}{'n':>5}{'WR':>7}{'PF':>7}{'neto':>13}{'avg':>10}")
for (bot,), s in agg(trades, lambda t: (t["bot"],)):
    print(f"  {mark(s['tot'])} {bot:<5}{s['n']:>5}{s['wr']*100:>6.1f}%{pf_s(s['pf']):>7}${s['tot']:>+11.2f}${s['avg']:>+8.2f}")

print()
print("  -- POR ACTIVO (todos los bots) --")
print(f"  {'sym':<10}{'n':>5}{'WR':>7}{'PF':>7}{'neto':>13}")
for (sym,), s in agg(trades, lambda t: (t["sym"],)):
    print(f"  {mark(s['tot'])} {sym:<8}{s['n']:>5}{s['wr']*100:>6.1f}%{pf_s(s['pf']):>7}${s['tot']:>+11.2f}")

print()
print("  -- POR ESTRATEGIA (bot + sym + comentario), ordenado por neto --")
print(f"  {'bot':<6}{'sym':<10}{'estrategia':<26}{'n':>4}{'WR':>6}{'PF':>6}{'neto':>11}{'avg':>9}")
for (bot, sym, strat), s in agg(trades, lambda t: (t["bot"], t["sym"], t["strat"])):
    print(f"  {mark(s['tot'])} {bot:<4}{sym:<10}{strat:<26}{s['n']:>4}{s['wr']*100:>5.0f}%{pf_s(s['pf']):>6}${s['tot']:>+9.2f}${s['avg']:>+7.2f}")

print()
print("  -- POR HORARIO (hora UTC de apertura, todos los bots) --")
print(f"  {'horaUTC':<8}{'n':>5}{'WR':>7}{'PF':>7}{'neto':>13}")
rows = agg(trades, lambda t: (t["hour"],))
rows.sort(key=lambda r: r[0][0])
for (h,), s in rows:
    print(f"  {mark(s['tot'])} {h:02d}:00  {s['n']:>4}{s['wr']*100:>6.1f}%{pf_s(s['pf']):>7}${s['tot']:>+11.2f}")

print()
print("  -- MATH por SESION (comentario) --")
print(f"  {'sesion':<10}{'n':>5}{'WR':>7}{'PF':>7}{'neto':>13}")
mt = [t for t in trades if t["magic"] == 1338]
for (sess,), s in agg(mt, lambda t: (t["sess"],)):
    print(f"  {mark(s['tot'])} {sess:<8}{s['n']:>5}{s['wr']*100:>6.1f}%{pf_s(s['pf']):>7}${s['tot']:>+11.2f}")

mt5.shutdown()
