# Optuna Management Optimization (with realistic friction)

Optimization on 35 strategies. Search space TP/SL ∈ [0.3, 3.5] step 0.1, expanded if at boundary.
Friction: per-symbol Vantage + 0.2R slippage.
Constraints: trades/yr ≥ 30, WR > 0.50, PF > 1.0. Objective: maximize expectancy_r.

## Per-strategy results (sorted by opt_exp)

| Symbol | Sess | Setup | Dir | TP cur->opt | SL cur->opt | WR cur->opt | PF cur->opt | Exp cur->opt | DD opt | TPY opt | Net R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XAGUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.50->1.10 | 0.75->0.50 | 0.552->0.631 | 1.75->2.70 | +0.411->+0.774 | 6.2 | 52 | +322.7 |
| XAGUSD | NY | GARCH_Z_FADE | NORMAL | 1.25->1.10 | 0.75->0.50 | 0.614->0.623 | 1.87->2.58 | +0.396->+0.730 | 8.8 | 122 | +728.1 |
| EURJPY | NY | OLS_SLOPE_STRONG | INVERT | 1.50->1.30 | 0.75->0.50 | 0.594->0.600 | 1.74->2.19 | +0.378->+0.655 | 11.3 | 183 | +984.6 |
| GBPAUD | NY | OLS_SLOPE_STRONG | INVERT | 1.50->1.20 | 0.75->0.50 | 0.570->0.587 | 1.68->2.11 | +0.360->+0.602 | 9.4 | 176 | +867.6 |
| XAGUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.50->0.80 | 0.75->0.50 | 0.554->0.705 | 1.76->2.61 | +0.412->+0.587 | 10.5 | 201 | +970.9 |
| XAUUSD | NY | GARCH_Z_FADE | NORMAL | 1.50->1.00 | 0.75->0.50 | 0.521->0.613 | 1.53->2.21 | +0.304->+0.575 | 7.4 | 123 | +578.8 |
| GBPUSD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.50->1.10 | 0.75->0.50 | 0.551->0.608 | 1.57->2.08 | +0.333->+0.573 | 10.0 | 216 | +1019.1 |
| GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.50->1.30 | 1.00->0.50 | 0.605->0.539 | 1.45->1.90 | +0.224->+0.567 | 15.2 | 63 | +291.5 |
| EURUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 2.00->1.10 | 0.75->0.50 | 0.520->0.622 | 1.68->2.04 | +0.414->+0.550 | 12.9 | 190 | +859.7 |
| GBPUSD | ASIA | OLS_SLOPE_STRONG | INVERT | 1.50->1.40 | 0.75->0.70 | 0.615->0.623 | 2.06->2.12 | +0.523->+0.547 | 9.4 | 91 | +410.8 |
| AUDUSD | LONDON_NY | OLS_SLOPE_STRONG | INVERT | 1.50->1.20 | 0.75->0.50 | 0.557->0.588 | 1.49->1.91 | +0.288->+0.534 | 17.7 | 221 | +970.7 |
| GBPAUD | ALL_DAY | HURST_TREND_MOM | INVERT | 1.50->1.10 | 0.75->0.50 | 0.526->0.587 | 1.43->1.94 | +0.264->+0.520 | 14.8 | 209 | +893.7 |
| EURJPY | LONDON_NY | SPECTRAL_TREND_MOM | INVERT | 1.50->1.20 | 0.75->0.50 | 0.554->0.577 | 1.46->1.82 | +0.268->+0.482 | 10.2 | 33 | +128.8 |
| GBPJPY | ASIA | OLS_SLOPE_STRONG | INVERT | 1.50->1.20 | 0.75->0.60 | 0.563->0.610 | 1.62->1.88 | +0.344->+0.466 | 14.1 | 131 | +499.5 |
| GBPJPY | ASIA | HURST_TREND_MOM | INVERT | 1.25->1.20 | 0.75->0.60 | 0.608->0.607 | 1.57->1.86 | +0.289->+0.450 | 10.6 | 141 | +520.6 |
| XAUUSD | LONDON | OLS_SLOPE_STRONG | INVERT | 1.50->1.20 | 0.75->0.70 | 0.582->0.636 | 1.87->2.01 | +0.435->+0.450 | 11.8 | 156 | +573.9 |
| EURJPY | NY | HURST_TREND_MOM | INVERT | 1.50->1.20 | 0.75->0.50 | 0.543->0.569 | 1.38->1.74 | +0.222->+0.445 | 12.8 | 153 | +560.1 |
| XAGUSD | NY | OLS_SLOPE_STRONG | INVERT | 2.00->1.60 | 0.75->0.90 | 0.539->0.612 | 2.07->1.99 | +0.565->+0.428 | 11.1 | 190 | +668.2 |
| EURUSD | ASIA | HURST_TREND_MOM | INVERT | 1.50->1.00 | 0.75->0.60 | 0.573->0.681 | 1.61->1.94 | +0.339->+0.416 | 9.6 | 126 | +429.5 |
| XAUUSD | ASIA | HURST_TREND_MOM | INVERT | 1.50->0.60 | 0.75->0.50 | 0.552->0.751 | 1.68->2.34 | +0.365->+0.414 | 6.7 | 132 | +448.4 |
| GBPJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.25->1.00 | 0.75->0.50 | 0.560->0.599 | 1.28->1.73 | +0.162->+0.406 | 18.0 | 249 | +831.7 |
| USDJPY | ALL_DAY | HURST_TREND_MOM | INVERT | 1.50->1.20 | 0.75->0.50 | 0.544->0.561 | 1.34->1.59 | +0.214->+0.389 | 16.2 | 227 | +726.8 |
| AUDUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.50->1.20 | 0.75->0.50 | 0.514->0.543 | 1.26->1.58 | +0.167->+0.383 | 23.8 | 196 | +618.1 |
| USDJPY | LONDON | OLS_SLOPE_STRONG | INVERT | 1.50->0.90 | 0.75->0.50 | 0.555->0.667 | 1.41->1.77 | +0.239->+0.374 | 10.8 | 161 | +493.9 |
| AUDUSD | LONDON | HURST_TREND_MOM | INVERT | 1.50->1.50 | 0.75->0.60 | 0.538->0.514 | 1.39->1.55 | +0.233->+0.363 | 13.4 | 138 | +411.6 |
| GBPAUD | NY | GARCH_Z_FADE | NORMAL | 1.25->0.80 | 0.75->0.50 | 0.558->0.647 | 1.32->1.72 | +0.174->+0.333 | 9.7 | 77 | +210.9 |
| EURUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.50->1.10 | 0.75->0.60 | 0.542->0.617 | 1.37->1.62 | +0.223->+0.330 | 15.7 | 163 | +441.1 |
| EURJPY | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.50->1.00 | 0.75->0.50 | 0.507->0.591 | 1.23->1.56 | +0.154->+0.327 | 17.7 | 242 | +650.6 |
| GBPAUD | ALL_DAY | KALMAN_INNOV_EXPAND | INVERT | 1.50->1.00 | 0.75->0.70 | 0.535->0.667 | 1.50->1.72 | +0.297->+0.313 | 13.9 | 242 | +621.5 |
| XAUUSD | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.50->0.60 | 0.75->0.50 | 0.524->0.715 | 1.54->1.84 | +0.317->+0.308 | 6.6 | 58 | +145.6 |
| GBPUSD | ASIA | KALMAN_INNOV_EXPAND | INVERT | 1.50->1.10 | 0.75->0.60 | 0.532->0.594 | 1.37->1.55 | +0.220->+0.302 | 13.8 | 166 | +412.3 |
| EURUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 1.25->1.10 | 0.75->0.60 | 0.561->0.576 | 1.26->1.42 | +0.149->+0.245 | 18.0 | 152 | +305.3 |
| AUDUSD | LONDON_NY | GARCH_Z_FADE | NORMAL | 1.25->0.90 | 0.75->0.50 | 0.555->0.599 | 1.21->1.41 | +0.122->+0.231 | 15.1 | 111 | +210.5 |
| GBPJPY | NY | GARCH_Z_FADE | NORMAL | 1.25->1.20 | 0.75->0.60 | 0.537->0.525 | 1.19->1.35 | +0.108->+0.211 | 18.9 | 71 | +123.7 |
| USDJPY | ALL_DAY | SPECTRAL_TREND_MOM | INVERT | 1.25->1.20 | 0.75->0.70 | 0.581->0.579 | 1.28->1.29 | +0.157->+0.167 | 25.1 | 54 | +73.7 |

## Aggregate

- Avg WR (cur->opt): 0.555 -> 0.610
- Avg PF (cur->opt): 1.52 -> 1.88
- Avg Exp (cur->opt): +0.288 -> +0.441
- Avg DD opt: 13.06
- Sum trades/yr: 5214
- Sum Net R (3y): 19004.6
- Strategies with boundary expansion: 0
