# Universe Pruning Recommendation

## Symbols with ZERO surviving strategies under real friction

- **NASDAQ100** (drop from math discovery universe)
- **NATGAS** (drop from math discovery universe)
- **SP500** (drop from math discovery universe)
- **VIX** (drop from math discovery universe)

## Symbols with surviving strategies (keep)

- **AUDUSD** — 391 validated combos
- **BRENT** — 473 validated combos
- **EURJPY** — 344 validated combos
- **EURUSD** — 394 validated combos
- **GBPAUD** — 484 validated combos
- **GBPJPY** — 377 validated combos
- **GBPUSD** — 335 validated combos
- **USDJPY** — 232 validated combos
- **WTI** — 496 validated combos
- **XAGUSD** — 546 validated combos
- **XAUUSD** — 482 validated combos

## New (symbol, session, setup) combinations in portfolio but NOT in current 6-setup bot

- XAGUSD / ALL_DAY / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.789R, WR=0.616, PF=3.03, trades/yr=264)
- WTI / NY / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.596R, WR=0.569, PF=2.33, trades/yr=215)
- BRENT / NY / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.626R, WR=0.585, PF=2.47, trades/yr=200)
- AUDUSD / LONDON_NY / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.488R, WR=0.566, PF=1.98, trades/yr=221)
- EURJPY / NY / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.578R, WR=0.610, PF=2.34, trades/yr=183)
- EURUSD / LONDON / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.556R, WR=0.590, PF=2.23, trades/yr=190)
- GBPJPY / ASIA / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.544R, WR=0.569, PF=2.15, trades/yr=131)
- AUDUSD / ASIA / KALMAN_INNOV_EXPAND / INVERT TP=1.25 SL=0.75 (exp=0.361R, WR=0.576, PF=1.75, trades/yr=196)
- EURUSD / ASIA / HURST_TREND_MOM / INVERT TP=1.5 SL=0.75 (exp=0.539R, WR=0.583, PF=2.14, trades/yr=126)
- GBPUSD / ASIA / OLS_SLOPE_STRONG / INVERT TP=1.5 SL=0.75 (exp=0.723R, WR=0.626, PF=2.73, trades/yr=91)
- USDJPY / NY / HURST_TREND_MOM / INVERT TP=1.5 SL=0.75 (exp=0.406R, WR=0.559, PF=1.80, trades/yr=162)
- XAUUSD / NY / GARCH_Z_FADE / NORMAL TP=1.25 SL=0.75 (exp=0.486R, WR=0.584, PF=2.15, trades/yr=123)
- USDJPY / ASIA / KALMAN_INNOV_EXPAND / INVERT TP=1.25 SL=0.75 (exp=0.287R, WR=0.566, PF=1.56, trades/yr=192)
- BRENT / ASIA / HURST_TREND_MOM / INVERT TP=1.25 SL=0.75 (exp=0.604R, WR=0.636, PF=2.69, trades/yr=90)
- WTI / ASIA / HURST_TREND_MOM / INVERT TP=1.5 SL=0.75 (exp=0.569R, WR=0.584, PF=2.35, trades/yr=85)
- GBPUSD / NY / VELOCITY_ACCEL_GO / INVERT TP=1.0 SL=0.75 (exp=0.209R, WR=0.566, PF=1.44, trades/yr=204)
- GBPUSD / LONDON / GARCH_Z_FADE / NORMAL TP=1.25 SL=0.75 (exp=0.381R, WR=0.574, PF=1.82, trades/yr=109)
- GBPJPY / NY / GARCH_Z_FADE / NORMAL TP=1.25 SL=0.75 (exp=0.308R, WR=0.556, PF=1.64, trades/yr=71)
- EURJPY / LONDON / GARCH_Z_FADE / NORMAL TP=1.0 SL=0.75 (exp=0.247R, WR=0.607, PF=1.55, trades/yr=81)
