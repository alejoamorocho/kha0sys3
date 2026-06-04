"""Generate a comprehensive markdown stats report for MATH, ORB, AMO8.

Pulls MT5 closed-trade history, attributes each trade to its bot (magic) and
strategy (comment), and cross-references AMO8 config indices to recover
schedule hour / OR duration / event type / direction. Breaks down PnL by
every meaningful dimension so the user can decide what to keep or cut.

Writes: reports/Live_Stats_Report.md  (also prints path)
Run on VPS.
"""
import MetaTrader5 as mt5
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from pathlib import Path

DAYS = 30
OUT = r"C:\Proyectos\kha0sys3\reports\Live_Stats_Report.md"

mt5.initialize()
acc = mt5.account_info()
balance = float(acc.balance) if acc else 0.0

to = datetime.now(timezone.utc)
frm = to - timedelta(days=DAYS)
deals = mt5.history_deals_get(frm + timedelta(hours=3), to + timedelta(hours=3)) or []

MAGICS = {1338: "MATH", 1339: "SWING", 1340: "ORB", 8338: "AMO8"}

# Load AMO8 config to map config index -> dimensions
amo_cfg = json.loads(Path(r"C:\Proyectos\kha0sys3\src\execution\bot_config_amo8.json").read_text(encoding="utf-8"))
# index map: the strategy id ends with _NNN; comment is AMO|OR_|<EVT>|<idx_or_tail>
# We map by the id tail used in make_order_comment: last "_"-split token, first 8 chars
amo_by_tail = {}
for s in amo_cfg["portfolio"]:
    tail = s["id"].split("_")[-1][:8]
    amo_by_tail[tail] = s

# Build closed trades
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
    ent = pp["ent"]
    pnl = sum(x.profit + x.commission + x.swap for x in pp["exits"]) + ent.commission + ent.swap
    comment = ent.comment or ""
    rec = {"magic": ent.magic, "bot": MAGICS[ent.magic], "sym": ent.symbol,
           "comment": comment, "pnl": pnl, "vol": ent.volume, "time": ent.time,
           "dir": "LONG" if ent.type == 0 else "SHORT"}
    # Parse dimensions per bot
    rec["hour"] = rec["dur"] = rec["event"] = rec["session"] = rec["setup"] = rec["tf"] = None
    if rec["bot"] == "MATH" and comment.startswith("M|"):
        parts = comment.split("|")
        if len(parts) >= 4:
            rec["tf"], rec["setup"], rec["session"] = parts[1], parts[2], parts[3]
    elif rec["bot"] == "ORB" and comment.startswith("O|"):
        parts = comment.split("|")
        if len(parts) >= 3:
            rec["hour"] = parts[1]  # e.g. "13h30m"
    elif rec["bot"] == "AMO8":
        parts = comment.split("|")
        if len(parts) >= 4:
            evt_tag = parts[2]
            tail = parts[3]
            rec["event"] = {"FBU": "FALSE_BREAK_UP", "FBD": "FALSE_BREAK_DOWN"}.get(evt_tag, evt_tag)
            cfg = amo_by_tail.get(tail)
            if cfg:
                rec["hour"] = cfg.get("magic_time")
                rec["dur"] = f"{cfg.get('or_duration_min')}m"
                rec["dir"] = cfg.get("direction", rec["dir"])
    trades.append(rec)


def agg(rows):
    n = len(rows)
    if n == 0:
        return None
    wins = [r for r in rows if r["pnl"] > 0]
    losses = [r for r in rows if r["pnl"] < 0]
    ws = sum(r["pnl"] for r in wins)
    ls = abs(sum(r["pnl"] for r in losses))
    pf = (ws / ls) if ls > 0 else (float("inf") if ws > 0 else 0.0)
    total = sum(r["pnl"] for r in rows)
    return {"n": n, "wins": len(wins), "wr": len(wins)/n, "pf": pf,
            "total": total, "avg": total/n,
            "best": max(r["pnl"] for r in rows), "worst": min(r["pnl"] for r in rows)}


def group_by(rows, key):
    g = defaultdict(list)
    for r in rows:
        g[r[key]].append(r)
    out = []
    for k, rs in g.items():
        a = agg(rs)
        a["key"] = k
        out.append(a)
    return sorted(out, key=lambda x: -x["total"])


def pf_str(pf):
    return "INF" if pf == float("inf") else f"{pf:.2f}"


def table(rows_agg, label="key"):
    lines = [f"| {label} | trades | WR | PF | PnL | avg | best | worst |",
             "|---|---|---|---|---|---|---|---|"]
    for a in rows_agg:
        mark = "🟢" if a["total"] > 0 else ("⚪" if a["total"] == 0 else "🔴")
        lines.append(f"| {mark} {a['key']} | {a['n']} | {a['wr']*100:.0f}% | {pf_str(a['pf'])} | "
                     f"${a['total']:+,.0f} | ${a['avg']:+,.0f} | ${a['best']:+,.0f} | ${a['worst']:+,.0f} |")
    return "\n".join(lines)


md = []
md.append(f"# Live Stats Report — {DAYS} días")
md.append(f"\n**Generado:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ")
md.append(f"**Balance:** ${balance:,.2f}  ")
md.append(f"**Trades cerrados:** {len(trades)}\n")

# Global summary per bot
md.append("## 1. Resumen por bot\n")
md.append(table(group_by(trades, "bot"), "bot"))

for bot in ["MATH", "ORB", "AMO8"]:
    bt = [r for r in trades if r["bot"] == bot]
    if not bt:
        md.append(f"\n## {bot}: 0 trades en el período\n")
        continue
    a = agg(bt)
    md.append(f"\n---\n\n## {bot} — {a['n']} trades · WR {a['wr']*100:.0f}% · PF {pf_str(a['pf'])} · PnL ${a['total']:+,.0f}\n")

    md.append(f"\n### {bot} · por símbolo\n")
    md.append(table(group_by(bt, "sym"), "símbolo"))

    md.append(f"\n### {bot} · por estrategia (comment)\n")
    md.append(table(group_by(bt, "comment"), "estrategia"))

    if bot == "AMO8":
        md.append(f"\n### {bot} · por HORARIO (magic_time UTC)\n")
        md.append(table([a for a in group_by(bt, "hour") if a["key"]], "horario"))
        md.append(f"\n### {bot} · por DURACIÓN OR\n")
        md.append(table([a for a in group_by(bt, "dur") if a["key"]], "or_dur"))
        md.append(f"\n### {bot} · por TIPO DE ENTRADA (evento)\n")
        md.append(table([a for a in group_by(bt, "event") if a["key"]], "evento"))
        md.append(f"\n### {bot} · por DIRECCIÓN\n")
        md.append(table(group_by(bt, "dir"), "dirección"))

    if bot == "MATH":
        md.append(f"\n### {bot} · por SESIÓN\n")
        md.append(table([a for a in group_by(bt, "session") if a["key"]], "sesión"))
        md.append(f"\n### {bot} · por SETUP\n")
        md.append(table([a for a in group_by(bt, "setup") if a["key"]], "setup"))
        md.append(f"\n### {bot} · por TIMEFRAME\n")
        md.append(table([a for a in group_by(bt, "tf") if a["key"]], "tf"))

    if bot == "ORB":
        md.append(f"\n### {bot} · por HORARIO/RANGO\n")
        md.append(table([a for a in group_by(bt, "hour") if a["key"]], "horario"))

# Decisiones sugeridas
md.append("\n---\n\n## Señales para decisión\n")
all_strats = group_by(trades, "comment")
strong = [a for a in all_strats if a["n"] >= 5 and a["pf"] != float("inf") and a["pf"] >= 1.5 and a["total"] > 0]
weak = [a for a in all_strats if a["n"] >= 5 and a["total"] < 0]
md.append(f"\n**Ganadoras sólidas (n≥5, PF≥1.5, PnL>0):** {len(strong)}\n")
if strong:
    md.append(table(sorted(strong, key=lambda x:-x["total"]), "estrategia"))
md.append(f"\n**Perdedoras a evaluar para cortar (n≥5, PnL<0):** {len(weak)}\n")
if weak:
    md.append(table(sorted(weak, key=lambda x:x["total"]), "estrategia"))

Path(OUT).write_text("\n".join(md), encoding="utf-8")
print(f"WROTE {OUT}")
print(f"trades={len(trades)} bots={set(r['bot'] for r in trades)}")
mt5.shutdown()
