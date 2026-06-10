"""Identify which AMO8 config GROUPS (sym,magic_time,or_dur,direction,event)
are in profit over the last 30 days. Prints the keep-list."""
import MetaTrader5 as mt5, json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from pathlib import Path
mt5.initialize()
DAYS=30
to=datetime.now(timezone.utc); frm=to-timedelta(days=DAYS)
deals=mt5.history_deals_get(frm+timedelta(hours=3),to+timedelta(hours=3)) or []
amo=json.loads(Path(r"C:\Proyectos\kha0sys3\src\execution\bot_config_amo8.json").read_text(encoding="utf-8"))
amo_tail={s["id"].split("_")[-1][:8]:s for s in amo["portfolio"]}
EVT={"FBU":"FALSE_BREAK_UP","FBD":"FALSE_BREAK_DOWN","BU":"BREAK_UP","BD":"BREAK_DOWN"}
pos={}
for d in deals:
    if d.magic!=8338: continue
    if d.entry==0: pos[d.position_id]={"ent":d,"ex":[]}
    elif d.position_id in pos: pos[d.position_id]["ex"].append(d)
grp=defaultdict(lambda:{"n":0,"pnl":0.0})
for pid,pp in pos.items():
    if not pp["ex"]: continue
    e=pp["ent"]; pnl=sum(x.profit+x.commission+x.swap for x in pp["ex"])+e.commission+e.swap
    parts=(e.comment or "").split("|")
    if len(parts)<4: continue
    cfg=amo_tail.get(parts[3])
    if not cfg: continue
    key=(cfg["internal_sym"],cfg["magic_time"],cfg["or_duration_min"],cfg["direction"],cfg["event_type"])
    grp[key]["n"]+=1; grp[key]["pnl"]+=pnl
# profit groups
keep=[k for k,v in grp.items() if v["pnl"]>0]
print("KEEP_GROUPS_JSON_START")
print(json.dumps([list(k) for k in keep]))
print("KEEP_GROUPS_JSON_END")
print(f"\nGrupos AMO con trades: {len(grp)} | en profit: {len(keep)}")
for k,v in sorted(grp.items(),key=lambda x:-x[1]['pnl']):
    mark="KEEP" if v["pnl"]>0 else "drop"
    print(f"  [{mark}] {k[0]} {k[1]}/{k[2]}m {k[3]} {k[4]}: n={v['n']} pnl=${v['pnl']:+.2f}")
mt5.shutdown()
