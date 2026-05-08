# Walk-Forward IS/OOS — Top 5 M1 Phase K2/K-F

## Configuration

- Windows: 5 rolling non-overlapping
- Split: 70% IS / 30% OOS per window
- No re-optimization in IS — fixed TP=1.0 SL=1.0 from K-F phase
- Friction: 0.05R FX / 0.10R non-FX
- Expected per window: ~210 IS trades + ~90 OOS trades (n=1500-1900 total)
- Robustness gate: OOS WR drop < 5pp AND OOS PF drop < 0.20
- Runtime: 5s (0.1 min)

---

## Per-candidate per-window IS vs OOS

### Candidate 1: EURUSD M1 HURST_TREND_MOM ASIA INV=False TP=1.0 SL=1.0

Full period: n=1490, WR=0.634, PF=1.57, ExpR=0.218

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 208 | 0.606 | 1.39 | 0.162 | 90 | 0.656 | 1.72 | 0.261 | +0.050 | +0.33 |
| 2 | 208 | 0.678 | 1.90 | 0.306 | 90 | 0.622 | 1.49 | 0.194 | -0.056 | -0.41 |
| 3 | 208 | 0.668 | 1.82 | 0.287 | 90 | 0.622 | 1.49 | 0.194 | -0.046 | -0.33 |
| 4 | 208 | 0.644 | 1.64 | 0.238 | 90 | 0.622 | 1.49 | 0.194 | -0.022 | -0.15 |
| 5 | 208 | 0.630 | 1.54 | 0.210 | 90 | 0.522 | 0.99 | -0.006 | -0.108 | -0.55 |
| **AVG** | — | 0.645 | 1.66* | 0.240 | — | 0.609 | 1.44* | 0.168 | -0.036 | -0.22 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 2: USDJPY M1 VELOCITY_ACCEL_GO ASIA INV=False TP=1.0 SL=1.0

Full period: n=1614, WR=0.650, PF=1.68, ExpR=0.250

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 225 | 0.640 | 1.61 | 0.230 | 97 | 0.670 | 1.84 | 0.290 | +0.030 | +0.23 |
| 2 | 225 | 0.716 | 2.28 | 0.381 | 97 | 0.619 | 1.47 | 0.187 | -0.097 | -0.81 |
| 3 | 225 | 0.622 | 1.49 | 0.194 | 97 | 0.598 | 1.35 | 0.146 | -0.024 | -0.14 |
| 4 | 225 | 0.613 | 1.44 | 0.177 | 97 | 0.588 | 1.29 | 0.125 | -0.026 | -0.15 |
| 5 | 225 | 0.693 | 2.05 | 0.337 | 97 | 0.711 | 2.23 | 0.373 | +0.018 | +0.18 |
| **AVG** | — | 0.657 | 1.77* | 0.264 | — | 0.637 | 1.63* | 0.224 | -0.020 | -0.14 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 3: EURUSD M1 KALMAN_INNOV_EXPAND ALL_DAY INV=True TP=1.0 SL=1.0

Full period: n=1888, WR=0.644, PF=1.64, ExpR=0.238

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 263 | 0.627 | 1.52 | 0.205 | 114 | 0.702 | 2.13 | 0.354 | +0.074 | +0.61 |
| 2 | 263 | 0.646 | 1.65 | 0.243 | 114 | 0.763 | 2.92 | 0.476 | +0.117 | +1.26 |
| 3 | 263 | 0.703 | 2.15 | 0.357 | 114 | 0.588 | 1.29 | 0.125 | -0.116 | -0.86 |
| 4 | 263 | 0.639 | 1.60 | 0.228 | 114 | 0.658 | 1.74 | 0.266 | +0.019 | +0.14 |
| 5 | 263 | 0.586 | 1.28 | 0.121 | 114 | 0.570 | 1.20 | 0.090 | -0.015 | -0.08 |
| **AVG** | — | 0.640 | 1.64* | 0.231 | — | 0.656 | 1.85* | 0.262 | +0.016 | +0.21 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 4: EURUSD M1 VELOCITY_ACCEL_GO ALL_DAY INV=True TP=1.0 SL=1.0

Full period: n=1861, WR=0.643, PF=1.63, ExpR=0.236

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 260 | 0.627 | 1.52 | 0.204 | 112 | 0.661 | 1.76 | 0.271 | +0.034 | +0.24 |
| 2 | 260 | 0.662 | 1.77 | 0.273 | 112 | 0.679 | 1.91 | 0.307 | +0.017 | +0.14 |
| 3 | 260 | 0.685 | 1.96 | 0.319 | 112 | 0.679 | 1.91 | 0.307 | -0.006 | -0.05 |
| 4 | 260 | 0.665 | 1.80 | 0.281 | 112 | 0.616 | 1.45 | 0.182 | -0.049 | -0.35 |
| 5 | 260 | 0.600 | 1.36 | 0.150 | 112 | 0.536 | 1.04 | 0.021 | -0.064 | -0.31 |
| **AVG** | — | 0.648 | 1.68* | 0.245 | — | 0.634 | 1.62* | 0.218 | -0.014 | -0.07 |
*PF capped at 99.0 for avg/drift when all-win windows present.

### Candidate 5: USDJPY M1 VELOCITY_ACCEL_GO ALL_DAY INV=False TP=1.0 SL=1.0

Full period: n=1833, WR=0.622, PF=1.49, ExpR=0.195

| window | IS n | IS WR | IS PF | IS expR | OOS n | OOS WR | OOS PF | OOS expR | drift_WR | drift_PF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 256 | 0.602 | 1.37 | 0.153 | 110 | 0.618 | 1.46 | 0.186 | +0.017 | +0.10 |
| 2 | 256 | 0.668 | 1.82 | 0.286 | 110 | 0.609 | 1.41 | 0.168 | -0.059 | -0.41 |
| 3 | 256 | 0.617 | 1.46 | 0.184 | 110 | 0.591 | 1.31 | 0.132 | -0.026 | -0.15 |
| 4 | 256 | 0.582 | 1.26 | 0.114 | 110 | 0.573 | 1.21 | 0.095 | -0.009 | -0.05 |
| 5 | 256 | 0.672 | 1.85 | 0.294 | 110 | 0.673 | 1.86 | 0.295 | +0.001 | +0.01 |
| **AVG** | — | 0.628 | 1.55* | 0.206 | — | 0.613 | 1.45* | 0.175 | -0.015 | -0.10 |
*PF capped at 99.0 for avg/drift when all-win windows present.

---

## Summary table (averages across 5 windows)

| candidate | avg IS WR | avg OOS WR | drift WR | avg IS PF | avg OOS PF | drift PF | OOS robust? |
|---|---|---|---|---|---|---|---|
| 1. EURUSD M1 HURST_TREND_MOM ASIA INV=False TP=1.0 SL=1.0 | 0.645 | 0.609 | -0.036 | 1.66 | 1.44 | -0.22 | NO |
| 2. USDJPY M1 VELOCITY_ACCEL_GO ASIA INV=False TP=1.0 SL=1.0 | 0.657 | 0.637 | -0.020 | 1.77 | 1.63 | -0.14 | YES |
| 3. EURUSD M1 KALMAN_INNOV_EXPAND ALL_DAY INV=True TP=1.0 SL=1.0 | 0.640 | 0.656 | +0.016 | 1.64 | 1.85 | +0.21 | YES |
| 4. EURUSD M1 VELOCITY_ACCEL_GO ALL_DAY INV=True TP=1.0 SL=1.0 | 0.648 | 0.634 | -0.014 | 1.68 | 1.62 | -0.07 | YES |
| 5. USDJPY M1 VELOCITY_ACCEL_GO ALL_DAY INV=False TP=1.0 SL=1.0 | 0.628 | 0.613 | -0.015 | 1.55 | 1.45 | -0.10 | YES |

---

## Robustness verdict

- **OOS robust** = OOS WR drop < 5pp AND OOS PF drop < 0.20
- Candidates evaluated: 5/5
- **Survivors that pass robustness: 4/5**

### Per-candidate verdict

- **Candidate 1** (EURUSD M1 HURST_TREND_MOM ASIA INV=False TP=1.0 SL=1.0): FAIL — PF drop -0.22 < -0.20 threshold
- **Candidate 2** (USDJPY M1 VELOCITY_ACCEL_GO ASIA INV=False TP=1.0 SL=1.0): PASS — avg OOS WR=0.637 (drift -0.020), avg OOS PF=1.63 (drift -0.14)
- **Candidate 3** (EURUSD M1 KALMAN_INNOV_EXPAND ALL_DAY INV=True TP=1.0 SL=1.0): PASS — avg OOS WR=0.656 (drift +0.016), avg OOS PF=1.85 (drift +0.21)
- **Candidate 4** (EURUSD M1 VELOCITY_ACCEL_GO ALL_DAY INV=True TP=1.0 SL=1.0): PASS — avg OOS WR=0.634 (drift -0.014), avg OOS PF=1.62 (drift -0.07)
- **Candidate 5** (USDJPY M1 VELOCITY_ACCEL_GO ALL_DAY INV=False TP=1.0 SL=1.0): PASS — avg OOS WR=0.613 (drift -0.015), avg OOS PF=1.45 (drift -0.10)

