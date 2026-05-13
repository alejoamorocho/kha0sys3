# ORB Edge Discovery Pipeline — Design Spec

**Date:** 2026-05-13
**Status:** Approved for implementation planning
**Scope:** Backtest research only. No live deploy in V1. Decision on deploying
to live (and on magic number) is deferred until pipeline results are reviewed.

## Motivation

The legacy `orb_breakfade` strategy was retired because it had look-ahead bias
(STOP at OR boundary filled on retracement created artifact WR=100%) and no
M1-precision management. Discovery research lives in `reports/AUDUSD_Edge.md`
("Matriz Probabilística") but never crystallized into deployable strategies.

This pipeline formalizes ORB edge discovery using the same M1-walk discipline
that produced K3M1-75: causal indicators, SL-first intra-bar conservatism,
UTC normalization, MFE/MAE in R-units before committing to TP/SL choices.

**Core insight:** find patterns that have edge *independently* of where you
stop or take profit. Then search optimal management for those patterns,
constrained to RR ≥ 1:1 (always win more than you lose). Then apply the same
robustness gates that survived K3M1-75 (MC 10k bootstrap + walk-forward 50/50
+ decay). Finally, Optuna fine-tunes the survivors.

## Scope

- **In scope (V1):** Backtest pipeline Phases A–D end-to-end. Output is
  parquets + human-readable reports for review. No live integration, no
  bot config generation, no magic assignment.
- **Deferred to post-V1 review:** Decision whether to deploy any subset of
  surviving strategies to live, what magic to assign, and how to merge with
  K3M1-75 (separate portfolio vs. unified).
- **Out of scope (V1):** Friction calibration for NATGAS, SP500, NASDAQ100,
  EURAUD. If snapshots are unavailable, V1 ships on the K3M1-11 universe and
  V2 extends.

## Architecture

Four sequential phases, each writing a parquet that's the input to the next:

```
Phase A: PATTERN + EDGE     → orb_phase_a.parquet
Phase B: MANAGEMENT GRID    → orb_phase_b.parquet
Phase C: ROBUSTEZ           → orb_robustness.parquet
Phase D: OPTUNA REFINE      → orb_optuna_results.parquet (+ final report)
```

Each phase is idempotent: re-running with the same inputs produces the same
output. `scripts/run_orb_pipeline.py` orchestrates A→B→C→D with `--skip-phase`
flags for partial reruns.

## Phase A — Pattern detection + Edge scoring

### Inputs
- M1 parquets from `data/enriched_math_tf/<SYM>_M1.parquet` (15 symbols)
- M15 parquets from `data/enriched_math_tf/<SYM>_M15.parquet` (base TF for OR
  computation, matches `enrich_with_opening_range` contract)

### Universe grid

- **Assets (15):** XAUUSD, XAGUSD, BRENT, WTI, GBPUSD, GBPJPY, EURUSD,
  GBPAUD, USDJPY, AUDUSD, EURJPY, NASDAQ100, NATGAS, SP500, EURAUD.
  (Friction-limited: if `friction_real.py` lacks the symbol, exclude with a
  warning, do not fall back to defaults silently.)
- **Magic times (4):** Asia 22:00, London 07:00, NY 12:30, All-day 00:00 (UTC)
- **OR durations (4):** 15m, 30m, 60m, 120m
- **Direction (2):** LONG, SHORT (dual per pattern, scored independently)

Total config slots before pattern enumeration: 15 × 4 × 4 × 2 = 480.

### Pattern definition (hybrid: event × state)

Each pattern = `(event, state)` tuple, where:

**Event** (8 types, dynamic post-OR triggers detected by M1 walk):
- `BREAK_UP` — first M1 high > or_high after `is_post_or == true`
- `BREAK_DOWN` — first M1 low < or_low after `is_post_or == true`
- `FALSE_BREAK_UP` — BREAK_UP that retraces back below or_high without
  reaching `or_high + 0.5 × or_width` within 30 M1 bars
- `FALSE_BREAK_DOWN` — symmetric
- `MITIG_PD_MID` — first M1 touch of pd_mid after `is_post_or == true`
- `MITIG_PD_CLOSE` — first M1 touch of pd_close after `is_post_or == true`
- `REENTRY_PD_OR_HIGH` — first M1 touch of pd_or_high (yesterday's OR high)
- `REENTRY_PD_OR_LOW` — symmetric

**State** (categorical context at OR close, ~36 combinations):
- `or_position_vs_pd` (5 values: ABOVE_PD_HIGH, BELOW_PD_LOW,
  BETWEEN_CLOSE_AND_HIGH, BETWEEN_LOW_AND_CLOSE, INSIDE_PD_RANGE)
- `or_atr_bucket` (3 values: compressed ≤ 0.3, normal (0.3, 0.7), expanded ≥ 0.7)
- `pd_or_overlap_bucket` (3 values: gap_up = today's or_low > pd_or_high,
  gap_down = today's or_high < pd_or_low, inside = overlap)

Pattern ID format: `<EVENT>_<or_pos>_<atr_bucket>_<pd_or_bucket>`.

Total enumerated patterns per (sym, magic_time, duration, dir): up to 8×45=360,
but sparsity filter (count ≥ 50/year) typically reduces to 30–80 active.

### Pattern dedup within a day

If a single M1 bar triggers multiple events (e.g., BREAK_UP that touches
pd_mid in the next 5 minutes), each event fires its own pattern, but a
dedup pass keeps only the first event per (sym, magic_time, duration) per
day — same dedup rule as K3M1-75 `(sym, setup_type)`.

### Edge metric — MFE/MAE in R-units

For each trigger at timestamp `t`:

1. Compute `atr_at_setup = atr_14` interpolated to `t` (join_asof backward)
2. Define `R = 0.5 × atr_at_setup` (notional risk unit, matches K3M1 default)
3. Walk M1 from `t+1` to `min(t + 8h, broker EOD)`, tracking running:
   - `MFE_long = max(high) - entry_close_at_t`
   - `MAE_long = entry_close_at_t - min(low)`
   - `MFE_short = entry_close_at_t - min(low)`
   - `MAE_short = max(high) - entry_close_at_t`
4. Convert to R-units: `MFE_long_R = MFE_long / R`, etc.
5. **No look-ahead:** the walk uses only bars with `time > t` (strict). UTC
   normalization via `_to_us_utc()` helper.
6. **SL-first conservative** does NOT apply here (no SL yet); we're measuring
   pure excursion bounds.

### Edge aggregation

Group by `(sym, magic_time, duration, pattern_id, direction)`:
- `count` (trigger count over data span)
- `count_per_year`
- `E[MFE_R]`, `E[MAE_R]`
- `p50_MFE_R`, `p50_MAE_R`, `p25_MFE_R`, `p75_MFE_R` (same for MAE)
- `edge_score = p50_MFE_R - p50_MAE_R`

### Phase A filter gates

Survive Phase A if:
- `count_per_year ≥ 50`
- `edge_score ≥ 0.3`
- `p50_MFE_R ≥ 1.0` (guarantees ≥1:1 RR is geometrically achievable)
- `p50_MAE_R ≤ 1.5` (cap on adverse excursion floor)

### Phase A output

`reports/orb/orb_phase_a.parquet` columns:
`symbol, magic_time, or_duration_min, pattern_id, event_type, or_position, or_atr_bucket, pd_or_bucket, direction, count, count_per_year, E_MFE_R, E_MAE_R, p25_MFE_R, p50_MFE_R, p75_MFE_R, p25_MAE_R, p50_MAE_R, p75_MAE_R, edge_score, span_start, span_end`

## Phase B — Management grid

### Inputs
- `orb_phase_a.parquet` (Phase A survivors)
- M1 parquets (re-walked for actual fill + exit simulation)

### Entry modes (3)
- `MARKET_AT_TRIGGER` — fill at close of trigger M1 bar
- `STOP_RETEST` — STOP order at `entry ± k × atr_at_setup` in trade direction,
  k ∈ {0.25, 0.5}. Fill wait window: `5 × or_duration_min`. No fill → cancel.
- `LIMIT_PULLBACK` — LIMIT order at `entry ∓ k × atr_at_setup`, k ∈ {0.25, 0.5}.
  Same fill window.

Total entry variants: 1 + 2 + 2 = 5.

### TP/SL grid (RR ≥ 1:1 hard constraint)

- `sl_atr_mult ∈ {0.3, 0.5, 0.7, 1.0}`
- `tp_atr_mult ∈ {sl_atr_mult × 1.0, × 1.5, × 2.0, × 3.0}`

16 TP/SL combos × 5 entry variants = 80 management combos per Phase A survivor.

### M1 exit walk (mirror of K3M1)

For each fill:
1. Compute TP price, SL price in symbol price units.
2. Walk M1 from `fill_ts + 1min` until any of:
   - TP touched (high ≥ TP for long, low ≤ TP for short) → exit at TP
   - SL touched → exit at SL
   - `max_hold_min = 10 × or_duration_min` elapsed → exit at last close
3. **Intra-bar tie (both TP and SL touched in same M1 bar):** SL-first
   conservative — assume SL hit first.
4. **Friction:** `friction_effective_R = friction_real(sym, sl_atr_mult, atr_at_setup) + 0.2R` deducted from realized R.

### Phase B metrics

Per `(sym, magic_time, duration, pattern_id, direction, entry_mode, sl_mult, tp_mult)`:
- `trades`, `trades_per_year`, `win_rate`, `pf`, `expectancy_R`,
  `max_dd_R`, `sharpe_annualized`, `rr = tp_mult / sl_mult`

### Phase B filter gates

- `pf ≥ 1.2`
- `win_rate > 0.5`
- `expectancy_R ≥ 0.1`
- `trades_per_year ≥ 30`
- `rr ≥ 1.0` (strict, sanity check on grid)

### Phase B output

`reports/orb/orb_phase_b.parquet` with all combo metrics for survivors.

## Phase C — Robustez (reuses k3m1_robustness)

### Inputs
- `orb_phase_b.parquet`
- Per-trade R-multiple series saved alongside Phase B (needed for bootstrap)

### Dedup before robustness

For each `(sym, magic_time, or_duration, pattern_id, direction)`, keep the
combo with highest `pf × log(trades_per_year)` (rank score). Reduces to one
management per pattern slot.

### Realistic filter
- `win_rate ∈ (0.55, 0.90)`
- `pf ∈ (1.5, 10.0)`
- `expectancy_R ≥ 0.1`
- `trades_per_year ≥ 30`

### Robustness tests (port from `src/engine/k3m1_robustness.py`)
- **MC bootstrap 10k:** ruin probability with DD threshold = 30R
- **Walk-forward 50/50:** PF_IS vs PF_OOS; gate `PF_OOS ≥ 0.8 × PF_IS` AND `PF_OOS ≥ 1.5`
- **Decay anual:** annual WR slope; gate `slope ≥ -0.05/yr`

### Classification

- **FUERTE:** passes all three robustness tests + realistic filter
- **ACEPTABLE:** passes 2 of 3 robustness tests
- **DEBIL:** passes 1 of 3
- **MUERTA:** passes 0

### Phase C output

`reports/orb/orb_robustness.parquet` + `reports/orb/ORB_Robustness.md` human-readable.

## Phase D — Optuna refinement

### Inputs
- `orb_robustness.parquet` filtered to `class ∈ {FUERTE, ACEPTABLE}`

### Study setup (per surviving strategy)

- Sampler: TPE
- Trials: 200
- Pruner: MedianPruner with `n_warmup_steps=20`

### Tunable parameters

Continuous (no discretization):
- `sl_atr_mult ∈ [0.2, 1.2]`
- `tp_atr_mult` constrained to `[sl_atr_mult, sl_atr_mult × 4.0]` (RR ≥ 1:1 enforced via Optuna `suggest_float` lower bound dependency)
- `entry_offset_atr ∈ [-0.5, 0.5]` (negative = LIMIT pullback, positive = STOP retest, 0 = market)
- `or_atr_ratio_min ∈ [0.0, 0.4]` (refine bucket lower edge)
- `or_atr_ratio_max ∈ [0.5, 1.5]` (refine bucket upper edge)
- `pd_distance_atr_min` and `pd_distance_atr_max` (refine pd_or_bucket edges to continuous)

### Objective

```
maximize PF_OOS
  with:
    walk-forward 60/40 inside Optuna (60% IS for param fit, 40% OOS for score)
    penalty if trades_per_year_OOS < 30 (multiply objective by 0.5)
    penalty if MC_ruin > 0.05 (multiply objective by 0.3)
```

### Phase D output

`reports/orb/orb_optuna_results.parquet` with refined parameters per strategy
+ `reports/orb/ORB_Pipeline_Report.md` consolidating Phase A→D results for
human review. No bot config produced in V1; that's a post-review decision.

## Module layout

```
src/engine/
  orb_universe_m1_mgmt.py       # Phase A orchestrator
  orb_management_grid.py        # Phase B orchestrator
  orb_robustness.py             # Phase C thin wrapper over k3m1_robustness
  orb_optuna_refine.py          # Phase D Optuna study runner

src/application/
  orb_patterns.py               # Pattern definitions (event detectors + state classifiers) — pure Polars
  orb_edge_metrics.py           # MFE/MAE M1 walker (Polars slicing + numpy hotpath)
  orb_management_walker.py      # M1 exit walker (TP/SL/MAX_HOLD) — numpy hotpath, mirrors K3M1

scripts/
  run_orb_pipeline.py           # End-to-end orchestrator with --skip-phase A|B|C|D

tests/
  test_orb_patterns.py          # Pattern detection determinism + no look-ahead
  test_orb_edge_metrics.py      # MFE/MAE bounds + edge case (single-bar trigger)
  test_orb_management_walker.py # SL-first tie, MAX_HOLD timeout, friction application

reports/orb/                    # All parquet outputs + ORB_Pipeline_Report.md
```

## Reused components

- `DataEnricher.enrich_with_daily_context` and `enrich_with_opening_range` from `src/application/calculators.py` (no changes)
- `_to_us_utc()` helper for UTC normalization (locate and reuse)
- `friction_real()` from `src/engine/friction_real.py` (extend for NATGAS/SP500/NASDAQ100/EURAUD if snapshots available; otherwise exclude these symbols in V1 with explicit warning)
- `k3m1_robustness` MC bootstrap, walk-forward, decay functions (port to thin wrapper)

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Multiple testing inflation (~370k combos in Phase B) | Phase A `edge_score ≥ 0.3R` aggressive prefilter; Phase C dedup to one management per pattern slot; WF gate `PF_OOS ≥ 0.8 × PF_IS` is strict |
| Event overlap (BREAK_UP + MITIG_PD_MID same trigger) | Daily dedup keeps first event per `(sym, magic_time, duration)` |
| Rare events with low statistical power | `count_per_year ≥ 50` floor in Phase A; raise to 100 for false-break events specifically |
| Friction unavailable for 4 new symbols | V1 ships K3M1-11 universe with warning; V2 adds remaining 4 once Vantage snapshots are captured |
| Look-ahead leakage via timezone | All datetime ops go through `_to_us_utc()`; unit test enforces strict `time > t` in M1 walks |
| Optuna overfitting to OOS fold | 60/40 split inside Optuna AND `MC_ruin` penalty; final report shows both pre-Optuna and post-Optuna metrics for sanity |

## Success criteria

V1 ships when:
1. End-to-end pipeline runs on the 11 K3M1 symbols without errors
2. All four phase parquets exist in `reports/orb/` and are reproducible
3. `reports/orb/ORB_Pipeline_Report.md` is generated with per-strategy summary
   (count, WR, PF_IS, PF_OOS, MC_ruin, decay slope, classification) for
   every (sym, magic_time, duration, pattern, direction) that reached Phase C
4. Unit tests for pattern detection, edge metrics, and management walker pass
   (including explicit no-look-ahead tests)

Note: V1 does NOT have a quality threshold gate (e.g. "≥20 strategies must
survive"). The point of V1 is to produce evidence; the deploy/no-deploy
decision happens after we see the report.

## Open questions deferred to implementation

- Exact `_to_us_utc` location: confirmed in K3M1 codebase, will locate during planning
- Whether to emit per-trade R-multiple series as separate parquet or embed in Phase B (decision: separate parquet `orb_phase_b_trades.parquet` for memory efficiency)
- Whether Phase D Optuna runs in parallel (joblib n_jobs=-1) — yes by default, can disable for debugging
