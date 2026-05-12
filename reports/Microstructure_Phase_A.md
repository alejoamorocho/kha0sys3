# Microstructure Tick-Imbalance — Phase A

- Combos kept (n_trades>=25, t/yr>=20): **46320**
- Proxies: CLOSE_VS_MID, TICK_RULE, BAR_DELTA
- Windows: (50, 100, 200)
- Entry-z grid: (1.5, 2.0, 2.5, 3.0)
- Signal kinds: ('MOMENTUM', 'FADE')
- Direction modes: ('NORMAL', 'INVERT')
- R:R Phase-A grid: ((0.5, 1.0), (0.5, 2.0), (1.0, 1.0), (1.0, 2.0), (2.0, 1.0), (2.0, 2.0))

## Distribution by proxy

| Proxy | Combos | Avg Exp R | Avg PF |
|---|---|---|---|
| TICK_RULE | 15588 | -0.1361 | 0.65 |
| BAR_DELTA | 15192 | -0.1372 | 0.65 |
| CLOSE_VS_MID | 15540 | -0.1399 | 0.65 |

## Distribution by signal kind

| Kind | Combos | Avg Exp R | Avg PF |
|---|---|---|---|
| FADE | 23160 | -0.1377 | 0.65 |
| MOMENTUM | 23160 | -0.1377 | 0.65 |

## Top 30 by expectancy_r

| Symbol | Sess | Proxy | Win | Z | Kind | Dir | TP | SL | n | WR | PF | Exp(R) | DD | T/yr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VIX | ALL_DAY | TICK_RULE | 200 | 2.0 | MOMENTUM | INVERT | 2.0 | 1.0 | 153 | 0.562 | 1.77 | +0.388 | 7.8 | 45.2 |
| VIX | ALL_DAY | TICK_RULE | 200 | 2.0 | FADE | NORMAL | 2.0 | 1.0 | 153 | 0.562 | 1.77 | +0.388 | 4.8 | 45.2 |
| VIX | LONDON_NY | BAR_DELTA | 200 | 2.5 | FADE | NORMAL | 2.0 | 1.0 | 89 | 0.517 | 1.52 | +0.286 | 12.6 | 26.5 |
| VIX | LONDON_NY | BAR_DELTA | 200 | 2.5 | MOMENTUM | INVERT | 2.0 | 1.0 | 89 | 0.517 | 1.52 | +0.286 | 15.6 | 26.5 |
| VIX | LONDON_NY | BAR_DELTA | 100 | 2.5 | MOMENTUM | NORMAL | 2.0 | 1.0 | 82 | 0.500 | 1.43 | +0.242 | 6.9 | 24.1 |
| VIX | LONDON_NY | BAR_DELTA | 100 | 2.5 | FADE | INVERT | 2.0 | 1.0 | 82 | 0.500 | 1.43 | +0.242 | 6.6 | 24.1 |
| EURJPY | LONDON | CLOSE_VS_MID | 50 | 2.5 | MOMENTUM | NORMAL | 2.0 | 1.0 | 171 | 0.456 | 1.45 | +0.239 | 6.6 | 21.0 |
| EURJPY | LONDON | CLOSE_VS_MID | 50 | 2.5 | FADE | INVERT | 2.0 | 1.0 | 171 | 0.456 | 1.45 | +0.239 | 6.6 | 21.0 |
| VIX | ASIA | BAR_DELTA | 200 | 2.0 | MOMENTUM | NORMAL | 2.0 | 1.0 | 76 | 0.513 | 1.50 | +0.235 | 5.7 | 22.5 |
| VIX | ASIA | BAR_DELTA | 200 | 2.0 | FADE | INVERT | 2.0 | 1.0 | 76 | 0.513 | 1.50 | +0.235 | 8.3 | 22.5 |
| AUDUSD | ASIA | CLOSE_VS_MID | 50 | 2.5 | FADE | INVERT | 2.0 | 1.0 | 205 | 0.478 | 1.40 | +0.223 | 18.9 | 25.1 |
| AUDUSD | ASIA | CLOSE_VS_MID | 50 | 2.5 | MOMENTUM | NORMAL | 2.0 | 1.0 | 205 | 0.478 | 1.40 | +0.223 | 17.2 | 25.1 |
| VIX | ASIA | TICK_RULE | 200 | 2.0 | MOMENTUM | NORMAL | 2.0 | 1.0 | 68 | 0.529 | 1.51 | +0.218 | 5.8 | 20.1 |
| VIX | ASIA | TICK_RULE | 200 | 2.0 | FADE | INVERT | 2.0 | 1.0 | 68 | 0.529 | 1.51 | +0.218 | 6.6 | 20.1 |
| VIX | LONDON | BAR_DELTA | 200 | 2.0 | MOMENTUM | INVERT | 2.0 | 1.0 | 101 | 0.485 | 1.40 | +0.216 | 11.5 | 30.1 |
| VIX | LONDON | BAR_DELTA | 200 | 2.0 | FADE | NORMAL | 2.0 | 1.0 | 101 | 0.485 | 1.40 | +0.216 | 14.7 | 30.1 |
| VIX | NY | TICK_RULE | 200 | 2.5 | FADE | NORMAL | 2.0 | 1.0 | 78 | 0.474 | 1.34 | +0.200 | 6.6 | 23.2 |
| VIX | NY | TICK_RULE | 200 | 2.5 | MOMENTUM | INVERT | 2.0 | 1.0 | 78 | 0.474 | 1.34 | +0.200 | 9.6 | 23.2 |
| AUDUSD | ASIA | CLOSE_VS_MID | 50 | 2.5 | MOMENTUM | INVERT | 2.0 | 1.0 | 192 | 0.453 | 1.34 | +0.199 | 8.5 | 23.5 |
| AUDUSD | ASIA | CLOSE_VS_MID | 50 | 2.5 | FADE | NORMAL | 2.0 | 1.0 | 192 | 0.453 | 1.34 | +0.199 | 8.4 | 23.5 |
| VIX | ALL_DAY | BAR_DELTA | 200 | 2.5 | MOMENTUM | INVERT | 2.0 | 1.0 | 114 | 0.474 | 1.34 | +0.196 | 9.6 | 33.9 |
| VIX | ALL_DAY | BAR_DELTA | 200 | 2.5 | FADE | NORMAL | 2.0 | 1.0 | 114 | 0.474 | 1.34 | +0.196 | 11.2 | 33.9 |
| VIX | LONDON_NY | TICK_RULE | 200 | 2.5 | FADE | NORMAL | 2.0 | 1.0 | 88 | 0.466 | 1.31 | +0.191 | 17.2 | 26.2 |
| VIX | LONDON_NY | TICK_RULE | 200 | 2.5 | MOMENTUM | INVERT | 2.0 | 1.0 | 88 | 0.466 | 1.31 | +0.191 | 16.9 | 26.2 |
| VIX | NY | CLOSE_VS_MID | 50 | 2.0 | MOMENTUM | INVERT | 2.0 | 1.0 | 203 | 0.483 | 1.34 | +0.189 | 8.6 | 58.9 |
| VIX | NY | CLOSE_VS_MID | 50 | 2.0 | FADE | NORMAL | 2.0 | 1.0 | 203 | 0.483 | 1.34 | +0.189 | 11.0 | 58.9 |
| USDJPY | NY | TICK_RULE | 50 | 3.0 | MOMENTUM | NORMAL | 2.0 | 1.0 | 166 | 0.452 | 1.34 | +0.187 | 11.6 | 20.4 |
| USDJPY | NY | TICK_RULE | 50 | 3.0 | FADE | INVERT | 2.0 | 1.0 | 166 | 0.452 | 1.34 | +0.187 | 10.1 | 20.4 |
| VIX | ASIA | TICK_RULE | 100 | 2.0 | MOMENTUM | NORMAL | 2.0 | 1.0 | 72 | 0.514 | 1.38 | +0.186 | 5.1 | 20.9 |
| VIX | ASIA | TICK_RULE | 100 | 2.0 | FADE | INVERT | 2.0 | 1.0 | 72 | 0.514 | 1.38 | +0.186 | 3.8 | 20.9 |
