# Traditional Indicators Rediscovery — REAL Broker Friction

Parallel sibling of the math-indicator pipeline. Same data, same
validation engine, different signal family.

- Phase A passers (trades/yr>=30, WR>0.50, PF>1.0, exp>0): **2**
- Phase B validated (WF>=0.80, MC<=0.02, decay>=0.60): **0**
- Phase C portfolio (session-disjoint, cap 4/symbol): **0**

Grid: TP {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0} x SL {0.75,1.0,1.5,2.0,2.5},
10 traditional setups (RSI/MACD/BB/ADX/Fractal),
5 sessions, 15 symbols, NORMAL + INVERT direction.

Friction: per-symbol USD per round-turn at vol_min, converted to R via
`friction_r = usd / (sl * median_atr * tick_val/tick_size * vol_min)` + 0.2R execution slippage.

Diagnostic: `combos_evaluated=4800
combos_with_>=30_trades=36000
survivors=2
max_WR_observed=0.794
max_PF_observed=1.21
max_exp_observed=0.180`

## Per-symbol max metrics across Phase-A grid (diagnostic)

| Symbol | n_combos | max WR | max PF | max exp_R |
|---|---|---|---|---|
| VIX | 2400 | 0.783 | 1.21 | 0.180 |
| XAGUSD | 2400 | 0.794 | 0.94 | -0.055 |
| GBPUSD | 2400 | 0.772 | 0.91 | -0.063 |
| XAUUSD | 2400 | 0.776 | 0.91 | -0.088 |
| WTI | 2400 | 0.770 | 0.88 | -0.092 |
| GBPJPY | 2400 | 0.768 | 0.88 | -0.116 |
| BRENT | 2400 | 0.781 | 0.86 | -0.128 |
| GBPAUD | 2400 | 0.784 | 0.85 | -0.126 |
| EURUSD | 2400 | 0.779 | 0.83 | -0.134 |
| USDJPY | 2400 | 0.767 | 0.80 | -0.171 |
| AUDUSD | 2400 | 0.768 | 0.77 | -0.188 |
| EURJPY | 2400 | 0.766 | 0.75 | -0.202 |
| NASDAQ100 | 2400 | 0.695 | 0.60 | -0.351 |
| SP500 | 2400 | 0.566 | 0.40 | -0.612 |
| NATGAS | 2400 | 0.395 | 0.09 | -1.470 |


## Phase B attribution

- Phase A survivors: 2
- Phase B survivors: 0
- All Phase A survivors were eliminated by MC ruin and/or decay; WF was OK (~1.01) but the absolute edge (PF~1.02, exp~0.012R) is too thin for 2% Monte-Carlo risk and recent 6-month decay is strongly negative.

