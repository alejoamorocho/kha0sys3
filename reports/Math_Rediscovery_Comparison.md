# Current 6-Setup Bot — Old vs Real Friction

Metrics of the live math portfolio recomputed with per-symbol real friction.

| Sym | Session | Setup | OldFric_R | RealFric_R | WR old | WR new | PF old | PF new | Exp old | Exp new | NewGate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XAUUSD | LONDON | OLS_SLOPE_STRONG | 0.100 | 0.022 | 0.806 | 0.811 | 1.76 | 2.27 | 0.141 | 0.219 | PASS |
| XAUUSD | ASIA | HURST_TREND_MOM | 0.100 | 0.022 | 0.847 | 0.848 | 1.37 | 1.95 | 0.056 | 0.134 | PASS |
| GBPAUD | NY | OLS_SLOPE_STRONG | 0.100 | 0.050 | 0.804 | 0.807 | 1.66 | 1.97 | 0.126 | 0.177 | PASS |
| NASDAQ100 | LONDON | HURST_TREND_MOM | 0.200 | 0.247 | 0.807 | 0.803 | 1.21 | 0.98 | 0.043 | -0.004 | FAIL |
| GBPAUD | ASIA | OLS_SLOPE_STRONG | 0.100 | 0.050 | 0.803 | 0.805 | 1.75 | 2.08 | 0.138 | 0.188 | PASS |
| EURJPY | ASIA | OLS_SLOPE_STRONG | 0.100 | 0.082 | 0.824 | 0.824 | 1.90 | 2.02 | 0.159 | 0.177 | PASS |

Gate: trades/year>=60, WR>=0.55, PF>=1.25, expectancy>=0.05R.
