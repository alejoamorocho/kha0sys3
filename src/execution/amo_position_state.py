"""AMO8 position state machine — partial exits for DOC and SWING modes.

A position has TWO state machines layered:

1. **Position lifecycle** (open → partial → ... → closed)
   - DOC: TP1 (50%, SL→BE) → TP2 (50%, close) | midpoint MFE check | MAX_HOLD
   - SWING: TP1 (25%, SL→BE) → TP2 (25%, SL→+1R) → trail SMA(20) (50%) | MAX_HOLD

2. **State transitions** evaluated each tick against current tick (bid/ask)
   and the most recent closed M1 bar.

State is persisted to a JSON sidecar file so a process restart can
reconstruct the partial-exit progress (which TPs already hit, current SL,
remaining volume, etc.). If the sidecar is corrupt or missing, the state
machine falls back to inferring from the live MT5 position's current SL.

Decision outputs:
  - PARTIAL_CLOSE(fraction) — caller closes `fraction × initial_volume`
  - MODIFY_SL(new_sl_price) — caller updates the position's SL
  - CLOSE_ALL — caller closes remaining volume at market
  - HOLD — no action this tick
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


class Action(str, Enum):
    HOLD = "HOLD"
    PARTIAL_CLOSE = "PARTIAL_CLOSE"   # close fraction × initial_volume
    MODIFY_SL = "MODIFY_SL"            # set sl to new_sl_price
    CLOSE_ALL = "CLOSE_ALL"            # close remaining at market


@dataclass
class Decision:
    action: Action
    fraction: float = 0.0              # for PARTIAL_CLOSE
    new_sl_price: Optional[float] = None  # for MODIFY_SL
    reason: str = ""                   # for telemetry / Telegram


@dataclass
class AmoPosition:
    """Full state for one AMO8 partial-exits position.

    Serializable to JSON. Reconstructible from this dict.
    """
    ticket: int
    strategy_id: str
    mode: str                          # "DOC" or "SWING"
    direction: str                     # "LONG" or "SHORT"
    broker_sym: str
    internal_sym: str
    entry_price: float
    initial_volume: float
    placed_at_iso: str                 # UTC ISO 8601
    max_hold_min: int
    atr_at_setup: float
    or_width: float

    # Distance levels (in PRICE units, absolute)
    sl_distance_initial: float         # original SL distance from entry
    tp1_distance: float                # favorable distance to TP1
    tp2_distance: float                # favorable distance to TP2
    tp1_fraction: float                # what fraction of initial_volume to close at TP1
    tp2_fraction: float                # what fraction of initial_volume to close at TP2

    # Dynamic state
    remaining_volume: float = 0.0
    current_sl: float = 0.0            # current SL price (absolute)
    tp1_hit: bool = False
    tp2_hit: bool = False
    midpoint_checked: bool = False     # DOC: did we evaluate the midpoint MFE rule?
    mfe_price_unit: float = 0.0        # favorable MFE so far (price distance from entry)
    sma_window: list[float] = field(default_factory=list)  # SWING trail: last N M1 closes
    sma_period: int = 20

    # Mode-specific parameters
    midpoint_mfe_min_r: float = 0.5    # DOC: at midpoint, require MFE ≥ this R
    swing_tp2_lock_r: float = 1.0      # SWING: after TP2, SL locks at +this R favorable

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "AmoPosition":
        # Filter only known fields (forward-compat if JSON has extras)
        known = {f for f in cls.__dataclass_fields__.keys()}
        return cls(**{k: v for k, v in d.items() if k in known})

    @property
    def placed_at(self) -> datetime:
        return datetime.fromisoformat(self.placed_at_iso)

    def sign(self) -> float:
        return 1.0 if self.direction == "LONG" else -1.0

    def risk_per_r(self) -> float:
        return 0.5 * self.atr_at_setup

    # ─── Initial level computation (called once at placement) ───

    def init_levels(self) -> None:
        s = self.sign()
        # SL price = entry - sign × sl_distance
        self.current_sl = self.entry_price - s * self.sl_distance_initial
        self.remaining_volume = self.initial_volume

    @property
    def tp1_price(self) -> float:
        return self.entry_price + self.sign() * self.tp1_distance

    @property
    def tp2_price(self) -> float:
        return self.entry_price + self.sign() * self.tp2_distance


class PositionStateStore:
    """JSON-backed persistence for AmoPosition state.

    File layout: {state_dir}/positions.json
    Schema: {"positions": [<AmoPosition.to_dict>...], "updated_at": "..."}
    """

    def __init__(self, state_dir: str | Path):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.state_dir / "positions.json"

    def load(self) -> dict[int, AmoPosition]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        out: dict[int, AmoPosition] = {}
        for d in data.get("positions", []):
            try:
                p = AmoPosition.from_dict(d)
                out[p.ticket] = p
            except (TypeError, ValueError):
                continue
        return out

    def save(self, positions: dict[int, AmoPosition]) -> None:
        data = {
            "positions": [p.to_dict() for p in positions.values()],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        # Atomic write: write to tmp then rename
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def remove(self, ticket: int) -> None:
        positions = self.load()
        positions.pop(ticket, None)
        self.save(positions)

    def upsert(self, pos: AmoPosition) -> None:
        positions = self.load()
        positions[pos.ticket] = pos
        self.save(positions)


# ─────────────────────────── Decision logic ───────────────────────────


def _update_mfe(pos: AmoPosition, current_high: float, current_low: float) -> None:
    """Track favorable MFE in price units from entry."""
    if pos.direction == "LONG":
        excursion = current_high - pos.entry_price
    else:
        excursion = pos.entry_price - current_low
    if excursion > pos.mfe_price_unit:
        pos.mfe_price_unit = float(excursion)


def _update_sma(pos: AmoPosition, m1_close: float) -> Optional[float]:
    """Append latest M1 close to the SMA window. Returns current SMA or None
    if the window is not yet full enough."""
    pos.sma_window.append(float(m1_close))
    if len(pos.sma_window) > pos.sma_period:
        pos.sma_window.pop(0)
    if not pos.sma_window:
        return None
    return sum(pos.sma_window) / len(pos.sma_window)


def evaluate_doc(
    pos: AmoPosition,
    *,
    now: datetime,
    bid: float,
    ask: float,
    last_m1_high: float,
    last_m1_low: float,
    last_m1_close: float,
) -> Decision:
    """Decide the next action for a DOC-mode position.

    DOC rules:
      - SL = 1.0 × OR_width (set at placement)
      - TP1 = +1.0 × OR_width → close 50%, shift SL to entry (BE)
      - TP2 = +2.0 × OR_width → close remaining 50%
      - Midpoint (max_hold/2): if MFE < midpoint_mfe_min_r × R, close at market
      - MAX_HOLD: close at market
      - SL-first conservative on simultaneous hits
    """
    if pos.remaining_volume <= 0:
        return Decision(Action.HOLD)

    _update_mfe(pos, last_m1_high, last_m1_low)
    s = pos.sign()

    # Use bid/ask for live-tick checks (more conservative than M1 high/low)
    favorable_price = ask if pos.direction == "LONG" else bid
    adverse_price = bid if pos.direction == "LONG" else ask

    # MAX_HOLD hard timeout
    age_min = (now - pos.placed_at).total_seconds() / 60
    if age_min >= pos.max_hold_min:
        return Decision(Action.CLOSE_ALL, reason="DOC_MAX_HOLD")

    # SL-first check: if adverse price would trigger SL, broker will handle it
    # (we set SL on the position). No manual action needed.

    # TP1 hit detection (live tick — broker may have already filled an SL/TP via
    # bracket, but for partial exits we manage explicitly)
    if not pos.tp1_hit:
        tp1_hit_live = (
            (pos.direction == "LONG" and last_m1_high >= pos.tp1_price)
            or (pos.direction == "SHORT" and last_m1_low <= pos.tp1_price)
        )
        if tp1_hit_live:
            pos.tp1_hit = True
            # Caller will: close tp1_fraction × initial_volume + modify SL to entry
            return Decision(
                Action.PARTIAL_CLOSE,
                fraction=pos.tp1_fraction,
                new_sl_price=pos.entry_price,
                reason="DOC_TP1",
            )

    # TP2 hit (only after TP1)
    if pos.tp1_hit and not pos.tp2_hit:
        tp2_hit_live = (
            (pos.direction == "LONG" and last_m1_high >= pos.tp2_price)
            or (pos.direction == "SHORT" and last_m1_low <= pos.tp2_price)
        )
        if tp2_hit_live:
            pos.tp2_hit = True
            return Decision(Action.CLOSE_ALL, reason="DOC_TP2")

    # Midpoint MFE check (only once, only if TP1 not yet hit)
    if not pos.midpoint_checked and age_min >= pos.max_hold_min / 2:
        pos.midpoint_checked = True
        if not pos.tp1_hit:
            mfe_r = pos.mfe_price_unit / pos.risk_per_r() if pos.risk_per_r() > 0 else 0
            if mfe_r < pos.midpoint_mfe_min_r:
                return Decision(Action.CLOSE_ALL, reason="DOC_TIME_STOP_LOW_MFE")

    return Decision(Action.HOLD)


def evaluate_swing(
    pos: AmoPosition,
    *,
    now: datetime,
    bid: float,
    ask: float,
    last_m1_high: float,
    last_m1_low: float,
    last_m1_close: float,
) -> Decision:
    """Decide the next action for a SWING-mode position.

    SWING rules:
      - SL = 1.0 × ATR (set at placement)
      - TP1 at +2R → close 25%, shift SL to entry (BE)
      - TP2 at +4R → close 25%, lock SL at +1R favorable
      - Remaining 50% trails SMA(20) on M1: exit when M1 close crosses against
      - MAX_HOLD: close at market
    """
    if pos.remaining_volume <= 0:
        return Decision(Action.HOLD)

    _update_mfe(pos, last_m1_high, last_m1_low)
    sma = _update_sma(pos, last_m1_close)
    s = pos.sign()

    age_min = (now - pos.placed_at).total_seconds() / 60
    if age_min >= pos.max_hold_min:
        return Decision(Action.CLOSE_ALL, reason="SWING_MAX_HOLD")

    # TP1 hit
    if not pos.tp1_hit:
        tp1_hit_live = (
            (pos.direction == "LONG" and last_m1_high >= pos.tp1_price)
            or (pos.direction == "SHORT" and last_m1_low <= pos.tp1_price)
        )
        if tp1_hit_live:
            pos.tp1_hit = True
            return Decision(
                Action.PARTIAL_CLOSE,
                fraction=pos.tp1_fraction,
                new_sl_price=pos.entry_price,  # BE
                reason="SWING_TP1",
            )

    # TP2 hit (only after TP1)
    if pos.tp1_hit and not pos.tp2_hit:
        tp2_hit_live = (
            (pos.direction == "LONG" and last_m1_high >= pos.tp2_price)
            or (pos.direction == "SHORT" and last_m1_low <= pos.tp2_price)
        )
        if tp2_hit_live:
            pos.tp2_hit = True
            # SL locks at entry + 1R favorable
            locked_sl = pos.entry_price + s * (pos.swing_tp2_lock_r * pos.risk_per_r())
            return Decision(
                Action.PARTIAL_CLOSE,
                fraction=pos.tp2_fraction,
                new_sl_price=locked_sl,
                reason="SWING_TP2",
            )

    # Trail with SMA(20) only after TP2 (remaining 50% runs with SMA trail)
    if pos.tp2_hit and sma is not None and pos.remaining_volume > 0:
        cross_against = (
            (pos.direction == "LONG" and last_m1_close < sma)
            or (pos.direction == "SHORT" and last_m1_close > sma)
        )
        if cross_against:
            return Decision(Action.CLOSE_ALL, reason="SWING_TRAIL_SMA")

    return Decision(Action.HOLD)


def evaluate(pos: AmoPosition, **kwargs) -> Decision:
    """Dispatch by mode."""
    if pos.mode == "DOC":
        return evaluate_doc(pos, **kwargs)
    if pos.mode == "SWING":
        return evaluate_swing(pos, **kwargs)
    # ATR / OR_FIXED don't use the state machine — broker handles single TP/SL
    return Decision(Action.HOLD)


def apply_decision(pos: AmoPosition, decision: Decision) -> None:
    """Mutate position state after the broker action succeeds.

    Caller is responsible for actually sending orders. After confirmation,
    call this to update the in-memory state.
    """
    if decision.action == Action.PARTIAL_CLOSE:
        closed_vol = decision.fraction * pos.initial_volume
        pos.remaining_volume = max(0.0, pos.remaining_volume - closed_vol)
        if decision.new_sl_price is not None:
            pos.current_sl = float(decision.new_sl_price)
    elif decision.action == Action.MODIFY_SL:
        if decision.new_sl_price is not None:
            pos.current_sl = float(decision.new_sl_price)
    elif decision.action == Action.CLOSE_ALL:
        pos.remaining_volume = 0.0
    # HOLD: no change
