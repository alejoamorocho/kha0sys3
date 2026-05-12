# M1 Management vs TF-OHLC Management

Re-backtested 110 FUERTE non-FADE strategies (M15/H1/H4 signals).
Signal/entry/dedup/guard semantics IDENTICAL to original.
Exit (TP/SL) detection: walked through M1 bars (first-touch, SL-first on ties).

## Aggregate

| Metric | TF-OHLC mgmt | M1 mgmt | Δ |
|---|---|---|---|
| Avg WR | 60.5% | 54.6% | -5.91pp |
| Avg PF | 2.474 | 2.132 | -0.341 |
| Avg Exp R | +0.767 | +0.682 | - |
| Avg DD | 11.67 | 14.20 | - |
| Sum Net R 8y | 81784 | 60993 | -20791 |
| Strategies improved | - | - | 17/110 |

## Per-TF

| TF | n | WR orig | WR M1 | PF orig | PF M1 | Net R orig | Net R M1 | Δ Net R |
|---|---|---|---|---|---|---|---|---|
| **M15** | 21 | 58.6% | 51.9% | 2.55 | 1.96 | 25652 | 18598 | -7054 |
| **H1** | 63 | 59.2% | 54.1% | 2.38 | 2.11 | 45441 | 35770 | -9671 |
| **H4** | 26 | 65.2% | 57.8% | 2.64 | 2.33 | 10692 | 6624 | -4067 |

## Top 20 IMPROVEMENT (Δ PF descending)

| TF | Symbol | Session | Setup | Dir | PF orig | PF M1 | Δ PF | WR orig | WR M1 |
|---|---|---|---|---|---|---|---|---|---|
| H1 | AUDUSD | NY | OLS_SLOPE_STRONG | INVERT | 3.10 | 4.49 | +1.40 | 53.6% | 57.6% |
| H1 | EURJPY | NY | OLS_SLOPE_STRONG | INVERT | 2.70 | 4.04 | +1.34 | 51.2% | 56.9% |
| H4 | AUDUSD | LONDON_NY | HURST_TREND_MOM | INVERT | 2.48 | 3.27 | +0.80 | 62.1% | 63.0% |
| H1 | XAUUSD | ASIA | OLS_SLOPE_STRONG | INVERT | 3.13 | 3.81 | +0.68 | 50.8% | 46.8% |
| H1 | XAGUSD | NY | HURST_TREND_MOM | INVERT | 2.40 | 2.81 | +0.41 | 58.4% | 58.0% |
| H4 | GBPJPY | LONDON_NY | HURST_TREND_MOM | INVERT | 4.21 | 4.56 | +0.35 | 69.8% | 63.2% |
| H1 | GBPAUD | LONDON_NY | HURST_TREND_MOM | INVERT | 2.62 | 2.95 | +0.33 | 51.5% | 52.5% |
| H4 | USDJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 3.70 | 3.97 | +0.27 | 64.7% | 62.1% |
| H1 | XAUUSD | NY | HURST_TREND_MOM | INVERT | 1.99 | 2.22 | +0.23 | 55.9% | 56.5% |
| H1 | AUDUSD | LONDON | KALMAN_INNOV_EXPAND | INVERT | 1.78 | 1.95 | +0.17 | 54.4% | 51.2% |
| H4 | XAUUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | 3.09 | 3.26 | +0.16 | 55.8% | 51.1% |
| H4 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 3.83 | 3.96 | +0.13 | 68.7% | 64.7% |
| H1 | GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | 2.30 | 2.39 | +0.10 | 54.8% | 54.3% |
| H1 | GBPUSD | NY | HURST_TREND_MOM | INVERT | 3.04 | 3.09 | +0.04 | 54.8% | 54.4% |
| H1 | GBPUSD | LONDON | HURST_TREND_MOM | INVERT | 1.88 | 1.92 | +0.04 | 59.9% | 56.1% |
| H1 | EURJPY | NY | HURST_TREND_MOM | INVERT | 2.07 | 2.10 | +0.03 | 57.6% | 57.1% |
| H1 | AUDUSD | LONDON_NY | KALMAN_INNOV_EXPAND | INVERT | 2.09 | 2.12 | +0.03 | 53.5% | 51.6% |
| H1 | EURJPY | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 2.43 | 2.40 | -0.03 | 54.3% | 52.4% |
| H1 | GBPUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | 2.53 | 2.47 | -0.06 | 55.4% | 52.5% |
| H1 | EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.84 | 1.77 | -0.07 | 62.3% | 57.5% |

## Top 10 DEGRADATION (Δ PF ascending)

| TF | Symbol | Session | Setup | Dir | PF orig | PF M1 | Δ PF |
|---|---|---|---|---|---|---|---|
| H1 | XAGUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 2.78 | 1.39 | -1.39 |
| M15 | XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 2.70 | 1.40 | -1.30 |
| H1 | XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 2.06 | 0.82 | -1.23 |
| H1 | XAGUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 4.57 | 3.35 | -1.22 |
| H4 | XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 2.47 | 1.42 | -1.05 |
| M15 | XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | 4.37 | 3.35 | -1.02 |
| M15 | GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | 3.08 | 2.13 | -0.95 |
| H1 | XAGUSD | ALL_DAY | OLS_SLOPE_STRONG | INVERT | 2.46 | 1.55 | -0.91 |
| H1 | XAGUSD | LONDON_NY | HURST_TREND_MOM | INVERT | 2.24 | 1.33 | -0.91 |
| M15 | XAUUSD | ASIA | HURST_TREND_MOM | INVERT | 2.72 | 1.82 | -0.89 |