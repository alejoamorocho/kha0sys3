"""Independent cross-audit of the profit report. Three checks:
  1. Sum of ALL trade PnL (pos+neg) vs the report's positive total.
  2. Reconcile against account balance change (deals of type balance + trades).
  3. Dump individual trades of 3 sample strategies for manual verification.
"""
import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
from collections import defaultdict
mt5.initialize()
DAYS=30
to=datetime.now(timezone.utc); frm=to-timedelta(days=DAYS)
deals=mt5.history_deals_get(frm+timedelta(hours=3),to+timedelta(hours=3)) or []
MAGICS={1338:"MATH",1339:"SWING",1340:"ORB",8338:"AMO"}

# ---- CHECK 1: total trade PnL of our 4 bots ----
pos=defaultdict(lambda:{"ent":None,"ex":[]})
for d in deals:
    if d.magic not in MAGICS: continue
    if d.entry==0: pos[d.position_id]["ent"]=d
    else: pos[d.position_id]["ex"].append(d)
tot_pos=tot_neg=0.0; n_pos=n_neg=0
per_bot=defaultdict(float)
for pid,pp in pos.items():
    if pp["ent"] is None or not pp["ex"]: continue
    e=pp["ent"]
    pnl=sum(x.profit+x.commission+x.swap for x in pp["ex"])+e.commission+e.swap
    per_bot[MAGICS[e.magic]]+=pnl
    if pnl>0: tot_pos+=pnl; n_pos+=1
    elif pnl<0: tot_neg+=pnl; n_neg+=1
print("="*60)
print("CHECK 1 — PnL de los 4 bots (30 dias)")
print("="*60)
print(f"  Positivas: {n_pos} trades = ${tot_pos:+,.2f}")
print(f"  Negativas: {n_neg} trades = ${tot_neg:+,.2f}")
print(f"  NETO total bots: ${tot_pos+tot_neg:+,.2f}")
print(f"  (El documento dice positivas = $16,825.97 — debe coincidir con ${tot_pos:,.2f})")
print(f"  Por bot: " + " ".join(f"{k}=${v:+,.0f}" for k,v in per_bot.items()))

# ---- CHECK 2: reconcile vs account ledger (all deal profit incl swap/comm) ----
all_profit=sum(d.profit for d in deals)
all_comm=sum(d.commission for d in deals)
all_swap=sum(d.swap for d in deals)
print()
print("="*60)
print("CHECK 2 — Reconciliacion con el ledger de la cuenta")
print("="*60)
print(f"  Suma profit TODOS los deals (todos magics): ${all_profit:+,.2f}")
print(f"  Suma commission: ${all_comm:+,.2f}  swap: ${all_swap:+,.2f}")
print(f"  Cambio neto por trading (todos): ${all_profit+all_comm+all_swap:+,.2f}")
acc=mt5.account_info()
print(f"  Balance actual: ${acc.balance:,.2f}")

# ---- CHECK 3: dump individual trades of 3 sample strategies ----
print()
print("="*60)
print("CHECK 3 — Trades individuales (auditoria manual)")
print("="*60)
SAMPLES=[(1340,"GBPAUD+","ORB GBPAUD 07h30"),(8338,"GBPUSD+","AMO GBPUSD 12:30"),(1338,"XAGUSD","MATH XAG ASIA")]
import json
from pathlib import Path
amo=json.loads(Path(r"C:\Proyectos\kha0sys3\src\execution\bot_config_amo8.json").read_text())
for magic,sym,label in SAMPLES:
    print(f"\n--- {label} ({sym}) ---")
    s=0.0; cnt=0
    for pid,pp in pos.items():
        if pp["ent"] is None or not pp["ex"]: continue
        e=pp["ent"]
        if e.magic!=magic or e.symbol!=sym: continue
        pnl=sum(x.profit+x.commission+x.swap for x in pp["ex"])+e.commission+e.swap
        ot=datetime.fromtimestamp(e.time,tz=timezone.utc)-timedelta(hours=3)
        print(f"    {ot.strftime('%m-%d %H:%M')} {('BUY' if e.type==0 else 'SELL')} vol={e.volume} pnl=${pnl:+.2f} [{e.comment}]")
        s+=pnl; cnt+=1
    print(f"    >>> {cnt} trades, suma=${s:+,.2f}")
mt5.shutdown()
