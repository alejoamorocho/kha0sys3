from datetime import datetime, timezone

from src.application.orb_utils import to_us_utc, SYMBOLS_V1, MAGIC_TIMES, OR_DURATIONS


def test_to_us_utc_naive_is_treated_as_utc():
    dt = datetime(2026, 1, 1, 12, 0, 0)
    expected = int(dt.replace(tzinfo=timezone.utc).timestamp() * 1_000_000)
    assert to_us_utc(dt) == expected


def test_to_us_utc_aware_preserves_offset():
    dt = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert to_us_utc(dt) == int(dt.timestamp() * 1_000_000)


def test_universe_v1_excludes_euraud_and_has_14_symbols():
    assert "EURAUD" not in SYMBOLS_V1
    assert len(SYMBOLS_V1) == 14
    assert set(SYMBOLS_V1) == {
        "XAUUSD", "XAGUSD", "BRENT", "WTI", "GBPUSD", "GBPJPY",
        "EURUSD", "GBPAUD", "USDJPY", "AUDUSD", "EURJPY",
        "NASDAQ100", "NATGAS", "SP500",
    }


def test_magic_times_are_four_utc_strings():
    assert MAGIC_TIMES == ["22:00", "07:00", "12:30", "00:00"]


def test_or_durations_are_15_30_60_120():
    assert OR_DURATIONS == [15, 30, 60, 120]
