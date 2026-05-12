# Trend Filter Study

Adds 4 higher-TF trend filters to math strategies (WR>=0.60, PF>=1.5).
Only trades aligned with the HTF trend pass through.

## Filters
- A_h1slope: H1 EMA50 slope (rising=LONG, falling=SHORT)
- B_h4ema200: H4 close vs EMA200 (above=LONG, below=SHORT)
- C_h4sma: H4 SMA20 vs SMA50 (20>50=LONG)
- D_d1ema50: D1 close vs EMA50 (above=LONG)

## Aggregate (avg across studied strategies)

| Filter | AvgWR | AvgPF | AvgExp | AvgMaxDD | AvgTpy |
|---|---|---|---|---|---|
| BASELINE | 0.662 | 2.28 | +0.462 | 9.3 | 178 |
| A_h1slope | 0.670 | 2.37 | +0.468 | 7.3 | 79 |
| B_h4ema200 | 0.668 | 2.34 | +0.468 | 8.0 | 103 |
| C_h4sma | 0.669 | 2.36 | +0.472 | 8.2 | 114 |
| D_d1ema50 | 0.666 | 2.33 | +0.466 | 8.0 | 106 |

## Top improvements (filter exp > baseline)

| Symbol | Session | Setup | TP/SL | Filter | WR base->filt | PF base->filt | Exp base->filt | Trades base->filt |
|---|---|---|---|---|---|---|---|---|
| GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | 1.0/0.75 | A_h1slope | 0.66->0.73 | 2.19->2.99 | +0.443->+0.595 (+0.152) | 514->295 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.5/1.0 | B_h4ema200 | 0.61->0.67 | 1.93->2.62 | +0.382->+0.528 (+0.146) | 1038->611 |
| XAGUSD | NY | OLS_SLOPE_STRONG | 1.5/0.75 | A_h1slope | 0.62->0.69 | 2.67->3.54 | +0.665->+0.802 (+0.137) | 1562->432 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.25/0.75 | B_h4ema200 | 0.61->0.66 | 2.21->2.84 | +0.507->+0.636 (+0.129) | 1038->611 |
| XAGUSD | NY | OLS_SLOPE_STRONG | 1.0/0.75 | A_h1slope | 0.69->0.76 | 2.58->3.54 | +0.505->+0.630 (+0.125) | 1562->432 |
| XAGUSD | NY | OLS_SLOPE_STRONG | 1.25/0.75 | A_h1slope | 0.65->0.71 | 2.61->3.47 | +0.586->+0.711 (+0.124) | 1562->432 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.5/1.0 | D_d1ema50 | 0.61->0.66 | 1.93->2.49 | +0.382->+0.503 (+0.121) | 1038->610 |
| XAGUSD | NY | OLS_SLOPE_STRONG | 1.5/1.0 | A_h1slope | 0.64->0.71 | 2.25->3.04 | +0.451->+0.570 (+0.119) | 1562->432 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.25/0.75 | D_d1ema50 | 0.61->0.66 | 2.21->2.77 | +0.507->+0.623 (+0.116) | 1038->610 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.5/1.0 | C_h4sma | 0.61->0.66 | 1.93->2.46 | +0.382->+0.498 (+0.116) | 1038->646 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.25/1.0 | B_h4ema200 | 0.65->0.70 | 1.99->2.63 | +0.359->+0.472 (+0.113) | 1038->611 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.25/0.75 | C_h4sma | 0.61->0.66 | 2.21->2.73 | +0.507->+0.617 (+0.111) | 1038->646 |
| EURJPY | ALL_DAY | OLS_SLOPE_STRONG | 1.25/0.75 | A_h1slope | 0.61->0.66 | 2.25->2.70 | +0.530->+0.640 (+0.110) | 2224->1016 |
| XAGUSD | NY | OLS_SLOPE_STRONG | 1.25/1.0 | A_h1slope | 0.67->0.74 | 2.20->3.00 | +0.394->+0.503 (+0.109) | 1562->432 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.0/0.75 | B_h4ema200 | 0.67->0.72 | 2.30->2.95 | +0.461->+0.570 (+0.109) | 1038->611 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.25/1.0 | D_d1ema50 | 0.65->0.70 | 1.99->2.58 | +0.359->+0.465 (+0.106) | 1038->610 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.25/1.0 | C_h4sma | 0.65->0.70 | 1.99->2.55 | +0.359->+0.462 (+0.103) | 1038->646 |
| GBPUSD | ALL_DAY | SPECTRAL_TREND_MOM | 1.25/0.75 | A_h1slope | 0.60->0.64 | 2.16->2.55 | +0.503->+0.604 (+0.101) | 514->295 |
| GBPUSD | ASIA | OLS_SLOPE_STRONG | 1.0/0.75 | A_h1slope | 0.71->0.76 | 2.81->3.53 | +0.585->+0.685 (+0.099) | 751->182 |
| EURJPY | LONDON_NY | OLS_SLOPE_STRONG | 1.25/0.75 | A_h1slope | 0.61->0.65 | 2.17->2.64 | +0.500->+0.598 (+0.098) | 1900->662 |
| EURUSD | NY | OLS_SLOPE_STRONG | 1.0/0.75 | B_h4ema200 | 0.69->0.74 | 2.52->3.21 | +0.501->+0.599 (+0.098) | 1716->808 |
| EURUSD | NY | OLS_SLOPE_STRONG | 1.25/0.75 | B_h4ema200 | 0.64->0.68 | 2.43->2.96 | +0.561->+0.656 (+0.096) | 1716->808 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.0/0.75 | C_h4sma | 0.67->0.71 | 2.30->2.84 | +0.461->+0.554 (+0.093) | 1038->646 |
| XAGUSD | LONDON | HURST_TREND_MOM | 1.0/0.75 | D_d1ema50 | 0.67->0.71 | 2.30->2.85 | +0.461->+0.554 (+0.093) | 1038->610 |
| GBPJPY | ASIA | HURST_TREND_MOM | 1.25/0.75 | A_h1slope | 0.61->0.65 | 2.21->2.64 | +0.510->+0.602 (+0.092) | 1157->655 |
| EURUSD | LONDON | OLS_SLOPE_STRONG | 1.25/0.75 | A_h1slope | 0.64->0.68 | 2.51->3.00 | +0.578->+0.667 (+0.089) | 1562->473 |
| GBPJPY | ASIA | HURST_TREND_MOM | 1.0/0.75 | A_h1slope | 0.67->0.71 | 2.31->2.82 | +0.465->+0.553 (+0.088) | 1157->655 |
| EURJPY | ASIA | OLS_SLOPE_STRONG | 1.25/0.75 | A_h1slope | 0.62->0.67 | 2.29->2.71 | +0.532->+0.619 (+0.087) | 1162->297 |
| XAGUSD | NY | OLS_SLOPE_STRONG | 0.75/0.75 | A_h1slope | 0.73->0.78 | 2.38->3.11 | +0.379->+0.466 (+0.087) | 1562->432 |
| XAGUSD | ASIA | KALMAN_INNOV_EXPAND | 0.75/0.75 | A_h1slope | 0.73->0.77 | 2.24->2.81 | +0.359->+0.442 (+0.082) | 1404->694 |
