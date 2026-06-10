"""Markdown report of ALL profitable strategies with full metrics:
bot, asset, hour/params, entry-type, n_trades, WR, PF, profit.
Run on VPS -> writes reports/Profit_Strategies.md
"""
import MetaTrader5 as mt5
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from pathlib import Path
mt5.initialize()

DAYS = 30
to = datetime.now(timezone.utc); frm = to - timedelta(days=DAYS)
deals = mt5.history_deals_get(frm+timedelta(hours=3), to+timedelta(hours=3)) or []
acc = mt5.account_info(); bal = float(acc.balance) if acc else 0
MAGICS = {1338:"MATH",1339:"SWING",1340:"ORB",8338:"AMO"}
amo = json.loads(Path(r"C:\Proyectos\kha0sys3\src\execution\bot_config_amo8.json").read_text(encoding="utf-8"))
amo_tail = {s["id"].split("_")[-1][:8]: s for s in amo["portfolio"]}
EVT = {"FBU":"FALSE_BREAK_UP","FBD":"FALSE_BREAK_DOWN","BU":"BREAK_UP","BD":"BREAK_DOWN"}

pos = {}
for d in deals:
    if d.magic not in MAGICS: continue
    if d.entry==0: pos[d.position_id]={"ent":d,"ex":[]}
    elif d.position_id in pos: pos[d.position_id]["ex"].append(d)

agg = defaultdict(lambda: {"n":0,"pnl":0.0,"w":0,"gw":0.0,"gl":0.0})
for pid,pp in pos.items():
    if not pp["ex"]: continue
    e=pp["ent"]
    pnl=sum(x.profit+x.commission+x.swap for x in pp["ex"])+e.commission+e.swap
    bot=MAGICS[e.magic]; sym=e.symbol; com=e.comment or ""; parts=com.split("|")
    hour="-"; entry="-"
    if bot=="MATH" and len(parts)>=4: hour=parts[3]; entry=f"{parts[2]}/{parts[1]}"
    elif bot=="ORB" and len(parts)>=2: hour=parts[1]; entry="ORB_breakout"
    elif bot=="AMO" and len(parts)>=4:
        cfg=amo_tail.get(parts[3]); entry=EVT.get(parts[2],parts[2])
        if cfg: hour=f"{cfg['magic_time']}/{cfg['or_duration_min']}m {cfg['direction']}"
    elif bot=="SWING": entry="swing_breakout"
    a=agg[(bot,sym,hour,entry)]; a["n"]+=1; a["pnl"]+=pnl
    if pnl>0: a["w"]+=1; a["gw"]+=pnl
    else: a["gl"]+=abs(pnl)

prof=[(k,v) for k,v in agg.items() if v["pnl"]>0]
prof.sort(key=lambda x:-x[1]["pnl"])

def pf(v): return v["gw"]/v["gl"] if v["gl"]>0 else 99.0

md=[f"# Estrategias en PROFIT — últimos {DAYS} días\n",
    f"**Generado:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · **Balance:** ${bal:,.2f}  ",
    f"**Estrategias en profit:** {len(prof)} de {len(agg)} con trades · "
    f"**Total ganado (solo positivas):** ${sum(v['pnl'] for _,v in prof):,.2f}\n",
    "## Todas las estrategias en profit (ordenadas por profit)\n",
    "| # | BOT | ACTIVO | HORARIO / PARAMS | TIPO ENTRADA | n | WR | PF | PROFIT |",
    "|---|---|---|---|---|---|---|---|---|"]
for i,((bot,sym,hour,entry),v) in enumerate(prof,1):
    wr=v["w"]/v["n"]*100 if v["n"] else 0
    p=pf(v); ps="∞" if p>=99 else f"{p:.2f}"
    md.append(f"| {i} | {bot} | {sym} | {hour} | {entry} | {v['n']} | {wr:.0f}% | {ps} | ${v['pnl']:+,.2f} |")

# per-bot sections
for bot in ["AMO","MATH","ORB","SWING"]:
    sub=[(k,v) for k,v in prof if k[0]==bot]
    if not sub: continue
    md.append(f"\n## {bot} — {len(sub)} en profit · ${sum(v['pnl'] for _,v in sub):,.2f}\n")
    md.append("| ACTIVO | HORARIO / PARAMS | TIPO ENTRADA | n | WR | PF | PROFIT |")
    md.append("|---|---|---|---|---|---|---|")
    for (b,sym,hour,entry),v in sub:
        wr=v["w"]/v["n"]*100 if v["n"] else 0
        p=pf(v); ps="∞" if p>=99 else f"{p:.2f}"
        md.append(f"| {sym} | {hour} | {entry} | {v['n']} | {wr:.0f}% | {ps} | ${v['pnl']:+,.2f} |")

md.append("\n## Notas\n")
md.append("- **HORARIO/PARAMS**: AMO = `magic_time/OR_dur DIRECCIÓN` · MATH = sesión · ORB = hora+rango OR")
md.append("- **TIPO ENTRADA**: AMO = FALSE_BREAK_UP/DOWN · MATH = setup/timeframe · ORB = breakout")
md.append("- **PF** = ganancia bruta / pérdida bruta (∞ = sin trades perdedores)")
md.append("- **n bajo (1-3)**: muestra pequeña, profit puede ser suerte — evaluar con cautela")
md.append(f"- Ventana: {DAYS} días. Incluye trades de configs ya purgadas que cerraron en el período.")

Path(r"C:\Proyectos\kha0sys3\reports\Profit_Strategies.md").write_text("\n".join(md),encoding="utf-8")
print(f"WROTE reports/Profit_Strategies.md — {len(prof)} estrategias en profit")
mt5.shutdown()
