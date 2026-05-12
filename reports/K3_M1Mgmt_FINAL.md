# K3 Universe + M1 Management — Full Comparison

Re-tested K3-97 universe (15 syms × 6 setups) at 4 signal TFs (M1, M15, H1, H4),
all with M1 management (SL-first conservative). K3-style friction (0.05R FX / 0.10R non-FX).

## Phase A → Phase B funnel

- Phase A combos passing minimal gates: **36816**
- Phase B unique survivors (PF≥1.20, WR≥50%, tpy threshold by TF): **845**

## Aggregate Phase B

- Avg WR: 80.1%
- Avg PF: inf
- Avg Exp R: +0.453
- Sum trades/yr: 116524

## By signal TF

| TF | n | Avg WR | Avg PF | Sum trades/yr |
|---|---|---|---|---|
| **H4** | 234 | 91.4% | inf | 12826 |
| **H1** | 221 | 88.0% | 6.21 | 21919 |
| **M15** | 217 | 80.9% | 3.62 | 40026 |
| **M1** | 173 | 53.8% | 1.72 | 41752 |

## By setup

| Setup | n | Avg PF | Sum trades/yr |
|---|---|---|---|
| OLS_SLOPE_STRONG | 221 | 9.27 | 34201 |
| HURST_TREND_MOM | 219 | inf | 29157 |
| KALMAN_INNOV_EXPAND | 208 | 8.06 | 30871 |
| VELOCITY_ACCEL_GO | 143 | 1.54 | 19264 |
| SPECTRAL_TREND_MOM | 52 | inf | 3011 |
| KAMA_CROSS_MOM | 2 | inf | 21 |

## Top 25 by PF

| # | TF | Symbol | Setup | Session | Dir | TP/SL | n | WR | PF | Exp R | tpy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H4 | EURUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 65 | 100.0% | inf | +0.571 | 9 |
| 2 | H4 | USDJPY | KAMA_CROSS_MOM | ALL_DAY | INVERT | 0.5/0.5 | 37 | 100.0% | inf | +0.490 | 5 |
| 3 | H4 | WTI | HURST_TREND_MOM | LONDON | INVERT | 0.5/1.0 | 226 | 100.0% | inf | +0.252 | 28 |
| 4 | H4 | EURUSD | SPECTRAL_TREND_MOM | LONDON_NY | INVERT | 0.5/1.5 | 48 | 100.0% | inf | +0.057 | 6 |
| 5 | H4 | EURUSD | SPECTRAL_TREND_MOM | NY | INVERT | 0.5/1.5 | 41 | 100.0% | inf | +0.057 | 5 |
| 6 | H4 | USDJPY | SPECTRAL_TREND_MOM | NY | INVERT | 0.5/0.5 | 43 | 100.0% | inf | +0.490 | 6 |
| 7 | H4 | AUDUSD | SPECTRAL_TREND_MOM | LONDON_NY | INVERT | 0.5/1.0 | 47 | 100.0% | inf | +0.173 | 6 |
| 8 | H4 | AUDUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 63 | 100.0% | inf | +0.547 | 8 |
| 9 | H4 | XAGUSD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 64 | 100.0% | inf | +0.758 | 8 |
| 10 | H4 | USDJPY | SPECTRAL_TREND_MOM | LONDON_NY | INVERT | 0.5/0.5 | 50 | 100.0% | inf | +0.490 | 6 |
| 11 | H4 | GBPAUD | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 48 | 100.0% | inf | +0.651 | 6 |
| 12 | H4 | USDJPY | SPECTRAL_TREND_MOM | ALL_DAY | INVERT | 0.5/0.5 | 61 | 100.0% | inf | +0.490 | 8 |
| 13 | H4 | XAGUSD | OLS_SLOPE_STRONG | ASIA | INVERT | 0.5/0.5 | 446 | 99.1% | 67.45 | +0.740 | 55 |
| 14 | H4 | GBPUSD | HURST_TREND_MOM | NY | INVERT | 0.5/0.5 | 436 | 99.3% | 66.67 | +0.618 | 53 |
| 15 | H4 | BRENT | OLS_SLOPE_STRONG | ASIA | INVERT | 0.5/0.5 | 449 | 99.1% | 61.04 | +0.691 | 55 |
| 16 | H4 | GBPAUD | OLS_SLOPE_STRONG | NY | INVERT | 0.5/0.5 | 452 | 98.9% | 50.72 | +0.632 | 55 |
| 17 | H4 | WTI | OLS_SLOPE_STRONG | ASIA | INVERT | 0.5/0.5 | 463 | 98.9% | 49.73 | +0.682 | 57 |
| 18 | H4 | WTI | HURST_TREND_MOM | NY | INVERT | 0.5/0.5 | 452 | 98.9% | 48.35 | +0.679 | 55 |
| 19 | H4 | GBPAUD | HURST_TREND_MOM | NY | INVERT | 0.5/0.5 | 403 | 98.5% | 37.40 | +0.625 | 51 |
| 20 | H4 | EURUSD | OLS_SLOPE_STRONG | ASIA | INVERT | 0.5/0.5 | 465 | 98.9% | 36.76 | +0.549 | 57 |
| 21 | H4 | EURJPY | HURST_TREND_MOM | LONDON_NY | INVERT | 0.5/0.5 | 466 | 98.9% | 35.27 | +0.532 | 57 |
| 22 | H4 | BRENT | OLS_SLOPE_STRONG | ALL_DAY | INVERT | 0.5/0.5 | 645 | 98.4% | 34.84 | +0.678 | 79 |
| 23 | H4 | GBPUSD | KALMAN_INNOV_EXPAND | NY | INVERT | 0.5/0.5 | 570 | 98.4% | 34.61 | +0.605 | 70 |
| 24 | H4 | XAGUSD | KALMAN_INNOV_EXPAND | ASIA | INVERT | 0.5/0.5 | 397 | 98.2% | 34.01 | +0.723 | 49 |
| 25 | H4 | GBPAUD | OLS_SLOPE_STRONG | ALL_DAY | INVERT | 0.5/0.5 | 780 | 98.6% | 33.77 | +0.623 | 96 |