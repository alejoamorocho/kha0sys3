"""Shared constants and helpers for the ORB discovery pipeline.

Re-exports `_to_us_utc` from K3M1 as `to_us_utc` (public name) to avoid
look-ahead bias from naive-datetime timestamp conversions on non-UTC dev
machines. See CLAUDE.md "Bias fixes críticos aplicados" §3.
"""
from __future__ import annotations

from datetime import timezone as _tz


def to_us_utc(dt) -> int:
    """Convert (possibly naive) datetime to microseconds since epoch as UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_tz.utc)
    return int(dt.timestamp() * 1_000_000)


SYMBOLS_V1 = [
    "XAUUSD", "XAGUSD", "BRENT", "WTI",
    "GBPUSD", "GBPJPY", "EURUSD", "GBPAUD",
    "USDJPY", "AUDUSD", "EURJPY",
    "NASDAQ100", "NATGAS", "SP500",
]

MAGIC_TIMES = ["22:00", "07:00", "12:30", "00:00"]
OR_DURATIONS = [15, 30, 60, 120]
DIRECTIONS = ["LONG", "SHORT"]

DATA_DIR = "data/enriched_math_tf"
REPORTS_DIR = "reports/orb"
