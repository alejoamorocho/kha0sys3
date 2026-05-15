# AMO8 Deploy Guide — VPS + NSSM + Telegram

**Strategy:** AMO8 — ORB false-break fade portfolio
**Magic:** 8338
**Risk per trade:** 0.1% (75 configs on 6 unique pattern slots — worst-case 1.2% per signal)
**Expected:** ~2,721 trades/year (with overlap), PF 1.70 weighted, WR 62%

## Pre-deploy checklist

Before pushing to VPS, verify locally:

```powershell
# 1) Imports + instantiation
py -3.12 -c "from src.execution.live_amo_trader import AmoTraderEngine; AmoTraderEngine(dry_run=True)"

# 2) DRY supervisor (Ctrl+C to stop). Should print [AMO8] ENGINE STARTED + heartbeats.
py -3.12 scripts/run_amo_bot_supervisor.py --dry-run

# 3) Verify magic 8338 does NOT collide with anything currently in MT5
py -3.12 -c "
import MetaTrader5 as mt5
mt5.initialize()
positions = mt5.positions_get() or []
orders = mt5.orders_get() or []
collide = [x for x in list(positions)+list(orders) if int(getattr(x,'magic',0))==8338]
print(f'Conflicts at magic 8338: {len(collide)}')
mt5.shutdown()
"
```

## Files to push to VPS

These are NEW files (no overlap with K3M1-75 magic 1338):

```
src/execution/bot_config_amo8.json       # Strategy portfolio
src/execution/amo_order_manager.py        # Order manager (magic 8338)
src/execution/live_amo_trader.py          # Live engine
scripts/run_amo_bot_supervisor.py         # Supervisor entry point
```

These files are SHARED with K3M1-75 (no changes required):
- `src/execution/mt5_client.py` (MT5 connection)
- `src/monitoring/telegram_notifier.py` (outbound Telegram)
- `src/application/calculators.py` (DataEnricher)
- `src/application/orb_patterns.py` (ORB event detection)
- `src/application/orb_utils.py` (UTC helper)
- `config/symbol_mapping.yaml` (internal → broker symbol map)
- `.env` (Telegram credentials, MT5 login)

## NSSM service config (Windows VPS)

Open elevated PowerShell on the VPS and run:

```powershell
# 1) Install NSSM if not yet installed
choco install nssm -y     # or download from nssm.cc and unzip to C:\nssm

# 2) Create the AMO8 service
nssm install Kha0sysAmo8 "C:\Python312\python.exe" "C:\proyectos\kha0sys3\scripts\run_amo_bot_supervisor.py --live"
nssm set Kha0sysAmo8 AppDirectory "C:\proyectos\kha0sys3"
nssm set Kha0sysAmo8 DisplayName "Kha0sys3 AMO8 ORB Trader (magic 8338)"
nssm set Kha0sysAmo8 Description "ORB false-break fade portfolio. Parallel to Kha0sysMathBot."
nssm set Kha0sysAmo8 AppStdout "C:\ProgramData\Kha0sysAmo8\logs\amo8.log"
nssm set Kha0sysAmo8 AppStderr "C:\ProgramData\Kha0sysAmo8\logs\amo8.err.log"
nssm set Kha0sysAmo8 AppRotateFiles 1
nssm set Kha0sysAmo8 AppRotateOnline 1
nssm set Kha0sysAmo8 AppRotateBytes 50000000  # 50 MB per file
nssm set Kha0sysAmo8 Start SERVICE_AUTO_START
nssm set Kha0sysAmo8 ObjectName LocalSystem
nssm set Kha0sysAmo8 AppExit Default Restart

# 3) Create the log directory
New-Item -ItemType Directory -Force -Path "C:\ProgramData\Kha0sysAmo8\logs"

# 4) Start as DRY first (validate Telegram + MT5 connection without real orders)
nssm set Kha0sysAmo8 AppParameters "C:\proyectos\kha0sys3\scripts\run_amo_bot_supervisor.py --dry-run"
nssm start Kha0sysAmo8
# Tail the log: Get-Content C:\ProgramData\Kha0sysAmo8\logs\amo8.log -Wait

# 5) After ~30 min of DRY validation (heartbeats + at least one [AMO8] ORDER PLACED [DRY]
#    shown), switch to LIVE:
nssm stop Kha0sysAmo8
nssm set Kha0sysAmo8 AppParameters "C:\proyectos\kha0sys3\scripts\run_amo_bot_supervisor.py --live"
nssm start Kha0sysAmo8
```

## Telegram integration

V1 uses **outbound notifications only** via the existing `TelegramNotifier`
(same token/chat as K3M1). Messages are prefixed `[AMO8]`:

- `[AMO8] ENGINE STARTED` — on supervisor start (shows magic, dry_run, configs, slots, expected PF)
- `[AMO8] HEARTBEAT` — every 15 min (balance, equity, open positions, active slots)
- `[AMO8] ORDER PLACED` — every market order (strategy id, sym, dir, entry/sl/tp, vol)
- `[AMO8] MAX_HOLD CLOSE` — when a position is force-closed past its max_hold_min

The interactive K3M1 command bot (`/status`, `/balance`, `/positions`) already
**includes all magics** by default since `MathTelegramBot` filters by
`MAGIC_NUMBER_MATH=1338` only when querying its own state. AMO8 positions show
in `/positions` because that command uses `mt5.positions_get()` unfiltered
unless a magic filter is explicitly set.

**If you want a dedicated AMO8 command bot (recommended for V2):** spawn a
second `MathTelegramBot` instance with `magic_filter=8338` — but use a
different command set (e.g. `/amo_status`, `/amo_positions`) to avoid
collision with the K3M1 commands on the same chat.

## Deploy via existing scripts

```powershell
# From local dev machine (Windows):
py -3.12 deploy/pull_and_restart.py --service Kha0sysAmo8
```

`deploy/pull_and_restart.py` already does:
1. `git push` from local
2. SSH/WinRM into VPS
3. `git pull` on VPS
4. `pip install -r requirements.txt --quiet`
5. `nssm stop <service>` / `nssm start <service>`

You may need to extend the script's `--service` arg if it hardcodes
`Kha0sysMathBot`. Inspect `deploy/pull_and_restart.py` before pushing.

## Monitoring

| Watch | Where |
|---|---|
| Live log | `C:\ProgramData\Kha0sysAmo8\logs\amo8.log` (tail -Wait) |
| Telegram events | `[AMO8] *` prefix |
| MT5 positions | Filter by magic=8338 in MT5 terminal |
| Service status | `Get-Service Kha0sysAmo8` |

## Rollback procedure

If AMO8 misbehaves:

```powershell
nssm stop Kha0sysAmo8
# Close all open AMO8 positions manually in MT5 terminal (magic 8338) or run:
py -3.12 -c "
import MetaTrader5 as mt5
mt5.initialize()
for p in mt5.positions_get() or []:
    if int(getattr(p,'magic',0)) == 8338:
        # Close at market
        tick = mt5.symbol_info_tick(p.symbol)
        close_type = mt5.ORDER_TYPE_SELL if p.type == 0 else mt5.ORDER_TYPE_BUY
        price = tick.bid if p.type == 0 else tick.ask
        mt5.order_send({'action': mt5.TRADE_ACTION_DEAL, 'symbol': p.symbol,
                        'volume': p.volume, 'type': close_type, 'position': p.ticket,
                        'price': price, 'deviation': 20, 'magic': 8338,
                        'comment': 'A8|ROLLBACK'})
mt5.shutdown()
"
```

K3M1-75 (magic 1338) is **completely unaffected** by stopping/starting
Kha0sysAmo8 — they share no files or state.

## V2 follow-up (DOC + SWING modes)

V1 ships only ATR + OR_FIXED management (75 of 84 PF≥1.3 configs).
The 9 dropped configs (3 DOC, 6 SWING) need partial-exit infrastructure:

1. Position fraction tracker (mid-trade)
2. Modify-order to shift SL after TP1 hit (BE shift)
3. Modify-order to lock at +1R after TP2 hit (SWING)
4. Live SMA(20) M1 calculation for trailing (SWING)
5. Time-conditional close logic at max_hold/2 if MFE < 0.5R (DOC)

Estimated effort: 3-5 days. Plan separately when ready.
