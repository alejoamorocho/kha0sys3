"""Tests for coherence filter and combo pipeline basics."""
from __future__ import annotations
from src.engine.run_math_combinations import (
    check_combination_coherence, SIGNAL_FAMILY, ALL_EXITS, EXIT_THESIS,
)


def test_family_taxonomy_covers_all_signals():
    from src.application.signal_generator import SIGNAL_TYPES
    missing = set(SIGNAL_TYPES) - set(SIGNAL_FAMILY.keys())
    assert not missing, f"Signals missing from family taxonomy: {missing}"


def test_coherence_rejects_redundant_pair():
    # Two mean-rev signals in same family should be rejected
    assert check_combination_coherence(("ZSCORE_REV", "BB_TOUCH_REV")) is False
    assert check_combination_coherence(("RSI_OB_REV", "FRAC_DIFF_REV")) is False


def test_coherence_accepts_diverse_pair():
    # Mean-rev + momentum is diverse
    assert check_combination_coherence(("ZSCORE_REV", "MACD_CROSS")) is True
    # Mean-rev + structural is diverse
    assert check_combination_coherence(("ZSCORE_REV", "ACCEL_SHOCK")) is True


def test_coherence_rejects_monochrome_triple():
    # All three mean-rev → reject
    assert check_combination_coherence(
        ("ZSCORE_REV", "BB_TOUCH_REV", "RSI_OB_REV")
    ) is False
    # All three momentum → reject
    assert check_combination_coherence(
        ("MACD_CROSS", "ADX_BREAKOUT", "BB_BREAKOUT")
    ) is False


def test_coherence_accepts_diverse_triple():
    # one of each family
    assert check_combination_coherence(
        ("ZSCORE_REV", "MACD_CROSS", "ACCEL_SHOCK")
    ) is True


def test_all_exits_have_thesis():
    for e in ALL_EXITS:
        assert e in EXIT_THESIS
