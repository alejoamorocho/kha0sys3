"""Edge ranking of the live portfolio measured in PIPS (size-independent).

Dollar PnL is distorted because MATH is oversized ~10-30x vs AMO8/ORB, so it
cannot be used to compare edge across strategies. Pips (price move normalized
by the symbol pip size, volume-weighted across partial exits) remove position
size entirely. Reports every strategy with NET PIPS > 0, ranked by net pips,
plus PF(pips), WR, avg pips/trade and dollar PnL for reference.

Window: post profit-purge (2026-06-09 20:00 UTC). Run on the VPS.
Pip size: point*10 for 3/5-digit FX, else point (printed per symbol as a note).
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict

mt5.initialize()
MAGICS = {1338: "MATH", 1339: "SWING", 1340: "ORB", 8338: "AMO8"}
SRV_OFF = timedelta(hours=3)
PURGE_UTC = datetime(2026, 6, 9, 20, 0, tzinfo=timezone.utc)
now = datetime.now(timezone.utc)
cut = (PURGE_UTC + SRV_OFF).timestamp()
days = (now - PURGE_UTC).total_seconds() / 86400.0

deals = mt5.history_deals_get(now - timedelta(days=14) + SRV_OFF, now + SRV_OFF) or []

_pip_cache = {}
def pip_size(sym):
    if sym in _pip_cache:
        return _pip_cache[sym]
    mt5.symbol_select(sym, True)
    si = mt5.symbol_info(sym)
    if si is None:
        ps = 0.01 if "JPY" in sym else 0.0001
    else:
        ps = si.point * 10 if si.digits in (3, 5) else si.point
    _pip_cache[sym] = ps
    return ps

positions = {}
for d in deals:
    if d.magic not in MAGICS:
        continue
    if d.entry == 0:
        positions[d.position_id] = {"e": d, "x": []}
    elif d.position_id in positions:
        positions[d.position_id]["x"].append(d)

rows = defaultdict(list)   # key -> list of {pips, usd}
for pid, pp in positions.items():
    e = pp["e"]
    if not pp["x"] or e.time < cut:
        continue
    ps = pip_size(e.symbol)
    tot_v = sum(x.volume for x in pp["x"]) or e.volume
    pips = 0.0
    for x in pp["x"]:
        move = (x.price - e.price) if e.type == 0 else (e.price - x.price)
        pips += (move / ps) * (x.volume / tot_v)
    usd = sum(x.profit + x.commission + x.swap for x in pp["x"]) + e.commission + e.swap
    cmt = (e.comment or "").strip()
    key = (MAGICS[e.magic], e.symbol, cmt)
    rows[key].append({"pips": pips, "usd": usd})


def strat_stats(ts):
    n = len(ts)
    pl = [t["pips"] for t in ts]
    wins = [p for p in pl if p > 0]
    gw = sum(p for p in pl if p > 0)
    gl = abs(sum(p for p in pl if p < 0))
    pf = (gw / gl) if gl > 0 else (float("inf") if gw > 0 else 0.0)
    return {
        "n": n, "wr": len(wins) / n, "pf": pf,
        "net_pips": sum(pl), "avg_pips": sum(pl) / n,
        "net_usd": sum(t["usd"] for t in ts),
    }


data = [(k, strat_stats(v)) for k, v in rows.items()]
positives = [(k, s) for k, s in data if s["net_pips"] > 0]
positives.sort(key=lambda r: -r[1]["net_pips"])

print("=" * 92)
print(f"  EDGE EN PIPS — estrategias POSITIVAS (post-purga, {PURGE_UTC:%Y-%m-%d} UTC, ~{days:.0f} dias)")
print("=" * 92)
print(f"  {'#':>2} {'bot':<5}{'simbolo':<10}{'estrategia':<22}{'n':>4}{'WR':>6}{'PF':>7}{'netoPips':>11}{'pips/op':>9}{'usd_ref':>11}")
for i, (k, s) in enumerate(positives, 1):
    bot, sym, cmt = k
    pf = "INF" if s["pf"] == float("inf") else f"{s['pf']:.2f}"
    print(f"  {i:>2} {bot:<5}{sym:<10}{cmt:<22}{s['n']:>4}{s['wr']*100:>5.0f}%{pf:>7}{s['net_pips']:>+11.1f}{s['avg_pips']:>+9.1f}${s['net_usd']:>+9.0f}")

tot_pips = sum(s["net_pips"] for _, s in positives)
print(f"\n  {len(positives)} estrategias con pips netos positivos. Suma pips netos (solo positivas): {tot_pips:+,.1f}")

print("\n  Pip size por simbolo (1 pip = ):")
for sym in sorted(_pip_cache):
    print(f"    {sym:<10} {_pip_cache[sym]}")

mt5.shutdown()
