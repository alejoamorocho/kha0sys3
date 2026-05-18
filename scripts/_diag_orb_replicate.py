"""Replicate exactly what _process_orb sees per symbol. Diagnostic only."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import MetaTrader5 as mt5
import polars as pl
from datetime import datetime, timezone

from src.execution.traders_live_engine import (
    _fetch_m1_bars, detect_broker_offset_hours, _now_utc,
    M1_BARS_LOOKBACK,
)
from src.execution.mt5_client import MT5Client
from src.infrastructure.symbol_mapper import SymbolMapper

client = MT5Client(attach_only=True)
client.ensure_connected()
mapper = SymbolMapper()

# Load ORB config
cfg = json.loads(Path("src/execution/bot_config_traders_orb.json").read_text())
orb_strats = cfg["portfolio"]

# Detect offset
probe = mapper.to_mt5(orb_strats[0]["sym"])
offset_h = detect_broker_offset_hours(client, probe, current_offset_h=3)
print(f"Broker offset detected: {offset_h:+d}h")
print()

now_utc = _now_utc()
now_min_of_day = now_utc.hour * 60 + now_utc.minute
print(f"Real UTC now: {now_utc.strftime('%Y-%m-%d %H:%M')} (min_of_day={now_min_of_day})")
print()

for strat in orb_strats:
    sid = strat["id"]
    sym_internal = strat["sym"]
    broker_sym = mapper.to_mt5(sym_internal)
    params = strat["orb_params"]
    oh = int(params["open_hour_utc"])
    om = int(params.get("open_minute_utc", 0))
    rm = int(params["range_minutes"])
    bw = int(params.get("breakout_window_minutes", 180))
    range_start_min = oh * 60 + om
    range_end_min = range_start_min + rm
    window_end_min = range_end_min + bw
    in_window = range_end_min <= now_min_of_day < window_end_min

    m1 = _fetch_m1_bars(client, broker_sym, offset_h, M1_BARS_LOOKBACK)
    if m1 is None or len(m1) < 60:
        print(f"{sid:<25} ({broker_sym:<10}): NO/few M1 bars (n={0 if m1 is None else len(m1)})")
        continue

    today = m1.tail(1)["time"][0].date()
    range_bars = m1.filter(
        (pl.col("time").dt.date() == today)
        & ((pl.col("time").dt.hour() * 60 + pl.col("time").dt.minute()) >= range_start_min)
        & ((pl.col("time").dt.hour() * 60 + pl.col("time").dt.minute()) < range_end_min)
    )
    if len(range_bars) < max(1, rm // 2):
        print(f"{sid:<25} ({broker_sym:<10}): range bars too few ({len(range_bars)})")
        continue

    r_high = float(range_bars["high"].max())
    r_low = float(range_bars["low"].min())
    last_close = float(m1.tail(1)["close"][0])
    tick = mt5.symbol_info_tick(broker_sym)
    ask = float(tick.ask) if tick else None
    broken = last_close > r_high
    status = "ACTIVE" if in_window else ("PAST" if now_min_of_day >= window_end_min else "FUTURE")
    print(f"{sid:<25} {broker_sym:<10} {oh:02d}:{om:02d}/{rm}m | win={status} "
          f"r=[{r_low:.4f}..{r_high:.4f}] last={last_close:.4f} ask={ask} "
          f"broken={broken}")

mt5.shutdown()
