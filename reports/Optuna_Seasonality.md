# Optuna 3-Regime — Seasonality Buckets

Per (symbol, bucket, direction) Phase-B survivor: 3 R:R regimes x 60 trials each.
Best regime chosen by SL-invariant objective = (expectancy_R * SL * trades_per_year) / max_dd_R.

## Best-regime distribution

- **HIGH_RR**: 5 strategies
- **BALANCED**: 3 strategies
- **HIGH_WR**: 1 strategies

## Per-strategy best regime

| Sym | UTC | Dir | Best | TP/SL | RR | WR | PF | Exp(R) | DD(R) | t/yr |
|---|---|---|---|---|---|---|---|---|---|---|
| GBPAUD | 20:30 | SHORT | **HIGH_WR** | 1.10/1.20 | 0.92 | 0.771 | 1.74 | +0.215 | 32.1 | 259 |
| GBPJPY | 20:30 | SHORT | **HIGH_RR** | 1.00/1.10 | 0.91 | 0.735 | 1.36 | +0.121 | 29.5 | 259 |
| XAGUSD | 21:30 | SHORT | **BALANCED** | 0.60/0.50 | 1.20 | 0.635 | 1.34 | +0.155 | 32.7 | 88 |
| XAGUSD | 21:45 | LONG | **HIGH_RR** | 1.30/0.70 | 1.86 | 0.500 | 1.32 | +0.199 | 70.2 | 88 |
| XAUUSD | 21:45 | LONG | **BALANCED** | 2.00/1.80 | 1.11 | 0.621 | 1.20 | +0.093 | 21.3 | 88 |
| GBPJPY | 20:45 | SHORT | **HIGH_RR** | 1.10/0.80 | 1.38 | 0.581 | 1.12 | +0.067 | 233.4 | 259 |
| XAGUSD | 20:30 | SHORT | **BALANCED** | 0.80/0.60 | 1.33 | 0.555 | 1.11 | +0.060 | 120.6 | 250 |
| GBPAUD | 20:45 | SHORT | **HIGH_RR** | 1.30/0.80 | 1.62 | 0.502 | 1.04 | +0.024 | 370.5 | 259 |
| EURJPY | 20:30 | SHORT | **HIGH_RR** | 1.20/1.00 | 1.20 | 0.609 | 1.03 | +0.017 | 204.0 | 259 |
