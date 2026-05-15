# ORB Managements — Configs con Edge Positivo

**Filtro:** PF ≥ 1.0 AND WR ≥ 50% AND expectancy_r > 0 AND trades ≥ 30

**Total configs que pasan:** 164 de 1073 (15.3%)

## 1. Distribución por modo (solo configs ganadoras)

| modo | n configs ganadoras | PF mediano | PF max | WR mediano | exp_r mediano | sum_R total |
|---|---|---|---|---|---|---|
| OR_FIXED | 84 | 1.32 | 2.47 | 56.0% | +0.31R | +11461.40R |
| ATR | 67 | 1.24 | 2.28 | 58.8% | +0.17R | +4559.09R |
| DOC | 13 | 1.12 | 2.45 | 56.4% | +0.12R | +1201.54R |

## 2. Distribución por símbolo (solo configs ganadoras)

| símbolo | n configs ganadoras | PF mediano | PF max | WR mediano | exp_r mediano | sum_R total |
|---|---|---|---|---|---|---|
| GBPUSD | 22 | 1.98 | 2.47 | 62.3% | +0.80R | +4921.66R |
| XAUUSD | 23 | 1.87 | 2.35 | 60.6% | +0.69R | +4309.19R |
| NATGAS | 50 | 1.21 | 1.66 | 56.2% | +0.18R | +3465.93R |
| SP500 | 37 | 1.15 | 1.50 | 55.3% | +0.12R | +2352.28R |
| NASDAQ100 | 32 | 1.19 | 1.48 | 55.2% | +0.16R | +2172.97R |

## 3. TODAS las configs ganadoras (ordenadas por PF desc)

| symbol | or_duration_min | pattern_id | direction | mode | params | trades | trades_per_year | win_rate | pf | expectancy_r | sum_r | max_dd_r |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.0,rr=1.0 | 265 | 32.38 | 73.2% | 2.47 | +1.17R | +309.02R | +18.15R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 265 | 32.38 | 72.8% | 2.45 | +1.16R | +307.23R | +19.86R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 254 | 31.06 | 72.0% | 2.35 | +1.09R | +275.98R | +21.11R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=1.0 | 254 | 31.06 | 78.0% | 2.28 | +0.48R | +121.53R | +8.70R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.0 | 254 | 31.06 | 74.8% | 2.23 | +0.69R | +176.18R | +14.40R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.0,rr=3.0 | 265 | 32.38 | 54.7% | 2.19 | +1.60R | +423.84R | +25.46R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.0 | 254 | 31.06 | 72.0% | 2.13 | +0.91R | +230.82R | +15.60R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.5,rr=2.0 | 265 | 32.38 | 59.6% | 2.12 | +1.65R | +437.00R | +32.82R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.7,rr=1.0 | 265 | 32.38 | 76.6% | 2.12 | +0.44R | +117.90R | +6.90R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 265 | 32.38 | 68.7% | 2.11 | +1.31R | +346.03R | +23.71R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=1.0,rr=1.0 | 265 | 32.38 | 73.6% | 2.06 | +0.64R | +170.50R | +16.70R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.5 | 254 | 31.06 | 69.3% | 2.05 | +0.63R | +161.23R | +19.26R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.5,rr=1.5 | 265 | 32.38 | 61.9% | 2.04 | +1.43R | +379.98R | +26.91R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.0,rr=1.5 | 265 | 32.38 | 62.6% | 2.04 | +1.16R | +308.72R | +24.52R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=1.0,rr=1.5 | 265 | 32.38 | 63.0% | 1.99 | +0.83R | +218.88R | +15.70R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=3.0 | 254 | 31.06 | 51.6% | 1.98 | +1.32R | +336.08R | +33.25R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=1.0,rr=2.0 | 265 | 32.38 | 55.8% | 1.98 | +0.97R | +255.90R | +14.70R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.0 | 254 | 31.06 | 78.3% | 1.98 | +0.44R | +110.76R | +16.66R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.0,rr=2.0 | 265 | 32.38 | 57.4% | 1.98 | +1.23R | +325.99R | +25.46R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=0.5,rr=2.0 | 265 | 32.38 | 58.1% | 1.97 | +0.78R | +206.55R | +19.12R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=1.5 | 254 | 31.06 | 65.4% | 1.97 | +0.57R | +145.05R | +11.80R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.7,rr=1.5 | 265 | 32.38 | 64.5% | 1.93 | +0.56R | +148.00R | +11.80R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.5,rr=1.0 | 254 | 31.06 | 78.0% | 1.90 | +0.26R | +65.80R | +5.70R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=1.5,rr=3.0 | 265 | 32.38 | 57.4% | 1.89 | +1.38R | +366.94R | +38.58R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.5,rr=2.0 | 254 | 31.06 | 59.1% | 1.88 | +0.47R | +118.47R | +13.50R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.5 | 254 | 31.06 | 60.2% | 1.87 | +0.97R | +246.71R | +14.98R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=2.0 | 254 | 31.06 | 55.1% | 1.87 | +1.08R | +275.53R | +35.78R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=2.0 | 254 | 31.06 | 59.1% | 1.86 | +0.67R | +169.05R | +20.73R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.5 | 254 | 31.06 | 60.6% | 1.85 | +0.73R | +186.26R | +15.60R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=0.5,rr=1.5 | 265 | 32.38 | 63.8% | 1.85 | +0.60R | +158.85R | +15.75R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=2.0 | 254 | 31.06 | 55.9% | 1.84 | +1.27R | +322.32R | +41.13R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.5,rr=1.5 | 254 | 31.06 | 66.5% | 1.84 | +0.36R | +92.30R | +12.00R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=3.0 | 254 | 31.06 | 53.9% | 1.83 | +1.31R | +332.36R | +41.13R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=2.0 | 254 | 31.06 | 53.5% | 1.82 | +0.84R | +212.59R | +18.30R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 254 | 31.06 | 65.0% | 1.81 | +0.99R | +252.41R | +20.40R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=2.0 | 254 | 31.06 | 54.7% | 1.78 | +0.59R | +148.89R | +14.50R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.5 | 254 | 31.06 | 58.3% | 1.78 | +1.13R | +286.25R | +41.13R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.7,rr=2.0 | 265 | 32.38 | 54.7% | 1.76 | +0.59R | +155.54R | +12.00R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | OR_FIXED | sl_or=0.5,rr=1.0 | 265 | 32.38 | 72.8% | 1.72 | +0.39R | +104.19R | +13.20R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 250 | 30.57 | 65.6% | 1.66 | +1.01R | +253.74R | +28.67R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=1.5 | 250 | 30.57 | 58.0% | 1.65 | +0.88R | +220.75R | +21.37R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.5 | 250 | 30.57 | 54.8% | 1.63 | +1.20R | +300.74R | +28.42R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 250 | 30.57 | 65.2% | 1.63 | +0.67R | +168.57R | +24.65R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=2.0 | 250 | 30.57 | 50.0% | 1.62 | +0.97R | +241.54R | +33.41R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=1.0 | 250 | 30.57 | 66.4% | 1.61 | +0.66R | +164.46R | +15.40R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.0 | 250 | 30.57 | 70.8% | 1.57 | +0.28R | +70.60R | +11.00R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.5 | 250 | 30.57 | 57.2% | 1.57 | +0.55R | +137.89R | +16.00R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.5 | 250 | 30.57 | 59.2% | 1.55 | +0.38R | +94.58R | +14.80R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=2.0 | 250 | 30.57 | 51.2% | 1.54 | +0.44R | +110.97R | +18.10R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.0 | 250 | 30.57 | 66.8% | 1.50 | +0.38R | +95.18R | +15.70R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=1.0 | 269 | 33.99 | 69.9% | 1.50 | +0.26R | +69.10R | +22.10R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=2.0 | 269 | 33.99 | 53.9% | 1.50 | +1.00R | +269.24R | +38.06R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=2.0 | 250 | 30.57 | 50.4% | 1.50 | +0.44R | +108.88R | +24.11R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.5,rr=1.5 | 265 | 32.38 | 61.9% | 1.50 | +0.25R | +65.50R | +10.70R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=2.0 | 294 | 37.48 | 53.1% | 1.48 | +0.95R | +279.99R | +52.35R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.5 | 250 | 30.57 | 59.2% | 1.48 | +0.35R | +88.18R | +19.48R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.0 | 250 | 30.57 | 70.8% | 1.48 | +0.26R | +64.14R | +11.70R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.5,rr=2.0 | 265 | 32.38 | 52.8% | 1.46 | +0.28R | +75.50R | +9.60R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.5 | 269 | 33.99 | 56.1% | 1.44 | +0.85R | +229.77R | +38.06R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.5 | 294 | 37.48 | 54.8% | 1.43 | +0.45R | +130.95R | +35.20R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=3.0 | 294 | 37.48 | 50.7% | 1.43 | +0.90R | +264.26R | +53.50R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=3.0 | 269 | 33.99 | 50.6% | 1.43 | +0.92R | +246.58R | +51.69R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.0 | 294 | 37.48 | 65.6% | 1.43 | +0.33R | +97.98R | +22.50R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.5 | 269 | 33.99 | 54.6% | 1.42 | +0.43R | +115.75R | +36.61R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=1.5 | 269 | 33.99 | 57.2% | 1.42 | +0.30R | +81.14R | +23.61R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.0 | 269 | 33.99 | 65.4% | 1.40 | +0.32R | +85.44R | +29.51R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=3.0 | 249 | 30.43 | 56.2% | 1.39 | +0.34R | +83.78R | +29.67R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.5 | 294 | 37.48 | 55.8% | 1.38 | +0.72R | +213.01R | +51.94R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.5 | 269 | 33.99 | 56.5% | 1.36 | +0.31R | +82.98R | +29.49R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.3,rr=2.0 | 254 | 31.06 | 57.5% | 1.35 | +0.13R | +34.20R | +7.20R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.0 | 294 | 37.48 | 66.7% | 1.35 | +0.21R | +63.14R | +12.94R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 269 | 33.99 | 61.3% | 1.34 | +0.59R | +158.69R | +37.04R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.0 | 269 | 33.99 | 68.0% | 1.34 | +0.22R | +59.00R | +25.09R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=1.0 | 294 | 37.48 | 67.0% | 1.33 | +0.18R | +53.34R | +12.60R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=2.0 | 249 | 30.43 | 56.2% | 1.33 | +0.28R | +70.63R | +29.67R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.5,rr=1.0 | 265 | 32.38 | 70.9% | 1.31 | +0.12R | +31.50R | +11.40R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 249 | 30.43 | 59.4% | 1.31 | +0.25R | +62.03R | +32.39R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 294 | 37.48 | 61.9% | 1.30 | +0.51R | +150.51R | +54.96R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.0 | 269 | 33.99 | 63.2% | 1.29 | +0.39R | +105.60R | +33.08R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.5 | 249 | 30.43 | 56.6% | 1.28 | +0.25R | +61.16R | +30.55R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.5 | 249 | 30.43 | 54.6% | 1.28 | +0.22R | +55.56R | +18.87R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 269 | 33.99 | 63.2% | 1.28 | +0.37R | +99.62R | +34.99R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 294 | 37.48 | 61.9% | 1.27 | +0.36R | +106.43R | +44.42R |
| NASDAQ100 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.5 | 248 | 31.63 | 54.4% | 1.27 | +0.21R | +51.71R | +18.70R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 362 | 44.21 | 58.0% | 1.27 | +0.32R | +114.55R | +47.51R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.0 | 362 | 44.21 | 62.4% | 1.24 | +0.20R | +73.16R | +25.36R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.5 | 294 | 37.48 | 54.4% | 1.24 | +0.38R | +110.73R | +46.97R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.5,rr=1.5 | 269 | 33.99 | 57.2% | 1.24 | +0.13R | +35.30R | +18.40R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.0 | 294 | 37.48 | 62.2% | 1.23 | +0.31R | +89.96R | +40.82R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.5 | 294 | 37.48 | 53.7% | 1.23 | +0.20R | +58.76R | +28.01R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=3.0 | 249 | 30.43 | 51.4% | 1.23 | +0.20R | +48.67R | +24.05R |
| NASDAQ100 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.0 | 248 | 31.63 | 64.5% | 1.22 | +0.14R | +35.36R | +16.03R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.5,rr=1.5 | 250 | 30.57 | 56.8% | 1.21 | +0.12R | +30.00R | +9.30R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.5 | 362 | 44.21 | 50.6% | 1.21 | +0.29R | +105.66R | +46.93R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=3.0 | 249 | 30.43 | 51.4% | 1.21 | +0.18R | +45.76R | +30.02R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.5 | 269 | 33.99 | 52.4% | 1.21 | +0.35R | +93.31R | +38.98R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.5,rr=1.0 | 269 | 33.99 | 69.1% | 1.21 | +0.08R | +22.30R | +9.40R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.7,rr=1.5 | 294 | 37.48 | 53.1% | 1.20 | +0.16R | +47.74R | +18.40R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=1.5 | 249 | 30.43 | 54.6% | 1.20 | +0.16R | +40.50R | +31.11R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=2.0 | 249 | 30.43 | 53.0% | 1.20 | +0.17R | +41.31R | +28.36R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=0.5,rr=1.0 | 262 | 33.37 | 65.6% | 1.20 | +0.10R | +26.17R | +13.17R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=2.0 | 249 | 30.43 | 51.8% | 1.19 | +0.16R | +39.33R | +21.70R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.3,rr=2.0 | 269 | 33.99 | 54.3% | 1.19 | +0.08R | +20.70R | +9.00R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.0,rr=1.5 | 262 | 33.37 | 50.4% | 1.18 | +0.20R | +52.83R | +37.57R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 262 | 33.37 | 55.7% | 1.17 | +0.17R | +44.36R | +31.00R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.5 | 362 | 44.21 | 51.4% | 1.17 | +0.17R | +63.22R | +53.34R |
| NASDAQ100 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.0 | 248 | 31.63 | 60.9% | 1.17 | +0.15R | +36.99R | +28.02R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=1.5 | 362 | 44.21 | 50.8% | 1.16 | +0.18R | +66.87R | +57.14R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 255 | 32.28 | 51.0% | 1.16 | +0.19R | +49.32R | +35.49R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 301 | 38.12 | 53.5% | 1.16 | +0.28R | +83.96R | +39.02R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.0 | 249 | 30.43 | 58.2% | 1.15 | +0.11R | +28.49R | +34.23R |
| SP500 | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.5 | 438 | 55.34 | 50.7% | 1.15 | +0.22R | +95.24R | +60.93R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.0 | 362 | 44.21 | 63.8% | 1.15 | +0.09R | +32.76R | +34.20R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.0 | 273 | 34.55 | 60.4% | 1.14 | +0.13R | +34.64R | +40.64R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.5 | 362 | 44.21 | 53.3% | 1.13 | +0.09R | +32.36R | +36.72R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.5 | 273 | 34.55 | 51.3% | 1.13 | +0.11R | +29.02R | +25.44R |
| SP500 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.3,rr=1.5 | 269 | 33.99 | 62.8% | 1.13 | +0.04R | +11.40R | +10.50R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=1.0,rr=1.0 | 262 | 33.37 | 58.8% | 1.13 | +0.11R | +27.99R | +23.30R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 262 | 33.37 | 54.2% | 1.12 | +0.15R | +40.17R | +40.35R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 362 | 44.21 | 57.7% | 1.12 | +0.11R | +40.93R | +68.83R |
| NASDAQ100 | 60 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_up | LONG | OR_FIXED | sl_or=0.5,rr=1.5 | 322 | 40.58 | 50.3% | 1.11 | +0.10R | +32.68R | +43.37R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 255 | 32.28 | 53.7% | 1.11 | +0.12R | +29.93R | +33.83R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.0 | 362 | 44.21 | 64.1% | 1.11 | +0.06R | +20.65R | +35.63R |
| NATGAS | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.5,rr=1.0 | 250 | 30.57 | 67.2% | 1.10 | +0.04R | +11.00R | +9.50R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=1.0 | 362 | 44.21 | 57.7% | 1.10 | +0.10R | +36.37R | +59.00R |
| XAUUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.3,rr=1.5 | 254 | 31.06 | 62.2% | 1.10 | +0.03R | +8.40R | +7.80R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.5 | 362 | 44.21 | 51.7% | 1.10 | +0.08R | +28.02R | +48.59R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=0.5,rr=1.5 | 262 | 33.37 | 52.3% | 1.09 | +0.06R | +16.99R | +19.11R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=0.5,rr=1.5 | 255 | 32.28 | 52.9% | 1.09 | +0.06R | +16.54R | +27.00R |
| NATGAS | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.5,rr=1.5 | 362 | 44.21 | 53.9% | 1.08 | +0.05R | +18.19R | +36.60R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.0,rr=1.0 | 249 | 30.43 | 57.8% | 1.08 | +0.06R | +16.15R | +45.96R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=0.5,rr=1.0 | 262 | 33.37 | 66.8% | 1.08 | +0.04R | +9.40R | +12.80R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 249 | 30.43 | 56.2% | 1.08 | +0.06R | +15.33R | +42.39R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=0.7,rr=1.0 | 262 | 33.37 | 61.8% | 1.08 | +0.05R | +13.27R | +20.51R |
| NASDAQ100 | 60 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_up | LONG | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 322 | 40.58 | 53.7% | 1.08 | +0.11R | +34.40R | +74.66R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.0,rr=1.0 | 262 | 33.37 | 56.5% | 1.08 | +0.08R | +20.56R | +34.57R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.5 | 249 | 30.43 | 51.0% | 1.08 | +0.06R | +13.72R | +28.39R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=0.5,rr=1.0 | 255 | 32.28 | 63.5% | 1.07 | +0.04R | +10.89R | +16.07R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=0.5,rr=1.5 | 255 | 32.28 | 53.7% | 1.07 | +0.04R | +10.94R | +23.26R |
| GBPUSD | 30 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | LONG | ATR | sl_atr=0.3,rr=2.0 | 265 | 32.38 | 51.7% | 1.07 | +0.03R | +8.10R | +10.80R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 273 | 34.55 | 56.4% | 1.07 | +0.10R | +26.77R | +36.94R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 301 | 38.12 | 54.8% | 1.07 | +0.10R | +29.23R | +37.70R |
| NASDAQ100 | 60 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_up | LONG | OR_FIXED | sl_or=1.0,rr=1.0 | 322 | 40.58 | 53.7% | 1.07 | +0.09R | +29.21R | +75.02R |
| NASDAQ100 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.0 | 248 | 31.63 | 62.1% | 1.06 | +0.04R | +9.60R | +22.50R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.0,rr=1.0 | 301 | 38.12 | 55.5% | 1.06 | +0.09R | +26.12R | +35.86R |
| NASDAQ100 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.5 | 248 | 31.63 | 50.8% | 1.06 | +0.06R | +13.66R | +28.41R |
| NATGAS | 30 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.5 | 303 | 36.88 | 50.2% | 1.06 | +0.05R | +14.04R | +36.77R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | OR_FIXED | sl_or=1.0,rr=1.0 | 255 | 32.28 | 55.3% | 1.05 | +0.06R | +14.51R | +37.34R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 273 | 34.55 | 55.3% | 1.05 | +0.10R | +27.15R | +48.66R |
| NASDAQ100 | 60 | FALSE_BREAK_DOWN_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | ATR | sl_atr=0.5,rr=1.5 | 294 | 37.48 | 53.1% | 1.05 | +0.03R | +8.94R | +15.90R |
| SP500 | 60 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=1.0,rr=1.0 | 301 | 38.12 | 58.1% | 1.05 | +0.05R | +13.90R | +33.75R |
| SP500 | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | DOC | sl=1.0OR,tp1=1.0OR(50%),tp2=2.0OR(50%),BE,timestop@1/2,mfe<0.5R | 438 | 55.34 | 50.7% | 1.05 | +0.05R | +22.76R | +38.20R |
| SP500 | 30 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 438 | 55.34 | 52.7% | 1.04 | +0.05R | +22.16R | +58.34R |
| NATGAS | 30 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_down | SHORT | ATR | sl_atr=1.0,rr=1.0 | 303 | 36.88 | 57.8% | 1.03 | +0.03R | +9.22R | +37.56R |
| NATGAS | 15 | BREAK_DOWN_BETWEEN_LOW_AND_CLOSE_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 264 | 32.97 | 50.8% | 1.03 | +0.03R | +7.87R | +34.83R |
| NATGAS | 15 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | ATR | sl_atr=0.7,rr=1.0 | 249 | 30.43 | 59.0% | 1.02 | +0.02R | +3.77R | +25.16R |
| SP500 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=0.7,rr=1.0 | 255 | 32.28 | 60.4% | 1.02 | +0.01R | +3.77R | +27.06R |
| NATGAS | 30 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 303 | 36.88 | 54.8% | 1.02 | +0.03R | +8.25R | +52.45R |
| SP500 | 120 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_down | SHORT | OR_FIXED | sl_or=1.5,rr=1.0 | 263 | 33.27 | 55.1% | 1.01 | +0.04R | +11.04R | +184.31R |
| NATGAS | 30 | BREAK_UP_BETWEEN_LOW_AND_CLOSE_expanded_gap_down | SHORT | OR_FIXED | sl_or=0.5,rr=1.5 | 303 | 36.88 | 50.5% | 1.01 | +0.01R | +2.62R | +48.06R |
| NASDAQ100 | 30 | FALSE_BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | SHORT | ATR | sl_atr=0.5,rr=1.5 | 262 | 33.37 | 52.3% | 1.01 | +0.01R | +1.90R | +19.30R |
| SP500 | 60 | BREAK_UP_BETWEEN_CLOSE_AND_HIGH_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 484 | 61.15 | 54.1% | 1.01 | +0.02R | +8.47R | +78.90R |
| NATGAS | 30 | BREAK_DOWN_BETWEEN_LOW_AND_CLOSE_expanded_gap_up | LONG | OR_FIXED | sl_or=1.5,rr=1.0 | 356 | 43.63 | 52.2% | 1.01 | +0.01R | +3.24R | +61.90R |
| NATGAS | 15 | BREAK_DOWN_BETWEEN_LOW_AND_CLOSE_expanded_gap_up | LONG | ATR | sl_atr=1.0,rr=1.0 | 264 | 32.97 | 54.5% | 1.00 | +0.00R | +0.53R | +37.04R |

## 4. Lectura

- **n_winners** = configs (de las 29 totales por patrón) que pasaron el filtro
- **sum_R total** = suma acumulada de R-units a través de TODAS las configs ganadoras del modo/símbolo
- Si un modo tiene muchos winners pero PF mediano bajo, es **consistente**
- Si un modo tiene pocos winners pero PF max alto, tiene **outliers buenos** pero poca robustez
