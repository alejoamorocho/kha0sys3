# Walk-Forward IS/OOS — Top 5 Phase K2

## Configuration

- Windows: 5 rolling non-overlapping
- Split: 70% IS / 30% OOS per window
- No re-optimization in IS — fixed TP/SL from K2
- Friction: 0.05R FX (EURUSD/USDJPY/GBPAUD) / 0.10R non-FX (WTI/NASDAQ100)
- Robustness gate: OOS WR drop < 5pp AND OOS PF drop < 0.20
- Runtime: 3s (0.1 min)

---

## Per-candidate per-window IS vs OOS

### Candidate 1: NASDAQ100 M15 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00

Full period: n=36, WR=0.722, PF=1.90, ExpR=0.215
> **Note:** min OOS window = 3 trades — per-window metrics are low-count and noisy. PF capped at 99.0 for avg/drift (all-win windows shown as inf).

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 1.000 | inf | 0.600 | 3 | 1.000 | inf | 0.600 | +0.000 | +0.00 |
| 2 | 4 | 1.000 | inf | 0.797 | 3 | 0.333 | 0.27 | -0.533 | -0.667 | -98.73 |
| 3 | 4 | 0.750 | 1.64 | 0.175 | 3 | 0.333 | 0.32 | -0.430 | -0.417 | -1.32 |
| 4 | 4 | 0.250 | 0.26 | -0.437 | 3 | 1.000 | inf | 0.600 | +0.750 | +98.74 |
| 5 | 4 | 0.750 | 1.64 | 0.175 | 3 | 0.667 | 308.40 | 0.399 | -0.083 | +97.36 |
| **AVG** | — | 0.750 | 40.31* | 0.262 | — | 0.667 | 59.52* | 0.127 | -0.083 | +19.21 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 2: GBPAUD H1 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00

Full period: n=41, WR=0.659, PF=1.86, ExpR=0.177
> **Note:** min OOS window = 3 trades — per-window metrics are low-count and noisy. PF capped at 99.0 for avg/drift (all-win windows shown as inf).

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 0.400 | 0.32 | -0.339 | 3 | 1.000 | inf | 0.650 | +0.600 | +98.68 |
| 2 | 5 | 0.800 | 13.38 | 0.481 | 3 | 0.333 | 0.54 | -0.080 | -0.467 | -12.85 |
| 3 | 5 | 0.600 | 1.26 | 0.080 | 3 | 0.667 | 75.27 | 0.221 | +0.067 | +74.02 |
| 4 | 5 | 1.000 | inf | 0.579 | 3 | 0.333 | 0.47 | -0.243 | -0.667 | -98.53 |
| 5 | 5 | 0.600 | 1.56 | 0.140 | 3 | 0.667 | 1.24 | 0.083 | +0.067 | -0.32 |
| **AVG** | — | 0.680 | 23.10* | 0.188 | — | 0.600 | 35.30* | 0.126 | -0.080 | +12.20 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 3: WTI M15 SPECTRAL_TREND_MOM ASIA TP=0.50 SL=1.50

Full period: n=66, WR=0.712, PF=2.13, ExpR=0.157
> **Note:** min OOS window = 4 trades — per-window metrics are low-count and noisy. PF capped at 99.0 for avg/drift (all-win windows shown as inf).

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 9 | 0.667 | 1.03 | 0.005 | 4 | 0.750 | 3.99 | 0.131 | +0.083 | +2.96 |
| 2 | 9 | 0.556 | 0.40 | -0.198 | 4 | 1.000 | inf | 0.233 | +0.444 | +98.60 |
| 3 | 9 | 0.556 | 0.39 | -0.199 | 4 | 0.500 | 26.61 | 2.230 | -0.056 | +26.22 |
| 4 | 9 | 0.778 | 2.95 | 0.120 | 4 | 1.000 | inf | 0.190 | +0.222 | +96.05 |
| 5 | 9 | 0.889 | 35.42 | 0.190 | 4 | 0.500 | 0.62 | -0.072 | -0.389 | -34.80 |
| **AVG** | — | 0.689 | 8.04* | -0.017 | — | 0.750 | 45.84* | 0.543 | +0.061 | +37.81 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 4: EURUSD H1 KAMA_CROSS_MOM NY INV=True TP=1.50 SL=2.00

Full period: n=67, WR=0.612, PF=1.67, ExpR=0.118
> **Note:** min OOS window = 4 trades — per-window metrics are low-count and noisy. PF capped at 99.0 for avg/drift (all-win windows shown as inf).

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 9 | 0.333 | 0.96 | -0.008 | 4 | 0.500 | 0.53 | -0.144 | +0.167 | -0.43 |
| 2 | 9 | 0.667 | 1.56 | 0.089 | 4 | 0.500 | 0.48 | -0.276 | -0.167 | -1.08 |
| 3 | 9 | 0.778 | 4.31 | 0.232 | 4 | 1.000 | inf | 0.298 | +0.222 | +94.69 |
| 4 | 9 | 0.778 | 10.30 | 0.456 | 4 | 0.500 | 0.28 | -0.217 | -0.278 | -10.02 |
| 5 | 9 | 0.556 | 1.57 | 0.126 | 4 | 0.500 | 2.02 | 0.176 | -0.056 | +0.45 |
| **AVG** | — | 0.622 | 3.74* | 0.179 | — | 0.600 | 20.46* | -0.032 | -0.022 | +16.72 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 5: USDJPY M15 SPECTRAL_TREND_MOM LONDON TP=0.70 SL=1.00

Full period: n=118, WR=0.669, PF=2.10, ExpR=0.330
> **Note:** min OOS window = 7 trades — per-window metrics are low-count and noisy. PF capped at 99.0 for avg/drift (all-win windows shown as inf).

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 16 | 0.750 | 1.93 | 0.202 | 7 | 0.286 | 0.25 | -0.564 | -0.464 | -1.69 |
| 2 | 16 | 0.688 | 7.51 | 1.752 | 7 | 0.571 | 0.83 | -0.079 | -0.116 | -6.69 |
| 3 | 16 | 0.500 | 0.94 | -0.021 | 7 | 0.857 | 3.71 | 0.407 | +0.357 | +2.77 |
| 4 | 16 | 0.688 | 1.20 | 0.065 | 7 | 0.714 | 1.55 | 0.164 | +0.027 | +0.35 |
| 5 | 16 | 0.750 | 2.30 | 0.275 | 7 | 0.857 | 3.71 | 0.407 | +0.107 | +1.42 |
| **AVG** | — | 0.675 | 2.78* | 0.455 | — | 0.657 | 2.01* | 0.067 | -0.018 | -0.77 |
*PF capped at 99.0 for avg/drift when all-win windows present.

---

## Summary table (averages across 5 windows)

| candidate | avg IS WR | avg OOS WR | drift WR | avg IS PF | avg OOS PF | drift PF | OOS robust? |
|---|---|---|---|---|---|---|---|
| 1. NASDAQ100 M15 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00 | 0.750 | 0.667 | -0.083 | 40.31 | 59.52 | +19.21 | NO |
| 2. GBPAUD H1 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00 | 0.680 | 0.600 | -0.080 | 23.10 | 35.30 | +12.20 | NO |
| 3. WTI M15 SPECTRAL_TREND_MOM ASIA TP=0.50 SL=1.50 | 0.689 | 0.750 | +0.061 | 8.04 | 45.84 | +37.81 | NO |
| 4. EURUSD H1 KAMA_CROSS_MOM NY INV=True TP=1.50 SL=2.00 | 0.622 | 0.600 | -0.022 | 3.74 | 20.46 | +16.72 | YES |
| 5. USDJPY M15 SPECTRAL_TREND_MOM LONDON TP=0.70 SL=1.00 | 0.675 | 0.657 | -0.018 | 2.78 | 2.01 | -0.77 | NO |

---

## Robustness verdict

- **OOS robust** = OOS WR drop < 5pp AND OOS PF drop < 0.20
- Candidates evaluated: 5/5
- **Survivors that pass robustness: 1/5**

### Per-candidate verdict

- **Candidate 1** (NASDAQ100 M15 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00): FAIL — WR instability -0.083 (|drift| > 0.05)
- **Candidate 2** (GBPAUD H1 KAMA_CROSS_MOM ASIA TP=0.70 SL=1.00): FAIL — WR instability -0.080 (|drift| > 0.05)
- **Candidate 3** (WTI M15 SPECTRAL_TREND_MOM ASIA TP=0.50 SL=1.50): FAIL — WR instability +0.061 (|drift| > 0.05)
- **Candidate 4** (EURUSD H1 KAMA_CROSS_MOM NY INV=True TP=1.50 SL=2.00): PASS — avg OOS WR=0.600 (drift -0.022), avg OOS PF=20.46 (drift +16.72)
- **Candidate 5** (USDJPY M15 SPECTRAL_TREND_MOM LONDON TP=0.70 SL=1.00): FAIL — PF drop -0.77 < -0.20 threshold

