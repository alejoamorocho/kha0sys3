"""List ONLY profitable strategies with full breakdown: bot, asset, hour,
entry-type, profit. Run on VPS. Crosses comments with AMO8 config for hour/dur.
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
MAGICS = {1338:"MATH",1339:"SWING",1340:"ORB",8338:"AMO"}

# AMO8 config: map id-tail -> (magic_time, or_dur, event, direction)
amo = json.loads(Path(r"C:\Proyectos\kha0sys3\src\execution\bot_config_amo8.json").read_text(encoding="utf-8"))
amo_tail = {}
for s in amo["portfolio"]:
    tail = s["id"].split("_")[-1][:8]
    amo_tail[tail] = s

EVT = {"FBU":"FALSE_BREAK_UP","FBD":"FALSE_BREAK_DOWN","BU":"BREAK_UP","BD":"BREAK_DOWN"}

# build positions
pos = {}
for d in deals:
    if d.magic not in MAGICS: continue
    if d.entry==0: pos[d.position_id]={"ent":d,"ex":[]}
    elif d.position_id in pos: pos[d.position_id]["ex"].append(d)

# aggregate by detailed strategy key
agg = defaultdict(lambda: {"n":0,"pnl":0.0,"w":0})
for pid,pp in pos.items():
    if not pp["ex"]: continue
    e=pp["ent"]
    pnl=sum(x.profit+x.commission+x.swap for x in pp["ex"])+e.commission+e.swap
    bot=MAGICS[e.magic]; sym=e.symbol; com=e.comment or ""
    hour="-"; entry="-"
    parts=com.split("|")
    if bot=="MATH" and len(parts)>=4:
        # M|TF|SETUP|SESSION
        hour=parts[3]; entry=f"{parts[2]}/{parts[1]}"
    elif bot=="ORB" and len(parts)>=2:
        hour=parts[1]; entry="ORB_breakout"
    elif bot=="AMO" and len(parts)>=4:
        tail=parts[3]; cfg=amo_tail.get(tail)
        entry=EVT.get(parts[2],parts[2])
        if cfg: hour=f"{cfg['magic_time']}/{cfg['or_duration_min']}m {cfg['direction']}"
    elif bot=="SWING":
        entry="swing_breakout"
    key=(bot,sym,hour,entry)
    a=agg[key]; a["n"]+=1; a["pnl"]+=pnl
    if pnl>0: a["w"]+=1

# only profitable, sorted desc
prof=[(k,v) for k,v in agg.items() if v["pnl"]>0]
prof.sort(key=lambda x:-x[1]["pnl"])
print(f"ESTRATEGIAS EN PROFIT (ultimos {DAYS} dias) — {len(prof)} de {len(agg)} totales\n")
print(f"{'BOT':<6}{'ACTIVO':<11}{'HORARIO/PARAMS':<24}{'TIPO ENTRADA':<20}{'n':>4}{'WR':>6}{'PROFIT':>11}")
print("-"*86)
total=0
for (bot,sym,hour,entry),v in prof:
    wr=v["w"]/v["n"]*100 if v["n"] else 0
    print(f"{bot:<6}{sym:<11}{hour:<24}{entry:<20}{v['n']:>4}{wr:>5.0f}%{'$'+format(v['pnl'],'+,.2f'):>11}")
    total+=v["pnl"]
print("-"*86)
print(f"{'TOTAL PROFIT (solo positivas):':<65}{'$'+format(total,'+,.2f'):>11}")
mt5.shutdown()
