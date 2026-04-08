# KHA0SYS3 - Edge Discovery Report

**Total permutaciones escaneadas:** 12920
**Estrategias desplegadas (excluidas):** 38
**Nuevos edges encontrados:** 3358
**Filtros:** WR >= 55%, PF > 1.0, N >= 30

## Distribucion por Arquetipo

- **FADE_DOWN**: 1593 edges
- **FADE_UP**: 1576 edges
- **SHAKEOUT_UP**: 89 edges
- **SHAKEOUT_DOWN**: 75 edges
- **MOMENTUM_DOWN**: 14 edges
- **MOMENTUM_UP**: 11 edges

## Distribucion por Activo

- **XAGUSD**: 309 edges
- **SP500**: 305 edges
- **WTI**: 296 edges
- **NASDAQ100**: 279 edges
- **BRENT**: 269 edges
- **EURJPY**: 263 edges
- **EURUSD**: 239 edges
- **GBPJPY**: 239 edges
- **XAUUSD**: 229 edges
- **GBPUSD**: 227 edges
- **USDJPY**: 192 edges
- **AUDUSD**: 168 edges
- **GBPAUD**: 155 edges
- **NATGAS**: 99 edges
- **VIX**: 89 edges

## Distribucion por Filtro

- **GapSmall**: 209 edges
- **BtwCloseHigh**: 203 edges
- **RSI_50-70**: 200 edges
- **RSI_30-50**: 199 edges
- **OR_Q4_Wide**: 196 edges
- **BtwLowClose**: 186 edges
- **BASE**: 183 edges
- **Wed**: 180 edges
- **Fri**: 174 edges
- **Thu**: 169 edges
- **Tue**: 164 edges
- **Mon**: 154 edges
- **BelowPD**: 150 edges
- **OR_Q1_Tight**: 149 edges
- **RSI_D<35**: 148 edges
- **RSI_D>65**: 147 edges
- **AbovePD**: 139 edges
- **ATR+10%**: 122 edges
- **RSI>70**: 89 edges
- **RSI<30**: 76 edges
- **AbovePD+RSI_D>65**: 66 edges
- **ATR-10%**: 52 edges
- **OR_Q4+ATR+**: 3 edges

## Top Edges (score = WR * log(N) * PF)

| # | Activo | Sesion | Dur | Arquetipo | Filtro | WR | N | T/Ano | PF | NetR | DD | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GBPAUD | Sydney | 15m | FADE_DOWN | BtwCloseHigh | `96.9%` | 32 | `4` | `31.00` | `30R` | `-1.0R` | `104.08` |
| 2 | GBPAUD | Sydney | 30m | FADE_DOWN | BtwLowClose | `96.7%` | 30 | `4` | `29.00` | `28R` | `-1.0R` | `95.35` |
| 3 | GBPAUD | Sydney | 15m | FADE_DOWN | OR_Q4_Wide | `95.8%` | 48 | `6` | `23.00` | `44R` | `-1.0R` | `85.33` |
| 4 | GBPAUD | Sydney | 30m | FADE_DOWN | GapSmall | `94.6%` | 56 | `7` | `17.67` | `50R` | `-1.0R` | `67.30` |
| 5 | GBPAUD | Sydney | 30m | FADE_DOWN | RSI_30-50 | `93.7%` | 63 | `8` | `14.75` | `55R` | `-1.0R` | `57.23` |
| 6 | GBPAUD | Sydney | 45m | FADE_DOWN | RSI_30-50 | `91.9%` | 37 | `5` | `11.33` | `31R` | `-1.0R` | `37.61` |
| 7 | GBPAUD | Sydney | 15m | FADE_DOWN | RSI_50-70 | `90.0%` | 40 | `5` | `9.00` | `32R` | `-2.0R` | `29.88` |
| 8 | GBPAUD | Sydney | 30m | FADE_DOWN | BtwCloseHigh | `90.3%` | 31 | `5` | `9.33` | `25R` | `-1.0R` | `28.95` |
| 9 | GBPAUD | Sydney | 15m | FADE_DOWN | GapSmall | `88.4%` | 69 | `9` | `7.62` | `53R` | `-2.0R` | `28.54` |
| 10 | GBPAUD | Sydney | 60m | FADE_DOWN | BASE | `88.1%` | 42 | `5` | `7.40` | `32R` | `-1.0R` | `24.37` |
| 11 | GBPAUD | Sydney | 15m | FADE_DOWN | RSI_30-50 | `86.7%` | 75 | `10` | `6.50` | `55R` | `-3.0R` | `24.32` |
| 12 | GBPUSD | NY | 60m | FADE_UP | RSI>70 | `86.5%` | 37 | `5` | `6.40` | `27R` | `-1.0R` | `19.99` |
| 13 | GBPAUD | Sydney | 15m | FADE_DOWN | BelowPD | `86.7%` | 30 | `5` | `6.50` | `22R` | `-2.0R` | `19.16` |
| 14 | GBPAUD | Sydney | 45m | FADE_DOWN | BASE | `83.8%` | 80 | `10` | `5.15` | `54R` | `-2.0R` | `18.91` |
| 15 | GBPAUD | Sydney | 30m | FADE_DOWN | RSI_50-70 | `85.7%` | 35 | `5` | `6.00` | `25R` | `-1.0R` | `18.28` |
| 16 | AUDUSD | Sydney | 45m | FADE_UP | RSI_30-50 | `83.3%` | 48 | `6` | `5.00` | `32R` | `-2.0R` | `16.13` |
| 17 | GBPAUD | Sydney | 45m | FADE_DOWN | GapSmall | `83.3%` | 42 | `5` | `5.00` | `28R` | `-2.0R` | `15.57` |
| 18 | VIX | NY Cash | 45m | FADE_DOWN | Wed | `81.5%` | 54 | `17` | `4.40` | `34R` | `-2.0R` | `14.30` |
| 19 | GBPAUD | Sydney | 45m | FADE_UP | BtwLowClose | `83.3%` | 30 | `4` | `5.00` | `20R` | `-2.0R` | `14.17` |
| 20 | WTI | NY Main | 60m | FADE_UP | AbovePD+RSI_D>65 | `83.3%` | 30 | `4` | `5.00` | `20R` | `-2.0R` | `14.17` |
| 21 | XAGUSD | NY | 60m | FADE_UP | RSI_30-50 | `78.4%` | 102 | `13` | `3.64` | `58R` | `-3.0R` | `13.19` |
| 22 | AUDUSD | Sydney | 45m | FADE_DOWN | RSI_50-70 | `81.6%` | 38 | `5` | `4.43` | `24R` | `-1.0R` | `13.14` |
| 23 | GBPAUD | Sydney | 15m | FADE_UP | BtwCloseHigh | `81.6%` | 38 | `5` | `4.43` | `24R` | `-2.0R` | `13.14` |
| 24 | VIX | NY Cash | 45m | FADE_DOWN | BtwLowClose | `79.2%` | 77 | `24` | `3.81` | `45R` | `-2.0R` | `13.12` |
| 25 | GBPAUD | Sydney | 15m | FADE_DOWN | BtwLowClose | `81.8%` | 33 | `4` | `4.50` | `21R` | `-3.0R` | `12.87` |
| 26 | EURUSD | London | 15m | SHAKEOUT_DOWN | OR_Q1_Tight | `80.0%` | 55 | `8` | `4.00` | `33R` | `-1.0R` | `12.82` |
| 27 | VIX | NY Cash | 60m | FADE_DOWN | Thu | `79.2%` | 48 | `16` | `3.80` | `28R` | `-2.0R` | `11.65` |
| 28 | GBPAUD | Sydney | 45m | FADE_UP | RSI_30-50 | `78.8%` | 52 | `6` | `3.73` | `30R` | `-2.0R` | `11.61` |
| 29 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | RSI_D>65 | `80.6%` | 31 | `4` | `4.17` | `19R` | `-2.0R` | `11.54` |
| 30 | AUDUSD | Sydney | 15m | FADE_DOWN | RSI_50-70 | `80.0%` | 35 | `5` | `4.00` | `21R` | `-2.0R` | `11.38` |
| 31 | GBPUSD | NY | 45m | FADE_UP | RSI>70 | `79.5%` | 39 | `5` | `3.88` | `23R` | `-2.0R` | `11.28` |
| 32 | AUDUSD | Sydney | 30m | FADE_DOWN | GapSmall | `78.0%` | 59 | `7` | `3.54` | `33R` | `-3.0R` | `11.25` |
| 33 | AUDUSD | Sydney | 15m | FADE_DOWN | GapSmall | `77.3%` | 66 | `8` | `3.40` | `36R` | `-3.0R` | `11.01` |
| 34 | AUDUSD | Sydney | 45m | FADE_DOWN | GapSmall | `77.3%` | 66 | `8` | `3.40` | `36R` | `-3.0R` | `11.01` |
| 35 | SP500 | Pre-Market | 60m | FADE_DOWN | OR_Q4+ATR+ | `80.0%` | 30 | `5` | `4.00` | `18R` | `-1.0R` | `10.88` |
| 36 | VIX | NY Cash | 45m | FADE_DOWN | Thu | `78.0%` | 50 | `15` | `3.55` | `28R` | `-2.0R` | `10.82` |
| 37 | NASDAQ100 | NY Cash | 45m | FADE_UP | OR_Q4_Wide | `75.3%` | 97 | `13` | `3.04` | `49R` | `-2.0R` | `10.47` |
| 38 | GBPAUD | Sydney | 45m | FADE_UP | GapSmall | `75.7%` | 70 | `9` | `3.12` | `36R` | `-3.0R` | `10.03` |
| 39 | GBPAUD | Sydney | 15m | FADE_UP | OR_Q4_Wide | `76.3%` | 59 | `8` | `3.21` | `31R` | `-2.0R` | `10.00` |
| 40 | GBPAUD | Sydney | 15m | FADE_UP | RSI_50-70 | `74.7%` | 87 | `11` | `2.95` | `43R` | `-3.0R` | `9.86` |
| 41 | GBPAUD | Sydney | 45m | FADE_DOWN | RSI_50-70 | `77.5%` | 40 | `6` | `3.44` | `22R` | `-2.0R` | `9.85` |
| 42 | VIX | NY Cash | 30m | FADE_UP | Mon | `77.5%` | 40 | `12` | `3.44` | `22R` | `-2.0R` | `9.85` |
| 43 | XAGUSD | NY | 45m | FADE_UP | RSI_30-50 | `73.2%` | 138 | `17` | `2.73` | `64R` | `-4.0R` | `9.84` |
| 44 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | RSI_D<35 | `77.8%` | 36 | `5` | `3.50` | `20R` | `-3.0R` | `9.76` |
| 45 | NATGAS | NY | 60m | FADE_DOWN | Fri | `74.7%` | 83 | `11` | `2.95` | `41R` | `-3.0R` | `9.75` |
| 46 | AUDUSD | Sydney | 30m | FADE_DOWN | RSI_50-70 | `78.1%` | 32 | `4` | `3.57` | `18R` | `-2.0R` | `9.67` |
| 47 | AUDUSD | Sydney | 45m | FADE_DOWN | BtwCloseHigh | `78.1%` | 32 | `4` | `3.57` | `18R` | `-2.0R` | `9.67` |
| 48 | VIX | NY Cash | 15m | FADE_UP | Mon | `78.1%` | 32 | `9` | `3.57` | `18R` | `-2.0R` | `9.67` |
| 49 | NATGAS | NY | 45m | FADE_DOWN | Fri | `73.1%` | 119 | `15` | `2.72` | `55R` | `-2.0R` | `9.50` |
| 50 | NATGAS | NY | 60m | FADE_UP | Wed | `73.5%` | 102 | `13` | `2.78` | `48R` | `-3.0R` | `9.45` |
| 51 | XAGUSD | NY | 45m | FADE_DOWN | RSI<30 | `76.9%` | 39 | `5` | `3.33` | `21R` | `-2.0R` | `9.39` |
| 52 | VIX | NY Cash | 45m | FADE_UP | Mon | `76.1%` | 46 | `14` | `3.18` | `24R` | `-3.0R` | `9.27` |
| 53 | AUDUSD | Sydney | 45m | FADE_UP | BtwLowClose | `77.1%` | 35 | `4` | `3.38` | `19R` | `-2.0R` | `9.26` |
| 54 | SP500 | NY Cash | 60m | FADE_UP | ATR+10% | `77.1%` | 35 | `5` | `3.38` | `19R` | `-2.0R` | `9.26` |
| 55 | EURJPY | London | 45m | FADE_UP | RSI_D>65 | `72.5%` | 120 | `16` | `2.64` | `54R` | `-4.0R` | `9.15` |
| 56 | WTI | NY Main | 60m | FADE_UP | RSI>70 | `74.6%` | 63 | `8` | `2.94` | `31R` | `-4.0R` | `9.08` |
| 57 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | OR_Q4_Wide | `70.6%` | 197 | `27` | `2.40` | `81R` | `-4.0R` | `8.93` |
| 58 | BRENT | NY | 45m | FADE_UP | OR_Q4_Wide | `71.5%` | 144 | `18` | `2.51` | `62R` | `-3.0R` | `8.93` |
| 59 | NATGAS | NY | 60m | FADE_UP | AbovePD | `71.9%` | 121 | `15` | `2.56` | `53R` | `-3.0R` | `8.82` |
| 60 | XAGUSD | NY | 60m | FADE_UP | GapSmall | `69.2%` | 286 | `35` | `2.25` | `110R` | `-5.0R` | `8.81` |
| 61 | XAGUSD | NY | 60m | FADE_UP | BelowPD | `74.2%` | 62 | `8` | `2.88` | `30R` | `-4.0R` | `8.80` |
| 62 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | Wed | `76.5%` | 34 | `4` | `3.25` | `18R` | `-1.0R` | `8.76` |
| 63 | SP500 | Pre-Market | 60m | FADE_DOWN | ATR+10% | `74.5%` | 55 | `7` | `2.93` | `27R` | `-3.0R` | `8.75` |
| 64 | GBPAUD | Sydney | 60m | FADE_UP | GapSmall | `75.6%` | 41 | `5` | `3.10` | `21R` | `-3.0R` | `8.70` |
| 65 | GBPAUD | Sydney | 45m | FADE_UP | BASE | `71.8%` | 110 | `14` | `2.55` | `48R` | `-5.0R` | `8.60` |
| 66 | GBPAUD | Sydney | 30m | FADE_UP | BtwCloseHigh | `76.7%` | 30 | `4` | `3.29` | `16R` | `-2.0R` | `8.57` |
| 67 | SP500 | Pre-Market | 30m | FADE_DOWN | OR_Q4+ATR+ | `76.7%` | 30 | `4` | `3.29` | `16R` | `-2.0R` | `8.57` |
| 68 | SP500 | Pre-Market | 30m | SHAKEOUT_DOWN | OR_Q1_Tight | `76.7%` | 30 | `8` | `3.29` | `16R` | `-2.0R` | `8.57` |
| 69 | SP500 | Pre-Market | 45m | FADE_DOWN | ATR+10% | `74.5%` | 51 | `7` | `2.92` | `25R` | `-2.0R` | `8.56` |
| 70 | XAGUSD | NY | 45m | FADE_UP | BtwLowClose | `70.9%` | 141 | `17` | `2.44` | `59R` | `-3.0R` | `8.56` |
| 71 | EURUSD | NY | 45m | FADE_UP | OR_Q4_Wide | `72.6%` | 84 | `10` | `2.65` | `38R` | `-3.0R` | `8.53` |
| 72 | XAGUSD | NY | 45m | FADE_UP | GapSmall | `67.9%` | 368 | `45` | `2.12` | `132R` | `-5.0R` | `8.50` |
| 73 | AUDUSD | Sydney | 15m | FADE_DOWN | OR_Q4_Wide | `73.4%` | 64 | `8` | `2.76` | `30R` | `-4.0R` | `8.44` |
| 74 | VIX | NY Cash | 30m | FADE_DOWN | Thu | `74.1%` | 54 | `16` | `2.86` | `26R` | `-4.0R` | `8.44` |
| 75 | XAGUSD | NY | 60m | FADE_UP | BtwLowClose | `71.3%` | 115 | `14` | `2.48` | `49R` | `-3.0R` | `8.41` |
| 76 | GBPUSD | NY | 30m | FADE_UP | OR_Q4_Wide | `70.9%` | 127 | `16` | `2.43` | `53R` | `-9.0R` | `8.35` |
| 77 | XAGUSD | NY | 60m | FADE_UP | OR_Q1_Tight | `70.8%` | 130 | `18` | `2.42` | `54R` | `-3.0R` | `8.34` |
| 78 | AUDUSD | London | 60m | FADE_UP | RSI_D>65 | `72.3%` | 83 | `10` | `2.61` | `37R` | `-3.0R` | `8.33` |
| 79 | BRENT | NY | 45m | FADE_UP | RSI>70 | `72.9%` | 70 | `9` | `2.68` | `32R` | `-2.0R` | `8.31` |
| 80 | SP500 | Pre-Market | 45m | FADE_DOWN | BtwCloseHigh | `68.7%` | 249 | `31` | `2.19` | `93R` | `-4.0R` | `8.31` |
| 81 | XAGUSD | NY | 60m | FADE_UP | RSI>70 | `75.0%` | 40 | `5` | `3.00` | `20R` | `-2.0R` | `8.30` |
| 82 | SP500 | NY Cash | 45m | FADE_UP | ATR+10% | `75.0%` | 40 | `5` | `3.00` | `20R` | `-2.0R` | `8.30` |
| 83 | XAUUSD | NY | 60m | FADE_UP | ATR+10% | `75.8%` | 33 | `4` | `3.12` | `17R` | `-2.0R` | `8.28` |
| 84 | XAGUSD | NY | 60m | FADE_DOWN | RSI<30 | `75.8%` | 33 | `4` | `3.12` | `17R` | `-2.0R` | `8.28` |
| 85 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | Tue | `75.8%` | 33 | `4` | `3.12` | `17R` | `-2.0R` | `8.28` |
| 86 | SP500 | Pre-Market | 45m | MOMENTUM_DOWN | AbovePD+RSI_D>65 | `68.3%` | 41 | `6` | `3.23` | `29R` | `-5.5R` | `8.19` |
| 87 | XAGUSD | NY | 45m | FADE_UP | Mon | `71.4%` | 98 | `12` | `2.50` | `42R` | `-3.0R` | `8.19` |
| 88 | SP500 | NY Cash | 45m | FADE_DOWN | Wed | `69.9%` | 153 | `19` | `2.33` | `61R` | `-3.0R` | `8.18` |
| 89 | BRENT | NY | 60m | FADE_UP | RSI>70 | `73.6%` | 53 | `7` | `2.79` | `25R` | `-4.0R` | `8.14` |
| 90 | NATGAS | NY | 45m | FADE_DOWN | OR_Q4_Wide | `69.7%` | 152 | `21` | `2.30` | `60R` | `-5.0R` | `8.07` |
| 91 | WTI | NY Main | 30m | FADE_UP | OR_Q4_Wide | `68.9%` | 196 | `25` | `2.21` | `74R` | `-3.0R` | `8.05` |
| 92 | EURJPY | Tokyo | 60m | FADE_DOWN | RSI_30-50 | `65.8%` | 573 | `70` | `1.92` | `181R` | `-10.0R` | `8.04` |
| 93 | AUDUSD | Sydney | 15m | FADE_DOWN | BASE | `71.3%` | 94 | `12` | `2.48` | `40R` | `-4.0R` | `8.04` |
| 94 | BRENT | NY | 30m | FADE_UP | OR_Q4_Wide | `69.0%` | 184 | `23` | `2.23` | `70R` | `-4.0R` | `8.02` |
| 95 | AUDUSD | Sydney | 60m | FADE_DOWN | GapSmall | `73.9%` | 46 | `6` | `2.83` | `22R` | `-2.0R` | `8.02` |
| 96 | SP500 | Pre-Market | 15m | FADE_UP | ATR+10% | `73.9%` | 46 | `6` | `2.83` | `22R` | `-3.0R` | `8.02` |
| 97 | AUDUSD | Sydney | 30m | FADE_DOWN | BASE | `71.0%` | 100 | `12` | `2.45` | `42R` | `-5.0R` | `8.01` |
| 98 | BRENT | NY | 45m | FADE_UP | AbovePD | `69.2%` | 172 | `22` | `2.25` | `66R` | `-5.0R` | `8.00` |
| 99 | AUDUSD | Sydney | 45m | FADE_UP | BASE | `70.9%` | 103 | `13` | `2.43` | `43R` | `-3.0R` | `7.99` |
| 100 | XAGUSD | NY | 60m | FADE_UP | Wed | `70.8%` | 106 | `13` | `2.42` | `44R` | `-5.0R` | `7.98` |
| 101 | WTI | NY Main | 60m | FADE_UP | OR_Q4_Wide | `70.6%` | 109 | `15` | `2.41` | `45R` | `-3.0R` | `7.97` |
| 102 | BRENT | London | 45m | FADE_UP | Thu | `69.0%` | 174 | `21` | `2.22` | `66R` | `-4.0R` | `7.91` |
| 103 | AUDUSD | London | 30m | FADE_UP | RSI_D>65 | `71.3%` | 87 | `11` | `2.48` | `37R` | `-3.0R` | `7.89` |
| 104 | XAGUSD | NY | 45m | FADE_UP | OR_Q4_Wide | `71.3%` | 87 | `15` | `2.48` | `37R` | `-5.0R` | `7.89` |
| 105 | XAGUSD | NY | 60m | FADE_UP | Thu | `72.3%` | 65 | `8` | `2.61` | `29R` | `-3.0R` | `7.88` |
| 106 | EURUSD | London | 60m | FADE_UP | OR_Q1_Tight | `67.7%` | 248 | `31` | `2.10` | `88R` | `-5.0R` | `7.84` |
| 107 | USDJPY | NY | 60m | FADE_DOWN | RSI_D<35 | `73.1%` | 52 | `6` | `2.71` | `24R` | `-3.0R` | `7.84` |
| 108 | GBPJPY | Tokyo | 30m | FADE_UP | Thu | `68.8%` | 173 | `21` | `2.20` | `65R` | `-5.0R` | `7.81` |
| 109 | GBPUSD | NY | 45m | FADE_DOWN | OR_Q4_Wide | `71.6%` | 74 | `9` | `2.52` | `32R` | `-2.0R` | `7.78` |
| 110 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | Wed | `73.8%` | 42 | `5` | `2.82` | `20R` | `-3.0R` | `7.77` |
| 111 | SP500 | Pre-Market | 60m | MOMENTUM_DOWN | AbovePD+RSI_D>65 | `66.7%` | 48 | `7` | `3.00` | `32R` | `-4.0R` | `7.74` |
| 112 | EURJPY | London | 60m | FADE_UP | Thu | `68.2%` | 198 | `25` | `2.14` | `72R` | `-5.0R` | `7.73` |
| 113 | WTI | NY Main | 45m | FADE_UP | AbovePD | `67.9%` | 215 | `27` | `2.12` | `77R` | `-6.0R` | `7.72` |
| 114 | EURUSD | London | 60m | FADE_UP | OR_Q4_Wide | `68.3%` | 189 | `23` | `2.15` | `69R` | `-3.0R` | `7.69` |
| 115 | XAGUSD | NY | 60m | FADE_UP | BtwCloseHigh | `69.9%` | 113 | `14` | `2.32` | `45R` | `-5.0R` | `7.68` |
| 116 | SP500 | Pre-Market | 30m | FADE_DOWN | ATR+10% | `72.1%` | 61 | `8` | `2.59` | `27R` | `-4.0R` | `7.67` |
| 117 | BRENT | NY | 45m | FADE_UP | RSI_D<35 | `71.9%` | 64 | `8` | `2.56` | `28R` | `-4.0R` | `7.64` |
| 118 | SP500 | NY Cash | 45m | FADE_UP | GapSmall | `64.9%` | 573 | `71` | `1.85` | `171R` | `-6.0R` | `7.63` |
| 119 | AUDUSD | Sydney | 15m | FADE_DOWN | BtwCloseHigh | `74.3%` | 35 | `5` | `2.89` | `17R` | `-3.0R` | `7.63` |
| 120 | XAGUSD | London | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `74.3%` | 35 | `4` | `2.89` | `17R` | `-3.0R` | `7.63` |
| 121 | GBPAUD | Sydney | 30m | FADE_UP | RSI_50-70 | `71.6%` | 67 | `9` | `2.53` | `29R` | `-4.0R` | `7.61` |
| 122 | GBPAUD | Sydney | 60m | FADE_UP | BASE | `71.6%` | 67 | `9` | `2.53` | `29R` | `-5.0R` | `7.61` |
| 123 | GBPUSD | NY | 60m | FADE_UP | BtwLowClose | `68.5%` | 165 | `20` | `2.17` | `61R` | `-5.0R` | `7.60` |
| 124 | VIX | NY Cash | 45m | FADE_DOWN | GapSmall | `67.8%` | 199 | `59` | `2.11` | `71R` | `-6.0R` | `7.57` |
| 125 | VIX | NY Cash | 45m | FADE_DOWN | RSI_30-50 | `69.4%` | 124 | `36` | `2.26` | `48R` | `-4.0R` | `7.57` |
| 126 | BRENT | London | 15m | FADE_UP | Thu | `71.1%` | 76 | `10` | `2.45` | `32R` | `-4.0R` | `7.55` |
| 127 | XAGUSD | London | 15m | FADE_DOWN | Mon | `69.6%` | 112 | `14` | `2.29` | `44R` | `-3.0R` | `7.54` |
| 128 | GBPUSD | NY | 60m | FADE_UP | Thu | `69.9%` | 103 | `13` | `2.32` | `41R` | `-4.0R` | `7.52` |
| 129 | BRENT | NY | 60m | FADE_UP | OR_Q4_Wide | `69.9%` | 103 | `13` | `2.32` | `41R` | `-4.0R` | `7.52` |
| 130 | WTI | NY Main | 60m | FADE_UP | BASE | `64.2%` | 689 | `84` | `1.79` | `195R` | `-11.0R` | `7.50` |
| 131 | NASDAQ100 | NY Cash | 60m | FADE_UP | OR_Q4_Wide | `72.2%` | 54 | `9` | `2.60` | `24R` | `-2.0R` | `7.49` |
| 132 | XAGUSD | NY | 30m | FADE_UP | RSI_50-70 | `65.8%` | 354 | `44` | `1.93` | `112R` | `-7.0R` | `7.44` |
| 133 | GBPUSD | NY | 60m | FADE_DOWN | BtwLowClose | `69.1%` | 123 | `15` | `2.24` | `47R` | `-3.0R` | `7.44` |
| 134 | GBPUSD | NY | 60m | FADE_DOWN | BASE | `64.9%` | 490 | `60` | `1.85` | `146R` | `-8.0R` | `7.43` |
| 135 | GBPUSD | NY | 45m | FADE_UP | Mon | `69.2%` | 120 | `15` | `2.24` | `46R` | `-4.0R` | `7.43` |
| 136 | WTI | NY Main | 45m | FADE_UP | Wed | `67.8%` | 183 | `22` | `2.10` | `65R` | `-5.0R` | `7.42` |
| 137 | SP500 | Pre-Market | 60m | FADE_DOWN | OR_Q4_Wide | `67.1%` | 225 | `28` | `2.04` | `77R` | `-4.0R` | `7.42` |
| 138 | EURUSD | London | 30m | FADE_UP | ATR-10% | `73.2%` | 41 | `5` | `2.73` | `19R` | `-5.0R` | `7.41` |
| 139 | BRENT | London | 45m | FADE_DOWN | RSI_30-50 | `64.9%` | 484 | `59` | `1.85` | `144R` | `-9.0R` | `7.41` |
| 140 | GBPUSD | NY | 60m | FADE_DOWN | Wed | `69.4%` | 111 | `14` | `2.26` | `43R` | `-3.0R` | `7.40` |
| 141 | WTI | London Initial | 30m | FADE_DOWN | AbovePD | `69.4%` | 111 | `14` | `2.26` | `43R` | `-3.0R` | `7.40` |
| 142 | EURJPY | Tokyo | 60m | FADE_DOWN | OR_Q4_Wide | `66.8%` | 241 | `30` | `2.01` | `81R` | `-4.0R` | `7.37` |
| 143 | XAGUSD | London | 30m | FADE_UP | OR_Q4_Wide | `66.3%` | 282 | `38` | `1.97` | `92R` | `-6.0R` | `7.36` |
| 144 | EURUSD | NY | 45m | FADE_UP | BtwCloseHigh | `68.2%` | 154 | `19` | `2.14` | `56R` | `-6.0R` | `7.36` |
| 145 | AUDUSD | London | 60m | FADE_UP | RSI>70 | `70.8%` | 72 | `9` | `2.43` | `30R` | `-3.0R` | `7.36` |
| 146 | BRENT | NY | 45m | FADE_UP | Wed | `67.8%` | 171 | `21` | `2.11` | `61R` | `-9.0R` | `7.36` |
| 147 | BRENT | NY | 30m | FADE_UP | RSI>70 | `70.7%` | 75 | `9` | `2.41` | `31R` | `-3.0R` | `7.35` |
| 148 | AUDUSD | London | 45m | FADE_UP | RSI_D>65 | `70.2%` | 84 | `10` | `2.36` | `34R` | `-3.0R` | `7.34` |
| 149 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | OR_Q4_Wide | `67.1%` | 210 | `29` | `2.04` | `72R` | `-6.0R` | `7.34` |
| 150 | AUDUSD | Sydney | 30m | FADE_DOWN | BtwCloseHigh | `74.2%` | 31 | `4` | `2.88` | `15R` | `-2.0R` | `7.32` |
| 151 | GBPAUD | Sydney | 30m | FADE_UP | Wed | `74.2%` | 31 | `4` | `2.88` | `15R` | `-2.0R` | `7.32` |
| 152 | GBPAUD | Sydney | 30m | FADE_UP | BASE | `68.3%` | 145 | `18` | `2.15` | `53R` | `-5.0R` | `7.31` |
| 153 | SP500 | NY Cash | 45m | FADE_UP | BtwCloseHigh | `67.0%` | 218 | `27` | `2.03` | `74R` | `-3.0R` | `7.31` |
| 154 | WTI | NY Main | 45m | FADE_UP | RSI_50-70 | `64.9%` | 444 | `54` | `1.85` | `132R` | `-7.0R` | `7.30` |
| 155 | BRENT | London | 45m | FADE_DOWN | BtwLowClose | `66.1%` | 289 | `36` | `1.95` | `93R` | `-8.0R` | `7.30` |
| 156 | XAGUSD | NY | 45m | FADE_UP | OR_Q1_Tight | `67.9%` | 159 | `22` | `2.12` | `57R` | `-5.0R` | `7.29` |
| 157 | EURJPY | London | 60m | FADE_UP | RSI_D>65 | `69.0%` | 116 | `16` | `2.22` | `44R` | `-3.0R` | `7.29` |
| 158 | XAGUSD | NY | 30m | FADE_UP | GapSmall | `64.5%` | 488 | `60` | `1.82` | `142R` | `-10.0R` | `7.28` |
| 159 | WTI | NY Main | 60m | FADE_DOWN | OR_Q4_Wide | `69.0%` | 113 | `15` | `2.23` | `43R` | `-4.0R` | `7.27` |
| 160 | BRENT | London | 45m | FADE_UP | RSI_50-70 | `64.4%` | 495 | `61` | `1.81` | `143R` | `-10.0R` | `7.25` |
| 161 | BRENT | London | 45m | FADE_UP | OR_Q4_Wide | `66.4%` | 250 | `31` | `1.98` | `82R` | `-6.0R` | `7.25` |
| 162 | SP500 | NY Cash | 45m | FADE_UP | Thu | `68.0%` | 150 | `19` | `2.12` | `54R` | `-5.0R` | `7.24` |
| 163 | EURUSD | NY | 60m | FADE_UP | BtwCloseHigh | `68.5%` | 127 | `16` | `2.17` | `47R` | `-4.0R` | `7.22` |
| 164 | NATGAS | NY | 45m | FADE_UP | Wed | `68.5%` | 127 | `16` | `2.17` | `47R` | `-5.0R` | `7.22` |
| 165 | BRENT | London | 45m | FADE_DOWN | BASE | `63.0%` | 825 | `101` | `1.70` | `215R` | `-10.0R` | `7.22` |
| 166 | GBPUSD | NY | 60m | FADE_DOWN | OR_Q4_Wide | `71.7%` | 53 | `7` | `2.53` | `23R` | `-2.0R` | `7.21` |
| 167 | GBPAUD | Sydney | 15m | FADE_UP | BelowPD | `73.5%` | 34 | `4` | `2.78` | `16R` | `-2.0R` | `7.20` |
| 168 | XAGUSD | London | 60m | FADE_UP | OR_Q4_Wide | `66.1%` | 271 | `41` | `1.95` | `87R` | `-5.0R` | `7.20` |
| 169 | EURUSD | London | 60m | FADE_UP | BtwCloseHigh | `65.5%` | 330 | `41` | `1.89` | `102R` | `-9.0R` | `7.19` |
| 170 | XAGUSD | London | 15m | FADE_DOWN | AbovePD | `69.6%` | 92 | `11` | `2.29` | `36R` | `-3.0R` | `7.19` |
| 171 | EURJPY | Tokyo | 30m | FADE_UP | Thu | `67.0%` | 197 | `24` | `2.03` | `67R` | `-4.0R` | `7.19` |
| 172 | XAGUSD | NY | 45m | FADE_UP | RSI>70 | `71.4%` | 56 | `7` | `2.50` | `24R` | `-3.0R` | `7.19` |
| 173 | VIX | NY Cash | 30m | FADE_DOWN | Wed | `71.4%` | 56 | `17` | `2.50` | `24R` | `-4.0R` | `7.19` |
| 174 | WTI | NY Main | 45m | FADE_UP | OR_Q4_Wide | `68.1%` | 141 | `18` | `2.13` | `51R` | `-6.0R` | `7.19` |
| 175 | WTI | NY Main | 60m | FADE_UP | RSI_50-70 | `64.9%` | 404 | `49` | `1.85` | `120R` | `-12.0R` | `7.18` |
| 176 | EURJPY | London | 60m | FADE_UP | OR_Q4_Wide | `67.2%` | 183 | `23` | `2.05` | `63R` | `-5.0R` | `7.18` |
| 177 | AUDUSD | Sydney | 45m | FADE_UP | GapSmall | `71.2%` | 59 | `7` | `2.47` | `25R` | `-2.0R` | `7.17` |
| 178 | XAGUSD | NY | 30m | FADE_UP | BASE | `63.5%` | 655 | `80` | `1.74` | `177R` | `-11.0R` | `7.17` |
| 179 | XAGUSD | NY | 60m | FADE_UP | Mon | `70.0%` | 80 | `10` | `2.33` | `32R` | `-3.0R` | `7.16` |
| 180 | SP500 | NY Cash | 30m | FADE_DOWN | Wed | `67.5%` | 166 | `20` | `2.07` | `58R` | `-5.0R` | `7.15` |
| 181 | BRENT | London | 45m | FADE_DOWN | GapSmall | `63.1%` | 761 | `93` | `1.71` | `199R` | `-9.0R` | `7.15` |
| 182 | XAGUSD | London | 15m | FADE_UP | OR_Q4_Wide | `66.3%` | 243 | `37` | `1.96` | `79R` | `-10.0R` | `7.15` |
| 183 | EURJPY | Tokyo | 45m | FADE_UP | Thu | `66.7%` | 210 | `26` | `2.00` | `70R` | `-4.0R` | `7.13` |
| 184 | GBPUSD | NY | 60m | FADE_UP | Mon | `68.8%` | 109 | `13` | `2.21` | `41R` | `-6.0R` | `7.12` |
| 185 | XAGUSD | London | 60m | FADE_UP | BASE | `62.2%` | 1022 | `125` | `1.65` | `250R` | `-8.0R` | `7.11` |
| 186 | EURUSD | NY | 45m | FADE_UP | BASE | `63.5%` | 606 | `74` | `1.74` | `164R` | `-10.0R` | `7.09` |
| 187 | XAGUSD | London | 45m | FADE_UP | BASE | `62.1%` | 1033 | `126` | `1.64` | `251R` | `-11.0R` | `7.08` |
| 188 | SP500 | Pre-Market | 45m | FADE_DOWN | Fri | `67.9%` | 137 | `17` | `2.11` | `49R` | `-4.0R` | `7.06` |
| 189 | USDJPY | Tokyo | 60m | FADE_DOWN | ATR-10% | `72.5%` | 40 | `5` | `2.64` | `18R` | `-3.0R` | `7.05` |
| 190 | VIX | NY Cash | 45m | FADE_DOWN | RSI<30 | `72.5%` | 40 | `12` | `2.64` | `18R` | `-2.0R` | `7.05` |
| 191 | GBPJPY | Tokyo | 30m | FADE_UP | Fri | `66.8%` | 187 | `23` | `2.02` | `63R` | `-5.0R` | `7.05` |
| 192 | WTI | London Initial | 45m | FADE_UP | OR_Q1_Tight | `67.9%` | 134 | `17` | `2.12` | `48R` | `-3.0R` | `7.04` |
| 193 | EURJPY | London | 45m | FADE_UP | Thu | `66.5%` | 206 | `25` | `1.99` | `68R` | `-6.0R` | `7.04` |
| 194 | EURUSD | London | 60m | FADE_UP | GapSmall | `62.4%` | 893 | `109` | `1.66` | `221R` | `-9.0R` | `7.03` |
| 195 | EURUSD | NY | 60m | FADE_DOWN | OR_Q4_Wide | `72.1%` | 43 | `5` | `2.58` | `19R` | `-3.0R` | `7.00` |
| 196 | EURJPY | Tokyo | 60m | FADE_DOWN | ATR-10% | `72.1%` | 43 | `5` | `2.58` | `19R` | `-2.0R` | `7.00` |
| 197 | XAGUSD | London | 15m | FADE_UP | AbovePD | `68.0%` | 128 | `16` | `2.12` | `46R` | `-6.0R` | `7.00` |
| 198 | EURJPY | Tokyo | 60m | FADE_UP | RSI>70 | `69.4%` | 85 | `11` | `2.27` | `33R` | `-5.0R` | `7.00` |
| 199 | VIX | NY Cash | 30m | FADE_DOWN | BtwLowClose | `69.4%` | 85 | `25` | `2.27` | `33R` | `-4.0R` | `7.00` |
| 200 | XAGUSD | London | 60m | FADE_UP | Mon | `66.3%` | 208 | `25` | `1.97` | `68R` | `-4.0R` | `6.98` |
| 201 | USDJPY | NY | 45m | FADE_DOWN | Mon | `68.0%` | 125 | `15` | `2.12` | `45R` | `-4.0R` | `6.98` |
| 202 | SP500 | Pre-Market | 45m | FADE_DOWN | GapSmall | `63.0%` | 644 | `79` | `1.71` | `168R` | `-7.0R` | `6.96` |
| 203 | EURUSD | NY | 60m | FADE_UP | BASE | `63.8%` | 481 | `59` | `1.76` | `133R` | `-6.0R` | `6.95` |
| 204 | SP500 | NY Cash | 45m | FADE_UP | RSI_D>65 | `67.1%` | 161 | `21` | `2.04` | `55R` | `-3.0R` | `6.95` |
| 205 | EURUSD | London | 45m | FADE_UP | RSI_50-70 | `63.3%` | 570 | `70` | `1.73` | `152R` | `-13.0R` | `6.94` |
| 206 | BRENT | London | 15m | FADE_DOWN | AbovePD | `70.0%` | 70 | `9` | `2.33` | `28R` | `-6.0R` | `6.94` |
| 207 | EURUSD | NY | 60m | FADE_UP | OR_Q4_Wide | `70.9%` | 55 | `7` | `2.44` | `23R` | `-4.0R` | `6.93` |
| 208 | XAGUSD | London | 45m | FADE_UP | AbovePD | `66.7%` | 180 | `22` | `2.00` | `60R` | `-7.0R` | `6.92` |
| 209 | WTI | NY Main | 30m | FADE_UP | Mon | `66.7%` | 180 | `22` | `2.00` | `60R` | `-7.0R` | `6.92` |
| 210 | USDJPY | NY | 60m | FADE_UP | Fri | `70.7%` | 58 | `7` | `2.41` | `24R` | `-3.0R` | `6.92` |
| 211 | GBPAUD | Sydney | 15m | FADE_UP | BASE | `66.9%` | 169 | `21` | `2.02` | `57R` | `-8.0R` | `6.92` |
| 212 | WTI | NY Main | 30m | FADE_UP | RSI_50-70 | `63.9%` | 441 | `54` | `1.77` | `123R` | `-8.0R` | `6.91` |
| 213 | NATGAS | NY | 60m | FADE_DOWN | Tue | `67.7%` | 130 | `16` | `2.10` | `46R` | `-4.0R` | `6.90` |
| 214 | AUDUSD | London | 45m | FADE_UP | Tue | `66.7%` | 177 | `22` | `2.00` | `59R` | `-5.0R` | `6.90` |
| 215 | SP500 | NY Cash | 45m | FADE_UP | RSI_50-70 | `64.4%` | 371 | `45` | `1.81` | `107R` | `-5.0R` | `6.90` |
| 216 | WTI | NY Main | 60m | FADE_UP | GapSmall | `63.3%` | 540 | `66` | `1.73` | `144R` | `-9.0R` | `6.88` |
| 217 | WTI | NY Main | 60m | FADE_DOWN | BelowPD | `67.7%` | 127 | `16` | `2.10` | `45R` | `-7.0R` | `6.88` |
| 218 | EURUSD | NY | 60m | FADE_UP | Tue | `68.9%` | 90 | `11` | `2.21` | `34R` | `-3.0R` | `6.86` |
| 219 | EURUSD | NY | 60m | FADE_DOWN | RSI<30 | `73.3%` | 30 | `4` | `2.75` | `14R` | `-2.0R` | `6.86` |
| 220 | XAUUSD | NY | 45m | FADE_UP | ATR-10% | `73.3%` | 30 | `4` | `2.75` | `14R` | `-2.0R` | `6.86` |
| 221 | WTI | NY Main | 30m | FADE_UP | AbovePD | `65.9%` | 217 | `27` | `1.93` | `69R` | `-6.0R` | `6.85` |
| 222 | GBPAUD | London | 45m | FADE_DOWN | RSI_30-50 | `63.1%` | 564 | `69` | `1.71` | `148R` | `-8.0R` | `6.84` |
| 223 | GBPUSD | NY | 60m | FADE_UP | GapSmall | `64.5%` | 346 | `42` | `1.81` | `100R` | `-5.0R` | `6.83` |
| 224 | XAGUSD | London | 45m | FADE_UP | Mon | `65.9%` | 214 | `26` | `1.93` | `68R` | `-5.0R` | `6.83` |
| 225 | GBPJPY | Tokyo | 30m | FADE_DOWN | Wed | `66.9%` | 157 | `20` | `2.02` | `53R` | `-5.0R` | `6.83` |
| 226 | XAUUSD | London | 60m | FADE_DOWN | Wed | `66.3%` | 187 | `23` | `1.97` | `61R` | `-4.0R` | `6.83` |
| 227 | XAGUSD | NY | 30m | FADE_UP | OR_Q1_Tight | `66.3%` | 187 | `27` | `1.97` | `61R` | `-4.0R` | `6.83` |
| 228 | XAGUSD | London | 15m | FADE_DOWN | BASE | `63.0%` | 586 | `72` | `1.70` | `152R` | `-7.0R` | `6.82` |
| 229 | BRENT | NY | 15m | FADE_UP | OR_Q4_Wide | `65.9%` | 211 | `29` | `1.93` | `67R` | `-5.0R` | `6.81` |
| 230 | AUDUSD | Sydney | 60m | FADE_DOWN | BASE | `69.1%` | 81 | `10` | `2.24` | `31R` | `-6.0R` | `6.81` |
| 231 | EURJPY | London | 15m | FADE_DOWN | Thu | `67.1%` | 143 | `18` | `2.04` | `49R` | `-8.0R` | `6.81` |
| 232 | GBPUSD | NY | 60m | FADE_DOWN | Tue | `68.3%` | 101 | `13` | `2.16` | `37R` | `-6.0R` | `6.80` |
| 233 | EURUSD | NY | 45m | FADE_UP | RSI_50-70 | `64.5%` | 327 | `40` | `1.82` | `95R` | `-8.0R` | `6.80` |
| 234 | AUDUSD | London | 60m | FADE_UP | Tue | `66.5%` | 173 | `21` | `1.98` | `57R` | `-4.0R` | `6.79` |
| 235 | XAGUSD | NY | 30m | FADE_UP | Mon | `67.4%` | 129 | `16` | `2.07` | `45R` | `-5.0R` | `6.79` |
| 236 | EURUSD | London | 45m | FADE_UP | BASE | `61.6%` | 978 | `120` | `1.60` | `226R` | `-13.0R` | `6.79` |
| 237 | EURUSD | NY | 45m | FADE_UP | Thu | `67.8%` | 115 | `14` | `2.11` | `41R` | `-5.0R` | `6.78` |
| 238 | GBPUSD | NY | 60m | FADE_DOWN | AbovePD | `67.8%` | 115 | `14` | `2.11` | `41R` | `-4.0R` | `6.78` |
| 239 | WTI | NY Main | 60m | FADE_UP | Wed | `66.7%` | 162 | `20` | `2.00` | `54R` | `-6.0R` | `6.78` |
| 240 | GBPUSD | NY | 45m | FADE_DOWN | ATR+10% | `72.7%` | 33 | `4` | `2.67` | `15R` | `-2.0R` | `6.78` |
| 241 | AUDUSD | Sydney | 30m | FADE_UP | BtwLowClose | `72.7%` | 33 | `4` | `2.67` | `15R` | `-2.0R` | `6.78` |
| 242 | WTI | NY Main | 45m | FADE_UP | AbovePD+RSI_D>65 | `72.7%` | 33 | `4` | `2.67` | `15R` | `-3.0R` | `6.78` |
| 243 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | RSI_D<35 | `72.7%` | 33 | `5` | `2.67` | `15R` | `-2.0R` | `6.78` |
| 244 | GBPAUD | London | 60m | FADE_DOWN | GapSmall | `62.2%` | 749 | `92` | `1.65` | `183R` | `-10.0R` | `6.78` |
| 245 | AUDUSD | London | 60m | FADE_UP | BASE | `61.6%` | 941 | `115` | `1.61` | `219R` | `-11.0R` | `6.78` |
| 246 | XAGUSD | NY | 45m | FADE_UP | Thu | `68.4%` | 98 | `12` | `2.16` | `36R` | `-7.0R` | `6.77` |
| 247 | XAGUSD | London | 60m | FADE_UP | GapSmall | `61.7%` | 894 | `109` | `1.61` | `210R` | `-7.0R` | `6.77` |
| 248 | AUDUSD | London | 60m | FADE_UP | Thu | `66.0%` | 197 | `24` | `1.94` | `63R` | `-5.0R` | `6.76` |
| 249 | BRENT | London | 60m | FADE_UP | OR_Q4_Wide | `65.4%` | 237 | `30` | `1.89` | `73R` | `-4.0R` | `6.76` |
| 250 | XAGUSD | NY | 45m | FADE_UP | Tue | `68.4%` | 95 | `12` | `2.17` | `35R` | `-4.0R` | `6.75` |
| 251 | EURJPY | London | 15m | FADE_DOWN | BtwCloseHigh | `65.3%` | 242 | `30` | `1.88` | `74R` | `-6.0R` | `6.74` |
| 252 | XAGUSD | London | 15m | FADE_DOWN | Fri | `67.9%` | 109 | `14` | `2.11` | `39R` | `-5.0R` | `6.73` |
| 253 | BRENT | London | 45m | FADE_UP | AbovePD | `67.9%` | 109 | `13` | `2.11` | `39R` | `-3.0R` | `6.73` |
| 254 | NASDAQ100 | Pre-Market | 45m | FADE_UP | Tue | `66.7%` | 156 | `19` | `2.00` | `52R` | `-7.0R` | `6.73` |
| 255 | SP500 | NY Cash | 60m | FADE_UP | GapSmall | `63.2%` | 492 | `61` | `1.72` | `130R` | `-5.0R` | `6.73` |
| 256 | BRENT | London | 30m | SHAKEOUT_DOWN | OR_Q1_Tight | `72.2%` | 36 | `5` | `2.60` | `16R` | `-5.0R` | `6.73` |
| 257 | BRENT | London | 45m | FADE_UP | AbovePD+RSI_D>65 | `72.2%` | 36 | `4` | `2.60` | `16R` | `-2.0R` | `6.73` |
| 258 | XAGUSD | London | 60m | FADE_UP | RSI_50-70 | `62.7%` | 600 | `73` | `1.68` | `152R` | `-6.0R` | `6.73` |
| 259 | EURUSD | NY | 60m | FADE_UP | RSI_50-70 | `64.9%` | 268 | `33` | `1.85` | `80R` | `-5.0R` | `6.72` |
| 260 | WTI | NY Main | 60m | FADE_UP | Fri | `67.5%` | 120 | `15` | `2.08` | `42R` | `-3.0R` | `6.71` |
| 261 | NATGAS | NY | 45m | FADE_DOWN | GapSmall | `62.8%` | 549 | `67` | `1.69` | `141R` | `-8.0R` | `6.70` |
| 262 | WTI | NY Main | 45m | FADE_UP | GapSmall | `62.5%` | 626 | `77` | `1.66` | `156R` | `-8.0R` | `6.69` |
| 263 | EURUSD | London | 45m | FADE_UP | GapSmall | `61.5%` | 909 | `111` | `1.60` | `209R` | `-13.0R` | `6.69` |
| 264 | GBPAUD | London | 60m | FADE_DOWN | BASE | `61.6%` | 887 | `109` | `1.60` | `205R` | `-10.0R` | `6.69` |
| 265 | BRENT | NY | 60m | FADE_UP | BASE | `62.3%` | 668 | `82` | `1.65` | `164R` | `-9.0R` | `6.69` |
| 266 | XAGUSD | NY | 45m | FADE_DOWN | Wed | `67.5%` | 117 | `14` | `2.08` | `41R` | `-4.0R` | `6.68` |
| 267 | BRENT | NY | 45m | FADE_UP | RSI_50-70 | `63.3%` | 450 | `55` | `1.73` | `120R` | `-13.0R` | `6.68` |
| 268 | WTI | NY Main | 30m | FADE_UP | BASE | `61.6%` | 867 | `106` | `1.60` | `201R` | `-8.0R` | `6.68` |
| 269 | GBPUSD | NY | 60m | FADE_UP | RSI_D>65 | `70.2%` | 57 | `7` | `2.35` | `23R` | `-3.0R` | `6.68` |
| 270 | EURJPY | London | 15m | SHAKEOUT_DOWN | OR_Q1_Tight | `70.2%` | 57 | `8` | `2.35` | `23R` | `-2.0R` | `6.68` |
| 271 | GBPUSD | NY | 30m | FADE_DOWN | ATR+10% | `71.4%` | 42 | `5` | `2.50` | `18R` | `-2.0R` | `6.67` |
| 272 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | Mon | `71.4%` | 42 | `5` | `2.50` | `18R` | `-2.0R` | `6.67` |
| 273 | XAGUSD | NY | 30m | FADE_UP | BtwCloseHigh | `65.8%` | 193 | `24` | `1.92` | `61R` | `-6.0R` | `6.66` |
| 274 | XAGUSD | NY | 45m | FADE_UP | RSI_D<35 | `71.1%` | 45 | `6` | `2.46` | `19R` | `-3.0R` | `6.66` |
| 275 | VIX | NY Cash | 45m | FADE_DOWN | OR_Q4_Wide | `71.1%` | 45 | `13` | `2.46` | `19R` | `-2.0R` | `6.66` |
| 276 | GBPAUD | London | 45m | FADE_DOWN | GapSmall | `61.7%` | 822 | `101` | `1.61` | `192R` | `-10.0R` | `6.66` |
| 277 | EURUSD | London | 60m | FADE_UP | RSI_50-70 | `62.7%` | 550 | `67` | `1.68` | `140R` | `-7.0R` | `6.66` |
| 278 | EURJPY | London | 45m | FADE_UP | RSI_50-70 | `62.7%` | 555 | `68` | `1.68` | `141R` | `-7.0R` | `6.66` |
| 279 | EURUSD | London | 45m | FADE_UP | BtwCloseHigh | `64.1%` | 337 | `41` | `1.79` | `95R` | `-9.0R` | `6.66` |
| 280 | NASDAQ100 | NY Cash | 45m | FADE_UP | Thu | `67.5%` | 114 | `14` | `2.08` | `40R` | `-4.0R` | `6.66` |
| 281 | EURJPY | Tokyo | 45m | FADE_DOWN | OR_Q4_Wide | `65.1%` | 238 | `29` | `1.87` | `72R` | `-7.0R` | `6.66` |
| 282 | EURUSD | London | 30m | FADE_UP | RSI_50-70 | `62.7%` | 557 | `68` | `1.68` | `141R` | `-18.0R` | `6.65` |
| 283 | AUDUSD | London | 30m | FADE_UP | BASE | `61.2%` | 971 | `119` | `1.58` | `217R` | `-17.0R` | `6.63` |
| 284 | GBPUSD | NY | 45m | FADE_UP | Thu | `67.2%` | 122 | `15` | `2.05` | `42R` | `-5.0R` | `6.62` |
| 285 | XAGUSD | London | 45m | FADE_UP | GapSmall | `61.3%` | 902 | `110` | `1.58` | `204R` | `-11.0R` | `6.61` |
| 286 | AUDUSD | London | 60m | FADE_UP | RSI_30-50 | `64.4%` | 292 | `36` | `1.81` | `84R` | `-5.0R` | `6.61` |
| 287 | GBPAUD | Sydney | 30m | FADE_UP | GapSmall | `68.1%` | 94 | `12` | `2.13` | `34R` | `-4.0R` | `6.60` |
| 288 | NATGAS | NY | 45m | FADE_DOWN | Tue | `66.7%` | 141 | `17` | `2.00` | `47R` | `-5.0R` | `6.60` |
| 289 | BRENT | NY | 60m | FADE_UP | RSI_50-70 | `63.4%` | 402 | `49` | `1.73` | `108R` | `-6.0R` | `6.60` |
| 290 | AUDUSD | Sydney | 30m | FADE_UP | BASE | `67.2%` | 119 | `15` | `2.05` | `41R` | `-4.0R` | `6.59` |
| 291 | EURJPY | London | 45m | FADE_UP | BtwCloseHigh | `63.9%` | 338 | `41` | `1.77` | `94R` | `-5.0R` | `6.59` |
| 292 | GBPJPY | London | 45m | FADE_DOWN | BtwCloseHigh | `64.4%` | 289 | `36` | `1.81` | `83R` | `-11.0R` | `6.59` |
| 293 | XAGUSD | NY | 60m | FADE_UP | Tue | `68.9%` | 74 | `9` | `2.22` | `28R` | `-3.0R` | `6.58` |
| 294 | SP500 | Pre-Market | 45m | FADE_DOWN | BASE | `61.6%` | 771 | `95` | `1.60` | `179R` | `-7.0R` | `6.57` |
| 295 | SP500 | NY Cash | 45m | FADE_DOWN | Mon | `66.9%` | 127 | `16` | `2.02` | `43R` | `-7.0R` | `6.56` |
| 296 | SP500 | Pre-Market | 60m | FADE_DOWN | BtwCloseHigh | `64.6%` | 260 | `32` | `1.83` | `76R` | `-5.0R` | `6.56` |
| 297 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | RSI_30-50 | `64.1%` | 309 | `38` | `1.78` | `87R` | `-13.0R` | `6.55` |
| 298 | XAGUSD | London | 45m | FADE_UP | OR_Q4_Wide | `64.5%` | 265 | `44` | `1.82` | `77R` | `-5.0R` | `6.55` |
| 299 | GBPJPY | Tokyo | 60m | FADE_DOWN | BtwCloseHigh | `62.2%` | 598 | `73` | `1.65` | `146R` | `-8.0R` | `6.55` |
| 300 | GBPJPY | Tokyo | 45m | FADE_UP | Fri | `65.3%` | 202 | `25` | `1.89` | `62R` | `-5.0R` | `6.54` |
| 301 | BRENT | London | 45m | FADE_DOWN | RSI_D>65 | `66.9%` | 124 | `15` | `2.02` | `42R` | `-6.0R` | `6.53` |
| 302 | BRENT | London | 60m | FADE_DOWN | RSI_30-50 | `62.5%` | 523 | `64` | `1.67` | `131R` | `-10.0R` | `6.53` |
| 303 | NATGAS | NY | 60m | FADE_DOWN | BASE | `62.2%` | 580 | `71` | `1.65` | `142R` | `-8.0R` | `6.53` |
| 304 | XAGUSD | NY | 45m | FADE_UP | RSI_50-70 | `64.2%` | 293 | `36` | `1.79` | `83R` | `-7.0R` | `6.53` |
| 305 | XAGUSD | London | 15m | FADE_DOWN | GapSmall | `62.6%` | 505 | `62` | `1.67` | `127R` | `-4.0R` | `6.51` |
| 306 | EURUSD | London | 60m | FADE_UP | BelowPD | `66.7%` | 132 | `16` | `2.00` | `44R` | `-3.0R` | `6.51` |
| 307 | SP500 | Pre-Market | 15m | FADE_UP | BtwLowClose | `66.7%` | 132 | `16` | `2.00` | `44R` | `-5.0R` | `6.51` |
| 308 | AUDUSD | London | 30m | FADE_UP | Tue | `65.6%` | 183 | `23` | `1.90` | `57R` | `-5.0R` | `6.51` |
| 309 | EURUSD | NY | 60m | FADE_DOWN | GapSmall | `63.7%` | 331 | `41` | `1.76` | `91R` | `-6.0R` | `6.50` |
| 310 | WTI | London Initial | 45m | FADE_DOWN | AbovePD | `66.9%` | 121 | `15` | `2.02` | `41R` | `-4.0R` | `6.50` |
| 311 | BRENT | London | 60m | FADE_DOWN | GapSmall | `61.2%` | 828 | `101` | `1.58` | `186R` | `-13.0R` | `6.50` |
| 312 | EURUSD | NY | 45m | FADE_UP | GapSmall | `63.0%` | 427 | `52` | `1.70` | `111R` | `-9.0R` | `6.50` |
| 313 | EURJPY | Tokyo | 60m | FADE_DOWN | BtwLowClose | `63.8%` | 318 | `39` | `1.77` | `88R` | `-6.0R` | `6.49` |
| 314 | GBPUSD | NY | 60m | FADE_DOWN | GapSmall | `63.6%` | 346 | `43` | `1.75` | `94R` | `-6.0R` | `6.49` |
| 315 | XAGUSD | London | 45m | FADE_UP | RSI_30-50 | `63.8%` | 323 | `39` | `1.76` | `89R` | `-5.0R` | `6.49` |
| 316 | SP500 | Pre-Market | 45m | FADE_UP | Tue | `66.2%` | 148 | `18` | `1.96` | `48R` | `-6.0R` | `6.49` |
| 317 | EURUSD | London | 60m | FADE_UP | RSI_D>65 | `67.7%` | 96 | `12` | `2.10` | `34R` | `-5.0R` | `6.48` |
| 318 | USDJPY | NY | 45m | FADE_DOWN | RSI_D<35 | `69.4%` | 62 | `8` | `2.26` | `24R` | `-4.0R` | `6.48` |
| 319 | AUDUSD | London | 45m | FADE_UP | Thu | `65.1%` | 209 | `26` | `1.86` | `63R` | `-4.0R` | `6.48` |
| 320 | GBPAUD | London | 45m | FADE_DOWN | OR_Q4_Wide | `65.1%` | 209 | `26` | `1.86` | `63R` | `-9.0R` | `6.48` |
| 321 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | RSI_50-70 | `67.3%` | 107 | `13` | `2.06` | `37R` | `-5.0R` | `6.47` |
| 322 | SP500 | Pre-Market | 60m | FADE_DOWN | BtwLowClose | `64.7%` | 235 | `29` | `1.83` | `69R` | `-8.0R` | `6.47` |
| 323 | BRENT | NY | 45m | FADE_UP | GapSmall | `62.0%` | 590 | `72` | `1.63` | `142R` | `-9.0R` | `6.47` |
| 324 | BRENT | London | 45m | FADE_UP | BASE | `61.1%` | 836 | `102` | `1.57` | `186R` | `-12.0R` | `6.47` |
| 325 | BRENT | London | 30m | FADE_DOWN | BASE | `61.7%` | 673 | `82` | `1.61` | `157R` | `-7.0R` | `6.46` |
| 326 | GBPUSD | NY | 60m | FADE_DOWN | RSI_30-50 | `64.4%` | 253 | `31` | `1.81` | `73R` | `-5.0R` | `6.46` |
| 327 | SP500 | NY Cash | 60m | FADE_UP | OR_Q4_Wide | `68.4%` | 79 | `13` | `2.16` | `29R` | `-5.0R` | `6.45` |
| 328 | EURJPY | London | 60m | FADE_UP | RSI_50-70 | `62.2%` | 545 | `67` | `1.65` | `133R` | `-9.0R` | `6.45` |
| 329 | GBPJPY | Tokyo | 45m | FADE_DOWN | Wed | `65.7%` | 169 | `21` | `1.91` | `53R` | `-4.0R` | `6.45` |
| 330 | USDJPY | NY | 60m | FADE_DOWN | Mon | `67.3%` | 104 | `13` | `2.06` | `36R` | `-2.0R` | `6.44` |
| 331 | SP500 | NY Cash | 60m | FADE_UP | Thu | `66.4%` | 134 | `17` | `1.98` | `44R` | `-4.0R` | `6.43` |
| 332 | NASDAQ100 | NY Cash | 30m | FADE_UP | OR_Q4_Wide | `66.4%` | 134 | `22` | `1.98` | `44R` | `-4.0R` | `6.43` |
| 333 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | BtwCloseHigh | `69.6%` | 56 | `7` | `2.29` | `22R` | `-2.0R` | `6.43` |
| 334 | NASDAQ100 | NY Cash | 60m | FADE_UP | RSI>70 | `69.6%` | 56 | `7` | `2.29` | `22R` | `-4.0R` | `6.43` |
| 335 | GBPJPY | Tokyo | 60m | FADE_DOWN | BASE | `60.6%` | 980 | `120` | `1.54` | `208R` | `-7.0R` | `6.42` |
| 336 | GBPJPY | Tokyo | 60m | FADE_DOWN | GapSmall | `60.6%` | 980 | `120` | `1.54` | `208R` | `-7.0R` | `6.42` |
| 337 | XAGUSD | London | 30m | FADE_DOWN | OR_Q4_Wide | `65.0%` | 203 | `31` | `1.86` | `61R` | `-6.0R` | `6.42` |
| 338 | SP500 | NY Cash | 45m | FADE_DOWN | GapSmall | `62.2%` | 534 | `66` | `1.64` | `130R` | `-7.0R` | `6.42` |
| 339 | XAGUSD | NY | 30m | FADE_UP | BtwLowClose | `65.1%` | 195 | `24` | `1.87` | `59R` | `-8.0R` | `6.41` |
| 340 | BRENT | London | 60m | FADE_UP | Thu | `65.1%` | 195 | `24` | `1.87` | `59R` | `-6.0R` | `6.41` |
| 341 | XAGUSD | London | 30m | FADE_DOWN | BASE | `61.1%` | 797 | `98` | `1.57` | `177R` | `-13.0R` | `6.41` |
| 342 | EURJPY | London | 45m | FADE_UP | OR_Q4_Wide | `64.9%` | 208 | `26` | `1.85` | `62R` | `-7.0R` | `6.41` |
| 343 | AUDUSD | London | 45m | FADE_UP | RSI_50-70 | `62.0%` | 568 | `70` | `1.63` | `136R` | `-7.0R` | `6.40` |
| 344 | SP500 | NY Cash | 60m | FADE_UP | BASE | `61.9%` | 590 | `72` | `1.62` | `140R` | `-6.0R` | `6.40` |
| 345 | EURUSD | NY | 60m | FADE_DOWN | BASE | `62.4%` | 484 | `59` | `1.66` | `120R` | `-10.0R` | `6.40` |
| 346 | EURJPY | Tokyo | 60m | FADE_DOWN | GapSmall | `60.5%` | 995 | `122` | `1.53` | `209R` | `-11.0R` | `6.40` |
| 347 | GBPUSD | NY | 60m | FADE_DOWN | RSI_D>65 | `70.0%` | 50 | `6` | `2.33` | `20R` | `-2.0R` | `6.39` |
| 348 | BRENT | London | 45m | FADE_DOWN | Mon | `65.8%` | 155 | `19` | `1.92` | `49R` | `-4.0R` | `6.39` |
| 349 | GBPJPY | Tokyo | 45m | FADE_UP | Thu | `65.1%` | 192 | `24` | `1.87` | `58R` | `-4.0R` | `6.39` |
| 350 | EURJPY | London | 30m | FADE_UP | BASE | `60.5%` | 982 | `120` | `1.53` | `206R` | `-9.0R` | `6.38` |
| 351 | XAGUSD | London | 60m | FADE_UP | AbovePD | `65.2%` | 184 | `23` | `1.88` | `56R` | `-5.0R` | `6.38` |
| 352 | GBPUSD | London | 60m | FADE_UP | Fri | `65.3%` | 176 | `22` | `1.89` | `54R` | `-7.0R` | `6.37` |
| 353 | BRENT | NY | 60m | FADE_UP | GapSmall | `62.1%` | 515 | `63` | `1.64` | `125R` | `-9.0R` | `6.37` |
| 354 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | Tue | `71.9%` | 32 | `4` | `2.56` | `14R` | `-2.0R` | `6.37` |
| 355 | EURUSD | NY | 30m | FADE_UP | OR_Q4_Wide | `66.2%` | 136 | `17` | `1.96` | `44R` | `-5.0R` | `6.36` |
| 356 | USDJPY | NY | 45m | FADE_DOWN | AbovePD | `66.2%` | 136 | `17` | `1.96` | `44R` | `-4.0R` | `6.36` |
| 357 | SP500 | NY Cash | 60m | FADE_DOWN | Wed | `66.2%` | 136 | `17` | `1.96` | `44R` | `-5.0R` | `6.36` |
| 358 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | BtwCloseHigh | `70.5%` | 44 | `5` | `2.38` | `18R` | `-3.0R` | `6.36` |
| 359 | GBPUSD | NY | 60m | FADE_DOWN | RSI_50-70 | `65.1%` | 189 | `23` | `1.86` | `57R` | `-7.0R` | `6.36` |
| 360 | EURJPY | London | 45m | FADE_UP | GapSmall | `60.8%` | 830 | `102` | `1.55` | `180R` | `-11.0R` | `6.35` |
| 361 | WTI | London Initial | 45m | FADE_UP | OR_Q4_Wide | `64.0%` | 264 | `33` | `1.78` | `74R` | `-8.0R` | `6.35` |
| 362 | EURJPY | London | 60m | FADE_UP | BASE | `60.6%` | 911 | `111` | `1.54` | `193R` | `-8.0R` | `6.35` |
| 363 | BRENT | London | 45m | FADE_UP | GapSmall | `61.1%` | 760 | `93` | `1.57` | `168R` | `-12.0R` | `6.35` |
| 364 | XAUUSD | NY | 15m | FADE_DOWN | AbovePD+RSI_D>65 | `70.7%` | 41 | `6` | `2.42` | `17R` | `-4.0R` | `6.35` |
| 365 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | OR_Q1_Tight | `70.7%` | 41 | `20` | `2.42` | `17R` | `-2.0R` | `6.35` |
| 366 | BRENT | NY | 30m | FADE_UP | AbovePD | `65.2%` | 181 | `23` | `1.87` | `55R` | `-6.0R` | `6.35` |
| 367 | XAGUSD | London | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `71.1%` | 38 | `5` | `2.45` | `16R` | `-3.0R` | `6.34` |
| 368 | SP500 | NY Cash | 30m | FADE_DOWN | GapSmall | `61.6%` | 602 | `74` | `1.61` | `140R` | `-8.0R` | `6.33` |
| 369 | WTI | NY Main | 15m | FADE_UP | RSI>70 | `67.4%` | 95 | `12` | `2.06` | `33R` | `-3.0R` | `6.33` |
| 370 | WTI | NY Main | 45m | FADE_UP | RSI>70 | `67.4%` | 95 | `12` | `2.06` | `33R` | `-4.0R` | `6.33` |
| 371 | XAGUSD | London | 60m | FADE_UP | BtwLowClose | `62.9%` | 375 | `46` | `1.70` | `97R` | `-9.0R` | `6.33` |
| 372 | BRENT | London | 30m | FADE_DOWN | BtwLowClose | `64.3%` | 238 | `29` | `1.80` | `68R` | `-4.0R` | `6.33` |
| 373 | GBPJPY | Tokyo | 60m | FADE_DOWN | Wed | `65.1%` | 186 | `23` | `1.86` | `56R` | `-8.0R` | `6.33` |
| 374 | EURJPY | London | 30m | FADE_DOWN | BtwCloseHigh | `63.7%` | 284 | `35` | `1.76` | `78R` | `-7.0R` | `6.33` |
| 375 | XAUUSD | NY | 60m | FADE_DOWN | RSI_50-70 | `65.8%` | 149 | `18` | `1.92` | `47R` | `-3.0R` | `6.32` |
| 376 | XAGUSD | NY | 45m | FADE_UP | BtwCloseHigh | `65.8%` | 149 | `19` | `1.92` | `47R` | `-4.0R` | `6.32` |
| 377 | NATGAS | NY | 60m | FADE_DOWN | GapSmall | `62.3%` | 469 | `57` | `1.65` | `115R` | `-9.0R` | `6.32` |
| 378 | XAGUSD | NY | 15m | FADE_UP | BtwCloseHigh | `64.3%` | 230 | `28` | `1.80` | `66R` | `-9.0R` | `6.32` |
| 379 | EURUSD | NY | 45m | FADE_UP | Tue | `66.7%` | 114 | `14` | `2.00` | `38R` | `-6.0R` | `6.31` |
| 380 | GBPJPY | Tokyo | 45m | FADE_DOWN | BtwCloseHigh | `61.9%` | 540 | `66` | `1.62` | `128R` | `-10.0R` | `6.31` |
| 381 | WTI | London Initial | 45m | FADE_UP | Thu | `65.3%` | 170 | `21` | `1.88` | `52R` | `-5.0R` | `6.31` |
| 382 | SP500 | Pre-Market | 60m | FADE_DOWN | GapSmall | `61.3%` | 664 | `81` | `1.58` | `150R` | `-12.0R` | `6.31` |
| 383 | GBPJPY | Tokyo | 45m | FADE_DOWN | BASE | `60.5%` | 887 | `108` | `1.53` | `187R` | `-8.0R` | `6.31` |
| 384 | GBPJPY | Tokyo | 45m | FADE_DOWN | GapSmall | `60.5%` | 887 | `108` | `1.53` | `187R` | `-8.0R` | `6.31` |
| 385 | GBPJPY | Tokyo | 15m | FADE_DOWN | Wed | `66.4%` | 122 | `15` | `1.98` | `40R` | `-4.0R` | `6.30` |
| 386 | EURUSD | London | 15m | FADE_UP | Wed | `65.4%` | 162 | `20` | `1.89` | `50R` | `-6.0R` | `6.30` |
| 387 | XAGUSD | NY | 60m | FADE_UP | RSI_50-70 | `64.2%` | 240 | `30` | `1.79` | `68R` | `-9.0R` | `6.30` |
| 388 | GBPJPY | Tokyo | 60m | FADE_DOWN | RSI_30-50 | `61.6%` | 581 | `71` | `1.61` | `135R` | `-11.0R` | `6.30` |
| 389 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | BASE | `64.3%` | 227 | `28` | `1.80` | `65R` | `-7.0R` | `6.29` |
| 390 | GBPAUD | London | 45m | FADE_DOWN | BASE | `60.2%` | 983 | `120` | `1.51` | `201R` | `-11.0R` | `6.28` |
| 391 | EURJPY | Tokyo | 60m | FADE_UP | Thu | `64.9%` | 188 | `23` | `1.85` | `56R` | `-4.0R` | `6.28` |
| 392 | XAGUSD | London | 45m | FADE_UP | RSI_50-70 | `61.4%` | 612 | `75` | `1.59` | `140R` | `-7.0R` | `6.28` |
| 393 | GBPAUD | London | 60m | FADE_DOWN | RSI_50-70 | `63.9%` | 255 | `31` | `1.77` | `71R` | `-5.0R` | `6.28` |
| 394 | BRENT | London | 60m | FADE_DOWN | BtwCloseHigh | `62.7%` | 381 | `47` | `1.68` | `97R` | `-5.0R` | `6.27` |
| 395 | GBPJPY | Tokyo | 45m | FADE_UP | GapSmall | `60.2%` | 980 | `120` | `1.51` | `200R` | `-9.0R` | `6.27` |
| 396 | WTI | London Initial | 45m | FADE_UP | BASE | `60.5%` | 878 | `107` | `1.53` | `184R` | `-12.0R` | `6.27` |
| 397 | EURJPY | London | 30m | FADE_UP | Thu | `64.8%` | 193 | `24` | `1.84` | `57R` | `-7.0R` | `6.27` |
| 398 | WTI | London Initial | 45m | FADE_UP | GapSmall | `60.6%` | 832 | `102` | `1.54` | `176R` | `-10.0R` | `6.26` |
| 399 | XAGUSD | London | 45m | FADE_DOWN | AbovePD | `65.7%` | 143 | `18` | `1.92` | `45R` | `-4.0R` | `6.26` |
| 400 | XAGUSD | London | 15m | FADE_UP | RSI>70 | `68.9%` | 61 | `8` | `2.21` | `23R` | `-4.0R` | `6.26` |
| 401 | AUDUSD | London | 45m | FADE_UP | BelowPD | `65.2%` | 164 | `20` | `1.88` | `50R` | `-6.0R` | `6.25` |
| 402 | WTI | NY Main | 15m | FADE_UP | OR_Q4_Wide | `64.4%` | 216 | `28` | `1.81` | `62R` | `-4.0R` | `6.24` |
| 403 | NATGAS | NY | 60m | FADE_DOWN | RSI_D<35 | `68.0%` | 75 | `9` | `2.12` | `27R` | `-4.0R` | `6.24` |
| 404 | SP500 | Pre-Market | 45m | FADE_DOWN | BtwLowClose | `64.0%` | 239 | `29` | `1.78` | `67R` | `-8.0R` | `6.24` |
| 405 | WTI | NY Main | 30m | FADE_UP | Wed | `64.7%` | 190 | `23` | `1.84` | `56R` | `-4.0R` | `6.24` |
| 406 | XAGUSD | London | 30m | FADE_DOWN | Fri | `65.5%` | 148 | `19` | `1.90` | `46R` | `-8.0R` | `6.23` |
| 407 | BRENT | London | 45m | FADE_UP | RSI_D>65 | `65.7%` | 140 | `17` | `1.92` | `44R` | `-3.0R` | `6.22` |
| 408 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | GapSmall | `65.7%` | 140 | `17` | `1.92` | `44R` | `-6.0R` | `6.22` |
| 409 | BRENT | London | 30m | FADE_DOWN | RSI_30-50 | `62.4%` | 402 | `49` | `1.66` | `100R` | `-8.0R` | `6.22` |
| 410 | BRENT | London | 45m | FADE_DOWN | OR_Q1_Tight | `66.1%` | 124 | `16` | `1.95` | `40R` | `-3.0R` | `6.22` |
| 411 | SP500 | Pre-Market | 60m | FADE_DOWN | RSI_D<35 | `69.0%` | 58 | `8` | `2.22` | `22R` | `-2.0R` | `6.22` |
| 412 | EURJPY | Tokyo | 45m | FADE_UP | OR_Q4_Wide | `63.8%` | 254 | `31` | `1.76` | `70R` | `-10.0R` | `6.22` |
| 413 | GBPUSD | NY | 45m | FADE_UP | BASE | `61.2%` | 636 | `78` | `1.57` | `142R` | `-9.0R` | `6.22` |
| 414 | XAGUSD | NY | 15m | FADE_UP | Mon | `65.2%` | 161 | `20` | `1.88` | `49R` | `-4.0R` | `6.21` |
| 415 | AUDUSD | London | 45m | FADE_UP | GapSmall | `60.4%` | 848 | `104` | `1.52` | `176R` | `-11.0R` | `6.20` |
| 416 | NATGAS | NY | 45m | FADE_UP | AbovePD | `65.4%` | 153 | `19` | `1.89` | `47R` | `-7.0R` | `6.20` |
| 417 | VIX | NY Cash | 30m | FADE_DOWN | RSI_30-50 | `65.4%` | 153 | `46` | `1.89` | `47R` | `-4.0R` | `6.20` |
| 418 | AUDUSD | London | 15m | FADE_UP | RSI_D>65 | `68.1%` | 72 | `9` | `2.13` | `26R` | `-2.0R` | `6.20` |
| 419 | XAGUSD | NY | 30m | FADE_DOWN | Wed | `65.5%` | 145 | `18` | `1.90` | `45R` | `-6.0R` | `6.20` |
| 420 | GBPUSD | London | 60m | FADE_DOWN | BelowPD | `66.4%` | 113 | `14` | `1.97` | `37R` | `-4.0R` | `6.19` |
| 421 | XAGUSD | London | 45m | FADE_UP | BelowPD | `65.7%` | 137 | `17` | `1.91` | `43R` | `-4.0R` | `6.19` |
| 422 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | Mon | `65.7%` | 137 | `17` | `1.91` | `43R` | `-7.0R` | `6.19` |
| 423 | NASDAQ100 | NY Cash | 45m | FADE_UP | GapSmall | `61.8%` | 477 | `59` | `1.62` | `113R` | `-9.0R` | `6.18` |
| 424 | XAGUSD | London | 30m | FADE_DOWN | GapSmall | `60.8%` | 704 | `86` | `1.55` | `152R` | `-12.0R` | `6.18` |
| 425 | XAGUSD | London | 15m | FADE_UP | BASE | `60.8%` | 692 | `85` | `1.55` | `150R` | `-10.0R` | `6.18` |
| 426 | GBPUSD | NY | 45m | FADE_UP | GapSmall | `62.2%` | 423 | `52` | `1.64` | `103R` | `-8.0R` | `6.18` |
| 427 | SP500 | Pre-Market | 15m | FADE_UP | OR_Q4_Wide | `64.5%` | 197 | `24` | `1.81` | `57R` | `-5.0R` | `6.18` |
| 428 | GBPJPY | Tokyo | 30m | FADE_UP | BASE | `60.1%` | 903 | `110` | `1.51` | `183R` | `-9.0R` | `6.17` |
| 429 | GBPJPY | Tokyo | 30m | FADE_UP | GapSmall | `60.1%` | 903 | `110` | `1.51` | `183R` | `-9.0R` | `6.17` |
| 430 | BRENT | NY | 60m | FADE_DOWN | GapSmall | `61.6%` | 518 | `63` | `1.60` | `120R` | `-6.0R` | `6.17` |
| 431 | EURUSD | London | 15m | FADE_UP | RSI_50-70 | `62.3%` | 398 | `49` | `1.65` | `98R` | `-7.0R` | `6.17` |
| 432 | EURUSD | London | 30m | FADE_UP | GapSmall | `60.0%` | 945 | `116` | `1.50` | `189R` | `-18.0R` | `6.17` |
| 433 | SP500 | Pre-Market | 60m | FADE_DOWN | RSI_30-50 | `61.8%` | 469 | `58` | `1.62` | `111R` | `-7.0R` | `6.16` |
| 434 | SP500 | NY Cash | 45m | FADE_DOWN | BtwLowClose | `64.6%` | 189 | `23` | `1.82` | `55R` | `-8.0R` | `6.16` |
| 435 | XAGUSD | London | 30m | FADE_UP | ATR+10% | `69.2%` | 52 | `6` | `2.25` | `20R` | `-2.0R` | `6.15` |
| 436 | BRENT | London | 30m | FADE_UP | RSI_D<35 | `69.2%` | 52 | `7` | `2.25` | `20R` | `-3.0R` | `6.15` |
| 437 | USDJPY | NY | 60m | FADE_UP | RSI_30-50 | `65.7%` | 134 | `16` | `1.91` | `42R` | `-6.0R` | `6.15` |
| 438 | EURJPY | London | 30m | FADE_UP | GapSmall | `60.3%` | 838 | `103` | `1.52` | `172R` | `-10.0R` | `6.15` |
| 439 | XAGUSD | NY | 45m | FADE_UP | AbovePD | `65.9%` | 126 | `16` | `1.93` | `40R` | `-5.0R` | `6.15` |
| 440 | SP500 | NY Cash | 30m | FADE_DOWN | Mon | `65.9%` | 126 | `16` | `1.93` | `40R` | `-6.0R` | `6.15` |
| 441 | AUDUSD | London | 60m | FADE_UP | GapSmall | `60.4%` | 795 | `98` | `1.52` | `165R` | `-8.0R` | `6.14` |
| 442 | EURUSD | London | 30m | FADE_UP | BASE | `59.8%` | 1014 | `124` | `1.49` | `198R` | `-15.0R` | `6.14` |
| 443 | NATGAS | NY | 45m | FADE_DOWN | RSI_30-50 | `62.8%` | 323 | `40` | `1.69` | `83R` | `-10.0R` | `6.14` |
| 444 | SP500 | NY Cash | 60m | FADE_UP | RSI_50-70 | `62.8%` | 323 | `40` | `1.69` | `83R` | `-4.0R` | `6.14` |
| 445 | AUDUSD | London | 60m | FADE_UP | OR_Q1_Tight | `63.7%` | 245 | `31` | `1.75` | `67R` | `-4.0R` | `6.14` |
| 446 | WTI | London Initial | 45m | FADE_DOWN | GapSmall | `60.2%` | 830 | `102` | `1.52` | `170R` | `-8.0R` | `6.13` |
| 447 | USDJPY | NY | 45m | FADE_UP | RSI_30-50 | `64.5%` | 186 | `23` | `1.82` | `54R` | `-4.0R` | `6.13` |
| 448 | EURJPY | Tokyo | 45m | FADE_UP | BASE | `59.7%` | 1027 | `126` | `1.48` | `199R` | `-11.0R` | `6.13` |
| 449 | EURJPY | Tokyo | 45m | FADE_UP | GapSmall | `59.7%` | 1027 | `126` | `1.48` | `199R` | `-11.0R` | `6.13` |
| 450 | GBPAUD | London | 60m | FADE_DOWN | AbovePD | `65.5%` | 139 | `17` | `1.90` | `43R` | `-7.0R` | `6.12` |
| 451 | SP500 | Pre-Market | 60m | FADE_DOWN | BASE | `60.3%` | 801 | `98` | `1.52` | `165R` | `-11.0R` | `6.12` |
| 452 | AUDUSD | Sydney | 30m | FADE_UP | RSI_30-50 | `69.4%` | 49 | `6` | `2.27` | `19R` | `-4.0R` | `6.12` |
| 453 | XAGUSD | London | 15m | FADE_DOWN | RSI_30-50 | `62.8%` | 325 | `40` | `1.69` | `83R` | `-8.0R` | `6.12` |
| 454 | XAGUSD | NY | 15m | FADE_UP | GapSmall | `61.2%` | 567 | `69` | `1.58` | `127R` | `-12.0R` | `6.12` |
| 455 | USDJPY | NY | 60m | FADE_UP | GapSmall | `62.8%` | 320 | `39` | `1.69` | `82R` | `-6.0R` | `6.12` |
| 456 | BRENT | London | 60m | FADE_DOWN | BtwLowClose | `63.0%` | 305 | `38` | `1.70` | `79R` | `-7.0R` | `6.12` |
| 457 | BRENT | London | 30m | FADE_DOWN | Mon | `65.9%` | 123 | `15` | `1.93` | `39R` | `-4.0R` | `6.11` |
| 458 | EURJPY | London | 45m | FADE_UP | Fri | `64.3%` | 196 | `24` | `1.80` | `56R` | `-7.0R` | `6.11` |
| 459 | XAGUSD | London | 45m | FADE_UP | RSI_D<35 | `67.0%` | 88 | `11` | `2.03` | `30R` | `-4.0R` | `6.11` |
| 460 | SP500 | NY Cash | 60m | FADE_UP | RSI>70 | `67.0%` | 88 | `11` | `2.03` | `30R` | `-4.0R` | `6.11` |
| 461 | GBPJPY | London | 15m | FADE_DOWN | OR_Q4_Wide | `63.5%` | 252 | `31` | `1.74` | `68R` | `-7.0R` | `6.11` |
| 462 | SP500 | Pre-Market | 15m | FADE_UP | Tue | `67.5%` | 77 | `9` | `2.08` | `27R` | `-3.0R` | `6.10` |
| 463 | EURJPY | London | 60m | FADE_UP | GapSmall | `60.3%` | 788 | `96` | `1.52` | `162R` | `-8.0R` | `6.10` |
| 464 | XAGUSD | NY | 30m | FADE_UP | RSI_30-50 | `63.8%` | 224 | `27` | `1.77` | `62R` | `-7.0R` | `6.10` |
| 465 | NASDAQ100 | NY Cash | 15m | FADE_UP | OR_Q4_Wide | `64.5%` | 183 | `23` | `1.82` | `53R` | `-7.0R` | `6.10` |
| 466 | EURJPY | Tokyo | 45m | FADE_DOWN | BtwLowClose | `63.0%` | 297 | `36` | `1.70` | `77R` | `-9.0R` | `6.09` |
| 467 | EURUSD | London | 45m | FADE_UP | OR_Q4_Wide | `63.8%` | 229 | `28` | `1.76` | `63R` | `-5.0R` | `6.09` |
| 468 | GBPUSD | NY | 60m | FADE_UP | RSI_30-50 | `65.0%` | 157 | `19` | `1.85` | `47R` | `-4.0R` | `6.09` |
| 469 | NASDAQ100 | Pre-Market | 30m | MOMENTUM_UP | Wed | `59.1%` | 115 | `14` | `2.17` | `55R` | `-5.0R` | `6.09` |
| 470 | GBPUSD | NY | 45m | FADE_DOWN | Wed | `65.4%` | 136 | `17` | `1.89` | `42R` | `-5.0R` | `6.09` |
| 471 | XAGUSD | London | 60m | FADE_UP | BelowPD | `65.4%` | 136 | `17` | `1.89` | `42R` | `-4.0R` | `6.09` |
| 472 | AUDUSD | Sydney | 30m | FADE_UP | OR_Q4_Wide | `69.6%` | 46 | `6` | `2.29` | `18R` | `-3.0R` | `6.09` |
| 473 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | RSI_50-70 | `69.6%` | 46 | `6` | `2.29` | `18R` | `-2.0R` | `6.09` |
| 474 | VIX | NY Cash | 60m | FADE_DOWN | OR_Q4_Wide | `69.6%` | 46 | `14` | `2.29` | `18R` | `-3.0R` | `6.09` |
| 475 | AUDUSD | London | 30m | FADE_UP | RSI_50-70 | `61.3%` | 532 | `65` | `1.58` | `120R` | `-13.0R` | `6.09` |
| 476 | SP500 | NY Cash | 60m | FADE_UP | BtwCloseHigh | `64.4%` | 188 | `23` | `1.81` | `54R` | `-6.0R` | `6.09` |
| 477 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | RSI_50-70 | `66.7%` | 96 | `12` | `2.00` | `32R` | `-5.0R` | `6.09` |
| 478 | XAGUSD | London | 45m | FADE_DOWN | BASE | `59.9%` | 886 | `109` | `1.50` | `176R` | `-18.0R` | `6.08` |
| 479 | SP500 | NY Cash | 45m | FADE_DOWN | BASE | `60.7%` | 666 | `82` | `1.54` | `142R` | `-6.0R` | `6.08` |
| 480 | AUDUSD | Sydney | 45m | FADE_DOWN | RSI_30-50 | `68.3%` | 63 | `8` | `2.15` | `23R` | `-4.0R` | `6.08` |
| 481 | NASDAQ100 | Pre-Market | 15m | FADE_UP | RSI_D>65 | `68.3%` | 63 | `8` | `2.15` | `23R` | `-3.0R` | `6.08` |
| 482 | WTI | London Initial | 30m | FADE_DOWN | BASE | `60.3%` | 749 | `92` | `1.52` | `155R` | `-9.0R` | `6.08` |
| 483 | BRENT | London | 45m | FADE_UP | BtwCloseHigh | `62.7%` | 324 | `40` | `1.68` | `82R` | `-6.0R` | `6.08` |
| 484 | WTI | NY Main | 60m | FADE_UP | RSI_D>65 | `66.3%` | 104 | `13` | `1.97` | `34R` | `-5.0R` | `6.07` |
| 485 | GBPJPY | London | 30m | FADE_DOWN | BtwCloseHigh | `62.8%` | 309 | `38` | `1.69` | `79R` | `-6.0R` | `6.07` |
| 486 | WTI | London Initial | 45m | FADE_DOWN | BASE | `59.9%` | 871 | `107` | `1.50` | `173R` | `-9.0R` | `6.07` |
| 487 | NASDAQ100 | NY Cash | 45m | FADE_UP | BtwCloseHigh | `64.1%` | 198 | `25` | `1.79` | `56R` | `-7.0R` | `6.07` |
| 488 | SP500 | Pre-Market | 45m | FADE_DOWN | RSI_30-50 | `61.7%` | 444 | `55` | `1.61` | `104R` | `-5.0R` | `6.06` |
| 489 | USDJPY | NY | 60m | FADE_UP | BASE | `61.6%` | 461 | `57` | `1.60` | `107R` | `-8.0R` | `6.06` |
| 490 | USDJPY | NY | 45m | FADE_UP | Fri | `67.6%` | 74 | `9` | `2.08` | `26R` | `-3.0R` | `6.06` |
| 491 | AUDUSD | Sydney | 30m | FADE_DOWN | OR_Q4_Wide | `69.8%` | 43 | `5` | `2.31` | `17R` | `-3.0R` | `6.06` |
| 492 | XAGUSD | London | 30m | FADE_UP | BASE | `59.6%` | 966 | `118` | `1.48` | `186R` | `-13.0R` | `6.05` |
| 493 | XAGUSD | London | 60m | FADE_UP | Fri | `63.9%` | 208 | `25` | `1.77` | `58R` | `-6.0R` | `6.05` |
| 494 | AUDUSD | London | 30m | FADE_UP | GapSmall | `60.0%` | 823 | `101` | `1.50` | `165R` | `-18.0R` | `6.05` |
| 495 | XAGUSD | London | 45m | FADE_UP | Fri | `63.8%` | 213 | `26` | `1.77` | `59R` | `-3.0R` | `6.05` |
| 496 | EURUSD | NY | 60m | FADE_UP | GapSmall | `62.4%` | 348 | `43` | `1.66` | `86R` | `-10.0R` | `6.04` |
| 497 | NATGAS | NY | 60m | FADE_UP | BtwCloseHigh | `65.1%` | 146 | `18` | `1.86` | `44R` | `-6.0R` | `6.04` |
| 498 | GBPUSD | NY | 45m | FADE_DOWN | BASE | `60.7%` | 638 | `78` | `1.54` | `136R` | `-13.0R` | `6.04` |
| 499 | BRENT | NY | 60m | FADE_UP | Wed | `64.8%` | 159 | `20` | `1.84` | `47R` | `-9.0R` | `6.04` |
| 500 | SP500 | Pre-Market | 45m | FADE_DOWN | RSI_D<35 | `68.3%` | 60 | `7` | `2.16` | `22R` | `-3.0R` | `6.04` |
| 501 | SP500 | NY Cash | 30m | FADE_DOWN | ATR+10% | `68.3%` | 60 | `7` | `2.16` | `22R` | `-3.0R` | `6.04` |
| 502 | NATGAS | NY | 60m | FADE_UP | OR_Q4_Wide | `65.8%` | 117 | `16` | `1.93` | `37R` | `-5.0R` | `6.03` |
| 503 | EURUSD | London | 30m | FADE_UP | BtwCloseHigh | `62.2%` | 360 | `44` | `1.65` | `88R` | `-8.0R` | `6.03` |
| 504 | EURJPY | London | 30m | FADE_UP | RSI>70 | `66.1%` | 109 | `14` | `1.95` | `35R` | `-6.0R` | `6.03` |
| 505 | EURJPY | London | 30m | FADE_DOWN | BASE | `59.8%` | 864 | `106` | `1.49` | `170R` | `-9.0R` | `6.03` |
| 506 | BRENT | London | 60m | FADE_UP | RSI_50-70 | `61.1%` | 537 | `66` | `1.57` | `119R` | `-10.0R` | `6.03` |
| 507 | SP500 | Pre-Market | 45m | FADE_DOWN | Wed | `65.2%` | 138 | `17` | `1.88` | `42R` | `-5.0R` | `6.03` |
| 508 | WTI | London Initial | 60m | FADE_UP | ATR+10% | `70.0%` | 40 | `5` | `2.33` | `16R` | `-4.0R` | `6.03` |
| 509 | GBPUSD | NY | 45m | FADE_DOWN | AbovePD | `64.6%` | 164 | `20` | `1.83` | `48R` | `-4.0R` | `6.02` |
| 510 | GBPJPY | Tokyo | 60m | FADE_DOWN | OR_Q4_Wide | `63.4%` | 243 | `30` | `1.73` | `65R` | `-5.0R` | `6.02` |
| 511 | WTI | NY Main | 30m | FADE_UP | BtwCloseHigh | `63.4%` | 243 | `30` | `1.73` | `65R` | `-6.0R` | `6.02` |
| 512 | EURJPY | Tokyo | 45m | FADE_UP | BtwCloseHigh | `60.5%` | 661 | `81` | `1.53` | `139R` | `-7.0R` | `6.02` |
| 513 | EURJPY | London | 30m | FADE_UP | OR_Q4_Wide | `63.3%` | 248 | `31` | `1.73` | `66R` | `-6.0R` | `6.02` |
| 514 | WTI | NY Main | 30m | FADE_UP | GapSmall | `60.5%` | 656 | `80` | `1.53` | `138R` | `-9.0R` | `6.02` |
| 515 | XAGUSD | London | 45m | FADE_UP | BtwLowClose | `62.0%` | 379 | `46` | `1.63` | `91R` | `-11.0R` | `6.01` |
| 516 | EURJPY | London | 30m | FADE_UP | Wed | `64.1%` | 192 | `24` | `1.78` | `54R` | `-4.0R` | `6.00` |
| 517 | EURJPY | London | 30m | FADE_UP | RSI_D>65 | `65.6%` | 122 | `16` | `1.90` | `38R` | `-3.0R` | `6.00` |
| 518 | SP500 | Pre-Market | 15m | FADE_UP | RSI_D<35 | `70.3%` | 37 | `5` | `2.36` | `15R` | `-3.0R` | `6.00` |
| 519 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | Thu | `70.3%` | 37 | `5` | `2.36` | `15R` | `-2.0R` | `6.00` |
| 520 | SP500 | NY Cash | 15m | FADE_DOWN | ATR-10% | `70.3%` | 37 | `5` | `2.36` | `15R` | `-2.0R` | `6.00` |
| 521 | EURJPY | London | 60m | FADE_UP | BtwLowClose | `62.8%` | 290 | `35` | `1.69` | `74R` | `-5.0R` | `6.00` |
| 522 | EURUSD | NY | 60m | FADE_UP | RSI_D<35 | `68.4%` | 57 | `8` | `2.17` | `21R` | `-2.0R` | `5.99` |
| 523 | EURJPY | Tokyo | 45m | FADE_DOWN | RSI<30 | `68.4%` | 57 | `7` | `2.17` | `21R` | `-2.0R` | `5.99` |
| 524 | NATGAS | NY | 60m | FADE_DOWN | AbovePD | `65.8%` | 114 | `14` | `1.92` | `36R` | `-5.0R` | `5.99` |
| 525 | XAUUSD | NY | 60m | FADE_DOWN | AbovePD | `66.3%` | 98 | `12` | `1.97` | `32R` | `-3.0R` | `5.99` |
| 526 | SP500 | NY Cash | 45m | FADE_UP | OR_Q4_Wide | `66.0%` | 106 | `13` | `1.94` | `34R` | `-5.0R` | `5.99` |
| 527 | XAGUSD | NY | 30m | FADE_UP | Thu | `65.2%` | 135 | `17` | `1.87` | `41R` | `-10.0R` | `5.99` |
| 528 | EURJPY | Tokyo | 30m | FADE_DOWN | ATR-10% | `70.6%` | 34 | `4` | `2.40` | `14R` | `-3.0R` | `5.97` |
| 529 | SP500 | NY Cash | 30m | FADE_DOWN | BtwLowClose | `63.5%` | 222 | `27` | `1.74` | `60R` | `-6.0R` | `5.97` |
| 530 | NATGAS | NY | 60m | FADE_DOWN | RSI_30-50 | `62.7%` | 292 | `36` | `1.68` | `74R` | `-7.0R` | `5.97` |
| 531 | WTI | London Initial | 30m | FADE_DOWN | GapSmall | `60.2%` | 706 | `86` | `1.51` | `144R` | `-10.0R` | `5.97` |
| 532 | EURJPY | Tokyo | 30m | FADE_DOWN | BtwLowClose | `62.7%` | 287 | `35` | `1.68` | `73R` | `-10.0R` | `5.97` |
| 533 | EURJPY | London | 60m | FADE_UP | BtwCloseHigh | `62.3%` | 329 | `40` | `1.65` | `81R` | `-6.0R` | `5.97` |
| 534 | XAGUSD | London | 30m | FADE_UP | RSI_50-70 | `61.0%` | 523 | `64` | `1.56` | `115R` | `-6.0R` | `5.97` |
| 535 | WTI | London Initial | 45m | FADE_DOWN | RSI_30-50 | `61.0%` | 513 | `63` | `1.56` | `113R` | `-8.0R` | `5.96` |
| 536 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | BASE | `60.0%` | 750 | `92` | `1.50` | `150R` | `-10.0R` | `5.96` |
| 537 | USDJPY | Tokyo | 60m | FADE_UP | ATR-10% | `71.0%` | 31 | `4` | `2.44` | `13R` | `-2.0R` | `5.96` |
| 538 | GBPJPY | London | 60m | FADE_DOWN | ATR-10% | `71.0%` | 31 | `4` | `2.44` | `13R` | `-3.0R` | `5.96` |
| 539 | WTI | London Initial | 45m | FADE_UP | AbovePD+RSI_D>65 | `71.0%` | 31 | `4` | `2.44` | `13R` | `-2.0R` | `5.96` |
| 540 | NATGAS | NY | 60m | FADE_UP | GapSmall | `61.4%` | 448 | `55` | `1.59` | `102R` | `-6.0R` | `5.96` |
| 541 | EURUSD | NY | 60m | FADE_UP | Thu | `66.7%` | 87 | `11` | `2.00` | `29R` | `-5.0R` | `5.95` |
| 542 | BRENT | London | 60m | FADE_DOWN | Mon | `64.2%` | 176 | `22` | `1.79` | `50R` | `-7.0R` | `5.95` |
| 543 | BRENT | NY | 45m | FADE_DOWN | GapSmall | `60.6%` | 589 | `72` | `1.54` | `125R` | `-9.0R` | `5.95` |
| 544 | XAGUSD | London | 45m | FADE_UP | ATR+10% | `68.5%` | 54 | `7` | `2.18` | `20R` | `-2.0R` | `5.95` |
| 545 | BRENT | London | 30m | FADE_DOWN | RSI_D<35 | `68.5%` | 54 | `7` | `2.18` | `20R` | `-3.0R` | `5.95` |
| 546 | GBPJPY | London | 60m | FADE_DOWN | RSI<30 | `66.3%` | 95 | `12` | `1.97` | `31R` | `-5.0R` | `5.95` |
| 547 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | RSI_30-50 | `66.0%` | 103 | `13` | `1.94` | `33R` | `-6.0R` | `5.94` |
| 548 | NASDAQ100 | NY Cash | 60m | FADE_UP | Thu | `66.0%` | 103 | `13` | `1.94` | `33R` | `-3.0R` | `5.94` |
| 549 | SP500 | Pre-Market | 45m | FADE_DOWN | OR_Q4_Wide | `63.4%` | 224 | `28` | `1.73` | `60R` | `-6.0R` | `5.94` |
| 550 | AUDUSD | London | 15m | FADE_UP | BtwLowClose | `63.2%` | 234 | `29` | `1.72` | `62R` | `-11.0R` | `5.94` |
| 551 | EURUSD | London | 60m | FADE_UP | Wed | `63.9%` | 191 | `24` | `1.77` | `53R` | `-6.0R` | `5.93` |
| 552 | WTI | London Initial | 60m | FADE_DOWN | GapSmall | `59.5%` | 884 | `108` | `1.47` | `168R` | `-10.0R` | `5.93` |
| 553 | BRENT | London | 30m | FADE_DOWN | GapSmall | `60.5%` | 612 | `75` | `1.53` | `128R` | `-10.0R` | `5.93` |
| 554 | SP500 | NY Cash | 45m | FADE_UP | AbovePD | `64.3%` | 168 | `21` | `1.80` | `48R` | `-4.0R` | `5.93` |
| 555 | SP500 | NY Cash | 60m | FADE_UP | BtwLowClose | `64.3%` | 168 | `21` | `1.80` | `48R` | `-4.0R` | `5.93` |
| 556 | XAGUSD | London | 15m | FADE_DOWN | BtwCloseHigh | `63.8%` | 196 | `24` | `1.76` | `54R` | `-5.0R` | `5.93` |
| 557 | XAGUSD | London | 15m | FADE_UP | GapSmall | `60.5%` | 588 | `72` | `1.53` | `124R` | `-8.0R` | `5.92` |
| 558 | EURUSD | NY | 60m | FADE_DOWN | Wed | `65.5%` | 116 | `14` | `1.90` | `36R` | `-4.0R` | `5.92` |
| 559 | NATGAS | NY | 60m | FADE_DOWN | OR_Q4_Wide | `65.5%` | 116 | `16` | `1.90` | `36R` | `-6.0R` | `5.92` |
| 560 | WTI | NY Main | 45m | FADE_UP | Mon | `64.5%` | 155 | `19` | `1.82` | `45R` | `-7.0R` | `5.92` |
| 561 | EURUSD | London | 60m | FADE_UP | Thu | `63.5%` | 211 | `26` | `1.74` | `57R` | `-5.0R` | `5.91` |
| 562 | GBPUSD | London | 45m | FADE_DOWN | BASE | `59.1%` | 1003 | `123` | `1.45` | `183R` | `-10.0R` | `5.91` |
| 563 | WTI | London Initial | 60m | FADE_UP | RSI_50-70 | `60.9%` | 516 | `63` | `1.55` | `112R` | `-7.0R` | `5.91` |
| 564 | GBPAUD | London | 45m | FADE_DOWN | BtwLowClose | `61.9%` | 352 | `43` | `1.63` | `84R` | `-11.0R` | `5.91` |
| 565 | XAUUSD | London | 45m | FADE_DOWN | Wed | `63.8%` | 188 | `23` | `1.76` | `52R` | `-4.0R` | `5.90` |
| 566 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | BASE | `60.4%` | 601 | `74` | `1.53` | `125R` | `-13.0R` | `5.89` |
| 567 | WTI | NY Main | 45m | FADE_UP | Fri | `64.6%` | 147 | `18` | `1.83` | `43R` | `-5.0R` | `5.89` |
| 568 | BRENT | London | 15m | FADE_DOWN | RSI_50-70 | `65.3%` | 121 | `15` | `1.88` | `37R` | `-5.0R` | `5.89` |
| 569 | AUDUSD | London | 30m | FADE_UP | Thu | `63.5%` | 203 | `25` | `1.74` | `55R` | `-7.0R` | `5.89` |
| 570 | WTI | London Initial | 60m | FADE_UP | OR_Q4_Wide | `62.9%` | 248 | `32` | `1.70` | `64R` | `-5.0R` | `5.88` |
| 571 | WTI | NY Main | 15m | FADE_UP | RSI_D<35 | `67.1%` | 73 | `9` | `2.04` | `25R` | `-3.0R` | `5.88` |
| 572 | BRENT | London | 15m | FADE_UP | RSI_50-70 | `63.3%` | 218 | `27` | `1.73` | `58R` | `-8.0R` | `5.88` |
| 573 | GBPUSD | London | 45m | FADE_DOWN | GapSmall | `59.2%` | 934 | `114` | `1.45` | `172R` | `-9.0R` | `5.88` |
| 574 | GBPJPY | London | 30m | FADE_UP | RSI>70 | `65.5%` | 113 | `14` | `1.90` | `35R` | `-5.0R` | `5.87` |
| 575 | SP500 | Pre-Market | 15m | FADE_UP | BASE | `61.7%` | 368 | `45` | `1.61` | `86R` | `-8.0R` | `5.87` |
| 576 | XAGUSD | NY | 60m | FADE_UP | RSI_D>65 | `66.7%` | 81 | `10` | `2.00` | `27R` | `-4.0R` | `5.86` |
| 577 | GBPAUD | Sydney | 30m | FADE_UP | BtwLowClose | `68.8%` | 48 | `6` | `2.20` | `18R` | `-3.0R` | `5.86` |
| 578 | USDJPY | Tokyo | 60m | FADE_DOWN | Mon | `63.4%` | 205 | `25` | `1.73` | `55R` | `-8.0R` | `5.85` |
| 579 | BRENT | London | 45m | FADE_DOWN | OR_Q4_Wide | `62.9%` | 240 | `30` | `1.70` | `62R` | `-7.0R` | `5.85` |
| 580 | SP500 | NY Cash | 15m | FADE_DOWN | BtwLowClose | `63.0%` | 235 | `29` | `1.70` | `61R` | `-5.0R` | `5.85` |
| 581 | GBPJPY | London | 15m | FADE_DOWN | Mon | `64.1%` | 167 | `21` | `1.78` | `47R` | `-6.0R` | `5.85` |
| 582 | USDJPY | NY | 60m | FADE_DOWN | BASE | `60.8%` | 497 | `61` | `1.55` | `107R` | `-6.0R` | `5.84` |
| 583 | XAGUSD | London | 30m | FADE_DOWN | RSI_30-50 | `61.2%` | 430 | `53` | `1.57` | `96R` | `-12.0R` | `5.84` |
| 584 | SP500 | NY Cash | 30m | FADE_DOWN | BASE | `59.6%` | 758 | `93` | `1.48` | `146R` | `-8.0R` | `5.84` |
| 585 | WTI | London Initial | 45m | FADE_UP | RSI_30-50 | `62.5%` | 272 | `33` | `1.67` | `68R` | `-5.0R` | `5.84` |
| 586 | SP500 | NY Cash | 15m | FADE_DOWN | GapSmall | `60.3%` | 594 | `73` | `1.52` | `122R` | `-11.0R` | `5.84` |
| 587 | EURUSD | NY | 45m | FADE_UP | BtwLowClose | `63.8%` | 177 | `22` | `1.77` | `49R` | `-6.0R` | `5.83` |
| 588 | XAUUSD | NY | 45m | FADE_UP | GapSmall | `61.5%` | 384 | `47` | `1.59` | `88R` | `-12.0R` | `5.83` |
| 589 | XAGUSD | London | 30m | FADE_UP | GapSmall | `59.3%` | 841 | `103` | `1.46` | `157R` | `-13.0R` | `5.83` |
| 590 | USDJPY | NY | 60m | FADE_DOWN | BelowPD | `65.5%` | 110 | `13` | `1.89` | `34R` | `-4.0R` | `5.83` |
| 591 | XAGUSD | NY | 15m | FADE_UP | BASE | `59.5%` | 783 | `96` | `1.47` | `149R` | `-11.0R` | `5.83` |
| 592 | EURJPY | Tokyo | 30m | FADE_DOWN | BASE | `59.3%` | 864 | `106` | `1.45` | `160R` | `-16.0R` | `5.83` |
| 593 | EURJPY | Tokyo | 30m | FADE_DOWN | GapSmall | `59.3%` | 864 | `106` | `1.45` | `160R` | `-16.0R` | `5.83` |
| 594 | EURUSD | London | 45m | FADE_UP | Wed | `63.6%` | 187 | `23` | `1.75` | `51R` | `-8.0R` | `5.83` |
| 595 | USDJPY | Tokyo | 30m | FADE_UP | Thu | `63.6%` | 187 | `23` | `1.75` | `51R` | `-5.0R` | `5.83` |
| 596 | VIX | NY Cash | 60m | FADE_DOWN | RSI_30-50 | `65.0%` | 123 | `37` | `1.86` | `37R` | `-9.0R` | `5.82` |
| 597 | XAGUSD | London | 45m | FADE_UP | Thu | `63.2%` | 212 | `26` | `1.72` | `56R` | `-5.0R` | `5.82` |
| 598 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | GapSmall | `60.0%` | 633 | `78` | `1.50` | `127R` | `-12.0R` | `5.82` |
| 599 | XAGUSD | London | 45m | FADE_DOWN | GapSmall | `59.4%` | 789 | `97` | `1.47` | `149R` | `-18.0R` | `5.81` |
| 600 | SP500 | Pre-Market | 30m | FADE_UP | ATR+10% | `68.9%` | 45 | `6` | `2.21` | `17R` | `-3.0R` | `5.81` |
| 601 | EURJPY | Tokyo | 30m | FADE_UP | OR_Q4_Wide | `62.5%` | 259 | `32` | `1.67` | `65R` | `-7.0R` | `5.80` |
| 602 | GBPJPY | London | 30m | FADE_DOWN | BASE | `59.1%` | 911 | `111` | `1.44` | `165R` | `-11.0R` | `5.80` |
| 603 | EURJPY | Tokyo | 45m | FADE_DOWN | BASE | `59.0%` | 913 | `112` | `1.44` | `165R` | `-14.0R` | `5.80` |
| 604 | EURJPY | Tokyo | 45m | FADE_DOWN | GapSmall | `59.0%` | 913 | `112` | `1.44` | `165R` | `-14.0R` | `5.80` |
| 605 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | BASE | `63.8%` | 174 | `21` | `1.76` | `48R` | `-8.0R` | `5.80` |
| 606 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | BtwLowClose | `63.8%` | 174 | `21` | `1.76` | `48R` | `-6.0R` | `5.80` |
| 607 | EURJPY | Tokyo | 45m | FADE_UP | RSI_30-50 | `62.3%` | 281 | `34` | `1.65` | `69R` | `-10.0R` | `5.80` |
| 608 | BRENT | London | 60m | FADE_DOWN | OR_Q4_Wide | `62.7%` | 244 | `31` | `1.68` | `62R` | `-8.0R` | `5.80` |
| 609 | XAGUSD | London | 60m | FADE_DOWN | Wed | `63.7%` | 179 | `22` | `1.75` | `49R` | `-6.0R` | `5.79` |
| 610 | BRENT | NY | 15m | FADE_DOWN | BtwCloseHigh | `62.8%` | 239 | `29` | `1.69` | `61R` | `-7.0R` | `5.79` |
| 611 | SP500 | Pre-Market | 45m | FADE_DOWN | RSI_50-70 | `62.8%` | 239 | `29` | `1.69` | `61R` | `-6.0R` | `5.79` |
| 612 | GBPUSD | NY | 30m | FADE_UP | Mon | `64.2%` | 151 | `18` | `1.80` | `43R` | `-6.0R` | `5.79` |
| 613 | GBPJPY | Tokyo | 60m | FADE_UP | Fri | `63.5%` | 189 | `23` | `1.74` | `51R` | `-9.0R` | `5.79` |
| 614 | EURJPY | Tokyo | 60m | FADE_DOWN | Wed | `63.5%` | 189 | `23` | `1.74` | `51R` | `-4.0R` | `5.79` |
| 615 | WTI | NY Main | 60m | FADE_UP | BtwLowClose | `63.5%` | 189 | `23` | `1.74` | `51R` | `-9.0R` | `5.79` |
| 616 | EURJPY | Tokyo | 45m | FADE_UP | RSI_D>65 | `64.7%` | 133 | `18` | `1.83` | `39R` | `-6.0R` | `5.79` |
| 617 | EURJPY | Tokyo | 60m | FADE_DOWN | Mon | `63.2%` | 209 | `26` | `1.71` | `55R` | `-9.0R` | `5.78` |
| 618 | SP500 | NY Cash | 15m | FADE_DOWN | RSI_D>65 | `64.1%` | 156 | `20` | `1.79` | `44R` | `-5.0R` | `5.78` |
| 619 | BRENT | London | 45m | FADE_DOWN | AbovePD | `65.0%` | 120 | `15` | `1.86` | `36R` | `-6.0R` | `5.78` |
| 620 | XAUUSD | London | 60m | FADE_DOWN | GapSmall | `59.2%` | 817 | `100` | `1.45` | `151R` | `-10.0R` | `5.77` |
| 621 | GBPAUD | London | 60m | FADE_DOWN | Tue | `64.0%` | 161 | `20` | `1.78` | `45R` | `-5.0R` | `5.77` |
| 622 | SP500 | NY Cash | 30m | FADE_DOWN | RSI_30-50 | `61.2%` | 392 | `48` | `1.58` | `88R` | `-9.0R` | `5.77` |
| 623 | BRENT | NY | 30m | FADE_DOWN | GapSmall | `59.9%` | 624 | `77` | `1.50` | `124R` | `-6.0R` | `5.77` |
| 624 | VIX | NY Cash | 60m | FADE_UP | Wed | `67.9%` | 56 | `17` | `2.11` | `20R` | `-6.0R` | `5.77` |
| 625 | EURJPY | London | 30m | FADE_UP | AbovePD | `63.7%` | 171 | `21` | `1.76` | `47R` | `-8.0R` | `5.76` |
| 626 | EURJPY | London | 45m | FADE_UP | ATR+10% | `69.0%` | 42 | `5` | `2.23` | `16R` | `-2.0R` | `5.76` |
| 627 | GBPAUD | Sydney | 30m | FADE_UP | RSI_30-50 | `66.7%` | 75 | `9` | `2.00` | `25R` | `-7.0R` | `5.76` |
| 628 | XAGUSD | NY | 45m | FADE_UP | RSI_D>65 | `65.9%` | 91 | `12` | `1.94` | `29R` | `-4.0R` | `5.76` |
| 629 | WTI | London Initial | 45m | SHAKEOUT_UP | OR_Q1_Tight | `65.9%` | 91 | `12` | `1.94` | `29R` | `-5.0R` | `5.76` |
| 630 | BRENT | London | 30m | FADE_UP | AbovePD | `65.9%` | 91 | `11` | `1.94` | `29R` | `-4.0R` | `5.76` |
| 631 | EURJPY | London | 15m | FADE_DOWN | GapSmall | `59.9%` | 621 | `76` | `1.49` | `123R` | `-7.0R` | `5.76` |
| 632 | EURUSD | London | 45m | FADE_UP | Fri | `63.0%` | 211 | `26` | `1.71` | `55R` | `-9.0R` | `5.75` |
| 633 | NATGAS | NY | 45m | FADE_DOWN | RSI_D>65 | `66.3%` | 83 | `11` | `1.96` | `27R` | `-3.0R` | `5.75` |
| 634 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | BtwLowClose | `63.4%` | 191 | `23` | `1.73` | `51R` | `-6.0R` | `5.75` |
| 635 | GBPUSD | NY | 45m | FADE_UP | BtwLowClose | `63.3%` | 196 | `24` | `1.72` | `52R` | `-8.0R` | `5.75` |
| 636 | XAUUSD | London | 60m | FADE_UP | Wed | `63.3%` | 196 | `24` | `1.72` | `52R` | `-6.0R` | `5.75` |
| 637 | AUDUSD | London | 30m | FADE_UP | BtwLowClose | `61.9%` | 302 | `37` | `1.63` | `72R` | `-9.0R` | `5.75` |
| 638 | XAGUSD | London | 60m | FADE_UP | RSI_30-50 | `61.8%` | 319 | `39` | `1.61` | `75R` | `-7.0R` | `5.75` |
| 639 | SP500 | NY Cash | 30m | FADE_UP | GapSmall | `59.9%` | 616 | `76` | `1.49` | `122R` | `-7.0R` | `5.75` |
| 640 | GBPJPY | Tokyo | 30m | FADE_DOWN | BASE | `59.2%` | 804 | `98` | `1.45` | `148R` | `-13.0R` | `5.75` |
| 641 | GBPJPY | Tokyo | 30m | FADE_DOWN | GapSmall | `59.2%` | 804 | `98` | `1.45` | `148R` | `-13.0R` | `5.75` |
| 642 | EURUSD | NY | 60m | FADE_UP | Wed | `64.6%` | 130 | `16` | `1.83` | `38R` | `-3.0R` | `5.74` |
| 643 | WTI | NY Main | 30m | FADE_UP | RSI>70 | `65.4%` | 104 | `13` | `1.89` | `32R` | `-5.0R` | `5.74` |
| 644 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | BtwLowClose | `62.6%` | 238 | `29` | `1.67` | `60R` | `-7.0R` | `5.74` |
| 645 | XAGUSD | NY | 15m | FADE_UP | RSI_50-70 | `61.1%` | 398 | `49` | `1.57` | `88R` | `-6.0R` | `5.73` |
| 646 | NATGAS | NY | 60m | FADE_DOWN | BelowPD | `64.4%` | 135 | `17` | `1.81` | `39R` | `-4.0R` | `5.73` |
| 647 | BRENT | London | 45m | FADE_DOWN | BtwCloseHigh | `61.6%` | 333 | `41` | `1.60` | `77R` | `-6.0R` | `5.73` |
| 648 | WTI | London Initial | 60m | FADE_UP | BASE | `58.8%` | 913 | `112` | `1.43` | `161R` | `-11.0R` | `5.73` |
| 649 | EURJPY | Tokyo | 30m | FADE_UP | BtwCloseHigh | `59.7%` | 643 | `79` | `1.48` | `125R` | `-10.0R` | `5.73` |
| 650 | GBPJPY | London | 60m | FADE_DOWN | OR_Q4_Wide | `63.7%` | 168 | `21` | `1.75` | `46R` | `-5.0R` | `5.72` |
| 651 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | GapSmall | `63.7%` | 168 | `21` | `1.75` | `46R` | `-6.0R` | `5.72` |
| 652 | GBPAUD | London | 60m | FADE_DOWN | BtwLowClose | `61.4%` | 345 | `42` | `1.59` | `79R` | `-9.0R` | `5.72` |
| 653 | WTI | London Initial | 60m | FADE_UP | GapSmall | `58.9%` | 867 | `106` | `1.44` | `155R` | `-11.0R` | `5.72` |
| 654 | XAGUSD | London | 60m | FADE_DOWN | RSI_30-50 | `60.4%` | 507 | `62` | `1.52` | `105R` | `-18.0R` | `5.72` |
| 655 | VIX | NY Cash | 30m | FADE_UP | OR_Q4_Wide | `67.2%` | 64 | `19` | `2.05` | `22R` | `-4.0R` | `5.72` |
| 656 | EURJPY | London | 30m | FADE_DOWN | GapSmall | `59.4%` | 731 | `89` | `1.46` | `137R` | `-10.0R` | `5.72` |
| 657 | BRENT | NY | 30m | FADE_UP | BASE | `59.0%` | 830 | `102` | `1.44` | `150R` | `-19.0R` | `5.72` |
| 658 | SP500 | Pre-Market | 60m | FADE_DOWN | Fri | `64.3%` | 140 | `17` | `1.80` | `40R` | `-7.0R` | `5.72` |
| 659 | WTI | NY Main | 15m | FADE_UP | Mon | `63.4%` | 183 | `22` | `1.73` | `49R` | `-5.0R` | `5.72` |
| 660 | BRENT | London | 60m | FADE_UP | GapSmall | `59.1%` | 823 | `101` | `1.44` | `149R` | `-14.0R` | `5.72` |
| 661 | EURUSD | London | 45m | FADE_DOWN | OR_Q4_Wide | `63.3%` | 188 | `23` | `1.72` | `50R` | `-5.0R` | `5.72` |
| 662 | EURJPY | London | 45m | FADE_UP | Wed | `63.2%` | 193 | `24` | `1.72` | `51R` | `-8.0R` | `5.72` |
| 663 | SP500 | NY Cash | 15m | FADE_DOWN | Mon | `64.8%` | 122 | `15` | `1.84` | `36R` | `-6.0R` | `5.72` |
| 664 | WTI | NY Main | 15m | FADE_UP | BASE | `59.0%` | 848 | `104` | `1.44` | `152R` | `-10.0R` | `5.71` |
| 665 | GBPJPY | London | 45m | FADE_DOWN | RSI<30 | `65.1%` | 109 | `13` | `1.87` | `33R` | `-4.0R` | `5.71` |
| 666 | XAGUSD | London | 45m | FADE_DOWN | RSI_30-50 | `60.4%` | 490 | `60` | `1.53` | `102R` | `-14.0R` | `5.71` |
| 667 | BRENT | London | 15m | FADE_UP | BtwCloseHigh | `64.1%` | 145 | `18` | `1.79` | `41R` | `-6.0R` | `5.71` |
| 668 | USDJPY | Tokyo | 30m | FADE_UP | GapSmall | `58.5%` | 1012 | `124` | `1.41` | `172R` | `-10.0R` | `5.71` |
| 669 | EURUSD | NY | 60m | FADE_DOWN | RSI_30-50 | `62.0%` | 284 | `35` | `1.63` | `68R` | `-12.0R` | `5.70` |
| 670 | GBPUSD | London | 60m | FADE_DOWN | GapSmall | `58.8%` | 884 | `108` | `1.43` | `156R` | `-8.0R` | `5.70` |
| 671 | GBPUSD | NY | 45m | FADE_UP | RSI_30-50 | `62.7%` | 225 | `28` | `1.68` | `57R` | `-7.0R` | `5.70` |
| 672 | GBPJPY | London | 30m | FADE_DOWN | OR_Q4_Wide | `62.7%` | 225 | `28` | `1.68` | `57R` | `-5.0R` | `5.70` |
| 673 | GBPAUD | London | 30m | FADE_DOWN | GapSmall | `59.1%` | 794 | `97` | `1.44` | `144R` | `-11.0R` | `5.69` |
| 674 | BRENT | London | 45m | FADE_DOWN | Thu | `63.7%` | 160 | `20` | `1.76` | `44R` | `-8.0R` | `5.69` |
| 675 | WTI | NY Main | 45m | FADE_UP | BtwCloseHigh | `62.9%` | 210 | `26` | `1.69` | `54R` | `-8.0R` | `5.69` |
| 676 | XAGUSD | London | 15m | FADE_UP | BelowPD | `64.9%` | 114 | `14` | `1.85` | `34R` | `-5.0R` | `5.69` |
| 677 | GBPJPY | Tokyo | 45m | FADE_UP | RSI_50-70 | `59.7%` | 632 | `77` | `1.48` | `122R` | `-12.0R` | `5.69` |
| 678 | NATGAS | NY | 60m | FADE_UP | RSI_50-70 | `62.1%` | 269 | `33` | `1.64` | `65R` | `-6.0R` | `5.69` |
| 679 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | RSI_30-50 | `60.8%` | 411 | `51` | `1.55` | `89R` | `-9.0R` | `5.68` |
| 680 | NATGAS | NY | 45m | FADE_UP | Thu | `63.5%` | 170 | `21` | `1.74` | `46R` | `-7.0R` | `5.68` |
| 681 | NATGAS | NY | 60m | FADE_UP | OR_Q1_Tight | `63.5%` | 170 | `21` | `1.74` | `46R` | `-4.0R` | `5.68` |
| 682 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | RSI_50-70 | `62.4%` | 242 | `30` | `1.66` | `60R` | `-10.0R` | `5.68` |
| 683 | GBPUSD | London | 60m | FADE_DOWN | RSI_30-50 | `60.0%` | 543 | `67` | `1.50` | `109R` | `-9.0R` | `5.68` |
| 684 | GBPJPY | Tokyo | 45m | FADE_UP | BtwCloseHigh | `59.9%` | 571 | `70` | `1.49` | `113R` | `-11.0R` | `5.68` |
| 685 | USDJPY | NY | 45m | FADE_DOWN | BASE | `59.8%` | 585 | `72` | `1.49` | `115R` | `-10.0R` | `5.68` |
| 686 | USDJPY | Tokyo | 60m | FADE_DOWN | RSI_30-50 | `60.0%` | 552 | `68` | `1.50` | `110R` | `-8.0R` | `5.67` |
| 687 | EURJPY | London | 30m | FADE_UP | BtwLowClose | `61.5%` | 322 | `39` | `1.60` | `74R` | `-10.0R` | `5.67` |
| 688 | GBPJPY | Tokyo | 15m | FADE_UP | Thu | `64.7%` | 119 | `15` | `1.83` | `35R` | `-4.0R` | `5.67` |
| 689 | GBPJPY | Tokyo | 30m | FADE_DOWN | RSI_30-50 | `60.4%` | 472 | `58` | `1.52` | `98R` | `-9.0R` | `5.67` |
| 690 | XAGUSD | London | 60m | FADE_DOWN | GapSmall | `59.0%` | 804 | `99` | `1.44` | `144R` | `-14.0R` | `5.66` |
| 691 | GBPUSD | NY | 45m | FADE_DOWN | RSI<30 | `67.2%` | 61 | `8` | `2.05` | `21R` | `-3.0R` | `5.66` |
| 692 | AUDUSD | London | 15m | FADE_UP | GapSmall | `59.6%` | 617 | `76` | `1.48` | `119R` | `-13.0R` | `5.66` |
| 693 | WTI | London Initial | 45m | FADE_UP | RSI_50-70 | `60.2%` | 500 | `61` | `1.51` | `102R` | `-11.0R` | `5.66` |
| 694 | EURUSD | London | 15m | FADE_UP | ATR+10% | `69.4%` | 36 | `5` | `2.27` | `14R` | `-5.0R` | `5.66` |
| 695 | AUDUSD | Sydney | 15m | FADE_DOWN | RSI_30-50 | `68.0%` | 50 | `7` | `2.12` | `18R` | `-5.0R` | `5.65` |
| 696 | NATGAS | NY | 30m | FADE_DOWN | RSI>70 | `68.0%` | 50 | `7` | `2.12` | `18R` | `-2.0R` | `5.65` |
| 697 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | ATR+10% | `68.0%` | 50 | `6` | `2.12` | `18R` | `-3.0R` | `5.65` |
| 698 | XAGUSD | London | 30m | FADE_DOWN | RSI_50-70 | `61.7%` | 295 | `37` | `1.61` | `69R` | `-11.0R` | `5.65` |
| 699 | XAGUSD | London | 30m | FADE_DOWN | Thu | `63.7%` | 157 | `19` | `1.75` | `43R` | `-6.0R` | `5.65` |
| 700 | USDJPY | NY | 60m | FADE_DOWN | OR_Q4_Wide | `66.7%` | 69 | `8` | `2.00` | `23R` | `-4.0R` | `5.65` |
| 701 | BRENT | NY | 30m | FADE_UP | RSI_50-70 | `60.5%` | 443 | `54` | `1.53` | `93R` | `-14.0R` | `5.65` |
| 702 | GBPJPY | Tokyo | 45m | FADE_UP | OR_Q4_Wide | `62.1%` | 256 | `31` | `1.64` | `62R` | `-7.0R` | `5.65` |
| 703 | USDJPY | NY | 60m | FADE_UP | BelowPD | `66.2%` | 77 | `10` | `1.96` | `25R` | `-3.0R` | `5.64` |
| 704 | XAGUSD | NY | 15m | FADE_DOWN | RSI_D<35 | `66.2%` | 77 | `11` | `1.96` | `25R` | `-5.0R` | `5.64` |
| 705 | XAGUSD | NY | 45m | FADE_UP | BelowPD | `66.2%` | 77 | `10` | `1.96` | `25R` | `-5.0R` | `5.64` |
| 706 | EURJPY | Tokyo | 30m | FADE_UP | RSI_D>65 | `64.3%` | 129 | `17` | `1.80` | `37R` | `-6.0R` | `5.64` |
| 707 | EURJPY | London | 15m | FADE_DOWN | BASE | `59.1%` | 743 | `91` | `1.44` | `135R` | `-9.0R` | `5.64` |
| 708 | WTI | NY Main | 60m | FADE_DOWN | GapSmall | `60.1%` | 504 | `62` | `1.51` | `102R` | `-8.0R` | `5.64` |
| 709 | GBPAUD | London | 45m | FADE_DOWN | RSI_D<35 | `65.3%` | 98 | `13` | `1.88` | `30R` | `-3.0R` | `5.64` |
| 710 | GBPJPY | Tokyo | 30m | FADE_UP | RSI_30-50 | `61.9%` | 268 | `33` | `1.63` | `64R` | `-8.0R` | `5.64` |
| 711 | BRENT | NY | 60m | FADE_DOWN | BASE | `59.4%` | 662 | `81` | `1.46` | `124R` | `-12.0R` | `5.63` |
| 712 | USDJPY | Tokyo | 45m | FADE_UP | BASE | `58.2%` | 1025 | `125` | `1.39` | `169R` | `-9.0R` | `5.63` |
| 713 | USDJPY | Tokyo | 45m | FADE_UP | GapSmall | `58.2%` | 1025 | `125` | `1.39` | `169R` | `-9.0R` | `5.63` |
| 714 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | GapSmall | `60.2%` | 492 | `60` | `1.51` | `100R` | `-11.0R` | `5.63` |
| 715 | NATGAS | NY | 45m | FADE_UP | BASE | `59.4%` | 648 | `80` | `1.46` | `122R` | `-16.0R` | `5.63` |
| 716 | BRENT | London | 60m | FADE_UP | BASE | `58.6%` | 891 | `109` | `1.41` | `153R` | `-14.0R` | `5.63` |
| 717 | EURJPY | Tokyo | 30m | FADE_UP | BASE | `58.3%` | 986 | `121` | `1.40` | `164R` | `-14.0R` | `5.62` |
| 718 | EURJPY | Tokyo | 30m | FADE_UP | GapSmall | `58.3%` | 986 | `121` | `1.40` | `164R` | `-14.0R` | `5.62` |
| 719 | WTI | London Initial | 15m | FADE_DOWN | RSI_50-70 | `64.0%` | 139 | `17` | `1.78` | `39R` | `-4.0R` | `5.62` |
| 720 | BRENT | NY | 60m | FADE_DOWN | RSI_30-50 | `61.0%` | 364 | `45` | `1.56` | `80R` | `-11.0R` | `5.62` |
| 721 | XAGUSD | NY | 45m | FADE_UP | Wed | `64.7%` | 116 | `14` | `1.83` | `34R` | `-6.0R` | `5.62` |
| 722 | BRENT | NY | 15m | FADE_DOWN | BASE | `58.9%` | 781 | `96` | `1.43` | `139R` | `-9.0R` | `5.62` |
| 723 | GBPJPY | Tokyo | 45m | FADE_DOWN | RSI_30-50 | `60.1%` | 501 | `62` | `1.50` | `101R` | `-8.0R` | `5.62` |
| 724 | SP500 | NY Cash | 45m | FADE_DOWN | RSI_30-50 | `61.1%` | 352 | `43` | `1.57` | `78R` | `-6.0R` | `5.62` |
| 725 | EURJPY | London | 45m | FADE_UP | BtwLowClose | `61.4%` | 316 | `39` | `1.59` | `72R` | `-10.0R` | `5.62` |
| 726 | WTI | London Initial | 45m | FADE_UP | BtwCloseHigh | `61.4%` | 316 | `39` | `1.59` | `72R` | `-7.0R` | `5.62` |
| 727 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | Fri | `63.9%` | 144 | `18` | `1.77` | `40R` | `-5.0R` | `5.62` |
| 728 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | OR_Q4_Wide | `63.9%` | 144 | `20` | `1.77` | `40R` | `-6.0R` | `5.62` |
| 729 | GBPJPY | Tokyo | 60m | FADE_DOWN | Mon | `62.8%` | 199 | `25` | `1.69` | `51R` | `-6.0R` | `5.62` |
| 730 | XAUUSD | London | 60m | FADE_DOWN | BASE | `58.5%` | 922 | `113` | `1.41` | `156R` | `-10.0R` | `5.62` |
| 731 | BRENT | NY | 15m | FADE_UP | BASE | `59.0%` | 744 | `91` | `1.44` | `134R` | `-14.0R` | `5.62` |
| 732 | GBPUSD | NY | 60m | FADE_DOWN | Fri | `65.6%` | 90 | `11` | `1.90` | `28R` | `-5.0R` | `5.61` |
| 733 | WTI | NY Main | 30m | FADE_DOWN | GapSmall | `59.4%` | 638 | `78` | `1.46` | `120R` | `-7.0R` | `5.61` |
| 734 | NATGAS | NY | 60m | FADE_UP | Thu | `63.8%` | 149 | `18` | `1.76` | `41R` | `-4.0R` | `5.61` |
| 735 | EURJPY | London | 15m | FADE_DOWN | RSI_50-70 | `62.1%` | 248 | `31` | `1.64` | `60R` | `-6.0R` | `5.61` |
| 736 | GBPUSD | London | 30m | FADE_UP | Fri | `63.1%` | 179 | `22` | `1.71` | `47R` | `-5.0R` | `5.61` |
| 737 | XAUUSD | NY | 15m | FADE_UP | Wed | `63.4%` | 164 | `20` | `1.73` | `44R` | `-6.0R` | `5.61` |
| 738 | SP500 | NY Cash | 45m | FADE_UP | RSI_30-50 | `63.2%` | 174 | `22` | `1.72` | `46R` | `-4.0R` | `5.61` |
| 739 | WTI | London Initial | 30m | FADE_DOWN | Tue | `63.3%` | 169 | `21` | `1.73` | `45R` | `-7.0R` | `5.61` |
| 740 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | OR_Q1_Tight | `69.7%` | 33 | `5` | `2.30` | `13R` | `-2.0R` | `5.61` |
| 741 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | Wed | `69.7%` | 33 | `5` | `2.30` | `13R` | `-2.0R` | `5.61` |
| 742 | USDJPY | NY | 60m | FADE_UP | RSI_50-70 | `61.7%` | 277 | `34` | `1.61` | `65R` | `-8.0R` | `5.60` |
| 743 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | RSI_30-50 | `60.6%` | 406 | `50` | `1.54` | `86R` | `-9.0R` | `5.60` |
| 744 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | RSI_D<35 | `68.1%` | 47 | `6` | `2.13` | `17R` | `-2.0R` | `5.59` |
| 745 | XAGUSD | NY | 30m | FADE_DOWN | BASE | `59.3%` | 637 | `78` | `1.46` | `119R` | `-8.0R` | `5.59` |
| 746 | NASDAQ100 | NY Cash | 45m | FADE_UP | RSI>70 | `64.8%` | 108 | `14` | `1.84` | `32R` | `-3.0R` | `5.59` |
| 747 | SP500 | Pre-Market | 45m | FADE_UP | GapSmall | `59.2%` | 683 | `84` | `1.45` | `125R` | `-14.0R` | `5.59` |
| 748 | EURUSD | London | 45m | FADE_UP | AbovePD | `64.1%` | 131 | `16` | `1.79` | `37R` | `-4.0R` | `5.59` |
| 749 | XAGUSD | NY | 60m | FADE_DOWN | OR_Q1_Tight | `64.1%` | 131 | `18` | `1.79` | `37R` | `-4.0R` | `5.59` |
| 750 | WTI | NY Main | 15m | FADE_DOWN | BASE | `58.6%` | 827 | `102` | `1.42` | `143R` | `-12.0R` | `5.59` |
| 751 | EURJPY | Tokyo | 45m | FADE_UP | RSI_D<35 | `66.2%` | 74 | `11` | `1.96` | `24R` | `-4.0R` | `5.59` |
| 752 | GBPJPY | London | 60m | FADE_DOWN | BtwCloseHigh | `61.8%` | 267 | `33` | `1.62` | `63R` | `-5.0R` | `5.59` |
| 753 | AUDUSD | London | 45m | FADE_UP | BtwLowClose | `61.3%` | 320 | `39` | `1.58` | `72R` | `-5.0R` | `5.58` |
| 754 | XAGUSD | London | 60m | FADE_DOWN | BtwCloseHigh | `61.3%` | 320 | `39` | `1.58` | `72R` | `-5.0R` | `5.58` |
| 755 | GBPJPY | Tokyo | 45m | FADE_UP | BtwLowClose | `60.5%` | 408 | `50` | `1.53` | `86R` | `-10.0R` | `5.58` |
| 756 | EURJPY | London | 60m | FADE_DOWN | BASE | `58.5%` | 854 | `104` | `1.41` | `146R` | `-12.0R` | `5.58` |
| 757 | EURJPY | London | 30m | FADE_DOWN | RSI_50-70 | `61.6%` | 279 | `34` | `1.61` | `65R` | `-7.0R` | `5.58` |
| 758 | GBPJPY | London | 30m | FADE_DOWN | GapSmall | `58.7%` | 797 | `97` | `1.42` | `139R` | `-9.0R` | `5.58` |
| 759 | SP500 | Pre-Market | 45m | FADE_UP | BASE | `58.7%` | 797 | `98` | `1.42` | `139R` | `-16.0R` | `5.58` |
| 760 | XAGUSD | London | 15m | FADE_UP | RSI_30-50 | `62.0%` | 245 | `30` | `1.63` | `59R` | `-7.0R` | `5.58` |
| 761 | EURJPY | London | 30m | FADE_UP | Tue | `62.8%` | 191 | `24` | `1.69` | `49R` | `-6.0R` | `5.58` |
| 762 | XAGUSD | London | 15m | FADE_UP | Thu | `63.8%` | 141 | `17` | `1.76` | `39R` | `-6.0R` | `5.57` |
| 763 | WTI | London Initial | 45m | FADE_DOWN | OR_Q1_Tight | `63.8%` | 141 | `18` | `1.76` | `39R` | `-5.0R` | `5.57` |
| 764 | AUDUSD | London | 30m | FADE_UP | AbovePD | `62.9%` | 186 | `23` | `1.70` | `48R` | `-6.0R` | `5.57` |
| 765 | AUDUSD | London | 30m | FADE_UP | BelowPD | `62.9%` | 186 | `23` | `1.70` | `48R` | `-5.0R` | `5.57` |
| 766 | GBPJPY | London | 60m | FADE_UP | Fri | `62.9%` | 186 | `23` | `1.70` | `48R` | `-5.0R` | `5.57` |
| 767 | USDJPY | NY | 60m | FADE_UP | BtwLowClose | `64.6%` | 113 | `14` | `1.82` | `33R` | `-4.0R` | `5.57` |
| 768 | GBPAUD | London | 30m | FADE_DOWN | BASE | `58.2%` | 953 | `117` | `1.39` | `157R` | `-13.0R` | `5.57` |
| 769 | SP500 | Pre-Market | 45m | FADE_DOWN | Mon | `63.7%` | 146 | `18` | `1.75` | `40R` | `-5.0R` | `5.57` |
| 770 | NATGAS | NY | 30m | FADE_DOWN | Fri | `63.6%` | 151 | `19` | `1.75` | `41R` | `-6.0R` | `5.57` |
| 771 | XAGUSD | NY | 45m | FADE_DOWN | BASE | `60.0%` | 485 | `59` | `1.50` | `97R` | `-7.0R` | `5.57` |
| 772 | XAGUSD | NY | 15m | FADE_DOWN | Wed | `63.4%` | 161 | `20` | `1.73` | `43R` | `-4.0R` | `5.57` |
| 773 | EURJPY | London | 45m | FADE_DOWN | BtwCloseHigh | `61.7%` | 269 | `33` | `1.61` | `63R` | `-7.0R` | `5.56` |
| 774 | EURUSD | London | 60m | FADE_UP | RSI_30-50 | `61.6%` | 281 | `34` | `1.60` | `65R` | `-13.0R` | `5.56` |
| 775 | USDJPY | NY | 60m | FADE_DOWN | RSI_30-50 | `61.6%` | 281 | `35` | `1.60` | `65R` | `-6.0R` | `5.56` |
| 776 | NATGAS | NY | 45m | FADE_UP | OR_Q1_Tight | `62.5%` | 208 | `27` | `1.67` | `52R` | `-5.0R` | `5.56` |
| 777 | GBPJPY | Tokyo | 30m | FADE_UP | BtwCloseHigh | `59.7%` | 543 | `66` | `1.48` | `105R` | `-10.0R` | `5.56` |
| 778 | GBPAUD | London | 60m | FADE_DOWN | RSI_30-50 | `59.8%` | 522 | `64` | `1.49` | `102R` | `-9.0R` | `5.56` |
| 779 | BRENT | NY | 30m | FADE_UP | BtwCloseHigh | `61.7%` | 264 | `32` | `1.61` | `62R` | `-9.0R` | `5.56` |
| 780 | GBPUSD | London | 60m | FADE_UP | RSI<30 | `70.0%` | 30 | `4` | `2.33` | `12R` | `-4.0R` | `5.56` |
| 781 | XAGUSD | London | 15m | FADE_DOWN | OR_Q4_Wide | `62.6%` | 203 | `34` | `1.67` | `51R` | `-4.0R` | `5.55` |
| 782 | BRENT | NY | 45m | FADE_DOWN | BASE | `58.8%` | 743 | `91` | `1.43` | `131R` | `-15.0R` | `5.55` |
| 783 | EURJPY | London | 45m | FADE_DOWN | RSI_50-70 | `61.2%` | 312 | `38` | `1.58` | `70R` | `-9.0R` | `5.55` |
| 784 | SP500 | Pre-Market | 30m | FADE_UP | Tue | `64.2%` | 123 | `15` | `1.80` | `35R` | `-4.0R` | `5.55` |
| 785 | GBPJPY | Tokyo | 45m | FADE_DOWN | OR_Q4_Wide | `62.0%` | 242 | `30` | `1.63` | `58R` | `-6.0R` | `5.55` |
| 786 | GBPJPY | London | 45m | FADE_DOWN | OR_Q4_Wide | `62.7%` | 193 | `24` | `1.68` | `49R` | `-8.0R` | `5.54` |
| 787 | NASDAQ100 | NY Cash | 30m | FADE_UP | BASE | `59.0%` | 683 | `84` | `1.44` | `123R` | `-9.0R` | `5.54` |
| 788 | AUDUSD | London | 15m | FADE_UP | BASE | `58.8%` | 747 | `91` | `1.43` | `131R` | `-17.0R` | `5.54` |
| 789 | WTI | NY Main | 15m | FADE_DOWN | GapSmall | `59.3%` | 614 | `75` | `1.46` | `114R` | `-8.0R` | `5.54` |
| 790 | XAGUSD | London | 60m | FADE_DOWN | RSI_50-70 | `61.2%` | 307 | `38` | `1.58` | `69R` | `-8.0R` | `5.54` |
| 791 | EURJPY | Tokyo | 60m | FADE_DOWN | BtwCloseHigh | `59.0%` | 676 | `83` | `1.44` | `122R` | `-13.0R` | `5.54` |
| 792 | EURJPY | Tokyo | 15m | FADE_DOWN | BtwLowClose | `61.8%` | 254 | `31` | `1.62` | `60R` | `-11.0R` | `5.54` |
| 793 | XAGUSD | London | 30m | FADE_DOWN | BtwCloseHigh | `61.8%` | 254 | `31` | `1.62` | `60R` | `-6.0R` | `5.54` |
| 794 | WTI | London Initial | 60m | FADE_DOWN | Fri | `62.8%` | 183 | `22` | `1.69` | `47R` | `-7.0R` | `5.54` |
| 795 | XAGUSD | NY | 30m | FADE_UP | Wed | `63.9%` | 133 | `16` | `1.77` | `37R` | `-5.0R` | `5.53` |
| 796 | EURUSD | London | 15m | FADE_UP | GapSmall | `58.8%` | 742 | `91` | `1.42` | `130R` | `-12.0R` | `5.53` |
| 797 | XAUUSD | London | 60m | FADE_DOWN | RSI_50-70 | `61.1%` | 314 | `38` | `1.57` | `70R` | `-9.0R` | `5.53` |
| 798 | EURJPY | London | 30m | FADE_UP | RSI_50-70 | `59.7%` | 528 | `65` | `1.48` | `102R` | `-11.0R` | `5.53` |
| 799 | EURJPY | Tokyo | 15m | FADE_DOWN | Fri | `63.8%` | 138 | `17` | `1.76` | `38R` | `-6.0R` | `5.53` |
| 800 | BRENT | London | 60m | FADE_DOWN | OR_Q1_Tight | `63.0%` | 173 | `21` | `1.70` | `45R` | `-6.0R` | `5.53` |
| 801 | BRENT | NY | 30m | FADE_UP | Wed | `63.0%` | 173 | `21` | `1.70` | `45R` | `-8.0R` | `5.53` |
| 802 | XAUUSD | London | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `68.2%` | 44 | `6` | `2.14` | `16R` | `-4.0R` | `5.53` |
| 803 | GBPJPY | London | 30m | FADE_DOWN | RSI_30-50 | `60.0%` | 465 | `57` | `1.50` | `93R` | `-8.0R` | `5.53` |
| 804 | BRENT | London | 60m | FADE_UP | Fri | `63.1%` | 168 | `21` | `1.71` | `44R` | `-5.0R` | `5.53` |
| 805 | EURUSD | NY | 30m | FADE_UP | Thu | `63.6%` | 143 | `18` | `1.75` | `39R` | `-5.0R` | `5.53` |
| 806 | VIX | NY Cash | 30m | FADE_DOWN | BASE | `61.7%` | 261 | `76` | `1.61` | `61R` | `-5.0R` | `5.53` |
| 807 | EURJPY | Tokyo | 15m | FADE_DOWN | BASE | `58.7%` | 753 | `92` | `1.42` | `131R` | `-14.0R` | `5.53` |
| 808 | EURJPY | Tokyo | 15m | FADE_DOWN | GapSmall | `58.7%` | 753 | `92` | `1.42` | `131R` | `-14.0R` | `5.53` |
| 809 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | BASE | `58.7%` | 753 | `92` | `1.42` | `131R` | `-12.0R` | `5.53` |
| 810 | XAUUSD | London | 60m | FADE_DOWN | BtwCloseHigh | `61.1%` | 321 | `39` | `1.57` | `71R` | `-10.0R` | `5.53` |
| 811 | WTI | NY Main | 15m | FADE_DOWN | Wed | `63.2%` | 163 | `20` | `1.72` | `43R` | `-5.0R` | `5.53` |
| 812 | BRENT | London | 30m | FADE_UP | BASE | `59.0%` | 673 | `83` | `1.44` | `121R` | `-9.0R` | `5.53` |
| 813 | EURUSD | London | 30m | FADE_UP | Tue | `62.4%` | 205 | `25` | `1.66` | `51R` | `-6.0R` | `5.53` |
| 814 | WTI | NY Main | 45m | FADE_DOWN | OR_Q4_Wide | `63.5%` | 148 | `19` | `1.74` | `40R` | `-3.0R` | `5.52` |
| 815 | WTI | NY Main | 45m | FADE_UP | BelowPD | `63.4%` | 153 | `19` | `1.73` | `41R` | `-4.0R` | `5.52` |
| 816 | BRENT | NY | 45m | FADE_DOWN | OR_Q4_Wide | `63.4%` | 153 | `19` | `1.73` | `41R` | `-5.0R` | `5.52` |
| 817 | NASDAQ100 | NY Cash | 45m | FADE_UP | BtwLowClose | `63.4%` | 153 | `19` | `1.73` | `41R` | `-4.0R` | `5.52` |
| 818 | EURUSD | NY | 45m | FADE_UP | RSI_D<35 | `66.7%` | 63 | `9` | `2.00` | `21R` | `-5.0R` | `5.52` |
| 819 | EURJPY | London | 15m | FADE_DOWN | RSI_D<35 | `66.7%` | 63 | `9` | `2.00` | `21R` | `-3.0R` | `5.52` |
| 820 | GBPJPY | Tokyo | 30m | FADE_UP | BtwLowClose | `60.7%` | 359 | `44` | `1.55` | `77R` | `-7.0R` | `5.52` |
| 821 | WTI | London Initial | 45m | FADE_DOWN | OR_Q4_Wide | `61.9%` | 244 | `31` | `1.62` | `58R` | `-8.0R` | `5.52` |
| 822 | GBPJPY | London | 45m | FADE_DOWN | GapSmall | `58.6%` | 789 | `96` | `1.41` | `135R` | `-12.0R` | `5.52` |
| 823 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | BtwLowClose | `61.9%` | 239 | `29` | `1.63` | `57R` | `-9.0R` | `5.52` |
| 824 | USDJPY | Tokyo | 45m | FADE_UP | Thu | `62.6%` | 195 | `24` | `1.67` | `49R` | `-3.0R` | `5.51` |
| 825 | EURJPY | London | 45m | FADE_DOWN | BASE | `58.3%` | 868 | `106` | `1.40` | `144R` | `-12.0R` | `5.51` |
| 826 | EURUSD | NY | 60m | FADE_UP | BelowPD | `64.3%` | 115 | `14` | `1.80` | `33R` | `-5.0R` | `5.51` |
| 827 | VIX | NY Cash | 30m | FADE_DOWN | GapSmall | `62.2%` | 217 | `64` | `1.65` | `53R` | `-5.0R` | `5.51` |
| 828 | GBPAUD | London | 45m | FADE_DOWN | Thu | `62.6%` | 190 | `23` | `1.68` | `48R` | `-6.0R` | `5.51` |
| 829 | NATGAS | NY | 60m | FADE_UP | RSI_30-50 | `62.6%` | 190 | `23` | `1.68` | `48R` | `-6.0R` | `5.51` |
| 830 | SP500 | NY Cash | 45m | FADE_UP | OR_Q1_Tight | `62.6%` | 190 | `24` | `1.68` | `48R` | `-5.0R` | `5.51` |
| 831 | AUDUSD | London | 30m | FADE_DOWN | GapSmall | `58.7%` | 736 | `90` | `1.42` | `128R` | `-12.0R` | `5.51` |
| 832 | XAUUSD | NY | 45m | FADE_UP | BASE | `59.6%` | 527 | `64` | `1.47` | `101R` | `-10.0R` | `5.50` |
| 833 | WTI | London Initial | 60m | FADE_UP | BtwCloseHigh | `60.9%` | 330 | `41` | `1.56` | `72R` | `-6.0R` | `5.50` |
| 834 | EURJPY | Tokyo | 15m | FADE_UP | BtwCloseHigh | `59.6%` | 520 | `64` | `1.48` | `100R` | `-9.0R` | `5.50` |
| 835 | EURUSD | London | 45m | FADE_UP | Thu | `62.3%` | 212 | `26` | `1.65` | `52R` | `-5.0R` | `5.50` |
| 836 | AUDUSD | London | 30m | FADE_DOWN | BASE | `58.1%` | 910 | `111` | `1.39` | `148R` | `-13.0R` | `5.50` |
| 837 | EURUSD | London | 45m | FADE_UP | Tue | `62.8%` | 180 | `22` | `1.69` | `46R` | `-7.0R` | `5.50` |
| 838 | WTI | NY Main | 15m | FADE_DOWN | RSI_50-70 | `61.2%` | 294 | `37` | `1.58` | `66R` | `-6.0R` | `5.49` |
| 839 | AUDUSD | London | 30m | FADE_UP | RSI_30-50 | `60.8%` | 344 | `43` | `1.55` | `74R` | `-6.0R` | `5.49` |
| 840 | GBPUSD | NY | 60m | FADE_UP | BtwCloseHigh | `64.0%` | 125 | `15` | `1.78` | `35R` | `-6.0R` | `5.49` |
| 841 | BRENT | NY | 60m | FADE_DOWN | OR_Q4_Wide | `64.0%` | 125 | `16` | `1.78` | `35R` | `-3.0R` | `5.49` |
| 842 | SP500 | NY Cash | 45m | FADE_UP | Tue | `64.0%` | 125 | `15` | `1.78` | `35R` | `-7.0R` | `5.49` |
| 843 | XAUUSD | London | 45m | FADE_UP | OR_Q4_Wide | `61.8%` | 241 | `37` | `1.62` | `57R` | `-8.0R` | `5.49` |
| 844 | EURUSD | NY | 45m | FADE_UP | RSI_30-50 | `62.1%` | 224 | `27` | `1.64` | `54R` | `-5.0R` | `5.49` |
| 845 | XAGUSD | London | 30m | FADE_DOWN | BtwLowClose | `61.1%` | 301 | `37` | `1.57` | `67R` | `-10.0R` | `5.49` |
| 846 | BRENT | London | 30m | FADE_DOWN | AbovePD | `64.7%` | 102 | `13` | `1.83` | `30R` | `-6.0R` | `5.49` |
| 847 | GBPAUD | London | 30m | FADE_DOWN | RSI_30-50 | `59.6%` | 517 | `63` | `1.47` | `99R` | `-9.0R` | `5.49` |
| 848 | BRENT | NY | 45m | FADE_DOWN | RSI_50-70 | `61.5%` | 265 | `33` | `1.60` | `61R` | `-10.0R` | `5.48` |
| 849 | WTI | London Initial | 45m | FADE_DOWN | RSI_D>65 | `63.7%` | 135 | `17` | `1.76` | `37R` | `-5.0R` | `5.48` |
| 850 | NATGAS | NY | 45m | FADE_DOWN | AbovePD | `63.7%` | 135 | `17` | `1.76` | `37R` | `-5.0R` | `5.48` |
| 851 | EURUSD | NY | 45m | FADE_DOWN | RSI_30-50 | `60.9%` | 320 | `39` | `1.56` | `70R` | `-13.0R` | `5.48` |
| 852 | WTI | London Initial | 30m | FADE_DOWN | OR_Q1_Tight | `65.8%` | 76 | `10` | `1.92` | `24R` | `-8.0R` | `5.48` |
| 853 | EURJPY | London | 30m | FADE_DOWN | RSI_30-50 | `59.8%` | 468 | `57` | `1.49` | `92R` | `-7.0R` | `5.48` |
| 854 | GBPJPY | Tokyo | 60m | FADE_DOWN | ATR-10% | `67.3%` | 52 | `7` | `2.06` | `18R` | `-4.0R` | `5.48` |
| 855 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | RSI_50-70 | `67.3%` | 52 | `6` | `2.06` | `18R` | `-4.0R` | `5.48` |
| 856 | XAGUSD | NY | 45m | FADE_DOWN | BelowPD | `65.2%` | 89 | `11` | `1.87` | `27R` | `-4.0R` | `5.47` |
| 857 | BRENT | NY | 15m | FADE_DOWN | GapSmall | `59.2%` | 588 | `72` | `1.45` | `108R` | `-9.0R` | `5.47` |
| 858 | GBPAUD | Sydney | 15m | FADE_UP | GapSmall | `64.5%` | 107 | `13` | `1.82` | `31R` | `-6.0R` | `5.47` |
| 859 | USDJPY | NY | 45m | FADE_UP | BASE | `59.3%` | 558 | `68` | `1.46` | `104R` | `-12.0R` | `5.47` |
| 860 | GBPAUD | London | 45m | FADE_DOWN | BtwCloseHigh | `60.9%` | 322 | `40` | `1.56` | `70R` | `-7.0R` | `5.47` |
| 861 | EURUSD | London | 45m | FADE_DOWN | Mon | `62.6%` | 182 | `23` | `1.68` | `46R` | `-7.0R` | `5.46` |
| 862 | BRENT | London | 45m | FADE_DOWN | Tue | `62.6%` | 182 | `22` | `1.68` | `46R` | `-7.0R` | `5.46` |
| 863 | XAGUSD | London | 15m | FADE_DOWN | RSI<30 | `68.3%` | 41 | `5` | `2.15` | `15R` | `-3.0R` | `5.46` |
| 864 | WTI | London Initial | 45m | FADE_UP | ATR+10% | `68.3%` | 41 | `5` | `2.15` | `15R` | `-5.0R` | `5.46` |
| 865 | SP500 | Pre-Market | 45m | FADE_DOWN | ATR-10% | `68.3%` | 41 | `5` | `2.15` | `15R` | `-3.0R` | `5.46` |
| 866 | VIX | NY Cash | 60m | FADE_UP | OR_Q4_Wide | `68.3%` | 41 | `13` | `2.15` | `15R` | `-2.0R` | `5.46` |
| 867 | VIX | NY Cash | 60m | FADE_DOWN | Wed | `68.3%` | 41 | `12` | `2.15` | `15R` | `-3.0R` | `5.46` |
| 868 | EURJPY | Tokyo | 45m | FADE_UP | RSI_50-70 | `58.9%` | 654 | `80` | `1.43` | `116R` | `-10.0R` | `5.46` |
| 869 | USDJPY | Tokyo | 45m | FADE_DOWN | Mon | `62.3%` | 204 | `25` | `1.65` | `50R` | `-5.0R` | `5.46` |
| 870 | AUDUSD | Sydney | 30m | FADE_DOWN | RSI_30-50 | `66.7%` | 60 | `7` | `2.00` | `20R` | `-3.0R` | `5.46` |
| 871 | USDJPY | Tokyo | 30m | FADE_UP | BtwCloseHigh | `58.8%` | 665 | `82` | `1.43` | `117R` | `-9.0R` | `5.45` |
| 872 | USDJPY | Tokyo | 15m | FADE_UP | Thu | `62.9%` | 167 | `21` | `1.69` | `43R` | `-10.0R` | `5.45` |
| 873 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | BASE | `62.4%` | 194 | `24` | `1.66` | `48R` | `-9.0R` | `5.45` |
| 874 | USDJPY | NY | 45m | FADE_DOWN | BelowPD | `63.9%` | 122 | `15` | `1.77` | `34R` | `-5.0R` | `5.44` |
| 875 | NASDAQ100 | Pre-Market | 30m | FADE_UP | Tue | `63.9%` | 122 | `15` | `1.77` | `34R` | `-6.0R` | `5.44` |
| 876 | XAGUSD | London | 60m | FADE_DOWN | RSI_D>65 | `63.8%` | 127 | `16` | `1.76` | `35R` | `-6.0R` | `5.44` |
| 877 | WTI | NY Main | 60m | FADE_DOWN | Mon | `63.8%` | 127 | `16` | `1.76` | `35R` | `-5.0R` | `5.44` |
| 878 | SP500 | NY Cash | 45m | FADE_UP | Mon | `63.8%` | 127 | `16` | `1.76` | `35R` | `-7.0R` | `5.44` |
| 879 | SP500 | NY Cash | 45m | FADE_DOWN | OR_Q1_Tight | `63.2%` | 152 | `19` | `1.71` | `40R` | `-6.0R` | `5.44` |
| 880 | EURUSD | London | 60m | FADE_UP | Fri | `62.4%` | 189 | `23` | `1.66` | `47R` | `-6.0R` | `5.44` |
| 881 | XAGUSD | London | 60m | FADE_DOWN | OR_Q4_Wide | `62.4%` | 189 | `29` | `1.66` | `47R` | `-9.0R` | `5.44` |
| 882 | WTI | NY Main | 15m | MOMENTUM_DOWN | ATR+10% | `60.9%` | 46 | `6` | `2.33` | `24R` | `-3.0R` | `5.44` |
| 883 | VIX | NY Cash | 60m | MOMENTUM_UP | Thu | `60.9%` | 46 | `14` | `2.33` | `24R` | `-3.0R` | `5.44` |
| 884 | EURJPY | London | 15m | FADE_DOWN | BelowPD | `63.6%` | 132 | `16` | `1.75` | `36R` | `-6.0R` | `5.44` |
| 885 | XAGUSD | London | 30m | FADE_DOWN | RSI_D>65 | `63.6%` | 132 | `16` | `1.75` | `36R` | `-5.0R` | `5.44` |
| 886 | WTI | NY Main | 60m | FADE_UP | BelowPD | `63.6%` | 132 | `16` | `1.75` | `36R` | `-7.0R` | `5.44` |
| 887 | XAGUSD | NY | 30m | FADE_UP | Tue | `63.5%` | 137 | `17` | `1.74` | `37R` | `-7.0R` | `5.44` |
| 888 | USDJPY | Tokyo | 45m | FADE_UP | BtwCloseHigh | `58.7%` | 664 | `81` | `1.42` | `116R` | `-10.0R` | `5.43` |
| 889 | GBPAUD | London | 60m | FADE_DOWN | RSI<30 | `64.6%` | 99 | `13` | `1.83` | `29R` | `-7.0R` | `5.43` |
| 890 | EURJPY | Tokyo | 45m | FADE_DOWN | RSI_30-50 | `59.4%` | 508 | `62` | `1.47` | `96R` | `-13.0R` | `5.43` |
| 891 | EURUSD | NY | 45m | FADE_DOWN | GapSmall | `60.2%` | 387 | `48` | `1.51` | `79R` | `-9.0R` | `5.43` |
| 892 | XAUUSD | London | 60m | FADE_DOWN | Fri | `62.6%` | 174 | `21` | `1.68` | `44R` | `-5.0R` | `5.42` |
| 893 | EURJPY | Tokyo | 30m | FADE_DOWN | RSI_30-50 | `59.5%` | 496 | `61` | `1.47` | `94R` | `-9.0R` | `5.42` |
| 894 | EURUSD | London | 30m | FADE_UP | RSI_D>65 | `65.1%` | 86 | `11` | `1.87` | `26R` | `-4.0R` | `5.41` |
| 895 | EURJPY | London | 30m | FADE_DOWN | Mon | `62.7%` | 169 | `21` | `1.68` | `43R` | `-5.0R` | `5.41` |
| 896 | GBPJPY | Tokyo | 45m | FADE_UP | OR_Q1_Tight | `62.3%` | 191 | `24` | `1.65` | `47R` | `-5.0R` | `5.41` |
| 897 | NATGAS | NY | 45m | FADE_DOWN | BtwLowClose | `62.3%` | 191 | `24` | `1.65` | `47R` | `-8.0R` | `5.41` |
| 898 | SP500 | NY Cash | 60m | FADE_UP | Fri | `64.2%` | 109 | `14` | `1.79` | `31R` | `-5.0R` | `5.41` |
| 899 | BRENT | NY | 15m | FADE_DOWN | RSI_50-70 | `61.2%` | 273 | `34` | `1.58` | `61R` | `-9.0R` | `5.41` |
| 900 | GBPUSD | London | 15m | SHAKEOUT_DOWN | OR_Q1_Tight | `67.3%` | 49 | `7` | `2.06` | `17R` | `-3.0R` | `5.41` |
| 901 | BRENT | London | 15m | FADE_UP | AbovePD | `67.3%` | 49 | `6` | `2.06` | `17R` | `-2.0R` | `5.41` |
| 902 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | Tue | `67.3%` | 49 | `7` | `2.06` | `17R` | `-2.0R` | `5.41` |
| 903 | BRENT | NY | 15m | FADE_UP | RSI_50-70 | `60.2%` | 384 | `47` | `1.51` | `78R` | `-7.0R` | `5.40` |
| 904 | XAGUSD | London | 45m | FADE_DOWN | RSI_50-70 | `60.8%` | 311 | `38` | `1.55` | `67R` | `-9.0R` | `5.40` |
| 905 | SP500 | NY Cash | 45m | FADE_UP | BtwLowClose | `62.4%` | 186 | `23` | `1.66` | `46R` | `-8.0R` | `5.40` |
| 906 | BRENT | London | 30m | FADE_UP | RSI_D>65 | `64.0%` | 114 | `14` | `1.78` | `32R` | `-3.0R` | `5.40` |
| 907 | SP500 | NY Cash | 30m | FADE_UP | OR_Q4_Wide | `63.0%` | 154 | `19` | `1.70` | `40R` | `-4.0R` | `5.40` |
| 908 | SP500 | NY Cash | 30m | FADE_DOWN | OR_Q1_Tight | `63.0%` | 154 | `19` | `1.70` | `40R` | `-5.0R` | `5.40` |
| 909 | GBPUSD | London | 30m | FADE_DOWN | RSI_30-50 | `59.6%` | 456 | `56` | `1.48` | `88R` | `-10.0R` | `5.40` |
| 910 | XAUUSD | NY | 60m | FADE_DOWN | Fri | `66.2%` | 65 | `8` | `1.95` | `21R` | `-3.0R` | `5.40` |
| 911 | SP500 | NY Cash | 60m | FADE_DOWN | GapSmall | `59.7%` | 449 | `55` | `1.48` | `87R` | `-12.0R` | `5.40` |
| 912 | AUDUSD | London | 60m | FADE_UP | OR_Q4_Wide | `62.1%` | 203 | `25` | `1.64` | `49R` | `-5.0R` | `5.40` |
| 913 | BRENT | London | 60m | FADE_UP | AbovePD | `63.9%` | 119 | `15` | `1.77` | `33R` | `-4.0R` | `5.39` |
| 914 | EURUSD | London | 45m | FADE_UP | ATR-10% | `68.4%` | 38 | `5` | `2.17` | `14R` | `-4.0R` | `5.39` |
| 915 | USDJPY | Tokyo | 30m | FADE_UP | ATR-10% | `68.4%` | 38 | `5` | `2.17` | `14R` | `-2.0R` | `5.39` |
| 916 | USDJPY | Tokyo | 45m | FADE_DOWN | ATR-10% | `68.4%` | 38 | `5` | `2.17` | `14R` | `-5.0R` | `5.39` |
| 917 | XAGUSD | London | 30m | FADE_DOWN | AbovePD | `63.7%` | 124 | `15` | `1.76` | `34R` | `-5.0R` | `5.39` |
| 918 | GBPUSD | NY | 30m | FADE_UP | Thu | `63.3%` | 139 | `17` | `1.73` | `37R` | `-4.0R` | `5.39` |
| 919 | GBPUSD | London | 45m | FADE_DOWN | BelowPD | `63.6%` | 129 | `16` | `1.74` | `35R` | `-5.0R` | `5.39` |
| 920 | BRENT | NY | 15m | FADE_DOWN | BelowPD | `63.6%` | 129 | `16` | `1.74` | `35R` | `-6.0R` | `5.39` |
| 921 | XAGUSD | London | 60m | FADE_UP | Thu | `61.9%` | 215 | `26` | `1.62` | `51R` | `-5.0R` | `5.39` |
| 922 | GBPJPY | Tokyo | 60m | FADE_UP | BASE | `57.6%` | 992 | `121` | `1.36` | `150R` | `-13.0R` | `5.39` |
| 923 | GBPJPY | Tokyo | 60m | FADE_UP | GapSmall | `57.6%` | 992 | `121` | `1.36` | `150R` | `-13.0R` | `5.39` |
| 924 | EURUSD | London | 60m | FADE_UP | Tue | `62.5%` | 176 | `22` | `1.67` | `44R` | `-5.0R` | `5.39` |
| 925 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | Tue | `65.4%` | 78 | `10` | `1.89` | `24R` | `-4.0R` | `5.38` |
| 926 | EURUSD | NY | 60m | FADE_UP | RSI_30-50 | `62.6%` | 171 | `21` | `1.67` | `43R` | `-5.0R` | `5.38` |
| 927 | GBPJPY | Tokyo | 45m | FADE_UP | RSI_30-50 | `61.1%` | 270 | `33` | `1.57` | `60R` | `-8.0R` | `5.38` |
| 928 | EURJPY | Tokyo | 60m | FADE_UP | BtwCloseHigh | `58.8%` | 609 | `75` | `1.43` | `107R` | `-12.0R` | `5.38` |
| 929 | XAGUSD | London | 30m | FADE_UP | AbovePD | `62.7%` | 166 | `21` | `1.68` | `42R` | `-6.0R` | `5.37` |
| 930 | BRENT | NY | 45m | FADE_UP | BtwCloseHigh | `61.4%` | 246 | `30` | `1.59` | `56R` | `-8.0R` | `5.37` |
| 931 | EURUSD | London | 15m | FADE_UP | BASE | `58.1%` | 792 | `97` | `1.39` | `128R` | `-11.0R` | `5.37` |
| 932 | GBPUSD | London | 30m | FADE_DOWN | GapSmall | `57.7%` | 904 | `111` | `1.37` | `140R` | `-16.0R` | `5.37` |
| 933 | WTI | London Initial | 30m | FADE_DOWN | RSI_30-50 | `59.6%` | 441 | `54` | `1.48` | `85R` | `-10.0R` | `5.37` |
| 934 | BRENT | NY | 30m | FADE_DOWN | BASE | `58.0%` | 814 | `100` | `1.38` | `130R` | `-11.0R` | `5.36` |
| 935 | GBPUSD | London | 15m | FADE_DOWN | RSI_D<35 | `64.4%` | 101 | `14` | `1.81` | `29R` | `-4.0R` | `5.36` |
| 936 | WTI | NY Main | 15m | FADE_UP | BtwCloseHigh | `61.4%` | 241 | `30` | `1.59` | `55R` | `-7.0R` | `5.36` |
| 937 | EURJPY | London | 15m | FADE_UP | Tue | `62.8%` | 156 | `19` | `1.69` | `40R` | `-9.0R` | `5.36` |
| 938 | BRENT | NY | 15m | FADE_DOWN | Wed | `62.8%` | 156 | `19` | `1.69` | `40R` | `-5.0R` | `5.36` |
| 939 | XAGUSD | London | 30m | FADE_UP | Thu | `62.0%` | 200 | `25` | `1.63` | `48R` | `-6.0R` | `5.36` |
| 940 | BRENT | NY | 15m | FADE_UP | GapSmall | `59.0%` | 558 | `69` | `1.44` | `100R` | `-12.0R` | `5.36` |
| 941 | XAGUSD | London | 15m | FADE_DOWN | OR_Q1_Tight | `64.2%` | 106 | `51` | `1.79` | `30R` | `-6.0R` | `5.35` |
| 942 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | Mon | `64.2%` | 106 | `13` | `1.79` | `30R` | `-6.0R` | `5.35` |
| 943 | XAGUSD | London | 60m | FADE_UP | RSI_D<35 | `65.1%` | 83 | `11` | `1.86` | `25R` | `-5.0R` | `5.35` |
| 944 | GBPUSD | London | 45m | FADE_DOWN | RSI_30-50 | `59.2%` | 512 | `63` | `1.45` | `94R` | `-10.0R` | `5.35` |
| 945 | EURUSD | NY | 60m | FADE_DOWN | Mon | `64.0%` | 111 | `14` | `1.77` | `31R` | `-6.0R` | `5.35` |
| 946 | XAUUSD | NY | 45m | FADE_UP | Mon | `64.0%` | 111 | `14` | `1.77` | `31R` | `-5.0R` | `5.35` |
| 947 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | Fri | `63.1%` | 141 | `18` | `1.71` | `37R` | `-6.0R` | `5.35` |
| 948 | BRENT | NY | 30m | FADE_DOWN | BtwCloseHigh | `61.0%` | 267 | `33` | `1.57` | `59R` | `-8.0R` | `5.35` |
| 949 | GBPJPY | London | 30m | FADE_DOWN | Mon | `62.4%` | 173 | `21` | `1.66` | `43R` | `-5.0R` | `5.35` |
| 950 | NASDAQ100 | Pre-Market | 60m | FADE_UP | Tue | `62.4%` | 173 | `21` | `1.66` | `43R` | `-8.0R` | `5.35` |
| 951 | WTI | London Initial | 45m | FADE_UP | RSI_D>65 | `63.2%` | 136 | `17` | `1.72` | `36R` | `-5.0R` | `5.34` |
| 952 | SP500 | Pre-Market | 60m | FADE_DOWN | Wed | `63.2%` | 136 | `17` | `1.72` | `36R` | `-6.0R` | `5.34` |
| 953 | GBPAUD | London | 60m | FADE_UP | OR_Q4_Wide | `62.1%` | 190 | `24` | `1.64` | `46R` | `-6.0R` | `5.34` |
| 954 | GBPUSD | NY | 60m | FADE_UP | Wed | `63.5%` | 126 | `15` | `1.74` | `34R` | `-8.0R` | `5.34` |
| 955 | XAUUSD | NY | 45m | FADE_DOWN | Wed | `63.5%` | 126 | `16` | `1.74` | `34R` | `-6.0R` | `5.34` |
| 956 | WTI | NY Main | 60m | FADE_DOWN | BASE | `58.5%` | 655 | `80` | `1.41` | `111R` | `-14.0R` | `5.34` |
| 957 | BRENT | NY | 45m | FADE_UP | Thu | `62.5%` | 168 | `21` | `1.67` | `42R` | `-6.0R` | `5.34` |
| 958 | AUDUSD | London | 15m | FADE_UP | RSI_50-70 | `59.8%` | 396 | `49` | `1.49` | `78R` | `-11.0R` | `5.34` |
| 959 | XAGUSD | NY | 60m | FADE_DOWN | BASE | `59.9%` | 382 | `47` | `1.50` | `76R` | `-8.0R` | `5.33` |
| 960 | AUDUSD | London | 60m | FADE_UP | BtwLowClose | `60.6%` | 307 | `38` | `1.54` | `65R` | `-6.0R` | `5.33` |
| 961 | WTI | NY Main | 30m | FADE_DOWN | RSI_50-70 | `60.6%` | 307 | `38` | `1.54` | `65R` | `-10.0R` | `5.33` |
| 962 | NATGAS | NY | 30m | FADE_UP | BtwCloseHigh | `61.9%` | 202 | `25` | `1.62` | `48R` | `-8.0R` | `5.33` |
| 963 | EURUSD | London | 45m | FADE_UP | RSI_D>65 | `64.8%` | 88 | `11` | `1.84` | `26R` | `-4.0R` | `5.33` |
| 964 | GBPUSD | NY | 45m | FADE_UP | OR_Q4_Wide | `64.8%` | 88 | `11` | `1.84` | `26R` | `-7.0R` | `5.33` |
| 965 | AUDUSD | London | 45m | FADE_DOWN | Mon | `62.2%` | 185 | `23` | `1.64` | `45R` | `-6.0R` | `5.33` |
| 966 | EURJPY | London | 60m | FADE_UP | Fri | `62.2%` | 185 | `23` | `1.64` | `45R` | `-5.0R` | `5.33` |
| 967 | AUDUSD | London | 30m | FADE_DOWN | RSI_30-50 | `59.6%` | 426 | `52` | `1.48` | `82R` | `-9.0R` | `5.33` |
| 968 | EURUSD | London | 60m | FADE_DOWN | Mon | `62.6%` | 163 | `20` | `1.67` | `41R` | `-4.0R` | `5.33` |
| 969 | XAUUSD | London | 30m | FADE_DOWN | RSI_D>65 | `62.6%` | 163 | `20` | `1.67` | `41R` | `-5.0R` | `5.33` |
| 970 | USDJPY | NY | 45m | FADE_DOWN | RSI<30 | `66.1%` | 62 | `8` | `1.95` | `20R` | `-5.0R` | `5.33` |
| 971 | WTI | London Initial | 45m | FADE_DOWN | BtwCloseHigh | `60.4%` | 321 | `39` | `1.53` | `67R` | `-6.0R` | `5.33` |
| 972 | BRENT | NY | 30m | FADE_UP | GapSmall | `58.6%` | 625 | `77` | `1.41` | `107R` | `-13.0R` | `5.33` |
| 973 | SP500 | NY Cash | 30m | FADE_UP | RSI_D>65 | `62.7%` | 158 | `21` | `1.68` | `40R` | `-6.0R` | `5.32` |
| 974 | EURJPY | Tokyo | 60m | FADE_UP | BASE | `57.5%` | 952 | `116` | `1.35` | `142R` | `-20.0R` | `5.32` |
| 975 | EURJPY | Tokyo | 60m | FADE_UP | GapSmall | `57.5%` | 952 | `116` | `1.35` | `142R` | `-20.0R` | `5.32` |
| 976 | GBPUSD | NY | 30m | FADE_UP | GapSmall | `59.1%` | 504 | `62` | `1.45` | `92R` | `-12.0R` | `5.32` |
| 977 | AUDUSD | London | 60m | FADE_UP | Mon | `62.2%` | 180 | `22` | `1.65` | `44R` | `-7.0R` | `5.32` |
| 978 | WTI | NY Main | 30m | FADE_UP | AbovePD+RSI_D>65 | `68.6%` | 35 | `4` | `2.18` | `13R` | `-4.0R` | `5.32` |
| 979 | BRENT | London | 30m | FADE_DOWN | OR_Q1_Tight | `66.7%` | 54 | `7` | `2.00` | `18R` | `-2.0R` | `5.32` |
| 980 | NASDAQ100 | Pre-Market | 15m | FADE_UP | Tue | `65.3%` | 75 | `9` | `1.88` | `23R` | `-5.0R` | `5.32` |
| 981 | NASDAQ100 | Pre-Market | 45m | FADE_UP | RSI>70 | `65.3%` | 75 | `9` | `1.88` | `23R` | `-4.0R` | `5.32` |
| 982 | NASDAQ100 | NY Cash | 60m | FADE_UP | BtwCloseHigh | `62.7%` | 153 | `19` | `1.68` | `39R` | `-5.0R` | `5.32` |
| 983 | SP500 | NY Cash | 30m | FADE_UP | BASE | `58.1%` | 735 | `91` | `1.39` | `119R` | `-10.0R` | `5.32` |
| 984 | GBPAUD | London | 30m | FADE_DOWN | Tue | `62.3%` | 175 | `22` | `1.65` | `43R` | `-4.0R` | `5.31` |
| 985 | AUDUSD | London | 60m | FADE_UP | RSI_50-70 | `58.8%` | 563 | `69` | `1.43` | `99R` | `-9.0R` | `5.31` |
| 986 | VIX | NY Cash | 60m | MOMENTUM_UP | OR_Q1_Tight | `61.0%` | 41 | `13` | `2.34` | `22R` | `-6.0R` | `5.31` |
| 987 | GBPUSD | NY | 30m | FADE_DOWN | RSI_30-50 | `59.8%` | 381 | `47` | `1.49` | `75R` | `-7.0R` | `5.30` |
| 988 | NATGAS | NY | 15m | MOMENTUM_UP | Fri | `56.0%` | 141 | `18` | `1.91` | `56R` | `-6.5R` | `5.30` |
| 989 | XAGUSD | London | 60m | FADE_DOWN | AbovePD | `63.0%` | 138 | `17` | `1.71` | `36R` | `-4.0R` | `5.30` |
| 990 | GBPUSD | London | 45m | FADE_DOWN | BtwCloseHigh | `60.1%` | 346 | `43` | `1.51` | `70R` | `-9.0R` | `5.30` |
| 991 | GBPUSD | NY | 30m | FADE_UP | BASE | `58.0%` | 743 | `91` | `1.38` | `119R` | `-12.0R` | `5.30` |
| 992 | WTI | London Initial | 60m | FADE_DOWN | BtwCloseHigh | `60.1%` | 353 | `43` | `1.50` | `71R` | `-7.0R` | `5.30` |
| 993 | GBPJPY | London | 45m | FADE_DOWN | Fri | `62.4%` | 165 | `20` | `1.66` | `41R` | `-5.0R` | `5.30` |
| 994 | BRENT | London | 60m | FADE_DOWN | RSI_D>65 | `63.2%` | 133 | `16` | `1.71` | `35R` | `-8.0R` | `5.29` |
| 995 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | Mon | `63.2%` | 133 | `17` | `1.71` | `35R` | `-9.0R` | `5.29` |
| 996 | BRENT | London | 45m | FADE_UP | OR_Q1_Tight | `63.9%` | 108 | `14` | `1.77` | `30R` | `-5.0R` | `5.29` |
| 997 | SP500 | Pre-Market | 60m | FADE_UP | GapSmall | `58.0%` | 727 | `89` | `1.38` | `117R` | `-14.0R` | `5.29` |
| 998 | GBPAUD | London | 60m | FADE_DOWN | OR_Q4_Wide | `62.1%` | 182 | `22` | `1.64` | `44R` | `-6.0R` | `5.29` |
| 999 | XAGUSD | NY | 30m | FADE_DOWN | BelowPD | `63.7%` | 113 | `14` | `1.76` | `31R` | `-4.0R` | `5.29` |
| 1000 | GBPJPY | London | 45m | FADE_DOWN | RSI_30-50 | `59.2%` | 473 | `58` | `1.45` | `87R` | `-7.0R` | `5.29` |
| 1001 | XAGUSD | NY | 30m | FADE_UP | OR_Q4_Wide | `63.4%` | 123 | `20` | `1.73` | `33R` | `-4.0R` | `5.29` |
| 1002 | GBPJPY | Tokyo | 30m | FADE_DOWN | BtwCloseHigh | `59.2%` | 466 | `57` | `1.45` | `86R` | `-11.0R` | `5.29` |
| 1003 | GBPAUD | London | 60m | FADE_UP | GapSmall | `57.8%` | 796 | `97` | `1.37` | `124R` | `-12.0R` | `5.28` |
| 1004 | GBPJPY | Tokyo | 30m | FADE_UP | OR_Q4_Wide | `60.9%` | 261 | `32` | `1.56` | `57R` | `-5.0R` | `5.28` |
| 1005 | GBPJPY | Tokyo | 60m | FADE_UP | BtwLowClose | `59.6%` | 406 | `50` | `1.48` | `78R` | `-11.0R` | `5.28` |
| 1006 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | GapSmall | `58.4%` | 632 | `78` | `1.40` | `106R` | `-12.0R` | `5.28` |
| 1007 | GBPAUD | London | 45m | FADE_DOWN | Tue | `62.1%` | 177 | `22` | `1.64` | `43R` | `-5.0R` | `5.28` |
| 1008 | EURUSD | London | 30m | FADE_UP | Wed | `61.7%` | 206 | `25` | `1.61` | `48R` | `-6.0R` | `5.28` |
| 1009 | EURJPY | Tokyo | 45m | FADE_DOWN | Mon | `61.7%` | 206 | `25` | `1.61` | `48R` | `-11.0R` | `5.28` |
| 1010 | VIX | NY Cash | 45m | FADE_UP | GapSmall | `61.7%` | 206 | `61` | `1.61` | `48R` | `-6.0R` | `5.28` |
| 1011 | XAGUSD | London | 30m | FADE_DOWN | Mon | `62.6%` | 155 | `19` | `1.67` | `39R` | `-4.0R` | `5.28` |
| 1012 | WTI | NY Main | 45m | FADE_DOWN | Mon | `62.6%` | 155 | `19` | `1.67` | `39R` | `-4.0R` | `5.28` |
| 1013 | EURUSD | NY | 15m | MOMENTUM_UP | ATR+10% | `61.8%` | 34 | `4` | `2.42` | `18R` | `-3.0R` | `5.28` |
| 1014 | USDJPY | NY | 45m | FADE_UP | GapSmall | `59.8%` | 378 | `47` | `1.49` | `74R` | `-10.0R` | `5.28` |
| 1015 | SP500 | Pre-Market | 45m | FADE_UP | RSI_50-70 | `59.2%` | 461 | `56` | `1.45` | `85R` | `-12.0R` | `5.27` |
| 1016 | USDJPY | NY | 60m | FADE_DOWN | GapSmall | `60.2%` | 329 | `40` | `1.51` | `67R` | `-8.0R` | `5.27` |
| 1017 | GBPJPY | Tokyo | 45m | FADE_DOWN | Tue | `62.2%` | 172 | `21` | `1.65` | `42R` | `-3.0R` | `5.27` |
| 1018 | NATGAS | NY | 30m | FADE_UP | Wed | `62.7%` | 150 | `19` | `1.68` | `38R` | `-11.0R` | `5.27` |
| 1019 | SP500 | Pre-Market | 60m | FADE_UP | Tue | `62.7%` | 150 | `19` | `1.68` | `38R` | `-13.0R` | `5.27` |
| 1020 | GBPAUD | London | 60m | FADE_DOWN | RSI_D<35 | `64.7%` | 85 | `11` | `1.83` | `25R` | `-2.0R` | `5.27` |
| 1021 | EURUSD | London | 45m | FADE_DOWN | GapSmall | `57.5%` | 873 | `107` | `1.35` | `131R` | `-13.0R` | `5.27` |
| 1022 | WTI | London Initial | 60m | FADE_DOWN | OR_Q4_Wide | `61.1%` | 244 | `31` | `1.57` | `54R` | `-8.0R` | `5.26` |
| 1023 | EURJPY | London | 15m | FADE_DOWN | RSI_30-50 | `59.7%` | 380 | `47` | `1.48` | `74R` | `-8.0R` | `5.26` |
| 1024 | AUDUSD | London | 60m | FADE_DOWN | Mon | `62.0%` | 184 | `23` | `1.63` | `44R` | `-6.0R` | `5.26` |
| 1025 | GBPAUD | London | 45m | FADE_UP | Thu | `62.0%` | 184 | `23` | `1.63` | `44R` | `-6.0R` | `5.26` |
| 1026 | NATGAS | NY | 30m | FADE_DOWN | RSI_30-50 | `59.8%` | 366 | `45` | `1.49` | `72R` | `-8.0R` | `5.26` |
| 1027 | EURUSD | NY | 45m | FADE_DOWN | BASE | `58.5%` | 588 | `72` | `1.41` | `100R` | `-18.0R` | `5.26` |
| 1028 | XAUUSD | London | 45m | FADE_DOWN | GapSmall | `57.6%` | 819 | `101` | `1.36` | `125R` | `-11.0R` | `5.26` |
| 1029 | GBPAUD | London | 60m | FADE_UP | Tue | `61.7%` | 196 | `24` | `1.61` | `46R` | `-7.0R` | `5.26` |
| 1030 | EURUSD | NY | 45m | FADE_DOWN | BelowPD | `62.9%` | 140 | `17` | `1.69` | `36R` | `-10.0R` | `5.26` |
| 1031 | XAGUSD | London | 30m | FADE_UP | BelowPD | `62.9%` | 140 | `17` | `1.69` | `36R` | `-7.0R` | `5.26` |
| 1032 | GBPJPY | Tokyo | 30m | FADE_UP | RSI>70 | `66.1%` | 59 | `7` | `1.95` | `19R` | `-3.0R` | `5.26` |
| 1033 | XAUUSD | London | 15m | FADE_UP | RSI>70 | `66.1%` | 59 | `7` | `1.95` | `19R` | `-5.0R` | `5.26` |
| 1034 | XAUUSD | NY | 60m | FADE_UP | OR_Q4_Wide | `66.1%` | 59 | `10` | `1.95` | `19R` | `-2.0R` | `5.26` |
| 1035 | GBPUSD | NY | 60m | FADE_DOWN | RSI<30 | `67.4%` | 43 | `5` | `2.07` | `15R` | `-2.0R` | `5.25` |
| 1036 | EURUSD | London | 15m | FADE_DOWN | BASE | `58.0%` | 716 | `88` | `1.38` | `114R` | `-9.0R` | `5.25` |
| 1037 | AUDUSD | London | 45m | FADE_UP | OR_Q1_Tight | `61.1%` | 239 | `30` | `1.57` | `53R` | `-6.0R` | `5.25` |
| 1038 | EURUSD | London | 30m | FADE_DOWN | GapSmall | `57.6%` | 823 | `101` | `1.36` | `125R` | `-9.0R` | `5.25` |
| 1039 | GBPAUD | London | 60m | FADE_DOWN | Thu | `62.0%` | 179 | `22` | `1.63` | `43R` | `-7.0R` | `5.25` |
| 1040 | XAGUSD | London | 60m | FADE_DOWN | Thu | `62.0%` | 179 | `22` | `1.63` | `43R` | `-8.0R` | `5.25` |
| 1041 | XAGUSD | London | 45m | FADE_DOWN | RSI_D>65 | `63.0%` | 135 | `17` | `1.70` | `35R` | `-6.0R` | `5.25` |
| 1042 | AUDUSD | Sydney | 30m | FADE_UP | GapSmall | `65.3%` | 72 | `9` | `1.88` | `22R` | `-6.0R` | `5.25` |
| 1043 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | RSI_D>65 | `65.3%` | 72 | `9` | `1.88` | `22R` | `-3.0R` | `5.25` |
| 1044 | XAUUSD | NY | 45m | FADE_UP | RSI_50-70 | `60.3%` | 305 | `37` | `1.52` | `63R` | `-8.0R` | `5.25` |
| 1045 | NASDAQ100 | Pre-Market | 45m | FADE_UP | OR_Q4_Wide | `61.2%` | 227 | `30` | `1.58` | `51R` | `-6.0R` | `5.25` |
| 1046 | BRENT | London | 60m | FADE_UP | BtwCloseHigh | `59.9%` | 347 | `43` | `1.50` | `69R` | `-7.0R` | `5.25` |
| 1047 | USDJPY | Tokyo | 30m | FADE_UP | RSI_30-50 | `60.3%` | 312 | `38` | `1.52` | `64R` | `-6.0R` | `5.25` |
| 1048 | GBPJPY | Tokyo | 30m | FADE_UP | RSI_50-70 | `58.6%` | 567 | `69` | `1.41` | `97R` | `-13.0R` | `5.24` |
| 1049 | GBPUSD | London | 45m | FADE_DOWN | OR_Q4_Wide | `61.4%` | 215 | `26` | `1.59` | `49R` | `-5.0R` | `5.24` |
| 1050 | BRENT | NY | 60m | FADE_DOWN | BtwCloseHigh | `61.4%` | 215 | `26` | `1.59` | `49R` | `-5.0R` | `5.24` |
| 1051 | NASDAQ100 | Pre-Market | 60m | FADE_UP | OR_Q4_Wide | `61.4%` | 215 | `29` | `1.59` | `49R` | `-6.0R` | `5.24` |
| 1052 | VIX | NY Cash | 45m | FADE_UP | Wed | `66.7%` | 51 | `15` | `2.00` | `17R` | `-3.0R` | `5.24` |
| 1053 | EURUSD | NY | 45m | FADE_UP | Wed | `62.4%` | 157 | `19` | `1.66` | `39R` | `-5.0R` | `5.24` |
| 1054 | GBPUSD | NY | 45m | FADE_UP | BtwCloseHigh | `62.4%` | 157 | `19` | `1.66` | `39R` | `-7.0R` | `5.24` |
| 1055 | GBPJPY | London | 60m | FADE_UP | AbovePD+RSI_D>65 | `68.8%` | 32 | `4` | `2.20` | `12R` | `-3.0R` | `5.24` |
| 1056 | EURJPY | London | 30m | FADE_UP | AbovePD+RSI_D>65 | `68.8%` | 32 | `5` | `2.20` | `12R` | `-4.0R` | `5.24` |
| 1057 | GBPAUD | Sydney | 45m | FADE_UP | BelowPD | `68.8%` | 32 | `4` | `2.20` | `12R` | `-3.0R` | `5.24` |
| 1058 | XAGUSD | NY | 60m | FADE_UP | RSI_D<35 | `68.8%` | 32 | `5` | `2.20` | `12R` | `-4.0R` | `5.24` |
| 1059 | BRENT | NY | 30m | FADE_UP | AbovePD+RSI_D>65 | `68.8%` | 32 | `4` | `2.20` | `12R` | `-4.0R` | `5.24` |
| 1060 | WTI | London Initial | 30m | FADE_UP | GapSmall | `58.0%` | 684 | `84` | `1.38` | `110R` | `-11.0R` | `5.24` |
| 1061 | EURJPY | London | 60m | FADE_DOWN | GapSmall | `57.9%` | 731 | `89` | `1.37` | `115R` | `-9.0R` | `5.24` |
| 1062 | GBPUSD | London | 45m | FADE_UP | Fri | `62.1%` | 174 | `21` | `1.64` | `42R` | `-8.0R` | `5.24` |
| 1063 | WTI | NY Main | 30m | FADE_DOWN | BASE | `57.5%` | 829 | `101` | `1.36` | `125R` | `-18.0R` | `5.24` |
| 1064 | GBPUSD | London | 60m | FADE_DOWN | RSI_D<35 | `64.0%` | 100 | `13` | `1.78` | `28R` | `-4.0R` | `5.24` |
| 1065 | EURUSD | London | 30m | FADE_UP | BtwLowClose | `59.5%` | 393 | `48` | `1.47` | `75R` | `-8.0R` | `5.23` |
| 1066 | BRENT | London | 30m | FADE_DOWN | RSI_D>65 | `63.6%` | 110 | `14` | `1.75` | `30R` | `-6.0R` | `5.23` |
| 1067 | AUDUSD | London | 30m | FADE_DOWN | BtwCloseHigh | `60.3%` | 300 | `37` | `1.52` | `62R` | `-7.0R` | `5.23` |
| 1068 | SP500 | Pre-Market | 60m | FADE_DOWN | Thu | `61.8%` | 186 | `23` | `1.62` | `44R` | `-6.0R` | `5.23` |
| 1069 | GBPJPY | Tokyo | 45m | FADE_DOWN | RSI_50-70 | `60.1%` | 328 | `40` | `1.50` | `66R` | `-9.0R` | `5.23` |
| 1070 | NATGAS | NY | 45m | FADE_UP | GapSmall | `58.7%` | 521 | `64` | `1.42` | `91R` | `-12.0R` | `5.23` |
| 1071 | EURUSD | NY | 15m | FADE_DOWN | BelowPD | `62.1%` | 169 | `21` | `1.64` | `41R` | `-9.0R` | `5.23` |
| 1072 | GBPUSD | London | 30m | FADE_DOWN | BASE | `57.1%` | 965 | `119` | `1.33` | `137R` | `-15.0R` | `5.22` |
| 1073 | USDJPY | Tokyo | 30m | FADE_UP | Mon | `61.9%` | 181 | `22` | `1.62` | `43R` | `-4.0R` | `5.22` |
| 1074 | SP500 | NY Cash | 15m | FADE_DOWN | OR_Q4_Wide | `61.3%` | 217 | `27` | `1.58` | `49R` | `-11.0R` | `5.22` |
| 1075 | WTI | London Initial | 30m | FADE_UP | BASE | `57.8%` | 723 | `89` | `1.37` | `113R` | `-12.0R` | `5.22` |
| 1076 | BRENT | London | 30m | FADE_DOWN | BtwCloseHigh | `60.6%` | 269 | `33` | `1.54` | `57R` | `-6.0R` | `5.21` |
| 1077 | BRENT | London | 30m | FADE_UP | GapSmall | `58.3%` | 604 | `74` | `1.40` | `100R` | `-9.0R` | `5.21` |
| 1078 | NATGAS | NY | 45m | FADE_UP | BtwCloseHigh | `61.9%` | 176 | `22` | `1.63` | `42R` | `-7.0R` | `5.21` |
| 1079 | XAUUSD | London | 45m | FADE_DOWN | BASE | `57.1%` | 931 | `114` | `1.33` | `133R` | `-10.0R` | `5.21` |
| 1080 | EURJPY | London | 60m | FADE_DOWN | OR_Q4_Wide | `62.3%` | 159 | `20` | `1.65` | `39R` | `-11.0R` | `5.21` |
| 1081 | XAGUSD | NY | 15m | FADE_UP | Wed | `62.3%` | 159 | `20` | `1.65` | `39R` | `-6.0R` | `5.21` |
| 1082 | EURJPY | London | 45m | FADE_DOWN | GapSmall | `57.7%` | 747 | `91` | `1.36` | `115R` | `-11.0R` | `5.21` |
| 1083 | WTI | London Initial | 60m | FADE_UP | Mon | `61.7%` | 188 | `23` | `1.61` | `44R` | `-5.0R` | `5.21` |
| 1084 | XAGUSD | London | 30m | FADE_UP | Mon | `61.5%` | 200 | `24` | `1.60` | `46R` | `-7.0R` | `5.21` |
| 1085 | EURJPY | London | 60m | FADE_DOWN | RSI_50-70 | `60.2%` | 304 | `37` | `1.51` | `62R` | `-9.0R` | `5.20` |
| 1086 | WTI | London Initial | 45m | FADE_UP | BtwLowClose | `60.1%` | 318 | `39` | `1.50` | `64R` | `-8.0R` | `5.20` |
| 1087 | GBPUSD | NY | 30m | FADE_DOWN | BASE | `57.5%` | 798 | `98` | `1.35` | `120R` | `-11.0R` | `5.20` |
| 1088 | GBPJPY | Tokyo | 15m | FADE_UP | Wed | `62.9%` | 132 | `16` | `1.69` | `34R` | `-7.0R` | `5.20` |
| 1089 | SP500 | Pre-Market | 45m | FADE_DOWN | OR_Q1_Tight | `62.9%` | 132 | `19` | `1.69` | `34R` | `-9.0R` | `5.20` |
| 1090 | VIX | NY Cash | 60m | FADE_DOWN | BASE | `61.2%` | 219 | `65` | `1.58` | `49R` | `-11.0R` | `5.20` |
| 1091 | SP500 | NY Cash | 60m | FADE_DOWN | BASE | `58.5%` | 556 | `68` | `1.41` | `94R` | `-12.0R` | `5.20` |
| 1092 | XAGUSD | NY | 15m | FADE_UP | OR_Q4_Wide | `62.0%` | 171 | `28` | `1.63` | `41R` | `-4.0R` | `5.20` |
| 1093 | EURUSD | London | 45m | FADE_DOWN | BASE | `57.1%` | 917 | `112` | `1.33` | `131R` | `-12.0R` | `5.20` |
| 1094 | GBPAUD | London | 60m | FADE_UP | RSI_50-70 | `58.6%` | 531 | `65` | `1.41` | `91R` | `-8.0R` | `5.20` |
| 1095 | EURUSD | London | 30m | FADE_UP | AbovePD | `63.0%` | 127 | `16` | `1.70` | `33R` | `-10.0R` | `5.19` |
| 1096 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | OR_Q4_Wide | `63.0%` | 127 | `16` | `1.70` | `33R` | `-6.0R` | `5.19` |
| 1097 | SP500 | Pre-Market | 60m | FADE_UP | RSI_50-70 | `58.7%` | 506 | `62` | `1.42` | `88R` | `-13.0R` | `5.19` |
| 1098 | GBPUSD | NY | 15m | FADE_DOWN | RSI_D>65 | `64.4%` | 87 | `11` | `1.81` | `25R` | `-5.0R` | `5.19` |
| 1099 | USDJPY | NY | 60m | FADE_UP | Thu | `64.4%` | 87 | `11` | `1.81` | `25R` | `-5.0R` | `5.19` |
| 1100 | AUDUSD | London | 45m | FADE_UP | AbovePD | `61.7%` | 183 | `22` | `1.61` | `43R` | `-7.0R` | `5.19` |
| 1101 | EURJPY | London | 60m | FADE_UP | Wed | `61.7%` | 183 | `23` | `1.61` | `43R` | `-5.0R` | `5.19` |
| 1102 | GBPUSD | London | 45m | FADE_DOWN | OR_Q1_Tight | `60.7%` | 252 | `31` | `1.55` | `54R` | `-9.0R` | `5.19` |
| 1103 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | RSI_50-70 | `63.1%` | 122 | `15` | `1.71` | `32R` | `-5.0R` | `5.19` |
| 1104 | EURJPY | Tokyo | 15m | FADE_UP | Thu | `62.4%` | 149 | `18` | `1.66` | `37R` | `-6.0R` | `5.19` |
| 1105 | XAUUSD | NY | 30m | FADE_DOWN | Wed | `62.4%` | 149 | `18` | `1.66` | `37R` | `-7.0R` | `5.19` |
| 1106 | AUDUSD | London | 45m | FADE_DOWN | BASE | `57.0%` | 947 | `116` | `1.33` | `133R` | `-18.0R` | `5.18` |
| 1107 | USDJPY | Tokyo | 15m | FADE_DOWN | RSI_30-50 | `59.0%` | 451 | `55` | `1.44` | `81R` | `-8.0R` | `5.18` |
| 1108 | XAUUSD | NY | 45m | FADE_DOWN | OR_Q1_Tight | `61.8%` | 178 | `27` | `1.62` | `42R` | `-8.0R` | `5.18` |
| 1109 | BRENT | NY | 45m | FADE_DOWN | BelowPD | `63.4%` | 112 | `14` | `1.73` | `30R` | `-16.0R` | `5.18` |
| 1110 | XAUUSD | NY | 45m | FADE_DOWN | BASE | `58.8%` | 485 | `60` | `1.43` | `85R` | `-8.0R` | `5.18` |
| 1111 | BRENT | London | 30m | FADE_UP | BtwCloseHigh | `60.8%` | 240 | `30` | `1.55` | `52R` | `-10.0R` | `5.18` |
| 1112 | AUDUSD | London | 45m | FADE_UP | RSI>70 | `65.2%` | 69 | `8` | `1.88` | `21R` | `-3.0R` | `5.18` |
| 1113 | EURJPY | London | 30m | FADE_UP | RSI_30-50 | `60.0%` | 315 | `39` | `1.50` | `63R` | `-10.0R` | `5.18` |
| 1114 | BRENT | London | 30m | FADE_DOWN | Thu | `62.5%` | 144 | `18` | `1.67` | `36R` | `-6.0R` | `5.18` |
| 1115 | SP500 | NY Cash | 60m | FADE_UP | AbovePD | `62.5%` | 144 | `18` | `1.67` | `36R` | `-4.0R` | `5.18` |
| 1116 | SP500 | NY Cash | 30m | FADE_UP | Thu | `62.1%` | 161 | `20` | `1.64` | `39R` | `-9.0R` | `5.17` |
| 1117 | NASDAQ100 | NY Cash | 30m | FADE_UP | GapSmall | `58.2%` | 582 | `72` | `1.40` | `96R` | `-9.0R` | `5.17` |
| 1118 | SP500 | NY Cash | 15m | FADE_DOWN | BASE | `57.6%` | 754 | `92` | `1.36` | `114R` | `-17.0R` | `5.17` |
| 1119 | XAUUSD | NY | 45m | FADE_UP | ATR+10% | `67.5%` | 40 | `5` | `2.08` | `14R` | `-4.0R` | `5.17` |
| 1120 | XAUUSD | London | 60m | FADE_UP | BASE | `56.9%` | 979 | `120` | `1.32` | `135R` | `-11.0R` | `5.17` |
| 1121 | USDJPY | Tokyo | 60m | FADE_DOWN | BASE | `56.9%` | 957 | `117` | `1.32` | `133R` | `-10.0R` | `5.17` |
| 1122 | USDJPY | Tokyo | 60m | FADE_DOWN | GapSmall | `56.9%` | 957 | `117` | `1.32` | `133R` | `-10.0R` | `5.17` |
| 1123 | GBPUSD | NY | 45m | FADE_DOWN | RSI_50-70 | `60.6%` | 254 | `31` | `1.54` | `54R` | `-11.0R` | `5.17` |
| 1124 | GBPAUD | London | 15m | FADE_DOWN | OR_Q4_Wide | `60.6%` | 254 | `31` | `1.54` | `54R` | `-12.0R` | `5.17` |
| 1125 | GBPUSD | London | 60m | FADE_DOWN | Mon | `61.8%` | 173 | `21` | `1.62` | `41R` | `-6.0R` | `5.17` |
| 1126 | EURJPY | London | 45m | FADE_DOWN | Mon | `61.8%` | 173 | `21` | `1.62` | `41R` | `-7.0R` | `5.17` |
| 1127 | XAGUSD | London | 30m | FADE_DOWN | OR_Q1_Tight | `61.8%` | 173 | `29` | `1.62` | `41R` | `-12.0R` | `5.17` |
| 1128 | SP500 | Pre-Market | 45m | FADE_DOWN | Thu | `61.8%` | 173 | `22` | `1.62` | `41R` | `-5.0R` | `5.17` |
| 1129 | NASDAQ100 | NY Cash | 45m | FADE_UP | RSI_30-50 | `62.6%` | 139 | `17` | `1.67` | `35R` | `-6.0R` | `5.17` |
| 1130 | EURUSD | London | 60m | FADE_DOWN | OR_Q4_Wide | `61.6%` | 185 | `23` | `1.61` | `43R` | `-6.0R` | `5.17` |
| 1131 | SP500 | NY Cash | 60m | FADE_DOWN | RSI_50-70 | `61.6%` | 185 | `23` | `1.61` | `43R` | `-5.0R` | `5.17` |
| 1132 | EURJPY | Tokyo | 30m | FADE_UP | RSI_30-50 | `60.1%` | 296 | `36` | `1.51` | `60R` | `-9.0R` | `5.16` |
| 1133 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | ATR+10% | `66.7%` | 48 | `6` | `2.00` | `16R` | `-2.0R` | `5.16` |
| 1134 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | RSI_D<35 | `66.7%` | 48 | `6` | `2.00` | `16R` | `-2.0R` | `5.16` |
| 1135 | EURUSD | London | 15m | FADE_DOWN | RSI_30-50 | `59.7%` | 347 | `43` | `1.48` | `67R` | `-9.0R` | `5.16` |
| 1136 | EURUSD | NY | 60m | FADE_UP | BtwLowClose | `62.7%` | 134 | `16` | `1.68` | `34R` | `-4.0R` | `5.16` |
| 1137 | WTI | London Initial | 45m | FADE_UP | AbovePD | `62.7%` | 134 | `17` | `1.68` | `34R` | `-5.0R` | `5.16` |
| 1138 | WTI | NY Main | 60m | FADE_UP | Mon | `62.7%` | 134 | `17` | `1.68` | `34R` | `-5.0R` | `5.16` |
| 1139 | XAUUSD | London | 30m | MOMENTUM_DOWN | RSI<30 | `59.3%` | 54 | `7` | `2.18` | `26R` | `-3.0R` | `5.16` |
| 1140 | BRENT | London | 45m | FADE_DOWN | RSI_50-70 | `60.6%` | 249 | `31` | `1.54` | `53R` | `-9.0R` | `5.16` |
| 1141 | WTI | NY Main | 30m | FADE_DOWN | Mon | `61.9%` | 168 | `21` | `1.62` | `40R` | `-5.0R` | `5.15` |
| 1142 | BRENT | London | 45m | FADE_DOWN | Wed | `61.9%` | 168 | `21` | `1.62` | `40R` | `-4.0R` | `5.15` |
| 1143 | BRENT | NY | 15m | FADE_UP | RSI>70 | `64.9%` | 74 | `9` | `1.85` | `22R` | `-3.0R` | `5.15` |
| 1144 | WTI | NY Main | 15m | FADE_UP | BelowPD | `61.7%` | 180 | `22` | `1.61` | `42R` | `-7.0R` | `5.15` |
| 1145 | WTI | London Initial | 60m | FADE_DOWN | RSI_50-70 | `60.3%` | 277 | `34` | `1.52` | `57R` | `-6.0R` | `5.15` |
| 1146 | XAGUSD | London | 15m | FADE_DOWN | BtwLowClose | `61.1%` | 211 | `26` | `1.57` | `47R` | `-7.0R` | `5.15` |
| 1147 | WTI | NY Main | 45m | FADE_DOWN | GapSmall | `58.3%` | 556 | `68` | `1.40` | `92R` | `-12.0R` | `5.14` |
| 1148 | AUDUSD | London | 60m | FADE_DOWN | BelowPD | `62.0%` | 163 | `20` | `1.63` | `39R` | `-4.0R` | `5.14` |
| 1149 | GBPJPY | London | 15m | FADE_UP | Thu | `62.0%` | 163 | `21` | `1.63` | `39R` | `-7.0R` | `5.14` |
| 1150 | BRENT | London | 45m | FADE_UP | Fri | `62.0%` | 163 | `20` | `1.63` | `39R` | `-10.0R` | `5.14` |
| 1151 | EURUSD | London | 30m | FADE_DOWN | RSI_30-50 | `59.0%` | 429 | `53` | `1.44` | `77R` | `-6.0R` | `5.14` |
| 1152 | EURJPY | Tokyo | 60m | FADE_DOWN | Tue | `61.5%` | 187 | `23` | `1.60` | `43R` | `-7.0R` | `5.14` |
| 1153 | XAUUSD | London | 60m | FADE_UP | RSI_50-70 | `58.2%` | 567 | `70` | `1.39` | `93R` | `-8.0R` | `5.14` |
| 1154 | WTI | London Initial | 15m | FADE_UP | Thu | `64.6%` | 79 | `10` | `1.82` | `23R` | `-3.0R` | `5.14` |
| 1155 | EURJPY | Tokyo | 30m | FADE_DOWN | OR_Q4_Wide | `60.6%` | 251 | `31` | `1.54` | `53R` | `-11.0R` | `5.14` |
| 1156 | GBPJPY | London | 60m | FADE_UP | BASE | `56.8%` | 959 | `117` | `1.32` | `131R` | `-14.0R` | `5.14` |
| 1157 | EURJPY | Tokyo | 15m | FADE_DOWN | OR_Q4_Wide | `60.5%` | 258 | `32` | `1.53` | `54R` | `-8.0R` | `5.14` |
| 1158 | VIX | NY Cash | 30m | FADE_UP | BASE | `60.5%` | 258 | `76` | `1.53` | `54R` | `-10.0R` | `5.14` |
| 1159 | XAGUSD | NY | 60m | FADE_UP | OR_Q4_Wide | `65.6%` | 61 | `11` | `1.90` | `19R` | `-6.0R` | `5.13` |
| 1160 | XAGUSD | London | 45m | FADE_DOWN | OR_Q4_Wide | `61.2%` | 206 | `32` | `1.57` | `46R` | `-8.0R` | `5.13` |
| 1161 | VIX | NY Cash | 30m | FADE_UP | GapSmall | `61.2%` | 206 | `61` | `1.57` | `46R` | `-9.0R` | `5.13` |
| 1162 | EURJPY | London | 30m | FADE_UP | BtwCloseHigh | `59.6%` | 337 | `41` | `1.48` | `65R` | `-12.0R` | `5.13` |
| 1163 | BRENT | NY | 15m | FADE_DOWN | RSI_30-50 | `59.1%` | 399 | `49` | `1.45` | `73R` | `-10.0R` | `5.13` |
| 1164 | GBPUSD | London | 60m | FADE_DOWN | Fri | `61.3%` | 194 | `24` | `1.59` | `44R` | `-8.0R` | `5.13` |
| 1165 | USDJPY | Tokyo | 60m | FADE_DOWN | BtwCloseHigh | `57.9%` | 618 | `76` | `1.38` | `98R` | `-9.0R` | `5.13` |
| 1166 | XAUUSD | London | 45m | FADE_DOWN | BtwCloseHigh | `59.9%` | 309 | `38` | `1.49` | `61R` | `-9.0R` | `5.12` |
| 1167 | VIX | NY Cash | 45m | FADE_UP | BASE | `60.5%` | 253 | `74` | `1.53` | `53R` | `-6.0R` | `5.12` |
| 1168 | XAUUSD | London | 15m | FADE_DOWN | AbovePD | `63.5%` | 104 | `13` | `1.74` | `28R` | `-5.0R` | `5.12` |
| 1169 | EURUSD | London | 30m | FADE_UP | OR_Q4_Wide | `60.4%` | 260 | `32` | `1.52` | `54R` | `-9.0R` | `5.12` |
| 1170 | WTI | London Initial | 45m | FADE_DOWN | RSI_50-70 | `60.4%` | 260 | `32` | `1.52` | `54R` | `-5.0R` | `5.12` |
| 1171 | GBPJPY | London | 15m | FADE_DOWN | BASE | `57.2%` | 815 | `100` | `1.34` | `117R` | `-17.0R` | `5.12` |
| 1172 | AUDUSD | London | 15m | FADE_DOWN | Thu | `62.5%` | 136 | `17` | `1.67` | `34R` | `-8.0R` | `5.12` |
| 1173 | BRENT | NY | 60m | FADE_UP | RSI_D>65 | `63.6%` | 99 | `12` | `1.75` | `27R` | `-5.0R` | `5.12` |
| 1174 | BRENT | NY | 60m | FADE_DOWN | BelowPD | `63.6%` | 99 | `12` | `1.75` | `27R` | `-10.0R` | `5.12` |
| 1175 | AUDUSD | London | 30m | FADE_DOWN | BtwLowClose | `60.3%` | 267 | `33` | `1.52` | `55R` | `-6.0R` | `5.12` |
| 1176 | AUDUSD | London | 15m | FADE_UP | Tue | `62.1%` | 153 | `19` | `1.64` | `37R` | `-6.0R` | `5.12` |
| 1177 | EURUSD | London | 30m | FADE_DOWN | BASE | `57.0%` | 872 | `107` | `1.33` | `122R` | `-10.0R` | `5.11` |
| 1178 | EURUSD | London | 45m | FADE_DOWN | BtwLowClose | `59.4%` | 355 | `44` | `1.47` | `67R` | `-9.0R` | `5.11` |
| 1179 | NASDAQ100 | Pre-Market | 15m | FADE_UP | BASE | `59.7%` | 325 | `40` | `1.48` | `63R` | `-8.0R` | `5.11` |
| 1180 | GBPJPY | London | 60m | FADE_DOWN | Mon | `61.8%` | 165 | `20` | `1.62` | `39R` | `-7.0R` | `5.11` |
| 1181 | USDJPY | Tokyo | 45m | FADE_DOWN | RSI_30-50 | `58.5%` | 496 | `61` | `1.41` | `84R` | `-8.0R` | `5.11` |
| 1182 | EURJPY | Tokyo | 15m | FADE_DOWN | RSI_30-50 | `58.9%` | 428 | `53` | `1.43` | `76R` | `-13.0R` | `5.11` |
| 1183 | WTI | London Initial | 60m | FADE_DOWN | AbovePD | `62.6%` | 131 | `16` | `1.67` | `33R` | `-5.0R` | `5.11` |
| 1184 | BRENT | London | 30m | FADE_UP | Thu | `62.6%` | 131 | `16` | `1.67` | `33R` | `-5.0R` | `5.11` |
| 1185 | BRENT | NY | 45m | FADE_DOWN | RSI_30-50 | `59.1%` | 396 | `48` | `1.44` | `72R` | `-19.0R` | `5.11` |
| 1186 | NATGAS | NY | 45m | FADE_DOWN | BelowPD | `62.2%` | 148 | `18` | `1.64` | `36R` | `-4.0R` | `5.10` |
| 1187 | EURJPY | Tokyo | 60m | FADE_DOWN | Thu | `60.9%` | 215 | `26` | `1.56` | `47R` | `-6.0R` | `5.10` |
| 1188 | NATGAS | NY | 60m | FADE_DOWN | RSI_D>65 | `65.2%` | 66 | `8` | `1.87` | `20R` | `-4.0R` | `5.10` |
| 1189 | SP500 | Pre-Market | 60m | FADE_UP | BASE | `57.1%` | 836 | `102` | `1.33` | `118R` | `-19.0R` | `5.10` |
| 1190 | EURJPY | London | 60m | FADE_DOWN | BelowPD | `62.7%` | 126 | `16` | `1.68` | `32R` | `-9.0R` | `5.10` |
| 1191 | SP500 | NY Cash | 45m | FADE_UP | Fri | `62.7%` | 126 | `16` | `1.68` | `32R` | `-5.0R` | `5.10` |
| 1192 | AUDUSD | London | 45m | FADE_UP | BtwCloseHigh | `59.7%` | 313 | `39` | `1.48` | `61R` | `-8.0R` | `5.10` |
| 1193 | EURJPY | Tokyo | 15m | FADE_UP | Wed | `61.6%` | 172 | `21` | `1.61` | `40R` | `-5.0R` | `5.09` |
| 1194 | GBPJPY | London | 60m | FADE_DOWN | BASE | `57.1%` | 818 | `100` | `1.33` | `116R` | `-11.0R` | `5.09` |
| 1195 | EURUSD | London | 45m | FADE_UP | BtwLowClose | `59.2%` | 375 | `46` | `1.45` | `69R` | `-9.0R` | `5.09` |
| 1196 | EURUSD | NY | 15m | FADE_DOWN | Fri | `62.2%` | 143 | `18` | `1.65` | `35R` | `-4.0R` | `5.09` |
| 1197 | XAGUSD | London | 45m | FADE_UP | OR_Q1_Tight | `60.6%` | 236 | `39` | `1.54` | `50R` | `-8.0R` | `5.09` |
| 1198 | SP500 | Pre-Market | 45m | FADE_UP | BtwLowClose | `60.6%` | 236 | `29` | `1.54` | `50R` | `-10.0R` | `5.09` |
| 1199 | XAUUSD | London | 60m | FADE_UP | OR_Q4_Wide | `60.5%` | 243 | `38` | `1.53` | `51R` | `-8.0R` | `5.09` |
| 1200 | GBPUSD | London | 45m | FADE_DOWN | Fri | `61.0%` | 210 | `26` | `1.56` | `46R` | `-9.0R` | `5.09` |
| 1201 | XAUUSD | NY | 30m | FADE_UP | RSI_30-50 | `61.0%` | 210 | `26` | `1.56` | `46R` | `-10.0R` | `5.09` |
| 1202 | EURUSD | London | 45m | FADE_UP | RSI_30-50 | `60.0%` | 285 | `35` | `1.50` | `57R` | `-8.0R` | `5.09` |
| 1203 | NATGAS | NY | 30m | FADE_DOWN | GapSmall | `57.7%` | 645 | `79` | `1.36` | `99R` | `-11.0R` | `5.08` |
| 1204 | XAUUSD | NY | 30m | FADE_UP | GapSmall | `58.3%` | 504 | `62` | `1.40` | `84R` | `-18.0R` | `5.08` |
| 1205 | WTI | London Initial | 30m | FADE_UP | OR_Q1_Tight | `64.8%` | 71 | `9` | `1.84` | `21R` | `-4.0R` | `5.08` |
| 1206 | AUDUSD | London | 15m | FADE_UP | Thu | `61.7%` | 167 | `21` | `1.61` | `39R` | `-8.0R` | `5.08` |
| 1207 | EURJPY | Tokyo | 30m | FADE_DOWN | OR_Q1_Tight | `61.7%` | 167 | `22` | `1.61` | `39R` | `-9.0R` | `5.08` |
| 1208 | GBPAUD | London | 60m | FADE_UP | Fri | `61.7%` | 167 | `20` | `1.61` | `39R` | `-11.0R` | `5.08` |
| 1209 | WTI | NY Main | 15m | FADE_UP | Tue | `61.7%` | 167 | `21` | `1.61` | `39R` | `-14.0R` | `5.08` |
| 1210 | GBPJPY | London | 15m | MOMENTUM_UP | BelowPD | `55.9%` | 118 | `15` | `1.90` | `47R` | `-8.5R` | `5.08` |
| 1211 | AUDUSD | London | 60m | FADE_DOWN | BASE | `56.6%` | 955 | `117` | `1.31` | `127R` | `-18.0R` | `5.08` |
| 1212 | XAGUSD | NY | 30m | FADE_DOWN | OR_Q4_Wide | `62.9%` | 116 | `18` | `1.70` | `30R` | `-4.0R` | `5.08` |
| 1213 | EURUSD | NY | 45m | FADE_UP | BelowPD | `62.3%` | 138 | `17` | `1.65` | `34R` | `-10.0R` | `5.08` |
| 1214 | WTI | London Initial | 15m | FADE_DOWN | GapSmall | `58.6%` | 461 | `57` | `1.41` | `79R` | `-8.0R` | `5.08` |
| 1215 | EURJPY | London | 15m | FADE_UP | BASE | `57.0%` | 817 | `100` | `1.33` | `115R` | `-14.0R` | `5.08` |
| 1216 | SP500 | Pre-Market | 60m | FADE_DOWN | ATR-10% | `66.7%` | 45 | `6` | `2.00` | `15R` | `-8.0R` | `5.08` |
| 1217 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | RSI_D<35 | `66.7%` | 45 | `6` | `2.00` | `15R` | `-4.0R` | `5.08` |
| 1218 | USDJPY | Tokyo | 60m | FADE_UP | RSI_50-70 | `58.0%` | 562 | `69` | `1.38` | `90R` | `-8.0R` | `5.07` |
| 1219 | GBPUSD | London | 30m | FADE_DOWN | BtwLowClose | `59.4%` | 347 | `43` | `1.46` | `65R` | `-12.0R` | `5.07` |
| 1220 | USDJPY | NY | 15m | FADE_DOWN | RSI_30-50 | `59.4%` | 347 | `42` | `1.46` | `65R` | `-8.0R` | `5.07` |
| 1221 | EURUSD | London | 30m | FADE_DOWN | BtwLowClose | `59.6%` | 324 | `40` | `1.47` | `62R` | `-8.0R` | `5.07` |
| 1222 | EURUSD | London | 15m | FADE_DOWN | GapSmall | `57.6%` | 660 | `81` | `1.36` | `100R` | `-11.0R` | `5.07` |
| 1223 | BRENT | London | 15m | FADE_UP | BASE | `59.0%` | 395 | `49` | `1.44` | `71R` | `-10.0R` | `5.07` |
| 1224 | SP500 | NY Cash | 45m | FADE_DOWN | RSI_50-70 | `61.0%` | 205 | `25` | `1.56` | `45R` | `-5.0R` | `5.07` |
| 1225 | SP500 | Pre-Market | 15m | FADE_UP | GapSmall | `60.0%` | 280 | `34` | `1.50` | `56R` | `-11.0R` | `5.07` |
| 1226 | GBPAUD | London | 60m | FADE_DOWN | Fri | `61.3%` | 186 | `23` | `1.58` | `42R` | `-8.0R` | `5.07` |
| 1227 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | BelowPD | `63.1%` | 111 | `14` | `1.71` | `29R` | `-6.0R` | `5.07` |
| 1228 | VIX | NY Cash | 15m | FADE_UP | OR_Q4_Wide | `64.5%` | 76 | `22` | `1.81` | `22R` | `-3.0R` | `5.07` |
| 1229 | SP500 | Pre-Market | 15m | FADE_UP | RSI_50-70 | `61.5%` | 174 | `21` | `1.60` | `40R` | `-8.0R` | `5.07` |
| 1230 | USDJPY | NY | 15m | FADE_DOWN | Wed | `62.4%` | 133 | `17` | `1.66` | `33R` | `-5.0R` | `5.07` |
| 1231 | GBPUSD | NY | 30m | FADE_DOWN | BtwLowClose | `60.8%` | 212 | `26` | `1.55` | `46R` | `-5.0R` | `5.07` |
| 1232 | WTI | NY Main | 15m | FADE_UP | GapSmall | `57.6%` | 644 | `79` | `1.36` | `98R` | `-12.0R` | `5.06` |
| 1233 | GBPUSD | London | 60m | FADE_UP | OR_Q4_Wide | `61.1%` | 193 | `24` | `1.57` | `43R` | `-6.0R` | `5.06` |
| 1234 | XAUUSD | London | 45m | FADE_UP | Wed | `61.1%` | 193 | `24` | `1.57` | `43R` | `-7.0R` | `5.06` |
| 1235 | XAGUSD | London | 30m | FADE_UP | Fri | `61.1%` | 193 | `24` | `1.57` | `43R` | `-6.0R` | `5.06` |
| 1236 | SP500 | NY Cash | 30m | FADE_UP | RSI_50-70 | `59.1%` | 381 | `47` | `1.44` | `69R` | `-7.0R` | `5.06` |
| 1237 | NASDAQ100 | NY Cash | 45m | FADE_UP | RSI_50-70 | `59.8%` | 296 | `37` | `1.49` | `58R` | `-6.0R` | `5.06` |
| 1238 | WTI | London Initial | 15m | FADE_UP | Mon | `63.4%` | 101 | `12` | `1.73` | `27R` | `-5.0R` | `5.06` |
| 1239 | XAGUSD | NY | 15m | FADE_DOWN | BASE | `57.2%` | 741 | `91` | `1.34` | `107R` | `-11.0R` | `5.06` |
| 1240 | BRENT | NY | 45m | FADE_UP | BelowPD | `62.5%` | 128 | `16` | `1.67` | `32R` | `-6.0R` | `5.05` |
| 1241 | XAGUSD | NY | 45m | FADE_UP | Fri | `64.0%` | 86 | `11` | `1.77` | `24R` | `-9.0R` | `5.05` |
| 1242 | AUDUSD | London | 30m | FADE_DOWN | RSI_50-70 | `59.1%` | 367 | `45` | `1.45` | `67R` | `-6.0R` | `5.05` |
| 1243 | EURUSD | NY | 15m | FADE_UP | Thu | `61.8%` | 157 | `19` | `1.62` | `37R` | `-5.0R` | `5.05` |
| 1244 | BRENT | NY | 30m | FADE_DOWN | Mon | `61.8%` | 157 | `19` | `1.62` | `37R` | `-6.0R` | `5.05` |
| 1245 | AUDUSD | London | 15m | FADE_DOWN | BASE | `57.3%` | 716 | `88` | `1.34` | `104R` | `-15.0R` | `5.04` |
| 1246 | WTI | NY Main | 60m | FADE_UP | Tue | `62.6%` | 123 | `15` | `1.67` | `31R` | `-4.0R` | `5.04` |
| 1247 | GBPJPY | Tokyo | 30m | FADE_DOWN | BtwLowClose | `59.3%` | 337 | `41` | `1.46` | `63R` | `-10.0R` | `5.04` |
| 1248 | GBPUSD | NY | 30m | FADE_DOWN | Wed | `61.4%` | 176 | `22` | `1.59` | `40R` | `-10.0R` | `5.04` |
| 1249 | BRENT | London | 60m | FADE_DOWN | Fri | `61.4%` | 176 | `22` | `1.59` | `40R` | `-6.0R` | `5.04` |
| 1250 | NATGAS | NY | 30m | FADE_DOWN | BtwLowClose | `60.5%` | 228 | `28` | `1.53` | `48R` | `-9.0R` | `5.04` |
| 1251 | EURJPY | London | 15m | FADE_DOWN | OR_Q4_Wide | `60.4%` | 235 | `30` | `1.53` | `49R` | `-10.0R` | `5.04` |
| 1252 | GBPJPY | Tokyo | 15m | FADE_DOWN | BASE | `57.5%` | 656 | `80` | `1.35` | `98R` | `-13.0R` | `5.04` |
| 1253 | GBPJPY | Tokyo | 15m | FADE_DOWN | GapSmall | `57.5%` | 656 | `80` | `1.35` | `98R` | `-13.0R` | `5.04` |
| 1254 | GBPUSD | NY | 60m | FADE_UP | RSI_50-70 | `59.4%` | 323 | `40` | `1.47` | `61R` | `-7.0R` | `5.03` |
| 1255 | XAUUSD | NY | 45m | FADE_DOWN | AbovePD | `62.7%` | 118 | `15` | `1.68` | `30R` | `-4.0R` | `5.03` |
| 1256 | GBPAUD | London | 60m | FADE_DOWN | BtwCloseHigh | `59.9%` | 279 | `34` | `1.49` | `55R` | `-10.0R` | `5.03` |
| 1257 | XAGUSD | NY | 60m | FADE_DOWN | RSI_30-50 | `60.6%` | 216 | `26` | `1.54` | `46R` | `-7.0R` | `5.02` |
| 1258 | EURUSD | London | 15m | FADE_DOWN | BtwLowClose | `59.9%` | 272 | `33` | `1.50` | `54R` | `-7.0R` | `5.02` |
| 1259 | EURJPY | London | 15m | FADE_UP | OR_Q4_Wide | `59.9%` | 272 | `33` | `1.50` | `54R` | `-8.0R` | `5.02` |
| 1260 | USDJPY | NY | 60m | FADE_DOWN | OR_Q1_Tight | `61.4%` | 171 | `21` | `1.59` | `39R` | `-4.0R` | `5.02` |
| 1261 | EURJPY | London | 60m | FADE_DOWN | Mon | `61.4%` | 171 | `21` | `1.59` | `39R` | `-9.0R` | `5.02` |
| 1262 | XAGUSD | NY | 30m | FADE_DOWN | GapSmall | `58.5%` | 441 | `54` | `1.41` | `75R` | `-10.0R` | `5.02` |
| 1263 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | BelowPD | `62.8%` | 113 | `14` | `1.69` | `29R` | `-6.0R` | `5.02` |
| 1264 | EURUSD | NY | 15m | FADE_UP | Tue | `61.9%` | 147 | `18` | `1.62` | `35R` | `-6.0R` | `5.02` |
| 1265 | WTI | London Initial | 15m | FADE_DOWN | BASE | `58.1%` | 497 | `62` | `1.39` | `81R` | `-9.0R` | `5.02` |
| 1266 | USDJPY | NY | 60m | FADE_UP | OR_Q1_Tight | `61.2%` | 178 | `22` | `1.58` | `40R` | `-5.0R` | `5.01` |
| 1267 | USDJPY | NY | 30m | FADE_UP | RSI_D<35 | `66.0%` | 50 | `6` | `1.94` | `16R` | `-3.0R` | `5.01` |
| 1268 | GBPJPY | Tokyo | 45m | FADE_DOWN | RSI<30 | `66.0%` | 50 | `6` | `1.94` | `16R` | `-3.0R` | `5.01` |
| 1269 | GBPJPY | London | 60m | FADE_UP | GapSmall | `56.8%` | 837 | `102` | `1.31` | `113R` | `-12.0R` | `5.01` |
| 1270 | EURUSD | NY | 30m | FADE_UP | BASE | `57.0%` | 756 | `92` | `1.33` | `106R` | `-14.0R` | `5.01` |
| 1271 | EURJPY | Tokyo | 30m | FADE_UP | Wed | `60.7%` | 211 | `26` | `1.54` | `45R` | `-7.0R` | `5.01` |
| 1272 | WTI | NY Main | 15m | FADE_DOWN | Fri | `61.4%` | 166 | `21` | `1.59` | `38R` | `-7.0R` | `5.01` |
| 1273 | EURJPY | Tokyo | 45m | FADE_DOWN | Tue | `61.1%` | 185 | `23` | `1.57` | `41R` | `-9.0R` | `5.00` |
| 1274 | SP500 | Pre-Market | 60m | FADE_UP | BtwLowClose | `60.1%` | 253 | `31` | `1.50` | `51R` | `-8.0R` | `5.00` |
| 1275 | GBPAUD | London | 60m | FADE_UP | RSI_D>65 | `63.1%` | 103 | `14` | `1.71` | `27R` | `-4.0R` | `5.00` |
| 1276 | USDJPY | Tokyo | 45m | FADE_UP | RSI_50-70 | `57.5%` | 610 | `75` | `1.36` | `92R` | `-9.0R` | `5.00` |
| 1277 | EURUSD | London | 60m | FADE_UP | AbovePD | `62.4%` | 125 | `16` | `1.66` | `31R` | `-5.0R` | `5.00` |
| 1278 | GBPJPY | Tokyo | 60m | FADE_UP | Thu | `60.9%` | 192 | `24` | `1.56` | `42R` | `-7.0R` | `5.00` |
| 1279 | USDJPY | NY | 30m | FADE_UP | Fri | `63.3%` | 98 | `12` | `1.72` | `26R` | `-3.0R` | `5.00` |
| 1280 | XAUUSD | NY | 30m | FADE_UP | BASE | `57.2%` | 687 | `84` | `1.34` | `99R` | `-14.0R` | `5.00` |
| 1281 | EURUSD | London | 15m | FADE_UP | BtwCloseHigh | `59.8%` | 276 | `34` | `1.49` | `54R` | `-6.0R` | `4.99` |
| 1282 | GBPUSD | NY | 45m | FADE_UP | RSI_D>65 | `64.4%` | 73 | `9` | `1.81` | `21R` | `-4.0R` | `4.99` |
| 1283 | XAUUSD | NY | 60m | FADE_UP | BelowPD | `64.4%` | 73 | `9` | `1.81` | `21R` | `-4.0R` | `4.99` |
| 1284 | NASDAQ100 | Pre-Market | 15m | FADE_UP | BelowPD | `64.4%` | 73 | `9` | `1.81` | `21R` | `-4.0R` | `4.99` |
| 1285 | WTI | London Initial | 60m | FADE_DOWN | RSI_30-50 | `57.8%` | 543 | `67` | `1.37` | `85R` | `-15.0R` | `4.99` |
| 1286 | XAUUSD | NY | 45m | FADE_DOWN | GapSmall | `59.1%` | 347 | `43` | `1.44` | `63R` | `-11.0R` | `4.99` |
| 1287 | EURJPY | London | 45m | FADE_UP | AbovePD+RSI_D>65 | `67.6%` | 34 | `5` | `2.09` | `12R` | `-4.0R` | `4.99` |
| 1288 | BRENT | London | 60m | FADE_UP | AbovePD+RSI_D>65 | `67.6%` | 34 | `4` | `2.09` | `12R` | `-2.0R` | `4.99` |
| 1289 | NASDAQ100 | Pre-Market | 15m | FADE_UP | ATR+10% | `67.6%` | 34 | `4` | `2.09` | `12R` | `-3.0R` | `4.99` |
| 1290 | NASDAQ100 | Pre-Market | 45m | SHAKEOUT_DOWN | ATR+10% | `67.6%` | 34 | `4` | `2.09` | `12R` | `-3.0R` | `4.99` |
| 1291 | GBPAUD | London | 60m | FADE_DOWN | Mon | `61.1%` | 180 | `22` | `1.57` | `40R` | `-5.0R` | `4.99` |
| 1292 | XAGUSD | London | 45m | FADE_DOWN | Thu | `61.1%` | 180 | `22` | `1.57` | `40R` | `-7.0R` | `4.99` |
| 1293 | SP500 | NY Cash | 60m | FADE_UP | RSI_D>65 | `61.7%` | 149 | `19` | `1.61` | `35R` | `-3.0R` | `4.99` |
| 1294 | EURJPY | London | 30m | FADE_DOWN | OR_Q4_Wide | `60.6%` | 213 | `26` | `1.54` | `45R` | `-8.0R` | `4.99` |
| 1295 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | BtwLowClose | `60.6%` | 213 | `26` | `1.54` | `45R` | `-5.0R` | `4.99` |
| 1296 | GBPJPY | Tokyo | 60m | FADE_UP | RSI_50-70 | `57.4%` | 627 | `77` | `1.35` | `93R` | `-10.0R` | `4.99` |
| 1297 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | BtwLowClose | `63.6%` | 88 | `11` | `1.75` | `24R` | `-4.0R` | `4.99` |
| 1298 | GBPAUD | London | 15m | FADE_DOWN | BtwLowClose | `60.1%` | 248 | `31` | `1.51` | `50R` | `-10.0R` | `4.99` |
| 1299 | USDJPY | NY | 60m | FADE_DOWN | Tue | `63.9%` | 83 | `10` | `1.77` | `23R` | `-4.0R` | `4.98` |
| 1300 | WTI | London Initial | 60m | FADE_UP | Thu | `61.0%` | 187 | `23` | `1.56` | `41R` | `-5.0R` | `4.98` |
| 1301 | GBPJPY | Tokyo | 15m | FADE_UP | BASE | `57.3%` | 662 | `81` | `1.34` | `96R` | `-10.0R` | `4.98` |
| 1302 | GBPJPY | Tokyo | 15m | FADE_UP | GapSmall | `57.3%` | 662 | `81` | `1.34` | `96R` | `-10.0R` | `4.98` |
| 1303 | SP500 | Pre-Market | 15m | MOMENTUM_DOWN | RSI<30 | `60.0%` | 40 | `5` | `2.25` | `20R` | `-3.0R` | `4.98` |
| 1304 | GBPJPY | London | 15m | FADE_DOWN | GapSmall | `57.1%` | 697 | `85` | `1.33` | `99R` | `-19.0R` | `4.98` |
| 1305 | USDJPY | NY | 45m | FADE_DOWN | GapSmall | `58.7%` | 383 | `47` | `1.42` | `67R` | `-8.0R` | `4.98` |
| 1306 | AUDUSD | London | 60m | FADE_UP | BtwCloseHigh | `59.5%` | 294 | `36` | `1.47` | `56R` | `-9.0R` | `4.98` |
| 1307 | WTI | London Initial | 45m | FADE_DOWN | Tue | `60.8%` | 194 | `24` | `1.55` | `42R` | `-8.0R` | `4.97` |
| 1308 | GBPUSD | London | 15m | FADE_UP | Fri | `61.5%` | 156 | `19` | `1.60` | `36R` | `-5.0R` | `4.97` |
| 1309 | XAGUSD | NY | 30m | FADE_UP | AbovePD | `61.5%` | 156 | `19` | `1.60` | `36R` | `-5.0R` | `4.97` |
| 1310 | BRENT | London | 15m | FADE_DOWN | BASE | `58.5%` | 419 | `51` | `1.41` | `71R` | `-10.0R` | `4.97` |
| 1311 | EURUSD | NY | 45m | FADE_DOWN | OR_Q4_Wide | `65.5%` | 55 | `7` | `1.89` | `17R` | `-3.0R` | `4.97` |
| 1312 | EURJPY | Tokyo | 60m | FADE_UP | OR_Q4_Wide | `60.6%` | 208 | `26` | `1.54` | `44R` | `-8.0R` | `4.97` |
| 1313 | WTI | NY Main | 15m | FADE_DOWN | AbovePD | `60.6%` | 208 | `26` | `1.54` | `44R` | `-4.0R` | `4.97` |
| 1314 | EURUSD | NY | 30m | FADE_UP | GapSmall | `57.9%` | 513 | `63` | `1.38` | `81R` | `-15.0R` | `4.97` |
| 1315 | AUDUSD | London | 60m | FADE_DOWN | GapSmall | `56.8%` | 784 | `96` | `1.31` | `106R` | `-17.0R` | `4.97` |
| 1316 | USDJPY | NY | 45m | FADE_UP | Thu | `62.7%` | 110 | `14` | `1.68` | `28R` | `-4.0R` | `4.96` |
| 1317 | USDJPY | NY | 60m | FADE_DOWN | AbovePD | `62.7%` | 110 | `14` | `1.68` | `28R` | `-3.0R` | `4.96` |
| 1318 | WTI | NY Main | 30m | FADE_UP | BelowPD | `61.0%` | 182 | `22` | `1.56` | `40R` | `-7.0R` | `4.96` |
| 1319 | WTI | NY Main | 45m | FADE_DOWN | BASE | `56.9%` | 729 | `89` | `1.32` | `101R` | `-24.0R` | `4.96` |
| 1320 | BRENT | London | 30m | FADE_UP | Fri | `61.9%` | 139 | `18` | `1.62` | `33R` | `-6.0R` | `4.95` |
| 1321 | WTI | NY Main | 30m | FADE_UP | OR_Q1_Tight | `60.7%` | 196 | `24` | `1.55` | `42R` | `-4.0R` | `4.95` |
| 1322 | NASDAQ100 | NY Cash | 30m | FADE_UP | RSI_50-70 | `59.0%` | 346 | `43` | `1.44` | `62R` | `-7.0R` | `4.95` |
| 1323 | WTI | NY Main | 45m | FADE_UP | Thu | `61.2%` | 170 | `21` | `1.58` | `38R` | `-8.0R` | `4.95` |
| 1324 | GBPUSD | London | 60m | FADE_DOWN | BtwCloseHigh | `59.1%` | 330 | `41` | `1.44` | `60R` | `-9.0R` | `4.95` |
| 1325 | XAUUSD | London | 60m | FADE_UP | GapSmall | `56.4%` | 870 | `107` | `1.30` | `112R` | `-12.0R` | `4.95` |
| 1326 | AUDUSD | London | 45m | FADE_DOWN | GapSmall | `56.8%` | 759 | `93` | `1.31` | `103R` | `-14.0R` | `4.95` |
| 1327 | WTI | London Initial | 15m | FADE_UP | GapSmall | `58.5%` | 407 | `50` | `1.41` | `69R` | `-11.0R` | `4.95` |
| 1328 | SP500 | NY Cash | 30m | FADE_UP | RSI_30-50 | `60.5%` | 210 | `26` | `1.53` | `44R` | `-8.0R` | `4.95` |
| 1329 | BRENT | NY | 15m | FADE_UP | BtwLowClose | `60.3%` | 224 | `28` | `1.52` | `46R` | `-5.0R` | `4.95` |
| 1330 | BRENT | NY | 60m | FADE_UP | Fri | `62.3%` | 122 | `15` | `1.65` | `30R` | `-5.0R` | `4.94` |
| 1331 | EURUSD | NY | 30m | FADE_UP | BtwCloseHigh | `61.0%` | 177 | `22` | `1.57` | `39R` | `-7.0R` | `4.94` |
| 1332 | GBPUSD | NY | 30m | FADE_UP | AbovePD | `61.0%` | 177 | `22` | `1.57` | `39R` | `-9.0R` | `4.94` |
| 1333 | AUDUSD | London | 60m | FADE_UP | AbovePD | `61.0%` | 177 | `22` | `1.57` | `39R` | `-8.0R` | `4.94` |
| 1334 | SP500 | NY Cash | 30m | FADE_DOWN | OR_Q4_Wide | `61.0%` | 177 | `22` | `1.57` | `39R` | `-6.0R` | `4.94` |
| 1335 | GBPJPY | Tokyo | 60m | FADE_DOWN | ATR+10% | `65.0%` | 60 | `8` | `1.86` | `18R` | `-5.0R` | `4.94` |
| 1336 | BRENT | London | 15m | FADE_UP | RSI_D>65 | `65.0%` | 60 | `8` | `1.86` | `18R` | `-4.0R` | `4.94` |
| 1337 | NATGAS | NY | 15m | FADE_DOWN | Fri | `61.4%` | 158 | `19` | `1.59` | `36R` | `-14.0R` | `4.94` |
| 1338 | GBPAUD | London | 60m | FADE_UP | BtwCloseHigh | `59.8%` | 261 | `32` | `1.49` | `51R` | `-8.0R` | `4.94` |
| 1339 | XAGUSD | NY | 45m | FADE_DOWN | RSI_30-50 | `59.8%` | 261 | `32` | `1.49` | `51R` | `-10.0R` | `4.94` |
| 1340 | NASDAQ100 | NY Cash | 45m | FADE_UP | Fri | `63.0%` | 100 | `13` | `1.70` | `26R` | `-4.0R` | `4.94` |
| 1341 | EURJPY | Tokyo | 30m | FADE_DOWN | BtwCloseHigh | `57.5%` | 574 | `70` | `1.35` | `86R` | `-12.0R` | `4.94` |
| 1342 | GBPUSD | London | 60m | FADE_UP | BASE | `56.3%` | 904 | `111` | `1.29` | `114R` | `-12.0R` | `4.94` |
| 1343 | NASDAQ100 | Pre-Market | 45m | FADE_UP | BASE | `56.6%` | 815 | `100` | `1.30` | `107R` | `-13.0R` | `4.94` |
| 1344 | XAGUSD | London | 45m | FADE_DOWN | BtwCloseHigh | `59.3%` | 300 | `37` | `1.46` | `56R` | `-5.0R` | `4.94` |
| 1345 | XAGUSD | London | 60m | FADE_DOWN | BtwLowClose | `59.2%` | 316 | `39` | `1.45` | `58R` | `-12.0R` | `4.94` |
| 1346 | XAGUSD | NY | 15m | FADE_DOWN | BelowPD | `61.6%` | 146 | `18` | `1.61` | `34R` | `-5.0R` | `4.94` |
| 1347 | GBPAUD | London | 45m | FADE_UP | RSI_50-70 | `57.8%` | 514 | `63` | `1.37` | `80R` | `-10.0R` | `4.94` |
| 1348 | EURJPY | Tokyo | 15m | FADE_UP | BASE | `56.6%` | 791 | `97` | `1.31` | `105R` | `-15.0R` | `4.94` |
| 1349 | EURJPY | Tokyo | 15m | FADE_UP | GapSmall | `56.6%` | 791 | `97` | `1.31` | `105R` | `-15.0R` | `4.94` |
| 1350 | GBPJPY | London | 30m | FADE_DOWN | Wed | `60.7%` | 191 | `23` | `1.55` | `41R` | `-7.0R` | `4.93` |
| 1351 | XAGUSD | London | 45m | FADE_DOWN | Fri | `61.2%` | 165 | `21` | `1.58` | `37R` | `-7.0R` | `4.93` |
| 1352 | XAGUSD | London | 15m | FADE_DOWN | RSI_50-70 | `60.6%` | 198 | `24` | `1.54` | `42R` | `-8.0R` | `4.93` |
| 1353 | XAGUSD | London | 15m | FADE_UP | OR_Q1_Tight | `62.4%` | 117 | `58` | `1.66` | `29R` | `-5.0R` | `4.93` |
| 1354 | BRENT | NY | 60m | FADE_UP | Tue | `62.4%` | 117 | `14` | `1.66` | `29R` | `-3.0R` | `4.93` |
| 1355 | WTI | London Initial | 15m | FADE_UP | BASE | `58.2%` | 440 | `54` | `1.39` | `72R` | `-11.0R` | `4.93` |
| 1356 | AUDUSD | Sydney | 30m | FADE_UP | RSI_50-70 | `64.6%` | 65 | `8` | `1.83` | `19R` | `-5.0R` | `4.93` |
| 1357 | SP500 | Pre-Market | 15m | FADE_UP | Wed | `64.6%` | 65 | `8` | `1.83` | `19R` | `-4.0R` | `4.93` |
| 1358 | XAUUSD | NY | 45m | FADE_UP | Fri | `63.3%` | 90 | `11` | `1.73` | `24R` | `-4.0R` | `4.92` |
| 1359 | GBPJPY | London | 60m | FADE_DOWN | RSI_30-50 | `58.1%` | 451 | `55` | `1.39` | `73R` | `-7.0R` | `4.92` |
| 1360 | SP500 | NY Cash | 60m | FADE_UP | Wed | `62.0%` | 129 | `16` | `1.63` | `31R` | `-3.0R` | `4.92` |
| 1361 | GBPUSD | NY | 30m | FADE_DOWN | OR_Q4_Wide | `61.7%` | 141 | `17` | `1.61` | `33R` | `-4.0R` | `4.92` |
| 1362 | WTI | NY Main | 30m | FADE_UP | RSI_D<35 | `64.3%` | 70 | `9` | `1.80` | `20R` | `-3.0R` | `4.92` |
| 1363 | EURUSD | London | 60m | FADE_DOWN | GapSmall | `56.4%` | 844 | `104` | `1.29` | `108R` | `-12.0R` | `4.92` |
| 1364 | BRENT | NY | 45m | FADE_DOWN | RSI_D>65 | `62.5%` | 112 | `14` | `1.67` | `28R` | `-5.0R` | `4.92` |
| 1365 | BRENT | London | 45m | FADE_DOWN | Fri | `61.3%` | 160 | `20` | `1.58` | `36R` | `-5.0R` | `4.91` |
| 1366 | WTI | London Initial | 60m | FADE_UP | RSI_D<35 | `64.0%` | 75 | `10` | `1.78` | `21R` | `-4.0R` | `4.91` |
| 1367 | NASDAQ100 | NY Cash | 60m | FADE_UP | Fri | `64.0%` | 75 | `9` | `1.78` | `21R` | `-6.0R` | `4.91` |
| 1368 | WTI | NY Main | 15m | FADE_UP | RSI_50-70 | `58.2%` | 435 | `53` | `1.39` | `71R` | `-6.0R` | `4.91` |
| 1369 | XAUUSD | NY | 60m | FADE_DOWN | BASE | `58.5%` | 390 | `48` | `1.41` | `66R` | `-7.0R` | `4.91` |
| 1370 | GBPJPY | London | 15m | FADE_DOWN | BtwCloseHigh | `59.7%` | 258 | `32` | `1.48` | `50R` | `-7.0R` | `4.91` |
| 1371 | GBPUSD | NY | 45m | FADE_UP | AbovePD | `61.5%` | 148 | `18` | `1.60` | `34R` | `-8.0R` | `4.91` |
| 1372 | WTI | NY Main | 45m | FADE_UP | RSI_30-50 | `59.8%` | 251 | `31` | `1.49` | `49R` | `-12.0R` | `4.90` |
| 1373 | NATGAS | NY | 30m | FADE_UP | BASE | `56.6%` | 752 | `92` | `1.31` | `100R` | `-18.0R` | `4.90` |
| 1374 | XAGUSD | London | 15m | FADE_UP | RSI_50-70 | `58.6%` | 365 | `45` | `1.42` | `63R` | `-8.0R` | `4.90` |
| 1375 | USDJPY | NY | 60m | FADE_UP | BtwCloseHigh | `61.8%` | 136 | `17` | `1.62` | `32R` | `-9.0R` | `4.90` |
| 1376 | EURJPY | Tokyo | 15m | FADE_DOWN | Wed | `61.8%` | 136 | `17` | `1.62` | `32R` | `-6.0R` | `4.90` |
| 1377 | GBPJPY | London | 30m | FADE_DOWN | RSI<30 | `62.6%` | 107 | `13` | `1.68` | `27R` | `-6.0R` | `4.90` |
| 1378 | EURUSD | London | 15m | FADE_DOWN | BtwCloseHigh | `59.9%` | 237 | `29` | `1.49` | `47R` | `-6.0R` | `4.90` |
| 1379 | USDJPY | NY | 30m | FADE_DOWN | OR_Q4_Wide | `61.3%` | 155 | `19` | `1.58` | `35R` | `-3.0R` | `4.89` |
| 1380 | USDJPY | Tokyo | 30m | FADE_UP | RSI_50-70 | `57.2%` | 594 | `73` | `1.34` | `86R` | `-11.0R` | `4.89` |
| 1381 | XAUUSD | London | 60m | FADE_UP | AbovePD | `60.6%` | 188 | `23` | `1.54` | `40R` | `-13.0R` | `4.89` |
| 1382 | XAGUSD | NY | 15m | FADE_DOWN | BtwCloseHigh | `60.6%` | 188 | `23` | `1.54` | `40R` | `-6.0R` | `4.89` |
| 1383 | VIX | NY Cash | 60m | FADE_DOWN | GapSmall | `60.6%` | 188 | `56` | `1.54` | `40R` | `-12.0R` | `4.89` |
| 1384 | GBPUSD | NY | 45m | FADE_UP | OR_Q1_Tight | `60.3%` | 209 | `26` | `1.52` | `43R` | `-6.0R` | `4.89` |
| 1385 | GBPJPY | London | 45m | FADE_UP | OR_Q4_Wide | `60.3%` | 209 | `26` | `1.52` | `43R` | `-7.0R` | `4.89` |
| 1386 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | RSI_50-70 | `60.4%` | 202 | `25` | `1.52` | `42R` | `-8.0R` | `4.89` |
| 1387 | GBPJPY | London | 15m | FADE_UP | BtwCloseHigh | `59.7%` | 253 | `31` | `1.48` | `49R` | `-11.0R` | `4.89` |
| 1388 | GBPJPY | London | 60m | FADE_UP | BtwCloseHigh | `58.8%` | 342 | `42` | `1.43` | `60R` | `-10.0R` | `4.89` |
| 1389 | VIX | NY Cash | 45m | FADE_UP | RSI_30-50 | `62.7%` | 102 | `31` | `1.68` | `26R` | `-5.0R` | `4.89` |
| 1390 | XAGUSD | NY | 45m | FADE_DOWN | BtwLowClose | `61.5%` | 143 | `18` | `1.60` | `33R` | `-5.0R` | `4.89` |
| 1391 | SP500 | NY Cash | 60m | FADE_DOWN | BtwLowClose | `61.5%` | 143 | `18` | `1.60` | `33R` | `-9.0R` | `4.89` |
| 1392 | EURJPY | Tokyo | 60m | FADE_UP | ATR-10% | `67.7%` | 31 | `4` | `2.10` | `11R` | `-4.0R` | `4.89` |
| 1393 | EURJPY | London | 60m | FADE_UP | AbovePD+RSI_D>65 | `67.7%` | 31 | `4` | `2.10` | `11R` | `-4.0R` | `4.89` |
| 1394 | XAUUSD | London | 45m | FADE_DOWN | RSI>70 | `67.7%` | 31 | `4` | `2.10` | `11R` | `-4.0R` | `4.89` |
| 1395 | BRENT | London | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `67.7%` | 31 | `4` | `2.10` | `11R` | `-3.0R` | `4.89` |
| 1396 | NASDAQ100 | Pre-Market | 60m | FADE_UP | ATR-10% | `67.7%` | 31 | `4` | `2.10` | `11R` | `-5.0R` | `4.89` |
| 1397 | NASDAQ100 | NY Cash | 60m | FADE_UP | GapSmall | `58.3%` | 396 | `49` | `1.40` | `66R` | `-7.0R` | `4.88` |
| 1398 | EURUSD | London | 15m | FADE_DOWN | ATR+10% | `66.7%` | 39 | `5` | `2.00` | `13R` | `-2.0R` | `4.88` |
| 1399 | AUDUSD | London | 30m | FADE_DOWN | ATR+10% | `66.7%` | 39 | `5` | `2.00` | `13R` | `-2.0R` | `4.88` |
| 1400 | EURJPY | Tokyo | 45m | FADE_DOWN | ATR+10% | `66.7%` | 39 | `5` | `2.00` | `13R` | `-3.0R` | `4.88` |
| 1401 | EURUSD | London | 15m | FADE_DOWN | Thu | `61.8%` | 131 | `16` | `1.62` | `31R` | `-6.0R` | `4.88` |
| 1402 | XAGUSD | NY | 15m | FADE_DOWN | RSI_50-70 | `59.3%` | 285 | `35` | `1.46` | `53R` | `-8.0R` | `4.88` |
| 1403 | EURJPY | London | 60m | FADE_DOWN | RSI_30-50 | `57.9%` | 463 | `57` | `1.37` | `73R` | `-6.0R` | `4.88` |
| 1404 | NASDAQ100 | NY Cash | 60m | FADE_UP | BASE | `57.9%` | 463 | `57` | `1.37` | `73R` | `-10.0R` | `4.88` |
| 1405 | NATGAS | NY | 30m | FADE_DOWN | BASE | `56.4%` | 805 | `99` | `1.29` | `103R` | `-11.0R` | `4.88` |
| 1406 | GBPJPY | Tokyo | 45m | FADE_DOWN | ATR+10% | `65.4%` | 52 | `7` | `1.89` | `16R` | `-4.0R` | `4.88` |
| 1407 | NATGAS | NY | 15m | FADE_UP | BtwCloseHigh | `59.9%` | 232 | `29` | `1.49` | `46R` | `-7.0R` | `4.88` |
| 1408 | EURJPY | Tokyo | 45m | FADE_DOWN | BtwCloseHigh | `57.1%` | 613 | `75` | `1.33` | `87R` | `-16.0R` | `4.88` |
| 1409 | EURJPY | Tokyo | 30m | FADE_UP | RSI_50-70 | `57.1%` | 602 | `74` | `1.33` | `86R` | `-15.0R` | `4.88` |
| 1410 | BRENT | London | 30m | FADE_UP | RSI_50-70 | `58.4%` | 380 | `47` | `1.41` | `64R` | `-8.0R` | `4.88` |
| 1411 | WTI | NY Main | 45m | FADE_DOWN | BelowPD | `61.3%` | 150 | `18` | `1.59` | `34R` | `-9.0R` | `4.87` |
| 1412 | WTI | NY Main | 60m | FADE_UP | Thu | `61.3%` | 150 | `18` | `1.59` | `34R` | `-7.0R` | `4.87` |
| 1413 | XAGUSD | NY | 60m | FADE_UP | AbovePD | `62.9%` | 97 | `12` | `1.69` | `25R` | `-5.0R` | `4.87` |
| 1414 | AUDUSD | London | 30m | FADE_DOWN | Thu | `60.8%` | 176 | `22` | `1.55` | `38R` | `-7.0R` | `4.87` |
| 1415 | GBPJPY | London | 45m | FADE_DOWN | Mon | `60.8%` | 176 | `22` | `1.55` | `38R` | `-5.0R` | `4.87` |
| 1416 | WTI | London Initial | 45m | FADE_UP | Fri | `60.8%` | 176 | `22` | `1.55` | `38R` | `-8.0R` | `4.87` |
| 1417 | WTI | London Initial | 45m | FADE_DOWN | Thu | `60.8%` | 176 | `22` | `1.55` | `38R` | `-6.0R` | `4.87` |
| 1418 | GBPAUD | London | 30m | FADE_DOWN | OR_Q4_Wide | `60.0%` | 225 | `28` | `1.50` | `45R` | `-8.0R` | `4.87` |
| 1419 | WTI | London Initial | 30m | FADE_DOWN | RSI_50-70 | `60.0%` | 225 | `28` | `1.50` | `45R` | `-7.0R` | `4.87` |
| 1420 | NATGAS | NY | 30m | FADE_UP | GapSmall | `57.1%` | 604 | `74` | `1.33` | `86R` | `-15.0R` | `4.87` |
| 1421 | BRENT | NY | 30m | FADE_DOWN | RSI_30-50 | `58.1%` | 418 | `51` | `1.39` | `68R` | `-11.0R` | `4.87` |
| 1422 | EURUSD | London | 45m | FADE_DOWN | RSI_30-50 | `57.8%` | 467 | `57` | `1.37` | `73R` | `-11.0R` | `4.87` |
| 1423 | BRENT | London | 60m | FADE_DOWN | Tue | `60.5%` | 190 | `23` | `1.53` | `40R` | `-8.0R` | `4.87` |
| 1424 | EURJPY | London | 30m | FADE_UP | Fri | `60.4%` | 197 | `24` | `1.53` | `41R` | `-9.0R` | `4.87` |
| 1425 | WTI | NY Main | 30m | FADE_DOWN | AbovePD | `60.4%` | 197 | `25` | `1.53` | `41R` | `-9.0R` | `4.87` |
| 1426 | XAUUSD | London | 15m | MOMENTUM_UP | OR_Q1_Tight | `55.5%` | 110 | `18` | `1.87` | `42R` | `-4.5R` | `4.87` |
| 1427 | GBPJPY | London | 15m | FADE_UP | GapSmall | `56.7%` | 689 | `84` | `1.31` | `93R` | `-17.0R` | `4.87` |
| 1428 | GBPJPY | London | 60m | FADE_DOWN | GapSmall | `56.6%` | 726 | `89` | `1.30` | `96R` | `-12.0R` | `4.87` |
| 1429 | XAGUSD | NY | 15m | FADE_UP | RSI_30-50 | `59.3%` | 280 | `34` | `1.46` | `52R` | `-8.0R` | `4.86` |
| 1430 | EURJPY | London | 15m | FADE_UP | RSI_50-70 | `58.2%` | 411 | `50` | `1.39` | `67R` | `-9.0R` | `4.86` |
| 1431 | EURUSD | London | 60m | FADE_DOWN | BASE | `56.1%` | 888 | `109` | `1.28` | `108R` | `-12.0R` | `4.86` |
| 1432 | BRENT | NY | 15m | FADE_UP | BtwCloseHigh | `59.8%` | 234 | `29` | `1.49` | `46R` | `-12.0R` | `4.86` |
| 1433 | GBPAUD | Sydney | 45m | FADE_UP | RSI_50-70 | `64.9%` | 57 | `7` | `1.85` | `17R` | `-4.0R` | `4.86` |
| 1434 | XAGUSD | London | 15m | FADE_DOWN | Thu | `62.4%` | 109 | `13` | `1.66` | `27R` | `-5.0R` | `4.85` |
| 1435 | EURJPY | London | 45m | FADE_UP | RSI_30-50 | `59.1%` | 298 | `37` | `1.44` | `54R` | `-10.0R` | `4.85` |
| 1436 | XAGUSD | London | 45m | FADE_DOWN | Mon | `60.8%` | 171 | `21` | `1.55` | `37R` | `-6.0R` | `4.85` |
| 1437 | WTI | NY Main | 60m | FADE_DOWN | RSI_30-50 | `58.6%` | 350 | `43` | `1.41` | `60R` | `-11.0R` | `4.85` |
| 1438 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | BASE | `60.7%` | 178 | `22` | `1.54` | `38R` | `-4.0R` | `4.85` |
| 1439 | NATGAS | NY | 45m | FADE_DOWN | RSI_50-70 | `59.7%` | 243 | `30` | `1.48` | `47R` | `-7.0R` | `4.85` |
| 1440 | GBPJPY | London | 30m | FADE_UP | Fri | `60.5%` | 185 | `23` | `1.53` | `39R` | `-7.0R` | `4.85` |
| 1441 | XAGUSD | London | 60m | FADE_UP | Wed | `60.3%` | 199 | `25` | `1.52` | `41R` | `-7.0R` | `4.85` |
| 1442 | AUDUSD | London | 45m | FADE_UP | Mon | `60.4%` | 192 | `24` | `1.53` | `40R` | `-9.0R` | `4.85` |
| 1443 | NASDAQ100 | NY Cash | 30m | FADE_UP | BtwLowClose | `60.4%` | 192 | `24` | `1.53` | `40R` | `-4.0R` | `4.85` |
| 1444 | USDJPY | Tokyo | 60m | FADE_UP | BASE | `55.9%` | 930 | `114` | `1.27` | `110R` | `-14.0R` | `4.85` |
| 1445 | USDJPY | Tokyo | 60m | FADE_UP | GapSmall | `55.9%` | 930 | `114` | `1.27` | `110R` | `-14.0R` | `4.85` |
| 1446 | GBPJPY | London | 15m | FADE_UP | BASE | `56.3%` | 805 | `98` | `1.29` | `101R` | `-22.0R` | `4.85` |
| 1447 | GBPUSD | London | 60m | FADE_UP | GapSmall | `56.1%` | 846 | `103` | `1.28` | `104R` | `-14.0R` | `4.85` |
| 1448 | GBPJPY | Tokyo | 60m | FADE_UP | OR_Q4_Wide | `59.7%` | 236 | `29` | `1.48` | `46R` | `-8.0R` | `4.85` |
| 1449 | GBPJPY | London | 30m | FADE_DOWN | BtwLowClose | `58.8%` | 325 | `40` | `1.43` | `57R` | `-7.0R` | `4.84` |
| 1450 | EURUSD | NY | 45m | FADE_UP | RSI_D>65 | `64.5%` | 62 | `8` | `1.82` | `18R` | `-3.0R` | `4.84` |
| 1451 | GBPJPY | London | 45m | FADE_UP | BASE | `55.8%` | 966 | `118` | `1.26` | `112R` | `-12.0R` | `4.84` |
| 1452 | WTI | NY Main | 45m | FADE_UP | BtwLowClose | `59.8%` | 229 | `28` | `1.49` | `45R` | `-15.0R` | `4.84` |
| 1453 | WTI | NY Main | 60m | FADE_DOWN | RSI_50-70 | `59.8%` | 229 | `28` | `1.49` | `45R` | `-7.0R` | `4.84` |
| 1454 | GBPUSD | NY | 45m | FADE_DOWN | RSI_30-50 | `58.9%` | 309 | `38` | `1.43` | `55R` | `-12.0R` | `4.84` |
| 1455 | WTI | London Initial | 30m | FADE_DOWN | BtwLowClose | `59.3%` | 268 | `33` | `1.46` | `50R` | `-11.0R` | `4.84` |
| 1456 | EURJPY | London | 60m | FADE_DOWN | Fri | `61.0%` | 159 | `20` | `1.56` | `35R` | `-7.0R` | `4.84` |
| 1457 | GBPUSD | NY | 60m | FADE_DOWN | Mon | `62.5%` | 104 | `13` | `1.67` | `26R` | `-5.0R` | `4.84` |
| 1458 | WTI | London Initial | 15m | FADE_DOWN | AbovePD | `63.6%` | 77 | `10` | `1.75` | `21R` | `-6.0R` | `4.84` |
| 1459 | AUDUSD | London | 45m | FADE_UP | RSI_30-50 | `58.7%` | 327 | `40` | `1.42` | `57R` | `-8.0R` | `4.84` |
| 1460 | GBPUSD | NY | 60m | FADE_DOWN | BtwCloseHigh | `61.4%` | 140 | `18` | `1.59` | `32R` | `-6.0R` | `4.83` |
| 1461 | XAUUSD | London | 30m | MOMENTUM_DOWN | BelowPD | `55.1%` | 118 | `15` | `1.84` | `44R` | `-7.0R` | `4.83` |
| 1462 | AUDUSD | London | 60m | FADE_DOWN | RSI<30 | `63.9%` | 72 | `9` | `1.77` | `20R` | `-3.0R` | `4.83` |
| 1463 | EURJPY | Tokyo | 45m | FADE_UP | Wed | `60.0%` | 215 | `26` | `1.50` | `43R` | `-9.0R` | `4.83` |
| 1464 | XAGUSD | London | 30m | FADE_UP | RSI_30-50 | `58.6%` | 345 | `42` | `1.41` | `59R` | `-8.0R` | `4.83` |
| 1465 | SP500 | Pre-Market | 45m | FADE_UP | Fri | `60.8%` | 166 | `20` | `1.55` | `36R` | `-8.0R` | `4.83` |
| 1466 | GBPJPY | London | 30m | FADE_UP | BASE | `55.8%` | 933 | `114` | `1.26` | `109R` | `-14.0R` | `4.83` |
| 1467 | BRENT | NY | 60m | FADE_DOWN | Tue | `61.7%` | 128 | `16` | `1.61` | `30R` | `-8.0R` | `4.83` |
| 1468 | XAUUSD | NY | 60m | FADE_DOWN | GapSmall | `59.1%` | 286 | `35` | `1.44` | `52R` | `-7.0R` | `4.83` |
| 1469 | GBPUSD | NY | 15m | FADE_DOWN | BASE | `56.3%` | 765 | `94` | `1.29` | `97R` | `-11.0R` | `4.83` |
| 1470 | AUDUSD | London | 30m | FADE_DOWN | Fri | `60.4%` | 187 | `23` | `1.53` | `39R` | `-5.0R` | `4.83` |
| 1471 | XAUUSD | London | 45m | FADE_UP | BASE | `55.7%` | 967 | `118` | `1.26` | `111R` | `-18.0R` | `4.83` |
| 1472 | GBPJPY | Tokyo | 60m | FADE_DOWN | RSI_50-70 | `58.7%` | 329 | `40` | `1.42` | `57R` | `-10.0R` | `4.83` |
| 1473 | EURJPY | Tokyo | 45m | FADE_UP | BtwLowClose | `58.4%` | 365 | `45` | `1.40` | `61R` | `-9.0R` | `4.82` |
| 1474 | XAGUSD | London | 15m | FADE_UP | Mon | `61.2%` | 147 | `18` | `1.58` | `33R` | `-9.0R` | `4.82` |
| 1475 | BRENT | NY | 45m | FADE_UP | Fri | `61.2%` | 147 | `18` | `1.58` | `33R` | `-7.0R` | `4.82` |
| 1476 | GBPJPY | Tokyo | 45m | FADE_DOWN | BtwLowClose | `58.5%` | 347 | `43` | `1.41` | `59R` | `-9.0R` | `4.82` |
| 1477 | NATGAS | NY | 60m | FADE_DOWN | Mon | `62.6%` | 99 | `12` | `1.68` | `25R` | `-4.0R` | `4.82` |
| 1478 | USDJPY | NY | 60m | FADE_DOWN | RSI<30 | `65.9%` | 44 | `6` | `1.93` | `14R` | `-3.0R` | `4.82` |
| 1479 | SP500 | Pre-Market | 30m | SHAKEOUT_DOWN | ATR+10% | `65.9%` | 44 | `5` | `1.93` | `14R` | `-4.0R` | `4.82` |
| 1480 | GBPJPY | Tokyo | 30m | FADE_DOWN | Tue | `61.0%` | 154 | `19` | `1.57` | `34R` | `-5.0R` | `4.82` |
| 1481 | EURJPY | London | 45m | FADE_DOWN | Fri | `61.0%` | 154 | `19` | `1.57` | `34R` | `-6.0R` | `4.82` |
| 1482 | GBPAUD | London | 15m | FADE_DOWN | Tue | `61.0%` | 154 | `19` | `1.57` | `34R` | `-6.0R` | `4.82` |
| 1483 | GBPJPY | London | 30m | FADE_DOWN | RSI_D>65 | `61.5%` | 135 | `17` | `1.60` | `31R` | `-4.0R` | `4.81` |
| 1484 | AUDUSD | London | 45m | FADE_UP | Fri | `60.0%` | 210 | `26` | `1.50` | `42R` | `-8.0R` | `4.81` |
| 1485 | WTI | London Initial | 30m | FADE_UP | OR_Q4_Wide | `59.4%` | 256 | `32` | `1.46` | `48R` | `-9.0R` | `4.81` |
| 1486 | BRENT | NY | 45m | FADE_DOWN | AbovePD | `60.9%` | 161 | `20` | `1.56` | `35R` | `-9.0R` | `4.81` |
| 1487 | BRENT | NY | 30m | FADE_DOWN | RSI_50-70 | `58.8%` | 306 | `38` | `1.43` | `54R` | `-13.0R` | `4.81` |
| 1488 | EURUSD | London | 30m | SHAKEOUT_DOWN | OR_Q1_Tight | `62.2%` | 111 | `14` | `1.64` | `27R` | `-8.0R` | `4.81` |
| 1489 | USDJPY | NY | 15m | MOMENTUM_DOWN | RSI<30 | `56.8%` | 74 | `9` | `1.97` | `31R` | `-5.5R` | `4.81` |
| 1490 | GBPUSD | NY | 15m | FADE_DOWN | BtwLowClose | `59.7%` | 233 | `29` | `1.48` | `45R` | `-7.0R` | `4.81` |
| 1491 | EURJPY | London | 30m | FADE_DOWN | BtwLowClose | `59.1%` | 281 | `34` | `1.44` | `51R` | `-7.0R` | `4.81` |
| 1492 | BRENT | London | 60m | FADE_DOWN | RSI_50-70 | `59.1%` | 281 | `35` | `1.44` | `51R` | `-11.0R` | `4.81` |
| 1493 | USDJPY | NY | 30m | FADE_UP | BtwLowClose | `60.7%` | 168 | `21` | `1.55` | `36R` | `-6.0R` | `4.81` |
| 1494 | XAGUSD | London | 45m | FADE_DOWN | BtwLowClose | `58.7%` | 315 | `39` | `1.42` | `55R` | `-14.0R` | `4.81` |
| 1495 | XAGUSD | London | 15m | FADE_UP | BtwCloseHigh | `60.2%` | 196 | `24` | `1.51` | `40R` | `-7.0R` | `4.81` |
| 1496 | XAUUSD | NY | 45m | FADE_UP | BelowPD | `62.8%` | 94 | `12` | `1.69` | `24R` | `-4.0R` | `4.81` |
| 1497 | XAGUSD | NY | 60m | FADE_DOWN | Wed | `62.8%` | 94 | `12` | `1.69` | `24R` | `-6.0R` | `4.81` |
| 1498 | GBPUSD | London | 45m | FADE_DOWN | BtwLowClose | `58.3%` | 360 | `44` | `1.40` | `60R` | `-12.0R` | `4.81` |
| 1499 | EURJPY | Tokyo | 30m | FADE_DOWN | Thu | `60.6%` | 175 | `22` | `1.54` | `37R` | `-6.0R` | `4.81` |
| 1500 | GBPUSD | London | 45m | FADE_UP | BtwLowClose | `58.5%` | 342 | `42` | `1.41` | `58R` | `-9.0R` | `4.81` |
| 1501 | USDJPY | NY | 45m | FADE_DOWN | RSI_50-70 | `60.3%` | 189 | `23` | `1.52` | `39R` | `-4.0R` | `4.81` |
| 1502 | GBPJPY | London | 60m | FADE_UP | RSI_50-70 | `57.0%` | 579 | `71` | `1.33` | `81R` | `-8.0R` | `4.81` |
| 1503 | XAUUSD | NY | 30m | FADE_UP | Wed | `61.3%` | 142 | `17` | `1.58` | `32R` | `-7.0R` | `4.80` |
| 1504 | XAUUSD | NY | 45m | FADE_UP | BtwLowClose | `61.3%` | 142 | `17` | `1.58` | `32R` | `-5.0R` | `4.80` |
| 1505 | XAGUSD | NY | 15m | FADE_DOWN | GapSmall | `57.3%` | 513 | `63` | `1.34` | `75R` | `-9.0R` | `4.80` |
| 1506 | EURJPY | London | 60m | FADE_UP | OR_Q1_Tight | `59.5%` | 242 | `30` | `1.47` | `46R` | `-7.0R` | `4.80` |
| 1507 | XAGUSD | London | 30m | FADE_UP | BtwCloseHigh | `58.8%` | 308 | `38` | `1.43` | `54R` | `-7.0R` | `4.80` |
| 1508 | SP500 | NY Cash | 45m | FADE_DOWN | BtwCloseHigh | `59.8%` | 219 | `27` | `1.49` | `43R` | `-5.0R` | `4.80` |
| 1509 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | OR_Q4_Wide | `59.8%` | 219 | `36` | `1.49` | `43R` | `-6.0R` | `4.80` |
| 1510 | GBPUSD | NY | 45m | FADE_UP | RSI_50-70 | `58.3%` | 362 | `44` | `1.40` | `60R` | `-12.0R` | `4.80` |
| 1511 | EURJPY | London | 60m | FADE_DOWN | BtwCloseHigh | `59.3%` | 258 | `32` | `1.46` | `48R` | `-9.0R` | `4.80` |
| 1512 | XAGUSD | London | 15m | FADE_UP | Tue | `61.1%` | 149 | `18` | `1.57` | `33R` | `-7.0R` | `4.79` |
| 1513 | WTI | NY Main | 60m | FADE_UP | RSI_30-50 | `59.9%` | 212 | `26` | `1.49` | `42R` | `-8.0R` | `4.79` |
| 1514 | GBPJPY | Tokyo | 60m | FADE_DOWN | BtwLowClose | `58.1%` | 382 | `47` | `1.39` | `62R` | `-7.0R` | `4.79` |
| 1515 | GBPJPY | Tokyo | 15m | FADE_DOWN | RSI_50-70 | `59.6%` | 235 | `29` | `1.47` | `45R` | `-8.0R` | `4.79` |
| 1516 | USDJPY | Tokyo | 45m | FADE_UP | RSI_30-50 | `58.9%` | 292 | `36` | `1.43` | `52R` | `-9.0R` | `4.79` |
| 1517 | GBPUSD | NY | 45m | FADE_DOWN | Tue | `61.5%` | 130 | `16` | `1.60` | `30R` | `-6.0R` | `4.79` |
| 1518 | XAGUSD | NY | 15m | FADE_UP | OR_Q1_Tight | `60.0%` | 205 | `27` | `1.50` | `41R` | `-5.0R` | `4.79` |
| 1519 | BRENT | London | 30m | FADE_DOWN | RSI_50-70 | `60.0%` | 205 | `25` | `1.50` | `41R` | `-9.0R` | `4.79` |
| 1520 | GBPJPY | London | 45m | FADE_UP | GapSmall | `56.0%` | 836 | `102` | `1.27` | `100R` | `-13.0R` | `4.79` |
| 1521 | GBPUSD | London | 15m | FADE_UP | BtwCloseHigh | `59.1%` | 276 | `34` | `1.44` | `50R` | `-8.0R` | `4.79` |
| 1522 | XAGUSD | London | 45m | FADE_UP | BtwCloseHigh | `58.5%` | 337 | `41` | `1.41` | `57R` | `-13.0R` | `4.79` |
| 1523 | AUDUSD | London | 30m | FADE_UP | Fri | `60.2%` | 191 | `23` | `1.51` | `39R` | `-10.0R` | `4.79` |
| 1524 | GBPJPY | Tokyo | 15m | FADE_DOWN | BtwLowClose | `59.2%` | 260 | `32` | `1.45` | `48R` | `-6.0R` | `4.79` |
| 1525 | EURJPY | London | 60m | FADE_DOWN | OR_Q1_Tight | `59.4%` | 244 | `30` | `1.46` | `46R` | `-7.0R` | `4.78` |
| 1526 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | BtwCloseHigh | `65.3%` | 49 | `6` | `1.88` | `15R` | `-6.0R` | `4.78` |
| 1527 | EURUSD | London | 30m | FADE_DOWN | OR_Q1_Tight | `60.3%` | 184 | `23` | `1.52` | `38R` | `-5.0R` | `4.78` |
| 1528 | GBPAUD | London | 30m | FADE_DOWN | AbovePD | `60.5%` | 177 | `22` | `1.53` | `37R` | `-8.0R` | `4.78` |
| 1529 | USDJPY | NY | 45m | FADE_UP | BtwLowClose | `61.3%` | 137 | `17` | `1.58` | `31R` | `-6.0R` | `4.78` |
| 1530 | SP500 | Pre-Market | 45m | FADE_UP | BelowPD | `61.3%` | 137 | `17` | `1.58` | `31R` | `-11.0R` | `4.78` |
| 1531 | XAUUSD | NY | 45m | FADE_UP | OR_Q4_Wide | `63.1%` | 84 | `14` | `1.71` | `22R` | `-7.0R` | `4.78` |
| 1532 | GBPJPY | London | 30m | FADE_UP | GapSmall | `56.0%` | 803 | `98` | `1.27` | `97R` | `-12.0R` | `4.78` |
| 1533 | WTI | London Initial | 30m | FADE_UP | RSI_30-50 | `59.5%` | 237 | `29` | `1.47` | `45R` | `-6.0R` | `4.78` |
| 1534 | BRENT | London | 15m | FADE_UP | RSI_D<35 | `66.7%` | 36 | `5` | `2.00` | `12R` | `-3.0R` | `4.78` |
| 1535 | SP500 | Pre-Market | 60m | FADE_UP | ATR-10% | `66.7%` | 36 | `5` | `2.00` | `12R` | `-4.0R` | `4.78` |
| 1536 | WTI | NY Main | 45m | FADE_DOWN | RSI_50-70 | `59.3%` | 253 | `31` | `1.46` | `47R` | `-11.0R` | `4.78` |
| 1537 | XAUUSD | NY | 30m | FADE_DOWN | GapSmall | `57.6%` | 448 | `55` | `1.36` | `68R` | `-9.0R` | `4.77` |
| 1538 | USDJPY | NY | 45m | FADE_UP | BelowPD | `62.4%` | 101 | `13` | `1.66` | `25R` | `-7.0R` | `4.77` |
| 1539 | SP500 | Pre-Market | 30m | SHAKEOUT_DOWN | RSI_50-70 | `62.4%` | 101 | `12` | `1.66` | `25R` | `-6.0R` | `4.77` |
| 1540 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | GapSmall | `61.1%` | 144 | `18` | `1.57` | `32R` | `-4.0R` | `4.77` |
| 1541 | VIX | NY Cash | 30m | FADE_UP | RSI_50-70 | `61.6%` | 125 | `37` | `1.60` | `29R` | `-4.0R` | `4.77` |
| 1542 | NASDAQ100 | Pre-Market | 45m | FADE_UP | GapSmall | `56.3%` | 712 | `87` | `1.29` | `90R` | `-14.0R` | `4.77` |
| 1543 | WTI | London Initial | 30m | FADE_DOWN | Mon | `60.9%` | 151 | `19` | `1.56` | `33R` | `-4.0R` | `4.77` |
| 1544 | WTI | NY Main | 30m | FADE_UP | Fri | `60.9%` | 151 | `19` | `1.56` | `33R` | `-5.0R` | `4.77` |
| 1545 | GBPJPY | Tokyo | 45m | FADE_DOWN | Mon | `60.1%` | 193 | `24` | `1.51` | `39R` | `-7.0R` | `4.77` |
| 1546 | XAGUSD | London | 45m | FADE_UP | Wed | `60.1%` | 193 | `24` | `1.51` | `39R` | `-6.0R` | `4.77` |
| 1547 | XAUUSD | London | 30m | FADE_DOWN | BASE | `56.0%` | 815 | `100` | `1.27` | `97R` | `-12.0R` | `4.76` |
| 1548 | EURJPY | London | 45m | FADE_DOWN | RSI_30-50 | `57.6%` | 441 | `54` | `1.36` | `67R` | `-9.0R` | `4.76` |
| 1549 | SP500 | NY Cash | 30m | FADE_DOWN | RSI_D>65 | `60.8%` | 158 | `20` | `1.55` | `34R` | `-4.0R` | `4.76` |
| 1550 | NASDAQ100 | Pre-Market | 15m | FADE_UP | RSI_50-70 | `60.8%` | 158 | `19` | `1.55` | `34R` | `-9.0R` | `4.76` |
| 1551 | EURUSD | NY | 45m | FADE_DOWN | RSI<30 | `64.8%` | 54 | `7` | `1.84` | `16R` | `-5.0R` | `4.76` |
| 1552 | GBPUSD | London | 15m | SHAKEOUT_UP | OR_Q1_Tight | `64.8%` | 54 | `7` | `1.84` | `16R` | `-2.0R` | `4.76` |
| 1553 | XAGUSD | NY | 30m | FADE_DOWN | RSI<30 | `64.8%` | 54 | `7` | `1.84` | `16R` | `-5.0R` | `4.76` |
| 1554 | SP500 | NY Cash | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `64.8%` | 54 | `7` | `1.84` | `16R` | `-3.0R` | `4.76` |
| 1555 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | GapSmall | `57.0%` | 553 | `68` | `1.32` | `77R` | `-8.0R` | `4.76` |
| 1556 | USDJPY | Tokyo | 45m | FADE_DOWN | Tue | `60.3%` | 179 | `22` | `1.52` | `37R` | `-6.0R` | `4.76` |
| 1557 | NATGAS | NY | 30m | FADE_UP | Thu | `60.6%` | 165 | `20` | `1.54` | `35R` | `-7.0R` | `4.76` |
| 1558 | EURJPY | Tokyo | 45m | FADE_DOWN | Wed | `60.5%` | 172 | `21` | `1.53` | `36R` | `-5.0R` | `4.76` |
| 1559 | EURJPY | London | 60m | FADE_UP | Tue | `60.5%` | 172 | `21` | `1.53` | `36R` | `-8.0R` | `4.76` |
| 1560 | XAUUSD | NY | 15m | FADE_DOWN | Wed | `60.5%` | 172 | `21` | `1.53` | `36R` | `-5.0R` | `4.76` |
| 1561 | GBPUSD | London | 15m | FADE_UP | GapSmall | `56.1%` | 748 | `92` | `1.28` | `92R` | `-13.0R` | `4.76` |
| 1562 | XAUUSD | London | 60m | FADE_DOWN | RSI_30-50 | `57.1%` | 520 | `64` | `1.33` | `74R` | `-8.0R` | `4.76` |
| 1563 | GBPJPY | Tokyo | 30m | FADE_DOWN | OR_Q4_Wide | `59.3%` | 248 | `31` | `1.46` | `46R` | `-7.0R` | `4.76` |
| 1564 | EURUSD | London | 60m | FADE_UP | RSI>70 | `62.5%` | 96 | `12` | `1.67` | `24R` | `-8.0R` | `4.75` |
| 1565 | GBPAUD | London | 15m | FADE_DOWN | GapSmall | `56.6%` | 631 | `77` | `1.30` | `83R` | `-13.0R` | `4.75` |
| 1566 | GBPJPY | London | 15m | FADE_DOWN | RSI_D<35 | `63.8%` | 69 | `10` | `1.76` | `19R` | `-4.0R` | `4.75` |
| 1567 | XAGUSD | London | 15m | FADE_UP | RSI_D<35 | `63.8%` | 69 | `10` | `1.76` | `19R` | `-5.0R` | `4.75` |
| 1568 | XAGUSD | London | 15m | SHAKEOUT_DOWN | Tue | `63.8%` | 69 | `9` | `1.76` | `19R` | `-4.0R` | `4.75` |
| 1569 | SP500 | Pre-Market | 60m | FADE_DOWN | RSI<30 | `63.8%` | 69 | `9` | `1.76` | `19R` | `-3.0R` | `4.75` |
| 1570 | AUDUSD | London | 45m | FADE_UP | OR_Q4_Wide | `59.6%` | 225 | `28` | `1.47` | `43R` | `-11.0R` | `4.75` |
| 1571 | XAGUSD | London | 60m | FADE_UP | BtwCloseHigh | `58.4%` | 327 | `40` | `1.40` | `55R` | `-8.0R` | `4.75` |
| 1572 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | BtwCloseHigh | `64.1%` | 64 | `8` | `1.78` | `18R` | `-5.0R` | `4.75` |
| 1573 | USDJPY | NY | 45m | FADE_UP | Tue | `61.7%` | 120 | `15` | `1.61` | `28R` | `-4.0R` | `4.75` |
| 1574 | XAGUSD | London | 15m | SHAKEOUT_DOWN | RSI_50-70 | `61.7%` | 120 | `15` | `1.61` | `28R` | `-4.0R` | `4.75` |
| 1575 | XAGUSD | NY | 30m | FADE_UP | RSI_D>65 | `61.7%` | 120 | `15` | `1.61` | `28R` | `-5.0R` | `4.75` |
| 1576 | XAGUSD | NY | 30m | FADE_DOWN | RSI_30-50 | `58.5%` | 318 | `39` | `1.41` | `54R` | `-6.0R` | `4.75` |
| 1577 | EURUSD | London | 45m | FADE_UP | OR_Q1_Tight | `59.3%` | 241 | `30` | `1.46` | `45R` | `-14.0R` | `4.75` |
| 1578 | EURJPY | Tokyo | 60m | FADE_UP | RSI_50-70 | `56.7%` | 609 | `74` | `1.31` | `81R` | `-12.0R` | `4.75` |
| 1579 | GBPUSD | London | 45m | FADE_DOWN | RSI_D<35 | `62.0%` | 108 | `14` | `1.63` | `26R` | `-5.0R` | `4.75` |
| 1580 | EURJPY | Tokyo | 30m | FADE_DOWN | Mon | `60.0%` | 195 | `24` | `1.50` | `39R` | `-9.0R` | `4.75` |
| 1581 | BRENT | NY | 60m | FADE_UP | BtwLowClose | `60.0%` | 195 | `24` | `1.50` | `39R` | `-11.0R` | `4.75` |
| 1582 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | BASE | `57.2%` | 491 | `60` | `1.34` | `71R` | `-13.0R` | `4.75` |
| 1583 | GBPUSD | NY | 45m | FADE_DOWN | Mon | `61.0%` | 146 | `18` | `1.56` | `32R` | `-6.0R` | `4.74` |
| 1584 | XAUUSD | London | 30m | FADE_DOWN | AbovePD | `61.0%` | 146 | `18` | `1.56` | `32R` | `-8.0R` | `4.74` |
| 1585 | GBPUSD | London | 45m | FADE_DOWN | RSI_50-70 | `58.4%` | 329 | `41` | `1.40` | `55R` | `-9.0R` | `4.74` |
| 1586 | XAUUSD | NY | 45m | FADE_DOWN | RSI_50-70 | `60.2%` | 181 | `22` | `1.51` | `37R` | `-7.0R` | `4.74` |
| 1587 | EURJPY | London | 30m | FADE_DOWN | Thu | `60.3%` | 174 | `21` | `1.52` | `36R` | `-8.0R` | `4.74` |
| 1588 | NATGAS | NY | 60m | FADE_UP | Tue | `62.6%` | 91 | `11` | `1.68` | `23R` | `-5.0R` | `4.74` |
| 1589 | EURUSD | NY | 30m | FADE_UP | RSI_50-70 | `57.9%` | 378 | `46` | `1.38` | `60R` | `-12.0R` | `4.74` |
| 1590 | BRENT | NY | 60m | FADE_DOWN | Fri | `61.4%` | 127 | `16` | `1.59` | `29R` | `-4.0R` | `4.74` |
| 1591 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | Wed | `61.4%` | 127 | `16` | `1.59` | `29R` | `-5.0R` | `4.74` |
| 1592 | EURJPY | Tokyo | 30m | MOMENTUM_DOWN | RSI_D<35 | `57.1%` | 63 | `9` | `2.00` | `27R` | `-4.5R` | `4.74` |
| 1593 | GBPAUD | London | 45m | FADE_UP | BtwCloseHigh | `59.3%` | 243 | `30` | `1.45` | `45R` | `-7.0R` | `4.73` |
| 1594 | EURJPY | Tokyo | 15m | FADE_DOWN | BtwCloseHigh | `57.1%` | 497 | `61` | `1.33` | `71R` | `-11.0R` | `4.73` |
| 1595 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | BASE | `56.3%` | 671 | `82` | `1.29` | `85R` | `-12.0R` | `4.73` |
| 1596 | BRENT | London | 30m | FADE_UP | OR_Q4_Wide | `59.1%` | 252 | `32` | `1.45` | `46R` | `-10.0R` | `4.73` |
| 1597 | XAUUSD | London | 45m | FADE_UP | GapSmall | `55.7%` | 862 | `105` | `1.26` | `98R` | `-13.0R` | `4.73` |
| 1598 | XAUUSD | NY | 60m | FADE_UP | GapSmall | `58.6%` | 304 | `37` | `1.41` | `52R` | `-11.0R` | `4.73` |
| 1599 | GBPUSD | NY | 30m | FADE_UP | BtwLowClose | `59.5%` | 220 | `27` | `1.47` | `42R` | `-6.0R` | `4.73` |
| 1600 | XAGUSD | NY | 60m | FADE_DOWN | BtwLowClose | `61.7%` | 115 | `14` | `1.61` | `27R` | `-4.0R` | `4.73` |
| 1601 | GBPUSD | London | 30m | FADE_DOWN | OR_Q4_Wide | `59.3%` | 236 | `29` | `1.46` | `44R` | `-7.0R` | `4.73` |
| 1602 | XAGUSD | London | 60m | FADE_DOWN | OR_Q1_Tight | `59.3%` | 236 | `33` | `1.46` | `44R` | `-12.0R` | `4.73` |
| 1603 | GBPUSD | NY | 60m | FADE_UP | OR_Q1_Tight | `59.9%` | 197 | `24` | `1.49` | `39R` | `-9.0R` | `4.73` |
| 1604 | EURUSD | NY | 60m | FADE_DOWN | Tue | `62.1%` | 103 | `13` | `1.64` | `25R` | `-4.0R` | `4.73` |
| 1605 | EURUSD | London | 30m | FADE_UP | RSI_30-50 | `58.3%` | 333 | `41` | `1.40` | `55R` | `-7.0R` | `4.72` |
| 1606 | SP500 | Pre-Market | 30m | FADE_UP | BtwLowClose | `60.0%` | 190 | `23` | `1.50` | `38R` | `-8.0R` | `4.72` |
| 1607 | XAUUSD | London | 45m | FADE_DOWN | RSI_50-70 | `58.3%` | 324 | `40` | `1.40` | `54R` | `-10.0R` | `4.72` |
| 1608 | AUDUSD | London | 15m | SHAKEOUT_DOWN | Tue | `62.8%` | 86 | `11` | `1.69` | `22R` | `-5.0R` | `4.72` |
| 1609 | SP500 | NY Cash | 30m | FADE_UP | Tue | `61.0%` | 141 | `18` | `1.56` | `31R` | `-5.0R` | `4.72` |
| 1610 | EURJPY | Tokyo | 30m | FADE_DOWN | RSI_50-70 | `58.5%` | 306 | `38` | `1.41` | `52R` | `-9.0R` | `4.72` |
| 1611 | USDJPY | Tokyo | 45m | FADE_UP | ATR+10% | `65.9%` | 41 | `5` | `1.93` | `13R` | `-4.0R` | `4.72` |
| 1612 | XAGUSD | London | 45m | FADE_UP | ATR-10% | `65.9%` | 41 | `5` | `1.93` | `13R` | `-3.0R` | `4.72` |
| 1613 | WTI | London Initial | 60m | FADE_DOWN | RSI_D>65 | `60.8%` | 148 | `18` | `1.55` | `32R` | `-5.0R` | `4.72` |
| 1614 | EURJPY | Tokyo | 60m | FADE_UP | Wed | `59.7%` | 206 | `25` | `1.48` | `40R` | `-9.0R` | `4.71` |
| 1615 | GBPUSD | London | 60m | FADE_UP | BtwLowClose | `58.2%` | 335 | `41` | `1.39` | `55R` | `-9.0R` | `4.71` |
| 1616 | AUDUSD | London | 45m | FADE_DOWN | BelowPD | `60.4%` | 169 | `21` | `1.52` | `35R` | `-7.0R` | `4.71` |
| 1617 | BRENT | NY | 15m | FADE_UP | Tue | `60.6%` | 155 | `19` | `1.54` | `33R` | `-9.0R` | `4.71` |
| 1618 | SP500 | Pre-Market | 30m | FADE_UP | RSI_50-70 | `58.4%` | 308 | `38` | `1.41` | `52R` | `-7.0R` | `4.71` |
| 1619 | GBPUSD | London | 15m | FADE_DOWN | BtwLowClose | `58.6%` | 290 | `36` | `1.42` | `50R` | `-9.0R` | `4.71` |
| 1620 | WTI | NY Main | 30m | FADE_DOWN | OR_Q4_Wide | `59.8%` | 199 | `25` | `1.49` | `39R` | `-6.0R` | `4.71` |
| 1621 | USDJPY | Tokyo | 30m | FADE_UP | BtwLowClose | `58.1%` | 346 | `42` | `1.39` | `56R` | `-6.0R` | `4.71` |
| 1622 | XAUUSD | London | 30m | FADE_DOWN | OR_Q4_Wide | `59.3%` | 231 | `35` | `1.46` | `43R` | `-11.0R` | `4.70` |
| 1623 | NATGAS | NY | 45m | FADE_DOWN | RSI_D<35 | `63.0%` | 81 | `10` | `1.70` | `21R` | `-6.0R` | `4.70` |
| 1624 | NASDAQ100 | NY Cash | 45m | FADE_UP | BelowPD | `63.0%` | 81 | `10` | `1.70` | `21R` | `-4.0R` | `4.70` |
| 1625 | GBPAUD | London | 15m | FADE_DOWN | BASE | `55.9%` | 762 | `94` | `1.27` | `90R` | `-14.0R` | `4.70` |
| 1626 | NATGAS | NY | 45m | FADE_UP | RSI_50-70 | `58.2%` | 328 | `40` | `1.39` | `54R` | `-9.0R` | `4.70` |
| 1627 | XAUUSD | London | 15m | FADE_UP | BASE | `56.3%` | 663 | `81` | `1.29` | `83R` | `-15.0R` | `4.70` |
| 1628 | GBPUSD | NY | 30m | FADE_UP | RSI_30-50 | `58.9%` | 265 | `33` | `1.43` | `47R` | `-7.0R` | `4.70` |
| 1629 | GBPUSD | NY | 30m | FADE_UP | RSI_50-70 | `57.6%` | 399 | `49` | `1.36` | `61R` | `-13.0R` | `4.70` |
| 1630 | GBPJPY | London | 15m | FADE_UP | BtwLowClose | `58.7%` | 283 | `35` | `1.42` | `49R` | `-7.0R` | `4.70` |
| 1631 | GBPUSD | London | 45m | FADE_DOWN | RSI<30 | `61.0%` | 136 | `17` | `1.57` | `30R` | `-6.0R` | `4.70` |
| 1632 | BRENT | London | 60m | FADE_UP | RSI_D>65 | `61.0%` | 136 | `17` | `1.57` | `30R` | `-5.0R` | `4.70` |
| 1633 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | Wed | `61.0%` | 136 | `17` | `1.57` | `30R` | `-5.0R` | `4.70` |
| 1634 | EURJPY | London | 45m | FADE_UP | Tue | `60.1%` | 178 | `22` | `1.51` | `36R` | `-8.0R` | `4.69` |
| 1635 | GBPJPY | London | 30m | FADE_UP | AbovePD | `60.2%` | 171 | `22` | `1.51` | `35R` | `-4.0R` | `4.69` |
| 1636 | AUDUSD | London | 15m | FADE_UP | Wed | `60.8%` | 143 | `18` | `1.55` | `31R` | `-6.0R` | `4.69` |
| 1637 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | GapSmall | `57.5%` | 412 | `51` | `1.35` | `62R` | `-12.0R` | `4.69` |
| 1638 | AUDUSD | London | 60m | FADE_DOWN | OR_Q4_Wide | `59.7%` | 201 | `25` | `1.48` | `39R` | `-8.0R` | `4.69` |
| 1639 | XAUUSD | London | 15m | FADE_UP | BtwCloseHigh | `59.7%` | 201 | `25` | `1.48` | `39R` | `-10.0R` | `4.69` |
| 1640 | WTI | London Initial | 30m | FADE_DOWN | OR_Q4_Wide | `59.2%` | 233 | `30` | `1.45` | `43R` | `-9.0R` | `4.69` |
| 1641 | GBPUSD | NY | 45m | FADE_DOWN | BtwCloseHigh | `60.4%` | 164 | `20` | `1.52` | `34R` | `-8.0R` | `4.69` |
| 1642 | GBPUSD | London | 30m | FADE_UP | BtwLowClose | `58.1%` | 341 | `42` | `1.38` | `55R` | `-10.0R` | `4.69` |
| 1643 | NATGAS | NY | 45m | FADE_UP | RSI_30-50 | `59.4%` | 217 | `27` | `1.47` | `41R` | `-10.0R` | `4.69` |
| 1644 | WTI | London Initial | 45m | FADE_DOWN | Fri | `60.5%` | 157 | `20` | `1.53` | `33R` | `-6.0R` | `4.69` |
| 1645 | NATGAS | NY | 60m | FADE_DOWN | BtwLowClose | `60.5%` | 157 | `19` | `1.53` | `33R` | `-9.0R` | `4.69` |
| 1646 | BRENT | London | 45m | FADE_UP | BelowPD | `62.4%` | 93 | `12` | `1.66` | `23R` | `-4.0R` | `4.68` |
| 1647 | XAGUSD | London | 45m | FADE_DOWN | OR_Q1_Tight | `59.3%` | 226 | `32` | `1.46` | `42R` | `-12.0R` | `4.68` |
| 1648 | XAUUSD | London | 30m | FADE_DOWN | GapSmall | `56.0%` | 707 | `87` | `1.27` | `85R` | `-12.0R` | `4.68` |
| 1649 | EURUSD | NY | 60m | FADE_DOWN | BtwLowClose | `61.3%` | 124 | `15` | `1.58` | `28R` | `-6.0R` | `4.68` |
| 1650 | GBPAUD | London | 60m | FADE_DOWN | BelowPD | `61.3%` | 124 | `16` | `1.58` | `28R` | `-5.0R` | `4.68` |
| 1651 | XAGUSD | NY | 30m | FADE_DOWN | Mon | `61.3%` | 124 | `15` | `1.58` | `28R` | `-7.0R` | `4.68` |
| 1652 | NASDAQ100 | Pre-Market | 60m | FADE_UP | BASE | `55.5%` | 867 | `106` | `1.25` | `95R` | `-12.0R` | `4.68` |
| 1653 | XAUUSD | London | 30m | FADE_UP | OR_Q4_Wide | `59.1%` | 235 | `30` | `1.45` | `43R` | `-9.0R` | `4.68` |
| 1654 | EURUSD | London | 60m | FADE_UP | BtwLowClose | `57.8%` | 365 | `45` | `1.37` | `57R` | `-18.0R` | `4.67` |
| 1655 | XAUUSD | London | 15m | FADE_UP | GapSmall | `56.5%` | 573 | `70` | `1.30` | `75R` | `-14.0R` | `4.67` |
| 1656 | NASDAQ100 | NY Cash | 15m | FADE_UP | RSI_50-70 | `57.7%` | 376 | `46` | `1.36` | `58R` | `-8.0R` | `4.67` |
| 1657 | XAGUSD | London | 15m | FADE_DOWN | Wed | `61.1%` | 131 | `17` | `1.57` | `29R` | `-7.0R` | `4.67` |
| 1658 | AUDUSD | London | 60m | FADE_DOWN | BtwCloseHigh | `58.3%` | 307 | `38` | `1.40` | `51R` | `-9.0R` | `4.67` |
| 1659 | AUDUSD | London | 15m | FADE_DOWN | GapSmall | `56.5%` | 575 | `70` | `1.30` | `75R` | `-13.0R` | `4.67` |
| 1660 | AUDUSD | London | 15m | FADE_DOWN | RSI_30-50 | `57.9%` | 356 | `44` | `1.37` | `56R` | `-9.0R` | `4.67` |
| 1661 | GBPAUD | London | 30m | FADE_DOWN | BtwCloseHigh | `58.4%` | 298 | `37` | `1.40` | `50R` | `-8.0R` | `4.67` |
| 1662 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | GapSmall | `56.4%` | 603 | `74` | `1.29` | `77R` | `-8.0R` | `4.67` |
| 1663 | XAUUSD | London | 45m | FADE_DOWN | RSI_30-50 | `56.9%` | 501 | `62` | `1.32` | `69R` | `-10.0R` | `4.67` |
| 1664 | GBPJPY | Tokyo | 30m | FADE_DOWN | RSI_50-70 | `58.6%` | 280 | `34` | `1.41` | `48R` | `-10.0R` | `4.67` |
| 1665 | AUDUSD | London | 30m | FADE_DOWN | Mon | `60.2%` | 166 | `21` | `1.52` | `34R` | `-7.0R` | `4.67` |
| 1666 | GBPUSD | NY | 60m | FADE_DOWN | BelowPD | `61.6%` | 112 | `14` | `1.60` | `26R` | `-7.0R` | `4.66` |
| 1667 | BRENT | London | 15m | FADE_UP | GapSmall | `57.9%` | 347 | `43` | `1.38` | `55R` | `-11.0R` | `4.66` |
| 1668 | SP500 | NY Cash | 45m | FADE_DOWN | ATR+10% | `64.7%` | 51 | `6` | `1.83` | `15R` | `-4.0R` | `4.66` |
| 1669 | SP500 | Pre-Market | 15m | FADE_UP | BelowPD | `62.5%` | 88 | `11` | `1.67` | `22R` | `-3.0R` | `4.66` |
| 1670 | EURUSD | London | 15m | FADE_UP | Fri | `60.7%` | 145 | `18` | `1.54` | `31R` | `-6.0R` | `4.66` |
| 1671 | EURUSD | London | 15m | FADE_UP | BtwLowClose | `58.2%` | 318 | `39` | `1.39` | `52R` | `-9.0R` | `4.66` |
| 1672 | BRENT | NY | 45m | FADE_DOWN | Fri | `60.5%` | 152 | `19` | `1.53` | `32R` | `-6.0R` | `4.66` |
| 1673 | SP500 | Pre-Market | 60m | FADE_DOWN | Mon | `60.5%` | 152 | `19` | `1.53` | `32R` | `-7.0R` | `4.66` |
| 1674 | GBPJPY | London | 30m | FADE_UP | AbovePD+RSI_D>65 | `66.7%` | 33 | `4` | `2.00` | `11R` | `-4.0R` | `4.66` |
| 1675 | EURJPY | Tokyo | 30m | FADE_UP | ATR-10% | `66.7%` | 33 | `4` | `2.00` | `11R` | `-3.0R` | `4.66` |
| 1676 | GBPAUD | Sydney | 45m | FADE_UP | Tue | `66.7%` | 33 | `4` | `2.00` | `11R` | `-3.0R` | `4.66` |
| 1677 | GBPAUD | London | 30m | FADE_UP | ATR+10% | `66.7%` | 33 | `4` | `2.00` | `11R` | `-5.0R` | `4.66` |
| 1678 | XAGUSD | London | 30m | FADE_DOWN | ATR-10% | `66.7%` | 33 | `4` | `2.00` | `11R` | `-4.0R` | `4.66` |
| 1679 | NATGAS | NY | 30m | FADE_UP | RSI<30 | `66.7%` | 33 | `4` | `2.00` | `11R` | `-2.0R` | `4.66` |
| 1680 | VIX | NY Cash | 15m | FADE_DOWN | Thu | `66.7%` | 33 | `10` | `2.00` | `11R` | `-3.0R` | `4.66` |
| 1681 | XAGUSD | NY | 30m | FADE_DOWN | RSI_50-70 | `58.9%` | 246 | `30` | `1.44` | `44R` | `-7.0R` | `4.66` |
| 1682 | BRENT | NY | 45m | FADE_UP | RSI_30-50 | `58.9%` | 246 | `30` | `1.44` | `44R` | `-12.0R` | `4.66` |
| 1683 | USDJPY | NY | 30m | FADE_DOWN | RSI_30-50 | `57.7%` | 369 | `45` | `1.37` | `57R` | `-7.0R` | `4.66` |
| 1684 | GBPUSD | London | 30m | FADE_DOWN | RSI_D<35 | `62.0%` | 100 | `13` | `1.63` | `24R` | `-4.0R` | `4.66` |
| 1685 | GBPAUD | London | 45m | FADE_UP | RSI_D>65 | `62.0%` | 100 | `13` | `1.63` | `24R` | `-7.0R` | `4.66` |
| 1686 | VIX | NY Cash | 30m | FADE_UP | Tue | `64.3%` | 56 | `17` | `1.80` | `16R` | `-6.0R` | `4.66` |
| 1687 | EURJPY | London | 15m | FADE_UP | BtwLowClose | `58.5%` | 282 | `35` | `1.41` | `48R` | `-12.0R` | `4.66` |
| 1688 | GBPJPY | London | 15m | FADE_UP | RSI_50-70 | `57.3%` | 424 | `52` | `1.34` | `62R` | `-16.0R` | `4.65` |
| 1689 | GBPAUD | London | 45m | FADE_UP | BASE | `55.2%` | 929 | `114` | `1.23` | `97R` | `-16.0R` | `4.65` |
| 1690 | EURJPY | London | 15m | FADE_UP | GapSmall | `56.0%` | 682 | `84` | `1.27` | `82R` | `-15.0R` | `4.65` |
| 1691 | USDJPY | Tokyo | 60m | FADE_UP | BtwCloseHigh | `56.4%` | 598 | `73` | `1.29` | `76R` | `-12.0R` | `4.65` |
| 1692 | BRENT | London | 30m | FADE_UP | RSI_30-50 | `59.3%` | 214 | `27` | `1.46` | `40R` | `-9.0R` | `4.65` |
| 1693 | GBPUSD | London | 60m | FADE_DOWN | OR_Q4_Wide | `59.6%` | 198 | `24` | `1.48` | `38R` | `-6.0R` | `4.65` |
| 1694 | XAGUSD | London | 60m | FADE_DOWN | Tue | `59.6%` | 198 | `24` | `1.48` | `38R` | `-7.0R` | `4.65` |
| 1695 | XAUUSD | NY | 60m | FADE_UP | Mon | `62.7%` | 83 | `10` | `1.68` | `21R` | `-5.0R` | `4.64` |
| 1696 | USDJPY | Tokyo | 45m | FADE_UP | Mon | `60.1%` | 168 | `21` | `1.51` | `34R` | `-8.0R` | `4.64` |
| 1697 | WTI | London Initial | 60m | FADE_UP | Fri | `60.1%` | 168 | `21` | `1.51` | `34R` | `-10.0R` | `4.64` |
| 1698 | GBPUSD | NY | 45m | FADE_DOWN | GapSmall | `57.2%` | 428 | `53` | `1.34` | `62R` | `-12.0R` | `4.64` |
| 1699 | GBPUSD | London | 15m | FADE_UP | BASE | `55.5%` | 818 | `100` | `1.25` | `90R` | `-14.0R` | `4.64` |
| 1700 | GBPUSD | NY | 15m | FADE_DOWN | RSI_50-70 | `58.1%` | 313 | `38` | `1.39` | `51R` | `-14.0R` | `4.64` |
| 1701 | GBPJPY | London | 45m | FADE_UP | Fri | `59.7%` | 191 | `23` | `1.48` | `37R` | `-6.0R` | `4.64` |
| 1702 | EURUSD | NY | 60m | FADE_DOWN | RSI_50-70 | `60.2%` | 161 | `20` | `1.52` | `33R` | `-5.0R` | `4.64` |
| 1703 | GBPJPY | London | 45m | FADE_UP | RSI>70 | `61.7%` | 107 | `13` | `1.61` | `25R` | `-8.0R` | `4.64` |
| 1704 | BRENT | NY | 15m | FADE_DOWN | OR_Q1_Tight | `61.7%` | 107 | `13` | `1.61` | `25R` | `-5.0R` | `4.64` |
| 1705 | NASDAQ100 | NY Cash | 45m | FADE_UP | Mon | `61.7%` | 107 | `13` | `1.61` | `25R` | `-8.0R` | `4.64` |
| 1706 | XAUUSD | NY | 60m | FADE_UP | BASE | `57.3%` | 419 | `51` | `1.34` | `61R` | `-11.0R` | `4.64` |
| 1707 | BRENT | NY | 60m | FADE_UP | Thu | `60.5%` | 147 | `18` | `1.53` | `31R` | `-5.0R` | `4.64` |
| 1708 | USDJPY | NY | 60m | FADE_UP | Tue | `62.1%` | 95 | `12` | `1.64` | `23R` | `-3.0R` | `4.64` |
| 1709 | NASDAQ100 | NY Cash | 30m | FADE_UP | RSI_30-50 | `59.8%` | 184 | `23` | `1.49` | `36R` | `-13.0R` | `4.63` |
| 1710 | NASDAQ100 | Pre-Market | 60m | FADE_UP | GapSmall | `55.7%` | 760 | `93` | `1.26` | `86R` | `-21.0R` | `4.63` |
| 1711 | GBPAUD | London | 45m | FADE_DOWN | OR_Q1_Tight | `58.8%` | 250 | `31` | `1.43` | `44R` | `-8.0R` | `4.63` |
| 1712 | AUDUSD | London | 30m | FADE_UP | Mon | `59.5%` | 200 | `25` | `1.47` | `38R` | `-13.0R` | `4.63` |
| 1713 | XAUUSD | NY | 15m | FADE_UP | BASE | `55.5%` | 798 | `98` | `1.25` | `88R` | `-12.0R` | `4.63` |
| 1714 | NASDAQ100 | Pre-Market | 15m | FADE_UP | OR_Q4_Wide | `59.9%` | 177 | `22` | `1.49` | `35R` | `-8.0R` | `4.63` |
| 1715 | AUDUSD | London | 30m | FADE_UP | BtwCloseHigh | `58.2%` | 297 | `37` | `1.40` | `49R` | `-7.0R` | `4.63` |
| 1716 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | Fri | `61.4%` | 114 | `14` | `1.59` | `26R` | `-5.0R` | `4.63` |
| 1717 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | Mon | `62.8%` | 78 | `10` | `1.69` | `20R` | `-10.0R` | `4.62` |
| 1718 | WTI | NY Main | 15m | FADE_DOWN | RSI_30-50 | `57.4%` | 401 | `49` | `1.35` | `59R` | `-9.0R` | `4.62` |
| 1719 | EURJPY | London | 45m | FADE_UP | OR_Q1_Tight | `58.8%` | 243 | `30` | `1.43` | `43R` | `-10.0R` | `4.62` |
| 1720 | BRENT | London | 60m | FADE_DOWN | Thu | `60.0%` | 170 | `21` | `1.50` | `34R` | `-8.0R` | `4.62` |
| 1721 | XAUUSD | London | 30m | FADE_DOWN | BtwCloseHigh | `58.5%` | 270 | `34` | `1.41` | `46R` | `-9.0R` | `4.62` |
| 1722 | NASDAQ100 | Pre-Market | 30m | FADE_UP | OR_Q4_Wide | `59.2%` | 218 | `30` | `1.45` | `40R` | `-10.0R` | `4.62` |
| 1723 | NATGAS | NY | 45m | FADE_UP | Tue | `61.2%` | 121 | `15` | `1.57` | `27R` | `-3.0R` | `4.62` |
| 1724 | BRENT | NY | 15m | FADE_UP | AbovePD | `60.3%` | 156 | `20` | `1.52` | `32R` | `-6.0R` | `4.61` |
| 1725 | GBPUSD | London | 30m | FADE_DOWN | BtwCloseHigh | `57.9%` | 330 | `41` | `1.37` | `52R` | `-8.0R` | `4.61` |
| 1726 | XAUUSD | London | 30m | FADE_DOWN | RSI_50-70 | `58.1%` | 310 | `38` | `1.38` | `50R` | `-9.0R` | `4.61` |
| 1727 | VIX | NY Cash | 30m | FADE_UP | BtwLowClose | `62.2%` | 90 | `27` | `1.65` | `22R` | `-9.0R` | `4.61` |
| 1728 | EURUSD | London | 15m | FADE_DOWN | OR_Q4_Wide | `58.9%` | 236 | `29` | `1.43` | `42R` | `-7.0R` | `4.61` |
| 1729 | EURUSD | London | 15m | FADE_DOWN | Wed | `60.4%` | 149 | `18` | `1.53` | `31R` | `-5.0R` | `4.61` |
| 1730 | SP500 | NY Cash | 45m | FADE_DOWN | RSI_D>65 | `60.4%` | 149 | `19` | `1.53` | `31R` | `-4.0R` | `4.61` |
| 1731 | WTI | London Initial | 15m | FADE_UP | RSI_30-50 | `60.7%` | 135 | `17` | `1.55` | `29R` | `-8.0R` | `4.61` |
| 1732 | WTI | London Initial | 60m | FADE_UP | RSI_D>65 | `60.7%` | 135 | `17` | `1.55` | `29R` | `-5.0R` | `4.61` |
| 1733 | GBPJPY | Tokyo | 15m | FADE_UP | Fri | `60.6%` | 142 | `17` | `1.54` | `30R` | `-5.0R` | `4.61` |
| 1734 | EURJPY | London | 15m | FADE_DOWN | Mon | `60.6%` | 142 | `18` | `1.54` | `30R` | `-7.0R` | `4.61` |
| 1735 | USDJPY | Tokyo | 60m | FADE_UP | Thu | `59.8%` | 179 | `22` | `1.49` | `35R` | `-6.0R` | `4.61` |
| 1736 | XAUUSD | NY | 15m | FADE_DOWN | AbovePD | `59.8%` | 179 | `22` | `1.49` | `35R` | `-9.0R` | `4.61` |
| 1737 | XAGUSD | London | 30m | FADE_UP | BtwLowClose | `57.7%` | 352 | `43` | `1.36` | `54R` | `-12.0R` | `4.61` |
| 1738 | BRENT | London | 15m | FADE_DOWN | Fri | `63.0%` | 73 | `9` | `1.70` | `19R` | `-5.0R` | `4.61` |
| 1739 | NATGAS | NY | 60m | FADE_DOWN | RSI<30 | `63.0%` | 73 | `9` | `1.70` | `19R` | `-4.0R` | `4.61` |
| 1740 | GBPUSD | London | 45m | FADE_DOWN | Wed | `59.5%` | 195 | `24` | `1.47` | `37R` | `-8.0R` | `4.61` |
| 1741 | XAUUSD | London | 30m | MOMENTUM_UP | AbovePD+RSI_D>65 | `58.5%` | 41 | `5` | `2.12` | `19R` | `-8.0R` | `4.60` |
| 1742 | XAGUSD | London | 15m | FADE_DOWN | ATR+10% | `65.8%` | 38 | `5` | `1.92` | `12R` | `-3.0R` | `4.60` |
| 1743 | XAGUSD | London | 45m | FADE_DOWN | ATR-10% | `65.8%` | 38 | `5` | `1.92` | `12R` | `-3.0R` | `4.60` |
| 1744 | BRENT | NY | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `65.8%` | 38 | `5` | `1.92` | `12R` | `-5.0R` | `4.60` |
| 1745 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `65.8%` | 38 | `5` | `1.92` | `12R` | `-3.0R` | `4.60` |
| 1746 | GBPUSD | NY | 30m | FADE_DOWN | AbovePD | `59.3%` | 204 | `25` | `1.46` | `38R` | `-7.0R` | `4.60` |
| 1747 | GBPAUD | London | 60m | FADE_DOWN | OR_Q1_Tight | `58.8%` | 238 | `29` | `1.43` | `42R` | `-7.0R` | `4.60` |
| 1748 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | BtwCloseHigh | `58.8%` | 238 | `29` | `1.43` | `42R` | `-5.0R` | `4.60` |
| 1749 | WTI | NY Main | 60m | FADE_UP | BtwCloseHigh | `59.6%` | 188 | `23` | `1.47` | `36R` | `-7.0R` | `4.60` |
| 1750 | USDJPY | Tokyo | 30m | FADE_DOWN | RSI_30-50 | `56.7%` | 485 | `59` | `1.31` | `65R` | `-12.0R` | `4.59` |
| 1751 | SP500 | NY Cash | 45m | FADE_DOWN | AbovePD | `60.1%` | 158 | `19` | `1.51` | `32R` | `-7.0R` | `4.59` |
| 1752 | GBPAUD | London | 60m | FADE_DOWN | Wed | `59.7%` | 181 | `22` | `1.48` | `35R` | `-10.0R` | `4.59` |
| 1753 | GBPAUD | London | 45m | FADE_DOWN | Wed | `59.4%` | 197 | `24` | `1.46` | `37R` | `-12.0R` | `4.59` |
| 1754 | EURUSD | London | 30m | FADE_DOWN | BelowPD | `61.9%` | 97 | `12` | `1.62` | `23R` | `-4.0R` | `4.59` |
| 1755 | GBPJPY | Tokyo | 60m | FADE_DOWN | OR_Q1_Tight | `58.8%` | 240 | `30` | `1.42` | `42R` | `-11.0R` | `4.59` |
| 1756 | GBPUSD | NY | 45m | FADE_UP | Wed | `60.3%` | 151 | `19` | `1.52` | `31R` | `-5.0R` | `4.59` |
| 1757 | BRENT | NY | 45m | FADE_UP | Mon | `60.3%` | 151 | `19` | `1.52` | `31R` | `-7.0R` | `4.59` |
| 1758 | AUDUSD | London | 45m | FADE_DOWN | RSI_50-70 | `57.5%` | 369 | `46` | `1.35` | `55R` | `-8.0R` | `4.59` |
| 1759 | BRENT | London | 15m | FADE_DOWN | GapSmall | `57.5%` | 369 | `45` | `1.35` | `55R` | `-9.0R` | `4.59` |
| 1760 | XAUUSD | NY | 30m | FADE_UP | OR_Q4_Wide | `61.0%` | 123 | `19` | `1.56` | `27R` | `-7.0R` | `4.58` |
| 1761 | BRENT | NY | 60m | FADE_UP | Mon | `61.0%` | 123 | `15` | `1.56` | `27R` | `-6.0R` | `4.58` |
| 1762 | AUDUSD | London | 15m | FADE_UP | AbovePD | `60.4%` | 144 | `18` | `1.53` | `30R` | `-7.0R` | `4.58` |
| 1763 | AUDUSD | London | 15m | FADE_DOWN | BelowPD | `60.4%` | 144 | `18` | `1.53` | `30R` | `-8.0R` | `4.58` |
| 1764 | XAGUSD | NY | 15m | FADE_UP | RSI_D>65 | `60.4%` | 144 | `18` | `1.53` | `30R` | `-7.0R` | `4.58` |
| 1765 | XAGUSD | London | 30m | FADE_UP | OR_Q1_Tight | `59.2%` | 206 | `34` | `1.45` | `38R` | `-9.0R` | `4.58` |
| 1766 | EURUSD | NY | 60m | FADE_DOWN | BtwCloseHigh | `60.8%` | 130 | `16` | `1.55` | `28R` | `-4.0R` | `4.58` |
| 1767 | USDJPY | Tokyo | 15m | FADE_DOWN | RSI_D>65 | `60.8%` | 130 | `16` | `1.55` | `28R` | `-3.0R` | `4.58` |
| 1768 | NATGAS | NY | 60m | FADE_DOWN | BtwCloseHigh | `59.8%` | 174 | `21` | `1.49` | `34R` | `-7.0R` | `4.58` |
| 1769 | USDJPY | Tokyo | 45m | FADE_UP | BtwLowClose | `57.5%` | 360 | `44` | `1.35` | `54R` | `-10.0R` | `4.58` |
| 1770 | GBPUSD | London | 45m | FADE_UP | GapSmall | `55.1%` | 856 | `105` | `1.23` | `88R` | `-16.0R` | `4.58` |
| 1771 | USDJPY | Tokyo | 15m | FADE_UP | BASE | `55.1%` | 856 | `105` | `1.23` | `88R` | `-25.0R` | `4.58` |
| 1772 | USDJPY | Tokyo | 15m | FADE_UP | GapSmall | `55.1%` | 856 | `105` | `1.23` | `88R` | `-25.0R` | `4.58` |
| 1773 | EURUSD | London | 15m | FADE_UP | OR_Q4_Wide | `58.5%` | 260 | `32` | `1.41` | `44R` | `-10.0R` | `4.58` |
| 1774 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | RSI_D>65 | `59.9%` | 167 | `21` | `1.49` | `33R` | `-6.0R` | `4.57` |
| 1775 | BRENT | NY | 45m | FADE_UP | BtwLowClose | `58.8%` | 233 | `29` | `1.43` | `41R` | `-13.0R` | `4.57` |
| 1776 | EURUSD | London | 30m | FADE_UP | Fri | `59.3%` | 199 | `24` | `1.46` | `37R` | `-10.0R` | `4.57` |
| 1777 | GBPUSD | NY | 15m | FADE_DOWN | ATR+10% | `65.1%` | 43 | `5` | `1.87` | `13R` | `-4.0R` | `4.57` |
| 1778 | EURJPY | Tokyo | 15m | FADE_DOWN | RSI<30 | `65.1%` | 43 | `6` | `1.87` | `13R` | `-3.0R` | `4.57` |
| 1779 | EURJPY | Tokyo | 45m | FADE_DOWN | ATR-10% | `65.1%` | 43 | `5` | `1.87` | `13R` | `-3.0R` | `4.57` |
| 1780 | WTI | London Initial | 45m | FADE_DOWN | BtwLowClose | `57.8%` | 320 | `40` | `1.37` | `50R` | `-9.0R` | `4.57` |
| 1781 | USDJPY | NY | 30m | FADE_DOWN | BASE | `55.6%` | 720 | `88` | `1.25` | `80R` | `-14.0R` | `4.57` |
| 1782 | EURJPY | Tokyo | 30m | FADE_DOWN | Wed | `60.0%` | 160 | `20` | `1.50` | `32R` | `-7.0R` | `4.57` |
| 1783 | NATGAS | NY | 45m | FADE_DOWN | BtwCloseHigh | `59.1%` | 208 | `26` | `1.45` | `38R` | `-8.0R` | `4.57` |
| 1784 | GBPUSD | NY | 30m | FADE_DOWN | GapSmall | `56.5%` | 510 | `63` | `1.30` | `66R` | `-13.0R` | `4.57` |
| 1785 | SP500 | Pre-Market | 45m | FADE_UP | OR_Q4_Wide | `59.0%` | 217 | `27` | `1.44` | `39R` | `-7.0R` | `4.56` |
| 1786 | USDJPY | NY | 15m | FADE_DOWN | RSI_D<35 | `63.8%` | 58 | `7` | `1.76` | `16R` | `-6.0R` | `4.56` |
| 1787 | EURJPY | London | 45m | FADE_DOWN | OR_Q1_Tight | `58.8%` | 226 | `28` | `1.43` | `40R` | `-6.0R` | `4.56` |
| 1788 | GBPAUD | London | 60m | FADE_UP | RSI_30-50 | `57.8%` | 322 | `40` | `1.37` | `50R` | `-9.0R` | `4.56` |
| 1789 | GBPUSD | London | 15m | FADE_DOWN | BASE | `55.3%` | 798 | `98` | `1.24` | `84R` | `-11.0R` | `4.56` |
| 1790 | GBPJPY | Tokyo | 60m | FADE_UP | BtwCloseHigh | `56.1%` | 585 | `72` | `1.28` | `71R` | `-12.0R` | `4.56` |
| 1791 | NASDAQ100 | NY Cash | 15m | FADE_UP | ATR+10% | `64.6%` | 48 | `6` | `1.82` | `14R` | `-3.0R` | `4.56` |
| 1792 | GBPUSD | London | 15m | FADE_DOWN | GapSmall | `55.4%` | 749 | `92` | `1.24` | `81R` | `-11.0R` | `4.56` |
| 1793 | EURUSD | NY | 45m | FADE_UP | Mon | `61.0%` | 118 | `14` | `1.57` | `26R` | `-7.0R` | `4.56` |
| 1794 | BRENT | NY | 30m | FADE_DOWN | RSI_D>65 | `61.0%` | 118 | `14` | `1.57` | `26R` | `-6.0R` | `4.56` |
| 1795 | SP500 | Pre-Market | 30m | FADE_UP | RSI_D>65 | `61.0%` | 118 | `15` | `1.57` | `26R` | `-9.0R` | `4.56` |
| 1796 | USDJPY | Tokyo | 15m | FADE_UP | BtwCloseHigh | `56.2%` | 559 | `68` | `1.28` | `69R` | `-11.0R` | `4.55` |
| 1797 | SP500 | NY Cash | 30m | FADE_DOWN | AbovePD | `59.8%` | 169 | `21` | `1.49` | `33R` | `-7.0R` | `4.55` |
| 1798 | SP500 | NY Cash | 60m | FADE_DOWN | OR_Q1_Tight | `60.6%` | 132 | `16` | `1.54` | `28R` | `-5.0R` | `4.55` |
| 1799 | GBPJPY | Tokyo | 60m | FADE_DOWN | Tue | `59.5%` | 185 | `23` | `1.47` | `35R` | `-4.0R` | `4.55` |
| 1800 | USDJPY | NY | 45m | FADE_UP | RSI_50-70 | `57.9%` | 304 | `37` | `1.38` | `48R` | `-12.0R` | `4.55` |
| 1801 | AUDUSD | London | 45m | FADE_DOWN | RSI_30-50 | `56.7%` | 466 | `57` | `1.31` | `62R` | `-11.0R` | `4.55` |
| 1802 | NASDAQ100 | NY Cash | 60m | MOMENTUM_UP | Mon | `55.2%` | 87 | `11` | `1.85` | `33R` | `-5.0R` | `4.55` |
| 1803 | BRENT | NY | 45m | FADE_DOWN | BtwCloseHigh | `58.8%` | 228 | `28` | `1.43` | `40R` | `-8.0R` | `4.55` |
| 1804 | WTI | NY Main | 15m | FADE_UP | RSI_30-50 | `58.2%` | 275 | `34` | `1.39` | `45R` | `-6.0R` | `4.55` |
| 1805 | WTI | London Initial | 15m | FADE_DOWN | BtwLowClose | `59.6%` | 178 | `22` | `1.47` | `34R` | `-6.0R` | `4.54` |
| 1806 | USDJPY | NY | 30m | FADE_UP | BASE | `55.6%` | 676 | `83` | `1.25` | `76R` | `-9.0R` | `4.54` |
| 1807 | EURUSD | London | 60m | FADE_DOWN | BtwLowClose | `57.4%` | 350 | `43` | `1.35` | `52R` | `-13.0R` | `4.54` |
| 1808 | USDJPY | Tokyo | 30m | FADE_UP | Fri | `59.0%` | 212 | `26` | `1.44` | `38R` | `-8.0R` | `4.54` |
| 1809 | XAGUSD | NY | 60m | FADE_DOWN | GapSmall | `58.1%` | 277 | `34` | `1.39` | `45R` | `-8.0R` | `4.54` |
| 1810 | XAGUSD | London | 15m | SHAKEOUT_UP | AbovePD | `62.1%` | 87 | `11` | `1.64` | `21R` | `-4.0R` | `4.54` |
| 1811 | SP500 | Pre-Market | 30m | FADE_DOWN | BtwLowClose | `59.4%` | 187 | `23` | `1.46` | `35R` | `-7.0R` | `4.54` |
| 1812 | EURUSD | London | 15m | FADE_DOWN | RSI>70 | `66.7%` | 30 | `4` | `2.00` | `10R` | `-3.0R` | `4.53` |
| 1813 | AUDUSD | Sydney | 45m | FADE_UP | Tue | `66.7%` | 30 | `4` | `2.00` | `10R` | `-5.0R` | `4.53` |
| 1814 | XAUUSD | NY | 30m | FADE_DOWN | RSI>70 | `66.7%` | 30 | `4` | `2.00` | `10R` | `-4.0R` | `4.53` |
| 1815 | XAGUSD | London | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `66.7%` | 30 | `4` | `2.00` | `10R` | `-3.0R` | `4.53` |
| 1816 | WTI | London Initial | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `66.7%` | 30 | `4` | `2.00` | `10R` | `-4.0R` | `4.53` |
| 1817 | SP500 | Pre-Market | 15m | FADE_UP | RSI>70 | `66.7%` | 30 | `4` | `2.00` | `10R` | `-3.0R` | `4.53` |
| 1818 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | ATR-10% | `66.7%` | 30 | `4` | `2.00` | `10R` | `-2.0R` | `4.53` |
| 1819 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | AbovePD | `60.1%` | 148 | `18` | `1.51` | `30R` | `-6.0R` | `4.53` |
| 1820 | XAUUSD | NY | 15m | FADE_UP | GapSmall | `56.0%` | 573 | `70` | `1.27` | `69R` | `-16.0R` | `4.53` |
| 1821 | EURJPY | Tokyo | 15m | MOMENTUM_DOWN | RSI_D<35 | `56.5%` | 62 | `9` | `1.94` | `26R` | `-5.0R` | `4.53` |
| 1822 | SP500 | Pre-Market | 30m | FADE_UP | BASE | `55.9%` | 590 | `72` | `1.27` | `70R` | `-13.0R` | `4.53` |
| 1823 | BRENT | London | 30m | FADE_DOWN | Wed | `60.3%` | 141 | `17` | `1.52` | `29R` | `-4.0R` | `4.53` |
| 1824 | WTI | London Initial | 60m | FADE_UP | RSI_30-50 | `58.1%` | 279 | `34` | `1.38` | `45R` | `-14.0R` | `4.53` |
| 1825 | WTI | London Initial | 15m | FADE_DOWN | Mon | `61.1%` | 113 | `14` | `1.57` | `25R` | `-4.0R` | `4.53` |
| 1826 | NASDAQ100 | NY Cash | 60m | FADE_UP | Wed | `61.1%` | 113 | `14` | `1.57` | `25R` | `-6.0R` | `4.53` |
| 1827 | GBPAUD | London | 45m | FADE_DOWN | Mon | `59.0%` | 205 | `25` | `1.44` | `37R` | `-7.0R` | `4.53` |
| 1828 | XAUUSD | London | 30m | FADE_DOWN | Wed | `59.8%` | 164 | `20` | `1.48` | `32R` | `-6.0R` | `4.53` |
| 1829 | WTI | NY Main | 45m | FADE_DOWN | AbovePD | `59.8%` | 164 | `20` | `1.48` | `32R` | `-11.0R` | `4.53` |
| 1830 | WTI | London Initial | 60m | FADE_DOWN | Thu | `59.4%` | 180 | `23` | `1.47` | `34R` | `-8.0R` | `4.52` |
| 1831 | EURUSD | London | 30m | FADE_DOWN | RSI_50-70 | `57.6%` | 321 | `40` | `1.36` | `49R` | `-7.0R` | `4.52` |
| 1832 | EURUSD | NY | 30m | FADE_DOWN | RSI_30-50 | `57.1%` | 389 | `48` | `1.33` | `55R` | `-12.0R` | `4.52` |
| 1833 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | BASE | `55.4%` | 728 | `89` | `1.24` | `78R` | `-11.0R` | `4.52` |
| 1834 | XAGUSD | NY | 60m | FADE_DOWN | BelowPD | `62.9%` | 70 | `9` | `1.69` | `18R` | `-6.0R` | `4.52` |
| 1835 | GBPJPY | Tokyo | 15m | FADE_UP | BtwCloseHigh | `57.0%` | 391 | `48` | `1.33` | `55R` | `-12.0R` | `4.52` |
| 1836 | USDJPY | NY | 45m | FADE_DOWN | RSI_30-50 | `57.7%` | 312 | `38` | `1.36` | `48R` | `-7.0R` | `4.52` |
| 1837 | AUDUSD | London | 15m | FADE_DOWN | OR_Q4_Wide | `58.3%` | 252 | `31` | `1.40` | `42R` | `-7.0R` | `4.52` |
| 1838 | EURJPY | London | 60m | FADE_DOWN | Wed | `59.5%` | 173 | `21` | `1.47` | `33R` | `-6.0R` | `4.51` |
| 1839 | BRENT | London | 30m | FADE_DOWN | OR_Q4_Wide | `58.5%` | 234 | `29` | `1.41` | `40R` | `-7.0R` | `4.51` |
| 1840 | GBPAUD | London | 60m | FADE_UP | BelowPD | `60.0%` | 150 | `19` | `1.50` | `30R` | `-5.0R` | `4.51` |
| 1841 | NATGAS | NY | 45m | FADE_UP | RSI>70 | `62.2%` | 82 | `10` | `1.65` | `20R` | `-6.0R` | `4.51` |
| 1842 | WTI | London Initial | 30m | FADE_UP | Fri | `60.1%` | 143 | `18` | `1.51` | `29R` | `-5.0R` | `4.50` |
| 1843 | GBPJPY | London | 15m | FADE_DOWN | BtwLowClose | `57.9%` | 285 | `35` | `1.38` | `45R` | `-7.0R` | `4.50` |
| 1844 | AUDUSD | Sydney | 15m | FADE_UP | RSI_30-50 | `63.1%` | 65 | `8` | `1.71` | `17R` | `-6.0R` | `4.50` |
| 1845 | BRENT | NY | 30m | FADE_UP | RSI_D<35 | `63.1%` | 65 | `8` | `1.71` | `17R` | `-4.0R` | `4.50` |
| 1846 | NASDAQ100 | Pre-Market | 15m | FADE_UP | Thu | `63.1%` | 65 | `8` | `1.71` | `17R` | `-5.0R` | `4.50` |
| 1847 | EURUSD | London | 60m | FADE_DOWN | RSI_30-50 | `56.2%` | 520 | `64` | `1.28` | `64R` | `-13.0R` | `4.50` |
| 1848 | GBPJPY | Tokyo | 60m | FADE_DOWN | Thu | `58.9%` | 209 | `26` | `1.43` | `37R` | `-12.0R` | `4.50` |
| 1849 | GBPJPY | Tokyo | 45m | FADE_DOWN | OR_Q1_Tight | `59.4%` | 175 | `22` | `1.46` | `33R` | `-9.0R` | `4.50` |
| 1850 | XAGUSD | NY | 30m | FADE_DOWN | BtwCloseHigh | `59.4%` | 175 | `22` | `1.46` | `33R` | `-9.0R` | `4.50` |
| 1851 | BRENT | NY | 15m | FADE_UP | Mon | `59.7%` | 159 | `19` | `1.48` | `31R` | `-6.0R` | `4.50` |
| 1852 | EURUSD | NY | 45m | FADE_DOWN | Mon | `60.5%` | 129 | `16` | `1.53` | `27R` | `-10.0R` | `4.49` |
| 1853 | GBPUSD | London | 60m | FADE_DOWN | RSI<30 | `60.7%` | 122 | `15` | `1.54` | `26R` | `-5.0R` | `4.49` |
| 1854 | XAUUSD | NY | 60m | FADE_UP | RSI_30-50 | `60.7%` | 122 | `15` | `1.54` | `26R` | `-8.0R` | `4.49` |
| 1855 | NASDAQ100 | NY Cash | 15m | FADE_UP | BASE | `55.2%` | 724 | `89` | `1.23` | `76R` | `-10.0R` | `4.49` |
| 1856 | USDJPY | Tokyo | 60m | FADE_UP | OR_Q1_Tight | `58.3%` | 247 | `31` | `1.40` | `41R` | `-11.0R` | `4.49` |
| 1857 | NASDAQ100 | Pre-Market | 60m | FADE_UP | RSI>70 | `61.8%` | 89 | `11` | `1.62` | `21R` | `-5.0R` | `4.49` |
| 1858 | XAGUSD | NY | 45m | FADE_DOWN | OR_Q1_Tight | `59.9%` | 152 | `21` | `1.49` | `30R` | `-7.0R` | `4.49` |
| 1859 | NATGAS | NY | 30m | FADE_UP | Tue | `59.9%` | 152 | `19` | `1.49` | `30R` | `-10.0R` | `4.49` |
| 1860 | SP500 | NY Cash | 30m | FADE_DOWN | Thu | `59.9%` | 152 | `19` | `1.49` | `30R` | `-9.0R` | `4.49` |
| 1861 | NASDAQ100 | NY Cash | 30m | FADE_UP | AbovePD | `59.9%` | 152 | `19` | `1.49` | `30R` | `-4.0R` | `4.49` |
| 1862 | GBPUSD | London | 45m | FADE_DOWN | Tue | `58.9%` | 202 | `25` | `1.43` | `36R` | `-8.0R` | `4.48` |
| 1863 | XAUUSD | NY | 15m | FADE_UP | BtwLowClose | `58.8%` | 211 | `26` | `1.43` | `37R` | `-10.0R` | `4.48` |
| 1864 | XAUUSD | London | 30m | FADE_UP | RSI_50-70 | `56.3%` | 485 | `59` | `1.29` | `61R` | `-12.0R` | `4.48` |
| 1865 | WTI | London Initial | 15m | FADE_UP | BtwCloseHigh | `60.0%` | 145 | `18` | `1.50` | `29R` | `-10.0R` | `4.48` |
| 1866 | BRENT | London | 30m | FADE_DOWN | Tue | `60.0%` | 145 | `18` | `1.50` | `29R` | `-5.0R` | `4.48` |
| 1867 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | GapSmall | `60.0%` | 145 | `18` | `1.50` | `29R` | `-11.0R` | `4.48` |
| 1868 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | RSI_50-70 | `60.0%` | 145 | `18` | `1.50` | `29R` | `-10.0R` | `4.48` |
| 1869 | GBPUSD | NY | 45m | FADE_UP | ATR+10% | `65.7%` | 35 | `4` | `1.92` | `11R` | `-2.0R` | `4.48` |
| 1870 | XAGUSD | London | 45m | FADE_UP | AbovePD+RSI_D>65 | `65.7%` | 35 | `5` | `1.92` | `11R` | `-4.0R` | `4.48` |
| 1871 | SP500 | NY Cash | 30m | FADE_DOWN | ATR-10% | `65.7%` | 35 | `4` | `1.92` | `11R` | `-2.0R` | `4.48` |
| 1872 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | ATR+10% | `65.7%` | 35 | `4` | `1.92` | `11R` | `-3.0R` | `4.48` |
| 1873 | EURJPY | London | 45m | FADE_DOWN | Wed | `59.3%` | 177 | `22` | `1.46` | `33R` | `-7.0R` | `4.48` |
| 1874 | GBPJPY | London | 45m | FADE_UP | RSI_50-70 | `56.0%` | 532 | `66` | `1.27` | `64R` | `-10.0R` | `4.48` |
| 1875 | EURUSD | NY | 30m | FADE_DOWN | GapSmall | `56.3%` | 474 | `58` | `1.29` | `60R` | `-14.0R` | `4.48` |
| 1876 | XAGUSD | NY | 45m | FADE_DOWN | GapSmall | `57.2%` | 346 | `42` | `1.34` | `50R` | `-8.0R` | `4.48` |
| 1877 | USDJPY | Tokyo | 15m | FADE_DOWN | Wed | `60.1%` | 138 | `17` | `1.51` | `28R` | `-4.0R` | `4.47` |
| 1878 | AUDUSD | London | 15m | FADE_DOWN | BtwLowClose | `58.6%` | 222 | `27` | `1.41` | `38R` | `-7.0R` | `4.47` |
| 1879 | GBPJPY | London | 45m | FADE_DOWN | Tue | `59.0%` | 195 | `24` | `1.44` | `35R` | `-9.0R` | `4.47` |
| 1880 | NASDAQ100 | NY Cash | 30m | FADE_UP | Tue | `60.3%` | 131 | `16` | `1.52` | `27R` | `-8.0R` | `4.47` |
| 1881 | XAUUSD | NY | 15m | FADE_DOWN | RSI_50-70 | `57.7%` | 293 | `36` | `1.36` | `45R` | `-9.0R` | `4.47` |
| 1882 | BRENT | NY | 60m | FADE_DOWN | RSI_D>65 | `61.2%` | 103 | `13` | `1.57` | `23R` | `-4.0R` | `4.46` |
| 1883 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | OR_Q4_Wide | `61.2%` | 103 | `13` | `1.57` | `23R` | `-7.0R` | `4.46` |
| 1884 | VIX | NY Cash | 15m | FADE_DOWN | RSI_30-50 | `61.2%` | 103 | `30` | `1.57` | `23R` | `-7.0R` | `4.46` |
| 1885 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | ATR+10% | `63.6%` | 55 | `7` | `1.75` | `15R` | `-5.0R` | `4.46` |
| 1886 | USDJPY | Tokyo | 45m | FADE_DOWN | BtwCloseHigh | `55.7%` | 574 | `70` | `1.26` | `66R` | `-15.0R` | `4.46` |
| 1887 | EURUSD | NY | 60m | FADE_DOWN | AbovePD | `60.9%` | 110 | `14` | `1.56` | `24R` | `-4.0R` | `4.46` |
| 1888 | SP500 | NY Cash | 45m | FADE_UP | RSI>70 | `60.9%` | 110 | `14` | `1.56` | `24R` | `-4.0R` | `4.46` |
| 1889 | EURUSD | NY | 60m | FADE_UP | OR_Q1_Tight | `59.2%` | 179 | `22` | `1.45` | `33R` | `-5.0R` | `4.46` |
| 1890 | EURJPY | London | 30m | FADE_DOWN | Tue | `59.2%` | 179 | `22` | `1.45` | `33R` | `-6.0R` | `4.46` |
| 1891 | XAGUSD | London | 15m | FADE_UP | RSI_D>65 | `60.7%` | 117 | `15` | `1.54` | `25R` | `-7.0R` | `4.46` |
| 1892 | NASDAQ100 | Pre-Market | 30m | FADE_UP | Thu | `60.7%` | 117 | `15` | `1.54` | `25R` | `-5.0R` | `4.46` |
| 1893 | EURUSD | NY | 15m | FADE_UP | BASE | `55.1%` | 739 | `90` | `1.23` | `75R` | `-14.0R` | `4.46` |
| 1894 | EURJPY | London | 15m | FADE_DOWN | Fri | `59.9%` | 147 | `18` | `1.49` | `29R` | `-9.0R` | `4.46` |
| 1895 | SP500 | NY Cash | 30m | FADE_UP | Mon | `59.9%` | 147 | `18` | `1.49` | `29R` | `-15.0R` | `4.46` |
| 1896 | XAGUSD | NY | 30m | FADE_DOWN | OR_Q1_Tight | `58.9%` | 197 | `26` | `1.43` | `35R` | `-5.0R` | `4.46` |
| 1897 | NATGAS | NY | 60m | FADE_UP | BtwLowClose | `59.5%` | 163 | `20` | `1.47` | `31R` | `-8.0R` | `4.46` |
| 1898 | USDJPY | NY | 60m | FADE_UP | RSI_D>65 | `62.5%` | 72 | `9` | `1.67` | `18R` | `-4.0R` | `4.45` |
| 1899 | SP500 | Pre-Market | 45m | FADE_UP | BtwCloseHigh | `58.0%` | 264 | `32` | `1.38` | `42R` | `-11.0R` | `4.45` |
| 1900 | GBPJPY | Tokyo | 15m | FADE_UP | OR_Q4_Wide | `58.2%` | 244 | `30` | `1.39` | `40R` | `-16.0R` | `4.45` |
| 1901 | USDJPY | NY | 45m | FADE_UP | RSI_D<35 | `65.0%` | 40 | `5` | `1.86` | `12R` | `-3.0R` | `4.45` |
| 1902 | GBPJPY | Tokyo | 15m | FADE_UP | RSI>70 | `65.0%` | 40 | `5` | `1.86` | `12R` | `-3.0R` | `4.45` |
| 1903 | XAUUSD | NY | 45m | FADE_DOWN | RSI<30 | `65.0%` | 40 | `5` | `1.86` | `12R` | `-4.0R` | `4.45` |
| 1904 | SP500 | NY Cash | 60m | FADE_DOWN | RSI_D<35 | `65.0%` | 40 | `6` | `1.86` | `12R` | `-3.0R` | `4.45` |
| 1905 | GBPAUD | London | 30m | FADE_DOWN | BtwLowClose | `57.3%` | 330 | `41` | `1.34` | `48R` | `-16.0R` | `4.45` |
| 1906 | XAGUSD | NY | 15m | FADE_UP | AbovePD+RSI_D>65 | `64.0%` | 50 | `6` | `1.78` | `14R` | `-5.0R` | `4.45` |
| 1907 | EURJPY | Tokyo | 15m | FADE_UP | OR_Q4_Wide | `58.0%` | 255 | `32` | `1.38` | `41R` | `-13.0R` | `4.45` |
| 1908 | EURJPY | London | 60m | FADE_UP | RSI_30-50 | `58.0%` | 255 | `31` | `1.38` | `41R` | `-9.0R` | `4.45` |
| 1909 | EURUSD | London | 45m | FADE_DOWN | Fri | `59.3%` | 172 | `21` | `1.46` | `32R` | `-5.0R` | `4.45` |
| 1910 | XAUUSD | NY | 45m | FADE_UP | BtwCloseHigh | `59.3%` | 172 | `21` | `1.46` | `32R` | `-8.0R` | `4.45` |
| 1911 | EURUSD | NY | 30m | FADE_UP | Tue | `60.0%` | 140 | `17` | `1.50` | `28R` | `-6.0R` | `4.45` |
| 1912 | GBPAUD | Sydney | 60m | FADE_UP | RSI_50-70 | `64.4%` | 45 | `6` | `1.81` | `13R` | `-3.0R` | `4.45` |
| 1913 | XAGUSD | London | 45m | FADE_DOWN | Wed | `59.1%` | 181 | `22` | `1.45` | `33R` | `-7.0R` | `4.44` |
| 1914 | USDJPY | NY | 30m | FADE_DOWN | GapSmall | `56.2%` | 477 | `58` | `1.28` | `59R` | `-8.0R` | `4.44` |
| 1915 | USDJPY | NY | 15m | FADE_UP | RSI_30-50 | `58.5%` | 217 | `27` | `1.41` | `37R` | `-9.0R` | `4.44` |
| 1916 | XAUUSD | NY | 15m | FADE_UP | RSI_50-70 | `56.6%` | 408 | `50` | `1.31` | `54R` | `-12.0R` | `4.44` |
| 1917 | GBPUSD | London | 45m | FADE_DOWN | Mon | `58.9%` | 190 | `23` | `1.44` | `34R` | `-11.0R` | `4.44` |
| 1918 | GBPUSD | NY | 15m | FADE_DOWN | OR_Q4_Wide | `58.9%` | 190 | `23` | `1.44` | `34R` | `-6.0R` | `4.44` |
| 1919 | GBPJPY | London | 60m | FADE_UP | OR_Q4_Wide | `58.9%` | 190 | `24` | `1.44` | `34R` | `-14.0R` | `4.44` |
| 1920 | BRENT | London | 60m | FADE_DOWN | Wed | `58.9%` | 190 | `23` | `1.44` | `34R` | `-6.0R` | `4.44` |
| 1921 | AUDUSD | London | 30m | FADE_UP | OR_Q1_Tight | `58.8%` | 199 | `25` | `1.43` | `35R` | `-8.0R` | `4.44` |
| 1922 | EURJPY | London | 60m | FADE_UP | BelowPD | `60.2%` | 133 | `16` | `1.51` | `27R` | `-6.0R` | `4.44` |
| 1923 | XAUUSD | London | 15m | FADE_UP | Thu | `60.2%` | 133 | `17` | `1.51` | `27R` | `-4.0R` | `4.44` |
| 1924 | GBPJPY | London | 15m | FADE_DOWN | RSI_30-50 | `56.5%` | 425 | `52` | `1.30` | `55R` | `-11.0R` | `4.43` |
| 1925 | GBPUSD | NY | 45m | FADE_DOWN | BelowPD | `59.7%` | 149 | `18` | `1.48` | `29R` | `-7.0R` | `4.43` |
| 1926 | BRENT | NY | 30m | FADE_UP | Fri | `59.7%` | 149 | `18` | `1.48` | `29R` | `-5.0R` | `4.43` |
| 1927 | GBPUSD | London | 15m | FADE_UP | RSI_50-70 | `56.6%` | 412 | `51` | `1.30` | `54R` | `-16.0R` | `4.43` |
| 1928 | BRENT | NY | 30m | FADE_UP | Mon | `59.2%` | 174 | `21` | `1.45` | `32R` | `-7.0R` | `4.43` |
| 1929 | EURUSD | NY | 45m | FADE_DOWN | RSI_D<35 | `62.7%` | 67 | `8` | `1.68` | `17R` | `-10.0R` | `4.43` |
| 1930 | GBPUSD | London | 15m | SHAKEOUT_UP | AbovePD | `62.7%` | 67 | `8` | `1.68` | `17R` | `-5.0R` | `4.43` |
| 1931 | AUDUSD | London | 15m | FADE_DOWN | RSI<30 | `62.7%` | 67 | `9` | `1.68` | `17R` | `-3.0R` | `4.43` |
| 1932 | BRENT | London | 30m | SHAKEOUT_UP | Wed | `62.7%` | 67 | `9` | `1.68` | `17R` | `-3.0R` | `4.43` |
| 1933 | WTI | London Initial | 45m | FADE_UP | Mon | `59.0%` | 183 | `22` | `1.44` | `33R` | `-10.0R` | `4.43` |
| 1934 | EURJPY | Tokyo | 15m | FADE_DOWN | RSI_50-70 | `57.8%` | 270 | `33` | `1.37` | `42R` | `-8.0R` | `4.43` |
| 1935 | AUDUSD | London | 60m | FADE_UP | Fri | `58.7%` | 201 | `25` | `1.42` | `35R` | `-7.0R` | `4.43` |
| 1936 | GBPJPY | London | 60m | FADE_UP | Thu | `58.7%` | 201 | `25` | `1.42` | `35R` | `-13.0R` | `4.43` |
| 1937 | USDJPY | Tokyo | 30m | FADE_DOWN | Mon | `58.9%` | 192 | `24` | `1.43` | `34R` | `-10.0R` | `4.43` |
| 1938 | NATGAS | NY | 60m | FADE_DOWN | RSI_50-70 | `58.9%` | 192 | `24` | `1.43` | `34R` | `-5.0R` | `4.43` |
| 1939 | SP500 | Pre-Market | 60m | FADE_UP | OR_Q4_Wide | `58.9%` | 192 | `24` | `1.43` | `34R` | `-8.0R` | `4.43` |
| 1940 | GBPJPY | London | 30m | FADE_UP | BtwCloseHigh | `57.4%` | 303 | `37` | `1.35` | `45R` | `-7.0R` | `4.43` |
| 1941 | XAUUSD | NY | 15m | FADE_DOWN | GapSmall | `55.8%` | 534 | `66` | `1.26` | `62R` | `-12.0R` | `4.43` |
| 1942 | BRENT | NY | 45m | FADE_UP | Tue | `59.9%` | 142 | `18` | `1.49` | `28R` | `-5.0R` | `4.42` |
| 1943 | GBPJPY | Tokyo | 15m | FADE_UP | RSI_50-70 | `56.4%` | 431 | `53` | `1.29` | `55R` | `-11.0R` | `4.42` |
| 1944 | XAUUSD | London | 45m | FADE_UP | RSI_50-70 | `55.6%` | 572 | `70` | `1.25` | `64R` | `-11.0R` | `4.42` |
| 1945 | WTI | London Initial | 30m | FADE_DOWN | BtwCloseHigh | `57.7%` | 272 | `33` | `1.37` | `42R` | `-6.0R` | `4.42` |
| 1946 | WTI | London Initial | 45m | FADE_UP | Tue | `59.3%` | 167 | `21` | `1.46` | `31R` | `-9.0R` | `4.42` |
| 1947 | USDJPY | NY | 30m | FADE_UP | Thu | `60.0%` | 135 | `17` | `1.50` | `27R` | `-5.0R` | `4.41` |
| 1948 | NASDAQ100 | NY Cash | 30m | FADE_UP | Thu | `60.0%` | 135 | `17` | `1.50` | `27R` | `-9.0R` | `4.41` |
| 1949 | NASDAQ100 | Pre-Market | 45m | FADE_UP | RSI_50-70 | `56.2%` | 463 | `57` | `1.28` | `57R` | `-8.0R` | `4.41` |
| 1950 | GBPJPY | London | 45m | FADE_DOWN | BtwLowClose | `57.2%` | 318 | `39` | `1.34` | `46R` | `-9.0R` | `4.41` |
| 1951 | GBPUSD | NY | 15m | FADE_DOWN | BtwCloseHigh | `59.1%` | 176 | `22` | `1.44` | `32R` | `-9.0R` | `4.41` |
| 1952 | GBPUSD | London | 60m | FADE_DOWN | BtwLowClose | `57.0%` | 342 | `42` | `1.33` | `48R` | `-10.0R` | `4.41` |
| 1953 | WTI | London Initial | 30m | FADE_UP | BtwCloseHigh | `57.9%` | 252 | `32` | `1.38` | `40R` | `-16.0R` | `4.41` |
| 1954 | SP500 | NY Cash | 15m | FADE_DOWN | RSI_50-70 | `57.9%` | 252 | `31` | `1.38` | `40R` | `-5.0R` | `4.41` |
| 1955 | SP500 | NY Cash | 30m | FADE_DOWN | BtwCloseHigh | `57.9%` | 252 | `31` | `1.38` | `40R` | `-5.0R` | `4.41` |
| 1956 | SP500 | NY Cash | 30m | FADE_UP | BtwLowClose | `58.6%` | 203 | `25` | `1.42` | `35R` | `-11.0R` | `4.41` |
| 1957 | EURUSD | London | 60m | FADE_UP | Mon | `58.9%` | 185 | `23` | `1.43` | `33R` | `-7.0R` | `4.41` |
| 1958 | GBPUSD | London | 30m | FADE_DOWN | Tue | `58.8%` | 194 | `24` | `1.43` | `34R` | `-6.0R` | `4.41` |
| 1959 | VIX | NY Cash | 15m | FADE_DOWN | BASE | `58.8%` | 194 | `57` | `1.43` | `34R` | `-7.0R` | `4.41` |
| 1960 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | RSI_30-50 | `61.6%` | 86 | `11` | `1.61` | `20R` | `-4.0R` | `4.41` |
| 1961 | EURJPY | London | 45m | FADE_DOWN | BelowPD | `60.2%` | 128 | `16` | `1.51` | `26R` | `-11.0R` | `4.41` |
| 1962 | WTI | NY Main | 15m | FADE_DOWN | BtwLowClose | `58.0%` | 243 | `30` | `1.38` | `39R` | `-8.0R` | `4.41` |
| 1963 | WTI | NY Main | 45m | FADE_DOWN | RSI_30-50 | `56.7%` | 383 | `47` | `1.31` | `51R` | `-24.0R` | `4.41` |
| 1964 | GBPUSD | London | 30m | FADE_DOWN | OR_Q1_Tight | `58.4%` | 214 | `27` | `1.40` | `36R` | `-8.0R` | `4.40` |
| 1965 | GBPAUD | London | 45m | FADE_DOWN | Fri | `58.4%` | 214 | `26` | `1.40` | `36R` | `-12.0R` | `4.40` |
| 1966 | XAGUSD | NY | 60m | FADE_UP | Fri | `62.9%` | 62 | `8` | `1.70` | `16R` | `-6.0R` | `4.40` |
| 1967 | WTI | London Initial | 30m | FADE_DOWN | RSI_D<35 | `62.9%` | 62 | `8` | `1.70` | `16R` | `-4.0R` | `4.40` |
| 1968 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | Mon | `62.9%` | 62 | `8` | `1.70` | `16R` | `-4.0R` | `4.40` |
| 1969 | AUDUSD | London | 45m | FADE_DOWN | BtwCloseHigh | `57.4%` | 298 | `37` | `1.35` | `44R` | `-14.0R` | `4.40` |
| 1970 | EURUSD | London | 15m | FADE_DOWN | Fri | `59.7%` | 144 | `18` | `1.48` | `28R` | `-7.0R` | `4.40` |
| 1971 | XAUUSD | NY | 60m | FADE_DOWN | OR_Q1_Tight | `59.7%` | 144 | `24` | `1.48` | `28R` | `-7.0R` | `4.40` |
| 1972 | BRENT | NY | 45m | FADE_DOWN | Mon | `59.7%` | 144 | `18` | `1.48` | `28R` | `-6.0R` | `4.40` |
| 1973 | SP500 | Pre-Market | 15m | FADE_UP | RSI_30-50 | `59.7%` | 144 | `18` | `1.48` | `28R` | `-6.0R` | `4.40` |
| 1974 | USDJPY | NY | 15m | FADE_UP | Fri | `60.3%` | 121 | `15` | `1.52` | `25R` | `-12.0R` | `4.40` |
| 1975 | EURUSD | NY | 15m | FADE_UP | RSI_30-50 | `57.6%` | 276 | `34` | `1.36` | `42R` | `-6.0R` | `4.40` |
| 1976 | GBPAUD | London | 30m | FADE_UP | RSI_50-70 | `56.1%` | 471 | `58` | `1.28` | `57R` | `-14.0R` | `4.40` |
| 1977 | XAUUSD | NY | 45m | FADE_DOWN | Mon | `61.3%` | 93 | `11` | `1.58` | `21R` | `-5.0R` | `4.40` |
| 1978 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | OR_Q4_Wide | `61.3%` | 93 | `12` | `1.58` | `21R` | `-6.0R` | `4.40` |
| 1979 | XAUUSD | London | 15m | FADE_DOWN | BtwCloseHigh | `59.0%` | 178 | `22` | `1.44` | `32R` | `-5.0R` | `4.40` |
| 1980 | EURJPY | London | 45m | FADE_DOWN | OR_Q4_Wide | `58.8%` | 187 | `23` | `1.43` | `33R` | `-14.0R` | `4.40` |
| 1981 | XAGUSD | London | 15m | SHAKEOUT_DOWN | Fri | `62.2%` | 74 | `10` | `1.64` | `18R` | `-5.0R` | `4.40` |
| 1982 | GBPJPY | Tokyo | 15m | FADE_DOWN | RSI_30-50 | `56.7%` | 374 | `46` | `1.31` | `50R` | `-15.0R` | `4.39` |
| 1983 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | RSI<30 | `61.0%` | 100 | `12` | `1.56` | `22R` | `-4.0R` | `4.39` |
| 1984 | NASDAQ100 | NY Cash | 45m | FADE_UP | Tue | `60.7%` | 107 | `13` | `1.55` | `23R` | `-8.0R` | `4.39` |
| 1985 | AUDUSD | London | 15m | FADE_UP | RSI_30-50 | `57.7%` | 267 | `33` | `1.36` | `41R` | `-9.0R` | `4.39` |
| 1986 | NASDAQ100 | NY Cash | 60m | FADE_UP | RSI_50-70 | `57.7%` | 267 | `33` | `1.36` | `41R` | `-8.0R` | `4.39` |
| 1987 | XAGUSD | NY | 15m | FADE_DOWN | OR_Q4_Wide | `59.5%` | 153 | `23` | `1.47` | `29R` | `-6.0R` | `4.39` |
| 1988 | SP500 | Pre-Market | 30m | FADE_UP | GapSmall | `55.9%` | 492 | `60` | `1.27` | `58R` | `-11.0R` | `4.39` |
| 1989 | WTI | London Initial | 30m | FADE_UP | Thu | `59.9%` | 137 | `17` | `1.49` | `27R` | `-6.0R` | `4.39` |
| 1990 | WTI | NY Main | 30m | FADE_UP | RSI_D>65 | `59.9%` | 137 | `17` | `1.49` | `27R` | `-7.0R` | `4.39` |
| 1991 | NATGAS | NY | 30m | FADE_UP | OR_Q1_Tight | `58.3%` | 216 | `28` | `1.40` | `36R` | `-7.0R` | `4.39` |
| 1992 | USDJPY | Tokyo | 60m | MOMENTUM_DOWN | ATR+10% | `58.3%` | 36 | `4` | `2.10` | `16R` | `-6.0R` | `4.39` |
| 1993 | XAGUSD | London | 60m | FADE_UP | OR_Q1_Tight | `58.1%` | 236 | `38` | `1.38` | `38R` | `-7.0R` | `4.39` |
| 1994 | BRENT | NY | 60m | FADE_UP | BtwCloseHigh | `58.5%` | 207 | `26` | `1.41` | `35R` | `-9.0R` | `4.39` |
| 1995 | AUDUSD | London | 60m | FADE_DOWN | RSI_30-50 | `55.7%` | 528 | `65` | `1.26` | `60R` | `-9.0R` | `4.39` |
| 1996 | GBPUSD | London | 60m | FADE_DOWN | OR_Q1_Tight | `57.9%` | 247 | `31` | `1.38` | `39R` | `-13.0R` | `4.39` |
| 1997 | GBPJPY | London | 45m | FADE_DOWN | RSI_50-70 | `57.5%` | 280 | `34` | `1.35` | `42R` | `-10.0R` | `4.38` |
| 1998 | USDJPY | NY | 60m | FADE_DOWN | BtwLowClose | `59.6%` | 146 | `18` | `1.47` | `28R` | `-7.0R` | `4.38` |
| 1999 | XAUUSD | NY | 45m | FADE_UP | RSI_30-50 | `59.6%` | 146 | `18` | `1.47` | `28R` | `-6.0R` | `4.38` |
| 2000 | BRENT | NY | 15m | FADE_DOWN | Mon | `59.6%` | 146 | `18` | `1.47` | `28R` | `-6.0R` | `4.38` |
| 2001 | SP500 | Pre-Market | 45m | FADE_UP | RSI>70 | `61.7%` | 81 | `11` | `1.61` | `19R` | `-5.0R` | `4.38` |
| 2002 | VIX | NY Cash | 60m | FADE_UP | BtwLowClose | `61.7%` | 81 | `24` | `1.61` | `19R` | `-3.0R` | `4.38` |
| 2003 | EURJPY | Tokyo | 60m | FADE_DOWN | OR_Q1_Tight | `57.7%` | 260 | `33` | `1.36` | `40R` | `-11.0R` | `4.37` |
| 2004 | GBPUSD | NY | 15m | FADE_UP | RSI_50-70 | `56.5%` | 382 | `47` | `1.30` | `50R` | `-15.0R` | `4.37` |
| 2005 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | BASE | `55.3%` | 591 | `72` | `1.24` | `63R` | `-13.0R` | `4.37` |
| 2006 | GBPAUD | London | 30m | FADE_DOWN | OR_Q1_Tight | `58.4%` | 209 | `26` | `1.40` | `35R` | `-10.0R` | `4.37` |
| 2007 | EURUSD | NY | 45m | FADE_DOWN | Tue | `60.2%` | 123 | `15` | `1.51` | `25R` | `-5.0R` | `4.37` |
| 2008 | SP500 | NY Cash | 60m | FADE_DOWN | Tue | `60.2%` | 123 | `16` | `1.51` | `25R` | `-5.0R` | `4.37` |
| 2009 | SP500 | NY Cash | 15m | FADE_UP | GapSmall | `55.2%` | 612 | `75` | `1.23` | `64R` | `-11.0R` | `4.37` |
| 2010 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | OR_Q1_Tight | `59.7%` | 139 | `22` | `1.48` | `27R` | `-9.0R` | `4.37` |
| 2011 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | RSI_D>65 | `59.7%` | 139 | `18` | `1.48` | `27R` | `-7.0R` | `4.37` |
| 2012 | EURJPY | London | 30m | FADE_DOWN | Fri | `59.1%` | 164 | `20` | `1.45` | `30R` | `-6.0R` | `4.37` |
| 2013 | SP500 | NY Cash | 15m | FADE_DOWN | AbovePD | `59.1%` | 164 | `21` | `1.45` | `30R` | `-7.0R` | `4.37` |
| 2014 | SP500 | Pre-Market | 60m | FADE_DOWN | RSI_50-70 | `57.8%` | 251 | `31` | `1.37` | `39R` | `-7.0R` | `4.37` |
| 2015 | EURJPY | London | 30m | FADE_DOWN | OR_Q1_Tight | `58.6%` | 191 | `24` | `1.42` | `33R` | `-9.0R` | `4.37` |
| 2016 | USDJPY | Tokyo | 45m | FADE_UP | OR_Q1_Tight | `57.6%` | 262 | `34` | `1.36` | `40R` | `-11.0R` | `4.37` |
| 2017 | EURUSD | London | 30m | FADE_DOWN | Fri | `59.0%` | 173 | `21` | `1.44` | `31R` | `-5.0R` | `4.36` |
| 2018 | USDJPY | Tokyo | 45m | FADE_UP | RSI_D>65 | `59.0%` | 173 | `22` | `1.44` | `31R` | `-4.0R` | `4.36` |
| 2019 | GBPJPY | Tokyo | 45m | FADE_UP | RSI>70 | `62.3%` | 69 | `9` | `1.65` | `17R` | `-7.0R` | `4.36` |
| 2020 | VIX | NY Cash | 15m | FADE_DOWN | OR_Q4_Wide | `62.3%` | 69 | `20` | `1.65` | `17R` | `-4.0R` | `4.36` |
| 2021 | NATGAS | NY | 45m | FADE_DOWN | RSI<30 | `61.4%` | 88 | `11` | `1.59` | `20R` | `-6.0R` | `4.36` |
| 2022 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | BelowPD | `61.4%` | 88 | `11` | `1.59` | `20R` | `-4.0R` | `4.36` |
| 2023 | EURUSD | London | 15m | FADE_DOWN | BelowPD | `61.1%` | 95 | `12` | `1.57` | `21R` | `-4.0R` | `4.36` |
| 2024 | EURUSD | NY | 45m | FADE_UP | OR_Q1_Tight | `58.4%` | 202 | `25` | `1.40` | `34R` | `-10.0R` | `4.36` |
| 2025 | AUDUSD | London | 30m | FADE_DOWN | OR_Q1_Tight | `58.4%` | 202 | `26` | `1.40` | `34R` | `-9.0R` | `4.36` |
| 2026 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | Tue | `63.5%` | 52 | `7` | `1.74` | `14R` | `-3.0R` | `4.36` |
| 2027 | EURJPY | Tokyo | 15m | FADE_UP | RSI_50-70 | `55.6%` | 516 | `63` | `1.25` | `58R` | `-11.0R` | `4.35` |
| 2028 | EURUSD | London | 45m | FADE_DOWN | Tue | `58.5%` | 193 | `24` | `1.41` | `33R` | `-12.0R` | `4.35` |
| 2029 | USDJPY | NY | 30m | FADE_DOWN | BtwCloseHigh | `58.5%` | 193 | `24` | `1.41` | `33R` | `-5.0R` | `4.35` |
| 2030 | NASDAQ100 | Pre-Market | 60m | FADE_UP | RSI_D>65 | `58.5%` | 193 | `25` | `1.41` | `33R` | `-6.0R` | `4.35` |
| 2031 | SP500 | NY Cash | 15m | FADE_DOWN | Thu | `59.2%` | 157 | `19` | `1.45` | `29R` | `-10.0R` | `4.35` |
| 2032 | BRENT | NY | 30m | FADE_DOWN | AbovePD | `58.9%` | 175 | `22` | `1.43` | `31R` | `-11.0R` | `4.35` |
| 2033 | NATGAS | NY | 15m | FADE_DOWN | GapSmall | `55.0%` | 638 | `78` | `1.22` | `64R` | `-37.0R` | `4.35` |
| 2034 | BRENT | NY | 45m | FADE_DOWN | Thu | `59.6%` | 141 | `17` | `1.47` | `27R` | `-9.0R` | `4.34` |
| 2035 | GBPAUD | Sydney | 15m | FADE_UP | Tue | `65.6%` | 32 | `4` | `1.91` | `10R` | `-3.0R` | `4.34` |
| 2036 | GBPAUD | Sydney | 30m | FADE_UP | OR_Q4_Wide | `65.6%` | 32 | `4` | `1.91` | `10R` | `-3.0R` | `4.34` |
| 2037 | XAUUSD | London | 60m | FADE_UP | ATR-10% | `65.6%` | 32 | `4` | `1.91` | `10R` | `-2.0R` | `4.34` |
| 2038 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | Thu | `65.6%` | 32 | `4` | `1.91` | `10R` | `-2.0R` | `4.34` |
| 2039 | GBPJPY | Tokyo | 15m | FADE_DOWN | BtwCloseHigh | `56.3%` | 396 | `49` | `1.29` | `50R` | `-16.0R` | `4.34` |
| 2040 | XAGUSD | NY | 60m | FADE_DOWN | Mon | `61.8%` | 76 | `10` | `1.62` | `18R` | `-7.0R` | `4.34` |
| 2041 | NATGAS | NY | 30m | FADE_UP | RSI_30-50 | `57.5%` | 268 | `33` | `1.35` | `40R` | `-5.0R` | `4.34` |
| 2042 | BRENT | NY | 60m | FADE_DOWN | OR_Q1_Tight | `58.5%` | 195 | `24` | `1.41` | `33R` | `-10.0R` | `4.34` |
| 2043 | GBPJPY | London | 45m | FADE_UP | BtwCloseHigh | `56.8%` | 329 | `40` | `1.32` | `45R` | `-8.0R` | `4.34` |
| 2044 | SP500 | Pre-Market | 30m | FADE_DOWN | OR_Q1_Tight | `63.8%` | 47 | `12` | `1.76` | `13R` | `-3.0R` | `4.34` |
| 2045 | SP500 | NY Cash | 15m | FADE_DOWN | AbovePD+RSI_D>65 | `63.8%` | 47 | `7` | `1.76` | `13R` | `-3.0R` | `4.34` |
| 2046 | USDJPY | Tokyo | 45m | FADE_UP | Fri | `58.1%` | 215 | `26` | `1.39` | `35R` | `-11.0R` | `4.34` |
| 2047 | WTI | London Initial | 45m | FADE_DOWN | Mon | `58.8%` | 177 | `22` | `1.42` | `31R` | `-6.0R` | `4.33` |
| 2048 | SP500 | NY Cash | 30m | FADE_UP | AbovePD | `58.8%` | 177 | `22` | `1.42` | `31R` | `-9.0R` | `4.33` |
| 2049 | GBPJPY | Tokyo | 15m | FADE_UP | BtwLowClose | `57.4%` | 270 | `33` | `1.35` | `40R` | `-10.0R` | `4.33` |
| 2050 | GBPUSD | London | 60m | FADE_UP | RSI_50-70 | `55.5%` | 517 | `63` | `1.25` | `57R` | `-8.0R` | `4.33` |
| 2051 | XAUUSD | NY | 30m | FADE_UP | RSI_50-70 | `56.4%` | 374 | `46` | `1.29` | `48R` | `-11.0R` | `4.33` |
| 2052 | EURJPY | Tokyo | 15m | FADE_UP | RSI_30-50 | `58.1%` | 217 | `27` | `1.38` | `35R` | `-6.0R` | `4.33` |
| 2053 | EURUSD | London | 30m | FADE_UP | Mon | `58.4%` | 197 | `24` | `1.40` | `33R` | `-8.0R` | `4.33` |
| 2054 | WTI | NY Main | 60m | FADE_DOWN | ATR+10% | `64.9%` | 37 | `5` | `1.85` | `11R` | `-5.0R` | `4.32` |
| 2055 | AUDUSD | London | 45m | FADE_DOWN | BtwLowClose | `57.4%` | 272 | `34` | `1.34` | `40R` | `-11.0R` | `4.32` |
| 2056 | EURUSD | NY | 15m | FADE_DOWN | RSI_D<35 | `60.6%` | 104 | `13` | `1.54` | `22R` | `-4.0R` | `4.32` |
| 2057 | EURUSD | London | 15m | FADE_DOWN | OR_Q1_Tight | `61.1%` | 90 | `13` | `1.57` | `20R` | `-6.0R` | `4.32` |
| 2058 | SP500 | NY Cash | 15m | FADE_DOWN | RSI_30-50 | `56.5%` | 363 | `45` | `1.30` | `47R` | `-15.0R` | `4.32` |
| 2059 | XAUUSD | London | 15m | FADE_UP | OR_Q4_Wide | `58.2%` | 208 | `27` | `1.39` | `34R` | `-10.0R` | `4.32` |
| 2060 | GBPUSD | London | 15m | FADE_UP | Wed | `59.2%` | 152 | `19` | `1.45` | `28R` | `-9.0R` | `4.32` |
| 2061 | WTI | NY Main | 60m | FADE_DOWN | AbovePD | `59.2%` | 152 | `19` | `1.45` | `28R` | `-7.0R` | `4.32` |
| 2062 | WTI | London Initial | 60m | FADE_DOWN | OR_Q1_Tight | `58.7%` | 179 | `22` | `1.42` | `31R` | `-9.0R` | `4.32` |
| 2063 | SP500 | Pre-Market | 30m | FADE_UP | OR_Q4_Wide | `58.0%` | 219 | `27` | `1.38` | `35R` | `-10.0R` | `4.31` |
| 2064 | GBPUSD | London | 15m | FADE_DOWN | BtwCloseHigh | `57.4%` | 263 | `33` | `1.35` | `39R` | `-10.0R` | `4.31` |
| 2065 | WTI | London Initial | 30m | FADE_UP | BtwLowClose | `57.4%` | 263 | `32` | `1.35` | `39R` | `-10.0R` | `4.31` |
| 2066 | GBPJPY | London | 30m | FADE_DOWN | Tue | `58.3%` | 199 | `24` | `1.40` | `33R` | `-6.0R` | `4.31` |
| 2067 | GBPAUD | London | 60m | FADE_UP | BtwLowClose | `56.5%` | 352 | `43` | `1.30` | `46R` | `-14.0R` | `4.31` |
| 2068 | SP500 | NY Cash | 30m | FADE_DOWN | RSI_50-70 | `57.5%` | 252 | `31` | `1.36` | `38R` | `-7.0R` | `4.31` |
| 2069 | NASDAQ100 | Pre-Market | 15m | FADE_UP | GapSmall | `57.5%` | 252 | `31` | `1.36` | `38R` | `-20.0R` | `4.31` |
| 2070 | WTI | London Initial | 30m | FADE_UP | RSI_D>65 | `60.0%` | 120 | `15` | `1.50` | `24R` | `-4.0R` | `4.31` |
| 2071 | BRENT | London | 30m | FADE_DOWN | Fri | `60.0%` | 120 | `15` | `1.50` | `24R` | `-5.0R` | `4.31` |
| 2072 | USDJPY | NY | 15m | FADE_DOWN | OR_Q4_Wide | `58.4%` | 190 | `23` | `1.41` | `32R` | `-12.0R` | `4.31` |
| 2073 | AUDUSD | London | 60m | FADE_DOWN | Thu | `58.4%` | 190 | `23` | `1.41` | `32R` | `-7.0R` | `4.31` |
| 2074 | GBPJPY | Tokyo | 45m | FADE_UP | Mon | `58.4%` | 190 | `23` | `1.41` | `32R` | `-4.0R` | `4.31` |
| 2075 | GBPAUD | London | 60m | FADE_UP | Thu | `58.4%` | 190 | `24` | `1.41` | `32R` | `-7.0R` | `4.31` |
| 2076 | EURJPY | Tokyo | 45m | FADE_UP | Fri | `58.1%` | 210 | `26` | `1.39` | `34R` | `-7.0R` | `4.31` |
| 2077 | WTI | London Initial | 30m | SHAKEOUT_UP | Wed | `62.0%` | 71 | `9` | `1.63` | `17R` | `-4.0R` | `4.30` |
| 2078 | BRENT | NY | 60m | FADE_DOWN | RSI_D<35 | `62.0%` | 71 | `9` | `1.63` | `17R` | `-6.0R` | `4.30` |
| 2079 | SP500 | Pre-Market | 30m | FADE_DOWN | BASE | `55.1%` | 575 | `70` | `1.23` | `59R` | `-21.0R` | `4.30` |
| 2080 | EURUSD | NY | 60m | FADE_DOWN | OR_Q1_Tight | `58.6%` | 181 | `23` | `1.41` | `31R` | `-7.0R` | `4.30` |
| 2081 | GBPAUD | London | 15m | FADE_UP | Thu | `59.3%` | 145 | `18` | `1.46` | `27R` | `-9.0R` | `4.30` |
| 2082 | GBPJPY | London | 30m | FADE_UP | OR_Q4_Wide | `57.8%` | 232 | `29` | `1.37` | `36R` | `-12.0R` | `4.30` |
| 2083 | SP500 | NY Cash | 30m | FADE_UP | BtwCloseHigh | `57.6%` | 243 | `30` | `1.36` | `37R` | `-9.0R` | `4.30` |
| 2084 | WTI | NY Main | 30m | FADE_DOWN | RSI_30-50 | `56.0%` | 416 | `51` | `1.27` | `50R` | `-13.0R` | `4.30` |
| 2085 | EURJPY | London | 60m | FADE_DOWN | RSI_D<35 | `62.7%` | 59 | `9` | `1.68` | `15R` | `-3.0R` | `4.30` |
| 2086 | VIX | NY Cash | 45m | FADE_DOWN | BelowPD | `62.7%` | 59 | `17` | `1.68` | `15R` | `-3.0R` | `4.30` |
| 2087 | XAGUSD | London | 30m | FADE_DOWN | Tue | `58.7%` | 172 | `22` | `1.42` | `30R` | `-7.0R` | `4.30` |
| 2088 | USDJPY | Tokyo | 30m | FADE_DOWN | Wed | `59.1%` | 154 | `19` | `1.44` | `28R` | `-8.0R` | `4.30` |
| 2089 | WTI | London Initial | 30m | FADE_DOWN | Thu | `59.1%` | 154 | `19` | `1.44` | `28R` | `-7.0R` | `4.30` |
| 2090 | AUDUSD | London | 45m | FADE_DOWN | RSI_D<35 | `60.2%` | 113 | `15` | `1.51` | `23R` | `-10.0R` | `4.30` |
| 2091 | EURJPY | London | 60m | FADE_DOWN | RSI_D>65 | `60.2%` | 113 | `15` | `1.51` | `23R` | `-7.0R` | `4.30` |
| 2092 | XAUUSD | NY | 60m | FADE_UP | Wed | `60.2%` | 113 | `14` | `1.51` | `23R` | `-5.0R` | `4.30` |
| 2093 | NASDAQ100 | Pre-Market | 15m | FADE_UP | BtwLowClose | `60.2%` | 113 | `14` | `1.51` | `23R` | `-9.0R` | `4.30` |
| 2094 | GBPJPY | London | 15m | FADE_UP | Tue | `58.9%` | 163 | `20` | `1.43` | `29R` | `-9.0R` | `4.30` |
| 2095 | WTI | NY Main | 15m | FADE_DOWN | BelowPD | `58.9%` | 163 | `20` | `1.43` | `29R` | `-8.0R` | `4.30` |
| 2096 | BRENT | NY | 15m | FADE_DOWN | Fri | `58.9%` | 163 | `20` | `1.43` | `29R` | `-9.0R` | `4.30` |
| 2097 | GBPUSD | NY | 60m | FADE_UP | AbovePD | `59.7%` | 129 | `16` | `1.48` | `25R` | `-7.0R` | `4.30` |
| 2098 | XAGUSD | London | 60m | FADE_UP | Tue | `58.3%` | 192 | `24` | `1.40` | `32R` | `-11.0R` | `4.29` |
| 2099 | NASDAQ100 | Pre-Market | 30m | FADE_UP | RSI_D>65 | `60.4%` | 106 | `14` | `1.52` | `22R` | `-7.0R` | `4.29` |
| 2100 | USDJPY | Tokyo | 30m | FADE_DOWN | BtwCloseHigh | `55.2%` | 547 | `67` | `1.23` | `57R` | `-13.0R` | `4.29` |
| 2101 | WTI | NY Main | 30m | FADE_UP | Thu | `58.5%` | 183 | `22` | `1.41` | `31R` | `-4.0R` | `4.29` |
| 2102 | GBPJPY | London | 60m | FADE_UP | BtwLowClose | `56.6%` | 334 | `41` | `1.30` | `44R` | `-8.0R` | `4.29` |
| 2103 | XAGUSD | NY | 45m | FADE_DOWN | Mon | `60.6%` | 99 | `12` | `1.54` | `21R` | `-7.0R` | `4.28` |
| 2104 | AUDUSD | London | 45m | FADE_DOWN | Thu | `58.6%` | 174 | `21` | `1.42` | `30R` | `-8.0R` | `4.28` |
| 2105 | AUDUSD | London | 45m | FADE_DOWN | OR_Q4_Wide | `57.9%` | 214 | `26` | `1.38` | `34R` | `-9.0R` | `4.28` |
| 2106 | XAGUSD | NY | 45m | FADE_DOWN | Thu | `61.2%` | 85 | `10` | `1.58` | `19R` | `-5.0R` | `4.28` |
| 2107 | EURUSD | NY | 45m | FADE_DOWN | BtwLowClose | `59.2%` | 147 | `18` | `1.45` | `27R` | `-7.0R` | `4.28` |
| 2108 | GBPJPY | London | 30m | FADE_DOWN | Fri | `58.8%` | 165 | `20` | `1.43` | `29R` | `-7.0R` | `4.28` |
| 2109 | EURUSD | London | 45m | FADE_DOWN | BelowPD | `60.9%` | 92 | `12` | `1.56` | `20R` | `-5.0R` | `4.28` |
| 2110 | GBPUSD | NY | 30m | FADE_UP | RSI_D>65 | `60.9%` | 92 | `11` | `1.56` | `20R` | `-4.0R` | `4.28` |
| 2111 | XAGUSD | NY | 60m | FADE_DOWN | AbovePD | `60.9%` | 92 | `11` | `1.56` | `20R` | `-4.0R` | `4.28` |
| 2112 | BRENT | NY | 15m | FADE_UP | Thu | `59.0%` | 156 | `19` | `1.44` | `28R` | `-5.0R` | `4.28` |
| 2113 | BRENT | London | 45m | FADE_UP | BtwLowClose | `56.8%` | 310 | `39` | `1.31` | `42R` | `-10.0R` | `4.28` |
| 2114 | GBPAUD | London | 45m | FADE_UP | Tue | `58.0%` | 205 | `25` | `1.38` | `33R` | `-9.0R` | `4.28` |
| 2115 | GBPUSD | London | 30m | FADE_DOWN | RSI_50-70 | `56.5%` | 338 | `42` | `1.30` | `44R` | `-13.0R` | `4.28` |
| 2116 | XAUUSD | NY | 45m | FADE_UP | OR_Q1_Tight | `58.4%` | 185 | `27` | `1.40` | `31R` | `-6.0R` | `4.27` |
| 2117 | XAUUSD | London | 60m | FADE_DOWN | BtwLowClose | `56.6%` | 325 | `40` | `1.30` | `43R` | `-9.0R` | `4.27` |
| 2118 | WTI | London Initial | 60m | FADE_DOWN | BtwLowClose | `56.6%` | 325 | `40` | `1.30` | `43R` | `-11.0R` | `4.27` |
| 2119 | GBPUSD | London | 15m | FADE_DOWN | RSI_30-50 | `56.1%` | 383 | `47` | `1.28` | `47R` | `-8.0R` | `4.27` |
| 2120 | WTI | NY Main | 30m | FADE_DOWN | BtwCloseHigh | `57.7%` | 227 | `28` | `1.36` | `35R` | `-13.0R` | `4.27` |
| 2121 | NATGAS | NY | 45m | FADE_UP | OR_Q4_Wide | `59.5%` | 131 | `18` | `1.47` | `25R` | `-6.0R` | `4.27` |
| 2122 | GBPUSD | NY | 30m | FADE_UP | RSI>70 | `63.0%` | 54 | `7` | `1.70` | `14R` | `-2.0R` | `4.27` |
| 2123 | SP500 | NY Cash | 45m | FADE_UP | AbovePD+RSI_D>65 | `63.0%` | 54 | `8` | `1.70` | `14R` | `-4.0R` | `4.27` |
| 2124 | NASDAQ100 | Pre-Market | 60m | FADE_UP | AbovePD+RSI_D>65 | `63.0%` | 54 | `7` | `1.70` | `14R` | `-4.0R` | `4.27` |
| 2125 | VIX | NY Cash | 30m | FADE_UP | Wed | `63.0%` | 54 | `16` | `1.70` | `14R` | `-4.0R` | `4.27` |
| 2126 | XAGUSD | London | 60m | FADE_UP | RSI_D>65 | `58.5%` | 176 | `23` | `1.41` | `30R` | `-8.0R` | `4.27` |
| 2127 | VIX | NY Cash | 30m | FADE_DOWN | BelowPD | `62.1%` | 66 | `20` | `1.64` | `16R` | `-4.0R` | `4.27` |
| 2128 | VIX | NY Cash | 30m | FADE_DOWN | OR_Q4_Wide | `62.1%` | 66 | `19` | `1.64` | `16R` | `-5.0R` | `4.27` |
| 2129 | GBPAUD | London | 30m | FADE_UP | BtwCloseHigh | `57.4%` | 251 | `31` | `1.35` | `37R` | `-14.0R` | `4.27` |
| 2130 | WTI | London Initial | 60m | FADE_UP | AbovePD | `59.3%` | 140 | `18` | `1.46` | `26R` | `-5.0R` | `4.27` |
| 2131 | NASDAQ100 | NY Cash | 60m | FADE_UP | BtwLowClose | `59.3%` | 140 | `17` | `1.46` | `26R` | `-5.0R` | `4.27` |
| 2132 | WTI | London Initial | 45m | FADE_DOWN | Wed | `58.7%` | 167 | `21` | `1.42` | `29R` | `-5.0R` | `4.27` |
| 2133 | XAUUSD | London | 60m | FADE_UP | BtwCloseHigh | `56.8%` | 301 | `37` | `1.32` | `41R` | `-9.0R` | `4.26` |
| 2134 | USDJPY | NY | 60m | FADE_DOWN | RSI_50-70 | `58.9%` | 158 | `19` | `1.43` | `28R` | `-5.0R` | `4.26` |
| 2135 | WTI | London Initial | 30m | FADE_UP | Mon | `58.9%` | 158 | `19` | `1.43` | `28R` | `-5.0R` | `4.26` |
| 2136 | NASDAQ100 | NY Cash | 30m | FADE_UP | Wed | `59.1%` | 149 | `18` | `1.44` | `27R` | `-5.0R` | `4.26` |
| 2137 | GBPUSD | London | 45m | FADE_UP | RSI_50-70 | `55.4%` | 491 | `60` | `1.24` | `53R` | `-10.0R` | `4.26` |
| 2138 | XAGUSD | NY | 15m | FADE_DOWN | RSI_30-50 | `56.4%` | 344 | `42` | `1.29` | `44R` | `-11.0R` | `4.26` |
| 2139 | GBPAUD | London | 15m | FADE_DOWN | RSI_30-50 | `55.9%` | 406 | `50` | `1.27` | `48R` | `-11.0R` | `4.26` |
| 2140 | GBPAUD | London | 45m | FADE_DOWN | RSI_50-70 | `56.8%` | 303 | `37` | `1.31` | `41R` | `-13.0R` | `4.26` |
| 2141 | GBPJPY | Tokyo | 15m | FADE_UP | RSI_30-50 | `58.4%` | 178 | `22` | `1.41` | `30R` | `-8.0R` | `4.25` |
| 2142 | GBPJPY | London | 15m | FADE_UP | OR_Q4_Wide | `57.4%` | 242 | `30` | `1.35` | `36R` | `-8.0R` | `4.25` |
| 2143 | WTI | NY Main | 30m | FADE_UP | RSI_30-50 | `56.8%` | 292 | `36` | `1.32` | `40R` | `-8.0R` | `4.25` |
| 2144 | SP500 | Pre-Market | 45m | FADE_UP | RSI_D>65 | `58.6%` | 169 | `22` | `1.41` | `29R` | `-7.0R` | `4.25` |
| 2145 | GBPUSD | London | 30m | FADE_DOWN | Wed | `58.2%` | 189 | `23` | `1.39` | `31R` | `-7.0R` | `4.25` |
| 2146 | GBPAUD | London | 30m | FADE_DOWN | Thu | `58.2%` | 189 | `24` | `1.39` | `31R` | `-10.0R` | `4.25` |
| 2147 | XAUUSD | London | 45m | FADE_DOWN | AbovePD | `58.8%` | 160 | `20` | `1.42` | `28R` | `-7.0R` | `4.25` |
| 2148 | GBPJPY | London | 45m | FADE_UP | Thu | `58.0%` | 200 | `25` | `1.38` | `32R` | `-12.0R` | `4.24` |
| 2149 | GBPAUD | London | 30m | FADE_DOWN | Wed | `58.0%` | 200 | `25` | `1.38` | `32R` | `-13.0R` | `4.24` |
| 2150 | NATGAS | NY | 45m | FADE_DOWN | OR_Q1_Tight | `58.0%` | 200 | `25` | `1.38` | `32R` | `-11.0R` | `4.24` |
| 2151 | EURJPY | Tokyo | 60m | FADE_UP | RSI_D>65 | `59.8%` | 117 | `16` | `1.49` | `23R` | `-7.0R` | `4.24` |
| 2152 | EURUSD | London | 45m | FADE_DOWN | BtwCloseHigh | `56.5%` | 322 | `40` | `1.30` | `42R` | `-13.0R` | `4.24` |
| 2153 | AUDUSD | London | 60m | FADE_DOWN | RSI_50-70 | `56.4%` | 337 | `41` | `1.29` | `43R` | `-16.0R` | `4.24` |
| 2154 | BRENT | London | 30m | FADE_UP | BelowPD | `60.9%` | 87 | `11` | `1.56` | `19R` | `-3.0R` | `4.24` |
| 2155 | VIX | NY Cash | 45m | FADE_UP | OR_Q4_Wide | `63.3%` | 49 | `14` | `1.72` | `13R` | `-2.0R` | `4.24` |
| 2156 | EURUSD | NY | 30m | FADE_UP | RSI_30-50 | `56.8%` | 296 | `36` | `1.31` | `40R` | `-8.0R` | `4.24` |
| 2157 | XAUUSD | NY | 15m | FADE_DOWN | OR_Q4_Wide | `58.1%` | 191 | `29` | `1.39` | `31R` | `-5.0R` | `4.24` |
| 2158 | VIX | NY Cash | 60m | FADE_UP | GapSmall | `58.1%` | 191 | `57` | `1.39` | `31R` | `-13.0R` | `4.24` |
| 2159 | EURUSD | NY | 15m | FADE_DOWN | GapSmall | `55.4%` | 475 | `58` | `1.24` | `51R` | `-12.0R` | `4.23` |
| 2160 | EURUSD | London | 30m | FADE_DOWN | BtwCloseHigh | `56.7%` | 298 | `37` | `1.31` | `40R` | `-12.0R` | `4.23` |
| 2161 | WTI | London Initial | 15m | FADE_DOWN | RSI_30-50 | `56.7%` | 298 | `37` | `1.31` | `40R` | `-11.0R` | `4.23` |
| 2162 | WTI | London Initial | 15m | FADE_DOWN | OR_Q4_Wide | `57.7%` | 213 | `27` | `1.37` | `33R` | `-7.0R` | `4.23` |
| 2163 | GBPUSD | NY | 60m | FADE_DOWN | RSI_D<35 | `62.3%` | 61 | `8` | `1.65` | `15R` | `-7.0R` | `4.23` |
| 2164 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | RSI<30 | `62.3%` | 61 | `8` | `1.65` | `15R` | `-4.0R` | `4.23` |
| 2165 | NASDAQ100 | Pre-Market | 45m | FADE_UP | RSI_D>65 | `58.6%` | 162 | `21` | `1.42` | `28R` | `-7.0R` | `4.23` |
| 2166 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | RSI_D>65 | `58.6%` | 162 | `21` | `1.42` | `28R` | `-7.0R` | `4.23` |
| 2167 | EURUSD | London | 45m | FADE_UP | BelowPD | `59.3%` | 135 | `17` | `1.45` | `25R` | `-4.0R` | `4.23` |
| 2168 | WTI | London Initial | 45m | FADE_UP | Wed | `58.2%` | 182 | `22` | `1.39` | `30R` | `-8.0R` | `4.23` |
| 2169 | GBPJPY | Tokyo | 45m | FADE_UP | RSI_D>65 | `58.8%` | 153 | `19` | `1.43` | `27R` | `-6.0R` | `4.23` |
| 2170 | VIX | NY Cash | 15m | FADE_DOWN | GapSmall | `58.8%` | 153 | `45` | `1.43` | `27R` | `-11.0R` | `4.23` |
| 2171 | XAUUSD | London | 60m | FADE_DOWN | AbovePD | `59.0%` | 144 | `18` | `1.44` | `26R` | `-5.0R` | `4.23` |
| 2172 | NATGAS | NY | 30m | FADE_DOWN | OR_Q4_Wide | `58.0%` | 193 | `26` | `1.38` | `31R` | `-7.0R` | `4.22` |
| 2173 | XAUUSD | London | 60m | FADE_UP | BtwLowClose | `56.1%` | 360 | `44` | `1.28` | `44R` | `-9.0R` | `4.22` |
| 2174 | XAUUSD | NY | 30m | FADE_DOWN | RSI_50-70 | `57.7%` | 215 | `27` | `1.36` | `33R` | `-8.0R` | `4.22` |
| 2175 | EURJPY | London | 15m | FADE_UP | Thu | `58.4%` | 173 | `22` | `1.40` | `29R` | `-8.0R` | `4.22` |
| 2176 | SP500 | Pre-Market | 60m | FADE_UP | Fri | `58.4%` | 173 | `21` | `1.40` | `29R` | `-8.0R` | `4.22` |
| 2177 | USDJPY | NY | 60m | FADE_UP | Mon | `60.2%` | 103 | `13` | `1.51` | `21R` | `-9.0R` | `4.22` |
| 2178 | GBPJPY | London | 45m | FADE_DOWN | BelowPD | `60.2%` | 103 | `13` | `1.51` | `21R` | `-6.0R` | `4.22` |
| 2179 | XAUUSD | London | 15m | FADE_DOWN | Wed | `59.7%` | 119 | `15` | `1.48` | `23R` | `-7.0R` | `4.22` |
| 2180 | WTI | London Initial | 60m | FADE_UP | BtwLowClose | `56.3%` | 332 | `41` | `1.29` | `42R` | `-8.0R` | `4.22` |
| 2181 | WTI | London Initial | 30m | FADE_UP | RSI_50-70 | `55.8%` | 396 | `49` | `1.26` | `46R` | `-11.0R` | `4.22` |
| 2182 | GBPJPY | London | 60m | FADE_DOWN | Fri | `58.5%` | 164 | `20` | `1.41` | `28R` | `-10.0R` | `4.21` |
| 2183 | EURUSD | London | 45m | FADE_DOWN | ATR+10% | `63.6%` | 44 | `5` | `1.75` | `12R` | `-2.0R` | `4.21` |
| 2184 | EURJPY | Tokyo | 30m | FADE_DOWN | ATR+10% | `63.6%` | 44 | `6` | `1.75` | `12R` | `-4.0R` | `4.21` |
| 2185 | WTI | London Initial | 15m | FADE_DOWN | RSI_D<35 | `63.6%` | 44 | `6` | `1.75` | `12R` | `-3.0R` | `4.21` |
| 2186 | EURUSD | London | 60m | FADE_DOWN | Fri | `58.2%` | 184 | `23` | `1.39` | `30R` | `-7.0R` | `4.21` |
| 2187 | BRENT | NY | 60m | FADE_DOWN | RSI_50-70 | `57.5%` | 228 | `28` | `1.35` | `34R` | `-8.0R` | `4.21` |
| 2188 | GBPUSD | London | 60m | FADE_DOWN | Tue | `57.9%` | 195 | `24` | `1.38` | `31R` | `-6.0R` | `4.21` |
| 2189 | WTI | London Initial | 15m | FADE_UP | OR_Q4_Wide | `57.9%` | 195 | `25` | `1.38` | `31R` | `-8.0R` | `4.21` |
| 2190 | XAUUSD | London | 15m | SHAKEOUT_UP | Fri | `61.8%` | 68 | `9` | `1.62` | `16R` | `-4.0R` | `4.21` |
| 2191 | VIX | NY Cash | 15m | FADE_DOWN | BtwLowClose | `61.8%` | 68 | `20` | `1.62` | `16R` | `-4.0R` | `4.21` |
| 2192 | NATGAS | NY | 15m | FADE_DOWN | RSI_30-50 | `56.0%` | 366 | `45` | `1.27` | `44R` | `-27.0R` | `4.21` |
| 2193 | EURUSD | NY | 30m | FADE_DOWN | RSI_D<35 | `60.4%` | 96 | `12` | `1.53` | `20R` | `-7.0R` | `4.21` |
| 2194 | WTI | London Initial | 30m | FADE_UP | BelowPD | `60.4%` | 96 | `12` | `1.53` | `20R` | `-4.0R` | `4.21` |
| 2195 | EURUSD | NY | 45m | FADE_UP | AbovePD | `59.1%` | 137 | `17` | `1.45` | `25R` | `-11.0R` | `4.21` |
| 2196 | USDJPY | NY | 60m | FADE_DOWN | Wed | `59.1%` | 137 | `17` | `1.45` | `25R` | `-5.0R` | `4.21` |
| 2197 | SP500 | NY Cash | 60m | FADE_DOWN | AbovePD | `59.1%` | 137 | `17` | `1.45` | `25R` | `-7.0R` | `4.21` |
| 2198 | XAUUSD | NY | 30m | FADE_UP | AbovePD | `58.3%` | 175 | `22` | `1.40` | `29R` | `-8.0R` | `4.21` |
| 2199 | XAGUSD | London | 60m | FADE_DOWN | Fri | `58.3%` | 175 | `22` | `1.40` | `29R` | `-8.0R` | `4.21` |
| 2200 | WTI | NY Main | 15m | FADE_DOWN | Tue | `58.3%` | 175 | `22` | `1.40` | `29R` | `-6.0R` | `4.21` |
| 2201 | BRENT | London | 45m | FADE_UP | Wed | `58.3%` | 175 | `22` | `1.40` | `29R` | `-8.0R` | `4.21` |
| 2202 | XAGUSD | NY | 30m | FADE_DOWN | Thu | `59.8%` | 112 | `14` | `1.49` | `22R` | `-8.0R` | `4.20` |
| 2203 | XAUUSD | London | 60m | FADE_UP | RSI>70 | `60.7%` | 89 | `11` | `1.54` | `19R` | `-6.0R` | `4.20` |
| 2204 | WTI | London Initial | 15m | FADE_DOWN | Fri | `60.7%` | 89 | `11` | `1.54` | `19R` | `-5.0R` | `4.20` |
| 2205 | GBPJPY | Tokyo | 60m | FADE_UP | RSI>70 | `61.3%` | 75 | `9` | `1.59` | `17R` | `-3.0R` | `4.20` |
| 2206 | XAUUSD | London | 30m | FADE_DOWN | RSI_30-50 | `55.6%` | 423 | `52` | `1.25` | `47R` | `-9.0R` | `4.20` |
| 2207 | XAUUSD | NY | 30m | FADE_DOWN | OR_Q1_Tight | `57.9%` | 197 | `30` | `1.37` | `31R` | `-6.0R` | `4.20` |
| 2208 | EURJPY | Tokyo | 45m | FADE_DOWN | RSI_50-70 | `56.2%` | 340 | `42` | `1.28` | `42R` | `-8.0R` | `4.20` |
| 2209 | XAUUSD | London | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `64.1%` | 39 | `5` | `1.79` | `11R` | `-3.0R` | `4.19` |
| 2210 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | RSI_D<35 | `64.1%` | 39 | `5` | `1.79` | `11R` | `-3.0R` | `4.19` |
| 2211 | BRENT | NY | 30m | FADE_DOWN | Thu | `58.6%` | 157 | `19` | `1.42` | `27R` | `-14.0R` | `4.19` |
| 2212 | WTI | NY Main | 45m | FADE_UP | RSI_D>65 | `59.5%` | 121 | `15` | `1.47` | `23R` | `-6.0R` | `4.19` |
| 2213 | WTI | London Initial | 15m | FADE_UP | BelowPD | `62.5%` | 56 | `7` | `1.67` | `14R` | `-6.0R` | `4.19` |
| 2214 | EURJPY | London | 60m | FADE_DOWN | AbovePD | `58.2%` | 177 | `22` | `1.39` | `29R` | `-7.0R` | `4.19` |
| 2215 | NASDAQ100 | NY Cash | 30m | FADE_UP | BtwCloseHigh | `57.1%` | 245 | `30` | `1.33` | `35R` | `-7.0R` | `4.19` |
| 2216 | WTI | NY Main | 15m | FADE_UP | Fri | `58.8%` | 148 | `18` | `1.43` | `26R` | `-6.0R` | `4.19` |
| 2217 | NATGAS | NY | 60m | FADE_DOWN | OR_Q1_Tight | `58.0%` | 188 | `23` | `1.38` | `30R` | `-9.0R` | `4.19` |
| 2218 | XAGUSD | London | 15m | FADE_UP | Fri | `59.2%` | 130 | `16` | `1.45` | `24R` | `-7.0R` | `4.19` |
| 2219 | GBPAUD | London | 15m | FADE_UP | RSI_30-50 | `56.5%` | 299 | `37` | `1.30` | `39R` | `-10.0R` | `4.19` |
| 2220 | XAUUSD | NY | 60m | FADE_DOWN | Wed | `60.0%` | 105 | `13` | `1.50` | `21R` | `-7.0R` | `4.19` |
| 2221 | SP500 | NY Cash | 60m | FADE_DOWN | BtwCloseHigh | `57.8%` | 199 | `25` | `1.37` | `31R` | `-6.0R` | `4.19` |
| 2222 | GBPJPY | Tokyo | 30m | FADE_UP | Wed | `58.3%` | 168 | `21` | `1.40` | `28R` | `-8.0R` | `4.18` |
| 2223 | XAUUSD | London | 45m | FADE_DOWN | Fri | `58.3%` | 168 | `21` | `1.40` | `28R` | `-5.0R` | `4.18` |
| 2224 | XAGUSD | London | 45m | FADE_UP | RSI_D>65 | `58.3%` | 168 | `22` | `1.40` | `28R` | `-5.0R` | `4.18` |
| 2225 | GBPUSD | NY | 30m | FADE_UP | ATR+10% | `64.7%` | 34 | `4` | `1.83` | `10R` | `-4.0R` | `4.18` |
| 2226 | XAGUSD | NY | 45m | FADE_DOWN | RSI_D<35 | `64.7%` | 34 | `5` | `1.83` | `10R` | `-3.0R` | `4.18` |
| 2227 | SP500 | NY Cash | 45m | FADE_DOWN | ATR-10% | `64.7%` | 34 | `4` | `1.83` | `10R` | `-2.0R` | `4.18` |
| 2228 | GBPUSD | London | 30m | FADE_UP | RSI_50-70 | `55.2%` | 475 | `58` | `1.23` | `49R` | `-15.0R` | `4.18` |
| 2229 | XAGUSD | NY | 15m | FADE_UP | AbovePD | `58.1%` | 179 | `22` | `1.39` | `29R` | `-7.0R` | `4.18` |
| 2230 | USDJPY | NY | 45m | FADE_UP | AbovePD | `58.5%` | 159 | `20` | `1.41` | `27R` | `-9.0R` | `4.18` |
| 2231 | GBPUSD | London | 30m | FADE_DOWN | Thu | `57.9%` | 190 | `23` | `1.38` | `30R` | `-7.0R` | `4.18` |
| 2232 | GBPUSD | NY | 45m | FADE_DOWN | Fri | `59.6%` | 114 | `14` | `1.48` | `22R` | `-6.0R` | `4.18` |
| 2233 | GBPJPY | London | 15m | FADE_UP | RSI_D>65 | `59.6%` | 114 | `15` | `1.48` | `22R` | `-8.0R` | `4.18` |
| 2234 | WTI | London Initial | 30m | FADE_DOWN | BelowPD | `60.2%` | 98 | `13` | `1.51` | `20R` | `-5.0R` | `4.18` |
| 2235 | USDJPY | Tokyo | 15m | FADE_DOWN | BtwLowClose | `56.7%` | 277 | `34` | `1.31` | `37R` | `-9.0R` | `4.17` |
| 2236 | BRENT | London | 45m | FADE_UP | Mon | `58.2%` | 170 | `21` | `1.39` | `28R` | `-7.0R` | `4.17` |
| 2237 | XAUUSD | NY | 30m | FADE_DOWN | BelowPD | `59.3%` | 123 | `15` | `1.46` | `23R` | `-5.0R` | `4.17` |
| 2238 | BRENT | NY | 60m | FADE_DOWN | Mon | `59.3%` | 123 | `15` | `1.46` | `23R` | `-7.0R` | `4.17` |
| 2239 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | BtwCloseHigh | `57.1%` | 238 | `30` | `1.33` | `34R` | `-10.0R` | `4.17` |
| 2240 | GBPAUD | London | 15m | FADE_DOWN | Thu | `58.9%` | 141 | `18` | `1.43` | `25R` | `-8.0R` | `4.17` |
| 2241 | USDJPY | Tokyo | 15m | FADE_UP | RSI>70 | `61.9%` | 63 | `8` | `1.62` | `15R` | `-4.0R` | `4.17` |
| 2242 | AUDUSD | Sydney | 60m | FADE_UP | BASE | `61.9%` | 63 | `8` | `1.62` | `15R` | `-3.0R` | `4.17` |
| 2243 | WTI | London Initial | 30m | FADE_DOWN | Fri | `59.1%` | 132 | `17` | `1.44` | `24R` | `-7.0R` | `4.17` |
| 2244 | SP500 | NY Cash | 60m | FADE_DOWN | RSI_30-50 | `56.5%` | 292 | `36` | `1.30` | `38R` | `-14.0R` | `4.17` |
| 2245 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | RSI_30-50 | `55.9%` | 354 | `44` | `1.27` | `42R` | `-12.0R` | `4.17` |
| 2246 | EURUSD | London | 60m | FADE_DOWN | BtwCloseHigh | `56.4%` | 307 | `38` | `1.29` | `39R` | `-7.0R` | `4.17` |
| 2247 | GBPJPY | London | 30m | FADE_DOWN | RSI_50-70 | `56.4%` | 307 | `38` | `1.29` | `39R` | `-12.0R` | `4.17` |
| 2248 | USDJPY | NY | 45m | FADE_DOWN | OR_Q4_Wide | `60.4%` | 91 | `11` | `1.53` | `19R` | `-4.0R` | `4.17` |
| 2249 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | Fri | `60.4%` | 91 | `11` | `1.53` | `19R` | `-6.0R` | `4.17` |
| 2250 | USDJPY | NY | 30m | FADE_UP | RSI_30-50 | `57.3%` | 227 | `28` | `1.34` | `33R` | `-11.0R` | `4.16` |
| 2251 | EURJPY | London | 45m | FADE_DOWN | BtwLowClose | `56.5%` | 294 | `36` | `1.30` | `38R` | `-13.0R` | `4.16` |
| 2252 | GBPAUD | London | 30m | FADE_DOWN | RSI_50-70 | `56.3%` | 309 | `38` | `1.29` | `39R` | `-9.0R` | `4.16` |
| 2253 | GBPUSD | NY | 60m | FADE_UP | BelowPD | `59.8%` | 107 | `14` | `1.49` | `21R` | `-5.0R` | `4.16` |
| 2254 | USDJPY | NY | 45m | FADE_DOWN | RSI_D>65 | `59.8%` | 107 | `14` | `1.49` | `21R` | `-7.0R` | `4.16` |
| 2255 | EURJPY | London | 15m | FADE_UP | RSI_30-50 | `56.6%` | 281 | `34` | `1.30` | `37R` | `-7.0R` | `4.16` |
| 2256 | AUDUSD | London | 45m | FADE_DOWN | RSI<30 | `60.7%` | 84 | `10` | `1.55` | `18R` | `-5.0R` | `4.16` |
| 2257 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | RSI<30 | `60.7%` | 84 | `10` | `1.55` | `18R` | `-3.0R` | `4.16` |
| 2258 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | RSI_30-50 | `56.1%` | 326 | `40` | `1.28` | `40R` | `-12.0R` | `4.16` |
| 2259 | GBPUSD | NY | 30m | FADE_UP | BtwCloseHigh | `58.1%` | 172 | `21` | `1.39` | `28R` | `-8.0R` | `4.16` |
| 2260 | NATGAS | NY | 15m | FADE_UP | Thu | `58.1%` | 172 | `21` | `1.39` | `28R` | `-10.0R` | `4.16` |
| 2261 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | Thu | `58.1%` | 172 | `21` | `1.39` | `28R` | `-11.0R` | `4.16` |
| 2262 | GBPAUD | London | 15m | FADE_DOWN | RSI<30 | `61.4%` | 70 | `9` | `1.59` | `16R` | `-3.0R` | `4.16` |
| 2263 | WTI | NY Main | 45m | FADE_UP | Tue | `58.6%` | 152 | `19` | `1.41` | `26R` | `-7.0R` | `4.16` |
| 2264 | USDJPY | NY | 60m | FADE_UP | OR_Q4_Wide | `62.7%` | 51 | `7` | `1.68` | `13R` | `-5.0R` | `4.15` |
| 2265 | EURJPY | Tokyo | 30m | FADE_DOWN | RSI<30 | `62.7%` | 51 | `7` | `1.68` | `13R` | `-4.0R` | `4.15` |
| 2266 | XAGUSD | London | 60m | FADE_UP | ATR+10% | `62.7%` | 51 | `6` | `1.68` | `13R` | `-4.0R` | `4.15` |
| 2267 | WTI | London Initial | 60m | FADE_DOWN | Mon | `57.9%` | 183 | `22` | `1.38` | `29R` | `-9.0R` | `4.15` |
| 2268 | XAUUSD | NY | 30m | FADE_UP | BtwLowClose | `57.7%` | 194 | `24` | `1.37` | `30R` | `-9.0R` | `4.15` |
| 2269 | XAGUSD | London | 15m | SHAKEOUT_UP | Fri | `61.0%` | 77 | `9` | `1.57` | `17R` | `-3.0R` | `4.15` |
| 2270 | NATGAS | NY | 60m | FADE_DOWN | Wed | `59.5%` | 116 | `14` | `1.47` | `22R` | `-5.0R` | `4.15` |
| 2271 | EURJPY | London | 45m | FADE_UP | BelowPD | `58.7%` | 143 | `18` | `1.42` | `25R` | `-7.0R` | `4.15` |
| 2272 | WTI | London Initial | 30m | FADE_DOWN | Wed | `58.7%` | 143 | `18` | `1.42` | `25R` | `-8.0R` | `4.15` |
| 2273 | WTI | NY Main | 60m | FADE_DOWN | Tue | `59.0%` | 134 | `17` | `1.44` | `24R` | `-10.0R` | `4.15` |
| 2274 | NASDAQ100 | Pre-Market | 45m | FADE_UP | BelowPD | `59.0%` | 134 | `17` | `1.44` | `24R` | `-7.0R` | `4.15` |
| 2275 | GBPJPY | Tokyo | 30m | FADE_UP | Mon | `57.8%` | 185 | `23` | `1.37` | `29R` | `-5.0R` | `4.14` |
| 2276 | GBPUSD | London | 60m | FADE_UP | BtwCloseHigh | `56.2%` | 317 | `39` | `1.28` | `39R` | `-12.0R` | `4.14` |
| 2277 | GBPUSD | NY | 15m | FADE_DOWN | Wed | `58.4%` | 154 | `19` | `1.41` | `26R` | `-7.0R` | `4.14` |
| 2278 | EURUSD | London | 60m | FADE_DOWN | RSI_50-70 | `56.8%` | 259 | `32` | `1.31` | `35R` | `-10.0R` | `4.14` |
| 2279 | USDJPY | NY | 30m | FADE_UP | GapSmall | `55.2%` | 446 | `55` | `1.23` | `46R` | `-8.0R` | `4.14` |
| 2280 | GBPJPY | London | 45m | FADE_UP | BtwLowClose | `56.0%` | 336 | `41` | `1.27` | `40R` | `-9.0R` | `4.13` |
| 2281 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | Thu | `58.2%` | 165 | `20` | `1.39` | `27R` | `-9.0R` | `4.13` |
| 2282 | GBPUSD | NY | 15m | FADE_DOWN | Tue | `58.6%` | 145 | `18` | `1.42` | `25R` | `-10.0R` | `4.13` |
| 2283 | SP500 | NY Cash | 45m | FADE_UP | Wed | `58.6%` | 145 | `18` | `1.42` | `25R` | `-6.0R` | `4.13` |
| 2284 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | Mon | `59.6%` | 109 | `13` | `1.48` | `21R` | `-9.0R` | `4.13` |
| 2285 | GBPJPY | London | 15m | FADE_DOWN | RSI_50-70 | `56.7%` | 261 | `32` | `1.31` | `35R` | `-11.0R` | `4.13` |
| 2286 | NASDAQ100 | Pre-Market | 30m | FADE_UP | BtwLowClose | `57.6%` | 198 | `24` | `1.36` | `30R` | `-13.0R` | `4.13` |
| 2287 | EURUSD | London | 60m | FADE_DOWN | RSI_D>65 | `60.2%` | 93 | `12` | `1.51` | `19R` | `-5.0R` | `4.13` |
| 2288 | XAUUSD | NY | 45m | FADE_DOWN | BelowPD | `60.2%` | 93 | `11` | `1.51` | `19R` | `-5.0R` | `4.13` |
| 2289 | EURUSD | London | 30m | FADE_DOWN | Tue | `58.0%` | 176 | `22` | `1.38` | `28R` | `-12.0R` | `4.13` |
| 2290 | AUDUSD | London | 30m | FADE_DOWN | OR_Q4_Wide | `57.0%` | 235 | `29` | `1.33` | `33R` | `-7.0R` | `4.13` |
| 2291 | BRENT | NY | 15m | FADE_DOWN | AbovePD | `57.8%` | 187 | `23` | `1.37` | `29R` | `-7.0R` | `4.13` |
| 2292 | GBPJPY | Tokyo | 60m | FADE_UP | RSI_30-50 | `56.5%` | 276 | `34` | `1.30` | `36R` | `-8.0R` | `4.13` |
| 2293 | WTI | London Initial | 30m | FADE_DOWN | RSI_D>65 | `59.3%` | 118 | `15` | `1.46` | `22R` | `-11.0R` | `4.13` |
| 2294 | EURUSD | London | 45m | FADE_DOWN | RSI_50-70 | `56.0%` | 323 | `40` | `1.27` | `39R` | `-10.0R` | `4.13` |
| 2295 | SP500 | NY Cash | 15m | FADE_UP | Tue | `59.1%` | 127 | `16` | `1.44` | `23R` | `-8.0R` | `4.13` |
| 2296 | USDJPY | Tokyo | 60m | FADE_UP | Mon | `58.3%` | 156 | `19` | `1.40` | `26R` | `-6.0R` | `4.12` |
| 2297 | NASDAQ100 | Pre-Market | 45m | FADE_UP | BtwLowClose | `56.8%` | 250 | `31` | `1.31` | `34R` | `-10.0R` | `4.12` |
| 2298 | EURJPY | London | 60m | FADE_DOWN | BtwLowClose | `56.3%` | 293 | `36` | `1.29` | `37R` | `-8.0R` | `4.12` |
| 2299 | EURJPY | Tokyo | 30m | FADE_UP | BtwLowClose | `55.8%` | 342 | `42` | `1.26` | `40R` | `-11.0R` | `4.12` |
| 2300 | GBPUSD | NY | 60m | FADE_DOWN | OR_Q1_Tight | `57.5%` | 200 | `25` | `1.35` | `30R` | `-6.0R` | `4.12` |
| 2301 | BRENT | NY | 30m | FADE_DOWN | Wed | `58.1%` | 167 | `21` | `1.39` | `27R` | `-7.0R` | `4.12` |
| 2302 | AUDUSD | London | 30m | FADE_DOWN | RSI_D>65 | `60.5%` | 86 | `11` | `1.53` | `18R` | `-5.0R` | `4.12` |
| 2303 | GBPJPY | Tokyo | 45m | FADE_UP | Wed | `57.7%` | 189 | `23` | `1.36` | `29R` | `-8.0R` | `4.12` |
| 2304 | XAGUSD | London | 45m | FADE_DOWN | Tue | `57.7%` | 189 | `23` | `1.36` | `29R` | `-7.0R` | `4.12` |
| 2305 | USDJPY | NY | 45m | FADE_DOWN | OR_Q1_Tight | `57.9%` | 178 | `22` | `1.37` | `28R` | `-10.0R` | `4.12` |
| 2306 | EURJPY | London | 30m | FADE_DOWN | Wed | `57.9%` | 178 | `22` | `1.37` | `28R` | `-6.0R` | `4.12` |
| 2307 | XAGUSD | NY | 30m | FADE_DOWN | BtwLowClose | `57.9%` | 178 | `22` | `1.37` | `28R` | `-8.0R` | `4.12` |
| 2308 | EURJPY | Tokyo | 15m | FADE_UP | RSI>70 | `63.0%` | 46 | `6` | `1.71` | `12R` | `-5.0R` | `4.12` |
| 2309 | XAUUSD | London | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `63.0%` | 46 | `6` | `1.71` | `12R` | `-5.0R` | `4.12` |
| 2310 | WTI | London Initial | 30m | SHAKEOUT_UP | OR_Q1_Tight | `63.0%` | 46 | `6` | `1.71` | `12R` | `-3.0R` | `4.12` |
| 2311 | WTI | NY Main | 15m | FADE_DOWN | BtwCloseHigh | `57.3%` | 213 | `27` | `1.34` | `31R` | `-7.0R` | `4.12` |
| 2312 | EURUSD | London | 60m | FADE_DOWN | OR_Q1_Tight | `56.7%` | 252 | `32` | `1.31` | `34R` | `-8.0R` | `4.12` |
| 2313 | WTI | London Initial | 15m | FADE_UP | RSI_50-70 | `56.7%` | 252 | `31` | `1.31` | `34R` | `-12.0R` | `4.12` |
| 2314 | EURUSD | London | 60m | FADE_UP | RSI_D<35 | `59.8%` | 102 | `13` | `1.49` | `20R` | `-5.0R` | `4.12` |
| 2315 | EURUSD | NY | 45m | FADE_UP | Fri | `59.8%` | 102 | `13` | `1.49` | `20R` | `-7.0R` | `4.12` |
| 2316 | EURJPY | Tokyo | 15m | FADE_UP | RSI_D>65 | `59.8%` | 102 | `14` | `1.49` | `20R` | `-10.0R` | `4.12` |
| 2317 | EURJPY | Tokyo | 15m | FADE_DOWN | OR_Q1_Tight | `59.8%` | 102 | `13` | `1.49` | `20R` | `-8.0R` | `4.12` |
| 2318 | XAUUSD | London | 45m | FADE_DOWN | BtwLowClose | `55.9%` | 329 | `41` | `1.27` | `39R` | `-8.0R` | `4.11` |
| 2319 | XAUUSD | London | 45m | FADE_UP | RSI_30-50 | `56.2%` | 297 | `36` | `1.28` | `37R` | `-10.0R` | `4.11` |
| 2320 | NASDAQ100 | Pre-Market | 60m | FADE_UP | ATR+10% | `61.5%` | 65 | `8` | `1.60` | `15R` | `-3.0R` | `4.11` |
| 2321 | NASDAQ100 | NY Cash | 30m | FADE_UP | Mon | `58.7%` | 138 | `17` | `1.42` | `24R` | `-7.0R` | `4.11` |
| 2322 | BRENT | London | 60m | FADE_UP | BtwLowClose | `55.9%` | 331 | `41` | `1.27` | `39R` | `-11.0R` | `4.11` |
| 2323 | EURJPY | Tokyo | 30m | FADE_DOWN | Fri | `58.2%` | 158 | `19` | `1.39` | `26R` | `-7.0R` | `4.11` |
| 2324 | EURJPY | London | 45m | FADE_DOWN | Tue | `57.6%` | 191 | `23` | `1.36` | `29R` | `-7.0R` | `4.11` |
| 2325 | WTI | London Initial | 60m | FADE_DOWN | Tue | `57.6%` | 191 | `24` | `1.36` | `29R` | `-9.0R` | `4.11` |
| 2326 | GBPAUD | London | 45m | FADE_UP | OR_Q4_Wide | `57.2%` | 215 | `26` | `1.34` | `31R` | `-8.0R` | `4.11` |
| 2327 | NATGAS | NY | 15m | FADE_DOWN | OR_Q4_Wide | `57.2%` | 215 | `29` | `1.34` | `31R` | `-12.0R` | `4.11` |
| 2328 | XAGUSD | NY | 15m | FADE_UP | BtwLowClose | `56.8%` | 241 | `30` | `1.32` | `33R` | `-10.0R` | `4.11` |
| 2329 | XAGUSD | NY | 30m | FADE_UP | BelowPD | `59.5%` | 111 | `14` | `1.47` | `21R` | `-7.0R` | `4.11` |
| 2330 | WTI | London Initial | 60m | FADE_UP | BelowPD | `59.5%` | 111 | `14` | `1.47` | `21R` | `-5.0R` | `4.11` |
| 2331 | NASDAQ100 | Pre-Market | 30m | FADE_UP | BelowPD | `59.5%` | 111 | `14` | `1.47` | `21R` | `-6.0R` | `4.11` |
| 2332 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | GapSmall | `56.5%` | 269 | `33` | `1.30` | `35R` | `-8.0R` | `4.11` |
| 2333 | SP500 | Pre-Market | 45m | FADE_UP | ATR+10% | `61.1%` | 72 | `9` | `1.57` | `16R` | `-6.0R` | `4.11` |
| 2334 | EURJPY | Tokyo | 60m | FADE_UP | Fri | `57.8%` | 180 | `22` | `1.37` | `28R` | `-8.0R` | `4.11` |
| 2335 | EURJPY | London | 60m | FADE_DOWN | Tue | `57.8%` | 180 | `22` | `1.37` | `28R` | `-5.0R` | `4.11` |
| 2336 | GBPUSD | London | 60m | FADE_UP | BelowPD | `58.9%` | 129 | `16` | `1.43` | `23R` | `-6.0R` | `4.11` |
| 2337 | XAUUSD | London | 60m | FADE_UP | Fri | `57.4%` | 204 | `25` | `1.34` | `30R` | `-7.0R` | `4.10` |
| 2338 | BRENT | NY | 15m | FADE_UP | RSI_30-50 | `56.6%` | 258 | `32` | `1.30` | `34R` | `-10.0R` | `4.10` |
| 2339 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | BASE | `55.9%` | 320 | `39` | `1.27` | `38R` | `-12.0R` | `4.10` |
| 2340 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | RSI_50-70 | `58.1%` | 160 | `20` | `1.39` | `26R` | `-11.0R` | `4.09` |
| 2341 | GBPUSD | London | 15m | FADE_DOWN | Tue | `57.9%` | 171 | `21` | `1.38` | `27R` | `-7.0R` | `4.09` |
| 2342 | GBPJPY | London | 45m | FADE_DOWN | Wed | `57.9%` | 171 | `21` | `1.38` | `27R` | `-7.0R` | `4.09` |
| 2343 | XAGUSD | NY | 30m | FADE_DOWN | AbovePD | `57.9%` | 171 | `21` | `1.38` | `27R` | `-6.0R` | `4.09` |
| 2344 | BRENT | NY | 30m | FADE_UP | Thu | `57.9%` | 171 | `21` | `1.38` | `27R` | `-7.0R` | `4.09` |
| 2345 | GBPUSD | London | 45m | FADE_DOWN | Thu | `57.3%` | 206 | `25` | `1.34` | `30R` | `-7.0R` | `4.09` |
| 2346 | EURUSD | NY | 45m | FADE_DOWN | Fri | `59.6%` | 104 | `13` | `1.48` | `20R` | `-3.0R` | `4.09` |
| 2347 | GBPUSD | NY | 60m | FADE_UP | Fri | `60.2%` | 88 | `11` | `1.51` | `18R` | `-4.0R` | `4.08` |
| 2348 | BRENT | NY | 60m | FADE_UP | RSI_30-50 | `57.2%` | 208 | `26` | `1.34` | `30R` | `-7.0R` | `4.08` |
| 2349 | SP500 | Pre-Market | 45m | SHAKEOUT_DOWN | RSI_D<35 | `63.4%` | 41 | `5` | `1.73` | `11R` | `-3.0R` | `4.08` |
| 2350 | BRENT | NY | 45m | FADE_DOWN | Wed | `58.0%` | 162 | `20` | `1.38` | `26R` | `-7.0R` | `4.08` |
| 2351 | SP500 | Pre-Market | 45m | FADE_DOWN | RSI_D>65 | `58.0%` | 162 | `21` | `1.38` | `26R` | `-12.0R` | `4.08` |
| 2352 | GBPUSD | London | 30m | FADE_UP | Tue | `57.4%` | 197 | `24` | `1.35` | `29R` | `-8.0R` | `4.08` |
| 2353 | NATGAS | NY | 15m | FADE_DOWN | OR_Q1_Tight | `57.5%` | 186 | `25` | `1.35` | `28R` | `-11.0R` | `4.07` |
| 2354 | XAUUSD | London | 45m | FADE_UP | RSI>70 | `60.5%` | 81 | `10` | `1.53` | `17R` | `-7.0R` | `4.07` |
| 2355 | XAGUSD | London | 15m | SHAKEOUT_DOWN | GapSmall | `55.9%` | 315 | `39` | `1.27` | `37R` | `-10.0R` | `4.07` |
| 2356 | GBPAUD | London | 60m | FADE_UP | AbovePD | `57.7%` | 175 | `21` | `1.36` | `27R` | `-10.0R` | `4.07` |
| 2357 | GBPUSD | London | 15m | FADE_UP | RSI>70 | `59.8%` | 97 | `12` | `1.49` | `19R` | `-7.0R` | `4.07` |
| 2358 | XAUUSD | NY | 30m | FADE_DOWN | OR_Q4_Wide | `58.6%` | 133 | `20` | `1.42` | `23R` | `-6.0R` | `4.07` |
| 2359 | USDJPY | NY | 15m | FADE_UP | OR_Q4_Wide | `57.9%` | 164 | `20` | `1.38` | `26R` | `-11.0R` | `4.07` |
| 2360 | GBPJPY | London | 15m | FADE_DOWN | Wed | `57.9%` | 164 | `20` | `1.38` | `26R` | `-8.0R` | `4.07` |
| 2361 | XAUUSD | NY | 15m | FADE_UP | RSI_30-50 | `56.3%` | 268 | `33` | `1.29` | `34R` | `-11.0R` | `4.07` |
| 2362 | EURUSD | NY | 30m | FADE_UP | RSI_D<35 | `60.8%` | 74 | `9` | `1.55` | `16R` | `-5.0R` | `4.06` |
| 2363 | WTI | London Initial | 30m | FADE_UP | RSI>70 | `60.8%` | 74 | `9` | `1.55` | `16R` | `-7.0R` | `4.06` |
| 2364 | SP500 | Pre-Market | 30m | FADE_DOWN | RSI_30-50 | `55.8%` | 319 | `39` | `1.26` | `37R` | `-12.0R` | `4.06` |
| 2365 | EURJPY | London | 15m | FADE_UP | RSI_D>65 | `59.4%` | 106 | `14` | `1.47` | `20R` | `-5.0R` | `4.06` |
| 2366 | XAUUSD | NY | 45m | FADE_UP | Tue | `59.4%` | 106 | `13` | `1.47` | `20R` | `-5.0R` | `4.06` |
| 2367 | SP500 | Pre-Market | 30m | FADE_DOWN | Mon | `59.4%` | 106 | `13` | `1.47` | `20R` | `-8.0R` | `4.06` |
| 2368 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | Mon | `59.4%` | 106 | `13` | `1.47` | `20R` | `-4.0R` | `4.06` |
| 2369 | BRENT | NY | 45m | FADE_UP | RSI_D>65 | `59.1%` | 115 | `14` | `1.45` | `21R` | `-5.0R` | `4.06` |
| 2370 | VIX | NY Cash | 60m | FADE_UP | RSI_50-70 | `59.1%` | 115 | `34` | `1.45` | `21R` | `-11.0R` | `4.06` |
| 2371 | GBPJPY | London | 30m | FADE_UP | RSI_D>65 | `58.3%` | 144 | `19` | `1.40` | `24R` | `-7.0R` | `4.06` |
| 2372 | EURJPY | London | 45m | FADE_DOWN | RSI_D<35 | `61.2%` | 67 | `10` | `1.58` | `15R` | `-4.0R` | `4.06` |
| 2373 | GBPJPY | Tokyo | 60m | FADE_DOWN | Fri | `57.2%` | 201 | `25` | `1.34` | `29R` | `-11.0R` | `4.06` |
| 2374 | GBPJPY | London | 60m | FADE_UP | Wed | `57.2%` | 201 | `25` | `1.34` | `29R` | `-6.0R` | `4.06` |
| 2375 | XAGUSD | London | 45m | FADE_UP | Tue | `57.2%` | 201 | `25` | `1.34` | `29R` | `-12.0R` | `4.06` |
| 2376 | XAUUSD | NY | 30m | FADE_DOWN | RSI_30-50 | `55.6%` | 340 | `42` | `1.25` | `38R` | `-13.0R` | `4.06` |
| 2377 | SP500 | Pre-Market | 45m | FADE_UP | RSI_30-50 | `56.6%` | 242 | `30` | `1.30` | `32R` | `-10.0R` | `4.05` |
| 2378 | XAUUSD | London | 45m | FADE_UP | BtwLowClose | `55.4%` | 361 | `44` | `1.24` | `39R` | `-10.0R` | `4.05` |
| 2379 | GBPAUD | Sydney | 30m | FADE_UP | BelowPD | `63.9%` | 36 | `5` | `1.77` | `10R` | `-3.0R` | `4.05` |
| 2380 | SP500 | NY Cash | 60m | FADE_UP | RSI_D<35 | `63.9%` | 36 | `4` | `1.77` | `10R` | `-3.0R` | `4.05` |
| 2381 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | BtwLowClose | `58.5%` | 135 | `17` | `1.41` | `23R` | `-8.0R` | `4.05` |
| 2382 | USDJPY | Tokyo | 60m | FADE_DOWN | OR_Q4_Wide | `56.7%` | 231 | `28` | `1.31` | `31R` | `-6.0R` | `4.04` |
| 2383 | AUDUSD | London | 15m | FADE_UP | BtwCloseHigh | `56.7%` | 231 | `29` | `1.31` | `31R` | `-10.0R` | `4.04` |
| 2384 | GBPJPY | Tokyo | 30m | FADE_UP | OR_Q1_Tight | `58.2%` | 146 | `18` | `1.39` | `24R` | `-8.0R` | `4.04` |
| 2385 | GBPJPY | London | 60m | FADE_UP | RSI_D>65 | `58.2%` | 146 | `19` | `1.39` | `24R` | `-7.0R` | `4.04` |
| 2386 | XAUUSD | NY | 45m | FADE_DOWN | BtwCloseHigh | `58.2%` | 146 | `18` | `1.39` | `24R` | `-6.0R` | `4.04` |
| 2387 | WTI | NY Main | 15m | FADE_DOWN | OR_Q1_Tight | `58.2%` | 146 | `18` | `1.39` | `24R` | `-8.0R` | `4.04` |
| 2388 | GBPJPY | Tokyo | 45m | FADE_DOWN | Fri | `57.7%` | 168 | `21` | `1.37` | `26R` | `-6.0R` | `4.04` |
| 2389 | XAUUSD | NY | 15m | FADE_UP | OR_Q4_Wide | `57.7%` | 168 | `28` | `1.37` | `26R` | `-7.0R` | `4.04` |
| 2390 | GBPJPY | London | 30m | FADE_UP | Thu | `57.3%` | 192 | `24` | `1.34` | `28R` | `-9.0R` | `4.04` |
| 2391 | EURUSD | NY | 30m | FADE_UP | BtwLowClose | `57.1%` | 205 | `25` | `1.33` | `29R` | `-11.0R` | `4.04` |
| 2392 | NASDAQ100 | Pre-Market | 60m | FADE_UP | BtwCloseHigh | `56.1%` | 278 | `34` | `1.28` | `34R` | `-9.0R` | `4.04` |
| 2393 | USDJPY | NY | 30m | FADE_UP | RSI_50-70 | `55.4%` | 350 | `43` | `1.24` | `38R` | `-12.0R` | `4.04` |
| 2394 | SP500 | Pre-Market | 30m | FADE_UP | Fri | `59.0%` | 117 | `14` | `1.44` | `21R` | `-5.0R` | `4.04` |
| 2395 | GBPUSD | London | 60m | FADE_UP | Tue | `57.5%` | 181 | `22` | `1.35` | `27R` | `-7.0R` | `4.03` |
| 2396 | EURUSD | NY | 60m | FADE_UP | Fri | `60.2%` | 83 | `11` | `1.52` | `17R` | `-7.0R` | `4.03` |
| 2397 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | OR_Q4_Wide | `60.2%` | 83 | `14` | `1.52` | `17R` | `-5.0R` | `4.03` |
| 2398 | BRENT | NY | 60m | FADE_UP | RSI_D<35 | `62.5%` | 48 | `7` | `1.67` | `12R` | `-5.0R` | `4.03` |
| 2399 | SP500 | NY Cash | 45m | FADE_DOWN | RSI_D<35 | `62.5%` | 48 | `7` | `1.67` | `12R` | `-3.0R` | `4.03` |
| 2400 | NASDAQ100 | Pre-Market | 30m | FADE_UP | RSI>70 | `62.5%` | 48 | `6` | `1.67` | `12R` | `-2.0R` | `4.03` |
| 2401 | EURUSD | NY | 15m | FADE_DOWN | OR_Q4_Wide | `57.2%` | 194 | `24` | `1.34` | `28R` | `-9.0R` | `4.03` |
| 2402 | AUDUSD | London | 30m | FADE_UP | Wed | `57.2%` | 194 | `24` | `1.34` | `28R` | `-9.0R` | `4.03` |
| 2403 | EURUSD | London | 30m | FADE_UP | Thu | `57.0%` | 207 | `26` | `1.33` | `29R` | `-8.0R` | `4.03` |
| 2404 | GBPJPY | London | 60m | FADE_UP | RSI_30-50 | `56.2%` | 265 | `32` | `1.28` | `33R` | `-9.0R` | `4.03` |
| 2405 | GBPJPY | London | 45m | FADE_UP | AbovePD | `57.6%` | 170 | `21` | `1.36` | `26R` | `-8.0R` | `4.03` |
| 2406 | WTI | NY Main | 30m | FADE_DOWN | Wed | `57.6%` | 170 | `21` | `1.36` | `26R` | `-7.0R` | `4.03` |
| 2407 | XAUUSD | NY | 45m | FADE_DOWN | RSI_30-50 | `56.4%` | 250 | `31` | `1.29` | `32R` | `-12.0R` | `4.03` |
| 2408 | EURUSD | London | 15m | FADE_UP | ATR-10% | `64.5%` | 31 | `4` | `1.82` | `9R` | `-4.0R` | `4.03` |
| 2409 | GBPUSD | NY | 45m | FADE_DOWN | ATR-10% | `64.5%` | 31 | `4` | `1.82` | `9R` | `-4.0R` | `4.03` |
| 2410 | USDJPY | Tokyo | 45m | FADE_UP | ATR-10% | `64.5%` | 31 | `4` | `1.82` | `9R` | `-2.0R` | `4.03` |
| 2411 | GBPAUD | Sydney | 30m | FADE_UP | AbovePD | `64.5%` | 31 | `4` | `1.82` | `9R` | `-3.0R` | `4.03` |
| 2412 | NATGAS | NY | 30m | FADE_DOWN | Tue | `57.9%` | 159 | `20` | `1.37` | `25R` | `-6.0R` | `4.03` |
| 2413 | BRENT | NY | 15m | FADE_UP | Fri | `58.6%` | 128 | `16` | `1.42` | `22R` | `-10.0R` | `4.02` |
| 2414 | XAUUSD | London | 30m | FADE_UP | RSI_D<35 | `60.5%` | 76 | `10` | `1.53` | `16R` | `-3.0R` | `4.02` |
| 2415 | USDJPY | Tokyo | 60m | FADE_DOWN | RSI<30 | `59.8%` | 92 | `11` | `1.49` | `18R` | `-9.0R` | `4.02` |
| 2416 | SP500 | NY Cash | 30m | FADE_DOWN | RSI<30 | `59.8%` | 92 | `11` | `1.49` | `18R` | `-7.0R` | `4.02` |
| 2417 | EURUSD | NY | 30m | FADE_DOWN | Wed | `57.8%` | 161 | `20` | `1.37` | `25R` | `-7.0R` | `4.01` |
| 2418 | GBPUSD | NY | 45m | FADE_DOWN | BtwLowClose | `57.8%` | 161 | `20` | `1.37` | `25R` | `-8.0R` | `4.01` |
| 2419 | GBPJPY | Tokyo | 45m | FADE_DOWN | Thu | `57.3%` | 185 | `23` | `1.34` | `27R` | `-12.0R` | `4.01` |
| 2420 | XAUUSD | NY | 30m | FADE_DOWN | AbovePD | `58.0%` | 150 | `18` | `1.38` | `24R` | `-8.0R` | `4.01` |
| 2421 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | Mon | `59.1%` | 110 | `14` | `1.44` | `20R` | `-7.0R` | `4.01` |
| 2422 | GBPUSD | London | 30m | MOMENTUM_DOWN | RSI>70 | `56.4%` | 39 | `5` | `1.94` | `16R` | `-5.0R` | `4.01` |
| 2423 | NASDAQ100 | NY Cash | 15m | MOMENTUM_DOWN | AbovePD+RSI_D>65 | `56.4%` | 39 | `6` | `1.94` | `16R` | `-3.0R` | `4.01` |
| 2424 | XAGUSD | London | 15m | FADE_DOWN | RSI_D<35 | `61.8%` | 55 | `7` | `1.62` | `13R` | `-4.0R` | `4.01` |
| 2425 | SP500 | Pre-Market | 45m | FADE_UP | RSI_D<35 | `61.8%` | 55 | `7` | `1.62` | `13R` | `-3.0R` | `4.01` |
| 2426 | VIX | NY Cash | 45m | FADE_UP | Tue | `61.8%` | 55 | `16` | `1.62` | `13R` | `-5.0R` | `4.01` |
| 2427 | VIX | NY Cash | 60m | FADE_DOWN | BelowPD | `61.8%` | 55 | `16` | `1.62` | `13R` | `-5.0R` | `4.01` |
| 2428 | XAGUSD | London | 15m | SHAKEOUT_DOWN | BASE | `55.2%` | 368 | `45` | `1.23` | `38R` | `-11.0R` | `4.01` |
| 2429 | BRENT | London | 45m | FADE_UP | RSI_30-50 | `56.4%` | 241 | `30` | `1.30` | `31R` | `-11.0R` | `4.01` |
| 2430 | EURUSD | London | 30m | FADE_DOWN | Mon | `57.5%` | 174 | `21` | `1.35` | `26R` | `-6.0R` | `4.01` |
| 2431 | GBPUSD | NY | 60m | FADE_UP | OR_Q4_Wide | `61.3%` | 62 | `8` | `1.58` | `14R` | `-6.0R` | `4.01` |
| 2432 | VIX | NY Cash | 45m | FADE_UP | RSI_50-70 | `58.5%` | 130 | `39` | `1.41` | `22R` | `-9.0R` | `4.00` |
| 2433 | USDJPY | NY | 30m | FADE_UP | AbovePD | `57.2%` | 187 | `23` | `1.34` | `27R` | `-8.0R` | `4.00` |
| 2434 | EURJPY | Tokyo | 45m | FADE_UP | Mon | `57.2%` | 187 | `23` | `1.34` | `27R` | `-8.0R` | `4.00` |
| 2435 | WTI | London Initial | 60m | FADE_DOWN | Wed | `57.2%` | 187 | `23` | `1.34` | `27R` | `-10.0R` | `4.00` |
| 2436 | XAUUSD | NY | 60m | FADE_UP | RSI_50-70 | `56.4%` | 243 | `30` | `1.29` | `31R` | `-12.0R` | `4.00` |
| 2437 | XAUUSD | London | 30m | FADE_DOWN | Thu | `57.7%` | 163 | `20` | `1.36` | `25R` | `-9.0R` | `4.00` |
| 2438 | SP500 | Pre-Market | 45m | FADE_UP | Thu | `57.7%` | 163 | `20` | `1.36` | `25R` | `-11.0R` | `4.00` |
| 2439 | EURUSD | London | 15m | FADE_DOWN | Tue | `58.2%` | 141 | `18` | `1.39` | `23R` | `-8.0R` | `4.00` |
| 2440 | XAUUSD | NY | 60m | FADE_UP | BtwCloseHigh | `58.2%` | 141 | `17` | `1.39` | `23R` | `-8.0R` | `4.00` |
| 2441 | WTI | London Initial | 60m | FADE_DOWN | RSI<30 | `60.0%` | 85 | `11` | `1.50` | `17R` | `-5.0R` | `4.00` |
| 2442 | WTI | NY Main | 45m | FADE_DOWN | BtwCloseHigh | `56.7%` | 215 | `26` | `1.31` | `29R` | `-10.0R` | `4.00` |
| 2443 | WTI | NY Main | 60m | FADE_DOWN | Fri | `58.7%` | 121 | `15` | `1.42` | `21R` | `-8.0R` | `4.00` |
| 2444 | GBPUSD | London | 15m | FADE_UP | Tue | `57.4%` | 176 | `22` | `1.35` | `26R` | `-5.0R` | `4.00` |
| 2445 | EURJPY | Tokyo | 30m | FADE_DOWN | Tue | `57.4%` | 176 | `22` | `1.35` | `26R` | `-7.0R` | `4.00` |
| 2446 | EURUSD | NY | 15m | FADE_UP | AbovePD | `57.1%` | 189 | `23` | `1.33` | `27R` | `-8.0R` | `3.99` |
| 2447 | NATGAS | NY | 45m | FADE_UP | BtwLowClose | `57.1%` | 189 | `23` | `1.33` | `27R` | `-10.0R` | `3.99` |
| 2448 | EURJPY | Tokyo | 45m | FADE_DOWN | OR_Q1_Tight | `56.7%` | 217 | `27` | `1.31` | `29R` | `-10.0R` | `3.99` |
| 2449 | USDJPY | Tokyo | 60m | FADE_DOWN | BtwLowClose | `55.3%` | 338 | `42` | `1.24` | `36R` | `-10.0R` | `3.99` |
| 2450 | GBPJPY | London | 60m | FADE_DOWN | BelowPD | `59.6%` | 94 | `12` | `1.47` | `18R` | `-7.0R` | `3.99` |
| 2451 | SP500 | Pre-Market | 15m | FADE_UP | BtwCloseHigh | `59.6%` | 94 | `12` | `1.47` | `18R` | `-8.0R` | `3.99` |
| 2452 | NASDAQ100 | NY Cash | 30m | FADE_UP | BelowPD | `59.6%` | 94 | `12` | `1.47` | `18R` | `-6.0R` | `3.99` |
| 2453 | SP500 | Pre-Market | 60m | FADE_UP | BtwCloseHigh | `55.9%` | 281 | `35` | `1.27` | `33R` | `-16.0R` | `3.99` |
| 2454 | NASDAQ100 | Pre-Market | 45m | FADE_UP | BtwCloseHigh | `56.1%` | 264 | `33` | `1.28` | `32R` | `-7.0R` | `3.99` |
| 2455 | GBPJPY | London | 60m | FADE_UP | RSI>70 | `59.2%` | 103 | `13` | `1.45` | `19R` | `-7.0R` | `3.99` |
| 2456 | XAGUSD | London | 30m | FADE_UP | RSI_D>65 | `57.8%` | 154 | `20` | `1.37` | `24R` | `-5.0R` | `3.99` |
| 2457 | BRENT | London | 45m | FADE_UP | Tue | `57.8%` | 154 | `19` | `1.37` | `24R` | `-7.0R` | `3.99` |
| 2458 | SP500 | NY Cash | 60m | FADE_DOWN | ATR+10% | `62.8%` | 43 | `5` | `1.69` | `11R` | `-4.0R` | `3.99` |
| 2459 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | BelowPD | `62.8%` | 43 | `5` | `1.69` | `11R` | `-8.0R` | `3.99` |
| 2460 | VIX | NY Cash | 15m | FADE_DOWN | Fri | `62.8%` | 43 | `13` | `1.69` | `11R` | `-2.0R` | `3.99` |
| 2461 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | BtwCloseHigh | `57.1%` | 191 | `23` | `1.33` | `27R` | `-9.0R` | `3.98` |
| 2462 | EURUSD | NY | 60m | FADE_DOWN | Thu | `60.3%` | 78 | `10` | `1.52` | `16R` | `-8.0R` | `3.98` |
| 2463 | USDJPY | Tokyo | 45m | FADE_DOWN | RSI<30 | `60.3%` | 78 | `10` | `1.52` | `16R` | `-8.0R` | `3.98` |
| 2464 | WTI | NY Main | 60m | FADE_DOWN | RSI_D<35 | `60.3%` | 78 | `10` | `1.52` | `16R` | `-6.0R` | `3.98` |
| 2465 | BRENT | London | 15m | FADE_DOWN | RSI_30-50 | `56.2%` | 251 | `31` | `1.28` | `31R` | `-9.0R` | `3.98` |
| 2466 | SP500 | Pre-Market | 30m | FADE_DOWN | Wed | `58.5%` | 123 | `16` | `1.41` | `21R` | `-4.0R` | `3.98` |
| 2467 | USDJPY | Tokyo | 30m | FADE_UP | OR_Q1_Tight | `56.4%` | 236 | `30` | `1.29` | `30R` | `-11.0R` | `3.98` |
| 2468 | GBPUSD | NY | 30m | FADE_DOWN | Mon | `57.2%` | 180 | `22` | `1.34` | `26R` | `-9.0R` | `3.97` |
| 2469 | EURUSD | NY | 45m | FADE_DOWN | Wed | `58.2%` | 134 | `17` | `1.39` | `22R` | `-7.0R` | `3.97` |
| 2470 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | Tue | `58.2%` | 134 | `17` | `1.39` | `22R` | `-9.0R` | `3.97` |
| 2471 | VIX | NY Cash | 60m | FADE_UP | BASE | `56.5%` | 223 | `66` | `1.30` | `29R` | `-14.0R` | `3.97` |
| 2472 | SP500 | NY Cash | 60m | FADE_UP | Mon | `58.8%` | 114 | `14` | `1.43` | `20R` | `-6.0R` | `3.97` |
| 2473 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | RSI_30-50 | `55.9%` | 272 | `34` | `1.27` | `32R` | `-16.0R` | `3.97` |
| 2474 | EURJPY | London | 15m | FADE_UP | BtwCloseHigh | `56.1%` | 255 | `31` | `1.28` | `31R` | `-16.0R` | `3.97` |
| 2475 | NATGAS | NY | 15m | FADE_UP | Tue | `57.4%` | 169 | `21` | `1.35` | `25R` | `-6.0R` | `3.97` |
| 2476 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | BtwCloseHigh | `57.4%` | 169 | `21` | `1.35` | `25R` | `-11.0R` | `3.97` |
| 2477 | NATGAS | NY | 30m | FADE_UP | RSI_50-70 | `55.3%` | 331 | `41` | `1.24` | `35R` | `-16.0R` | `3.97` |
| 2478 | XAGUSD | London | 30m | FADE_UP | Tue | `56.9%` | 195 | `24` | `1.32` | `27R` | `-10.0R` | `3.97` |
| 2479 | USDJPY | NY | 45m | FADE_UP | RSI_D>65 | `59.8%` | 87 | `11` | `1.49` | `17R` | `-5.0R` | `3.97` |
| 2480 | BRENT | London | 15m | FADE_DOWN | RSI_D>65 | `59.8%` | 87 | `11` | `1.49` | `17R` | `-8.0R` | `3.97` |
| 2481 | BRENT | London | 15m | FADE_DOWN | Mon | `59.8%` | 87 | `11` | `1.49` | `17R` | `-4.0R` | `3.97` |
| 2482 | USDJPY | Tokyo | 15m | FADE_DOWN | Mon | `57.1%` | 182 | `22` | `1.33` | `26R` | `-13.0R` | `3.96` |
| 2483 | XAUUSD | NY | 30m | FADE_DOWN | BtwLowClose | `57.1%` | 182 | `22` | `1.33` | `26R` | `-11.0R` | `3.96` |
| 2484 | USDJPY | Tokyo | 60m | FADE_DOWN | RSI_D<35 | `60.6%` | 71 | `9` | `1.54` | `15R` | `-4.0R` | `3.96` |
| 2485 | EURUSD | London | 15m | FADE_DOWN | RSI_50-70 | `56.2%` | 240 | `30` | `1.29` | `30R` | `-7.0R` | `3.96` |
| 2486 | GBPUSD | London | 45m | FADE_UP | BtwCloseHigh | `55.4%` | 312 | `38` | `1.24` | `34R` | `-14.0R` | `3.96` |
| 2487 | BRENT | NY | 60m | FADE_DOWN | BtwLowClose | `56.7%` | 210 | `26` | `1.31` | `28R` | `-11.0R` | `3.96` |
| 2488 | EURUSD | NY | 60m | FADE_UP | AbovePD | `59.0%` | 105 | `13` | `1.44` | `19R` | `-6.0R` | `3.96` |
| 2489 | GBPUSD | London | 30m | SHAKEOUT_UP | OR_Q1_Tight | `59.0%` | 105 | `13` | `1.44` | `19R` | `-6.0R` | `3.96` |
| 2490 | XAUUSD | London | 45m | FADE_DOWN | OR_Q4_Wide | `56.4%` | 225 | `34` | `1.30` | `29R` | `-9.0R` | `3.96` |
| 2491 | USDJPY | Tokyo | 45m | FADE_UP | RSI>70 | `59.4%` | 96 | `12` | `1.46` | `18R` | `-6.0R` | `3.96` |
| 2492 | SP500 | NY Cash | 15m | FADE_DOWN | RSI<30 | `59.4%` | 96 | `12` | `1.46` | `18R` | `-4.0R` | `3.96` |
| 2493 | USDJPY | NY | 30m | FADE_DOWN | BelowPD | `57.6%` | 158 | `19` | `1.36` | `24R` | `-6.0R` | `3.96` |
| 2494 | GBPAUD | London | 45m | FADE_DOWN | AbovePD | `57.6%` | 158 | `19` | `1.36` | `24R` | `-7.0R` | `3.96` |
| 2495 | AUDUSD | Sydney | 15m | FADE_UP | BASE | `58.4%` | 125 | `15` | `1.40` | `21R` | `-6.0R` | `3.96` |
| 2496 | XAGUSD | London | 15m | FADE_UP | Wed | `58.4%` | 125 | `16` | `1.40` | `21R` | `-7.0R` | `3.96` |
| 2497 | GBPUSD | London | 60m | FADE_DOWN | Thu | `56.9%` | 197 | `24` | `1.32` | `27R` | `-6.0R` | `3.96` |
| 2498 | GBPJPY | London | 30m | FADE_DOWN | ATR+10% | `62.0%` | 50 | `6` | `1.63` | `12R` | `-4.0R` | `3.96` |
| 2499 | GBPJPY | London | 45m | FADE_UP | ATR+10% | `62.0%` | 50 | `6` | `1.63` | `12R` | `-6.0R` | `3.96` |
| 2500 | WTI | London Initial | 30m | SHAKEOUT_DOWN | OR_Q1_Tight | `62.0%` | 50 | `6` | `1.63` | `12R` | `-5.0R` | `3.96` |
| 2501 | WTI | London Initial | 30m | FADE_UP | Tue | `57.8%` | 147 | `18` | `1.37` | `23R` | `-9.0R` | `3.96` |
| 2502 | SP500 | NY Cash | 30m | FADE_UP | Wed | `57.8%` | 147 | `18` | `1.37` | `23R` | `-5.0R` | `3.96` |
| 2503 | XAUUSD | London | 45m | FADE_UP | AbovePD | `57.3%` | 171 | `21` | `1.34` | `25R` | `-14.0R` | `3.96` |
| 2504 | XAUUSD | NY | 30m | FADE_UP | Mon | `58.1%` | 136 | `17` | `1.39` | `22R` | `-5.0R` | `3.96` |
| 2505 | XAUUSD | NY | 30m | FADE_UP | Fri | `58.1%` | 136 | `17` | `1.39` | `22R` | `-5.0R` | `3.96` |
| 2506 | NASDAQ100 | NY Cash | 30m | FADE_UP | RSI>70 | `58.1%` | 136 | `17` | `1.39` | `22R` | `-5.0R` | `3.96` |
| 2507 | USDJPY | Tokyo | 60m | FADE_UP | Tue | `56.6%` | 212 | `26` | `1.30` | `28R` | `-11.0R` | `3.95` |
| 2508 | XAUUSD | NY | 15m | FADE_UP | RSI_D<35 | `60.9%` | 64 | `8` | `1.56` | `14R` | `-5.0R` | `3.95` |
| 2509 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | BtwCloseHigh | `55.9%` | 261 | `32` | `1.27` | `31R` | `-7.0R` | `3.95` |
| 2510 | XAUUSD | London | 45m | FADE_UP | BtwCloseHigh | `55.5%` | 299 | `37` | `1.25` | `33R` | `-9.0R` | `3.95` |
| 2511 | WTI | NY Main | 15m | FADE_UP | BtwLowClose | `56.3%` | 229 | `28` | `1.29` | `29R` | `-6.0R` | `3.95` |
| 2512 | GBPUSD | London | 60m | FADE_DOWN | AbovePD | `57.5%` | 160 | `20` | `1.35` | `24R` | `-7.0R` | `3.95` |
| 2513 | XAGUSD | NY | 15m | FADE_UP | Tue | `57.5%` | 160 | `20` | `1.35` | `24R` | `-14.0R` | `3.95` |
| 2514 | EURJPY | London | 15m | FADE_UP | OR_Q1_Tight | `58.6%` | 116 | `15` | `1.42` | `20R` | `-6.0R` | `3.95` |
| 2515 | XAUUSD | NY | 60m | FADE_UP | BtwLowClose | `58.6%` | 116 | `14` | `1.42` | `20R` | `-7.0R` | `3.95` |
| 2516 | SP500 | Pre-Market | 30m | FADE_UP | BelowPD | `58.6%` | 116 | `14` | `1.42` | `20R` | `-8.0R` | `3.95` |
| 2517 | AUDUSD | London | 15m | FADE_DOWN | BtwCloseHigh | `56.5%` | 214 | `26` | `1.30` | `28R` | `-14.0R` | `3.95` |
| 2518 | GBPUSD | London | 60m | FADE_DOWN | Wed | `57.0%` | 186 | `23` | `1.32` | `26R` | `-7.0R` | `3.95` |
| 2519 | XAUUSD | London | 30m | FADE_UP | Tue | `57.0%` | 186 | `23` | `1.32` | `26R` | `-12.0R` | `3.95` |
| 2520 | SP500 | Pre-Market | 60m | FADE_UP | RSI_D>65 | `57.0%` | 186 | `24` | `1.32` | `26R` | `-9.0R` | `3.95` |
| 2521 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | RSI_50-70 | `57.0%` | 186 | `23` | `1.32` | `26R` | `-7.0R` | `3.95` |
| 2522 | USDJPY | Tokyo | 60m | FADE_DOWN | Tue | `57.2%` | 173 | `21` | `1.34` | `25R` | `-7.0R` | `3.95` |
| 2523 | GBPUSD | NY | 45m | FADE_DOWN | RSI_D<35 | `60.0%` | 80 | `11` | `1.50` | `16R` | `-7.0R` | `3.94` |
| 2524 | BRENT | NY | 15m | FADE_DOWN | Thu | `57.7%` | 149 | `18` | `1.37` | `23R` | `-9.0R` | `3.94` |
| 2525 | GBPAUD | London | 30m | FADE_DOWN | Mon | `56.7%` | 201 | `25` | `1.31` | `27R` | `-10.0R` | `3.94` |
| 2526 | XAUUSD | NY | 30m | FADE_UP | BtwCloseHigh | `56.7%` | 201 | `25` | `1.31` | `27R` | `-8.0R` | `3.94` |
| 2527 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | RSI_30-50 | `58.9%` | 107 | `13` | `1.43` | `19R` | `-4.0R` | `3.94` |
| 2528 | AUDUSD | Sydney | 15m | FADE_UP | BelowPD | `63.2%` | 38 | `5` | `1.71` | `10R` | `-3.0R` | `3.94` |
| 2529 | GBPJPY | London | 15m | FADE_DOWN | RSI>70 | `63.2%` | 38 | `5` | `1.71` | `10R` | `-4.0R` | `3.94` |
| 2530 | GBPAUD | London | 15m | SHAKEOUT_UP | OR_Q1_Tight | `63.2%` | 38 | `5` | `1.71` | `10R` | `-5.0R` | `3.94` |
| 2531 | XAGUSD | NY | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `63.2%` | 38 | `5` | `1.71` | `10R` | `-4.0R` | `3.94` |
| 2532 | WTI | London Initial | 15m | SHAKEOUT_UP | Tue | `63.2%` | 38 | `5` | `1.71` | `10R` | `-4.0R` | `3.94` |
| 2533 | VIX | NY Cash | 60m | FADE_UP | Mon | `63.2%` | 38 | `13` | `1.71` | `10R` | `-6.0R` | `3.94` |
| 2534 | WTI | NY Main | 30m | FADE_DOWN | BelowPD | `57.4%` | 162 | `20` | `1.35` | `24R` | `-12.0R` | `3.94` |
| 2535 | AUDUSD | London | 30m | FADE_UP | OR_Q4_Wide | `56.0%` | 250 | `31` | `1.27` | `30R` | `-10.0R` | `3.94` |
| 2536 | GBPAUD | London | 15m | FADE_DOWN | RSI_D<35 | `59.6%` | 89 | `11` | `1.47` | `17R` | `-7.0R` | `3.94` |
| 2537 | BRENT | London | 15m | FADE_UP | Fri | `59.6%` | 89 | `11` | `1.47` | `17R` | `-7.0R` | `3.94` |
| 2538 | XAUUSD | London | 45m | FADE_DOWN | RSI_D>65 | `57.1%` | 175 | `22` | `1.33` | `25R` | `-10.0R` | `3.94` |
| 2539 | GBPAUD | London | 45m | FADE_DOWN | BelowPD | `57.6%` | 151 | `19` | `1.36` | `23R` | `-8.0R` | `3.93` |
| 2540 | WTI | NY Main | 60m | FADE_DOWN | Wed | `57.6%` | 151 | `19` | `1.36` | `23R` | `-9.0R` | `3.93` |
| 2541 | XAUUSD | NY | 30m | FADE_DOWN | Fri | `58.5%` | 118 | `14` | `1.41` | `20R` | `-8.0R` | `3.93` |
| 2542 | XAUUSD | NY | 15m | FADE_UP | OR_Q1_Tight | `56.8%` | 190 | `31` | `1.32` | `26R` | `-12.0R` | `3.93` |
| 2543 | SP500 | NY Cash | 15m | FADE_UP | OR_Q4_Wide | `56.6%` | 205 | `26` | `1.30` | `27R` | `-8.0R` | `3.93` |
| 2544 | SP500 | NY Cash | 60m | FADE_UP | RSI_30-50 | `57.3%` | 164 | `20` | `1.34` | `24R` | `-5.0R` | `3.93` |
| 2545 | AUDUSD | London | 45m | FADE_DOWN | Fri | `57.1%` | 177 | `22` | `1.33` | `25R` | `-6.0R` | `3.93` |
| 2546 | WTI | London Initial | 60m | FADE_UP | OR_Q1_Tight | `57.1%` | 177 | `22` | `1.33` | `25R` | `-10.0R` | `3.93` |
| 2547 | GBPUSD | London | 60m | FADE_UP | RSI_30-50 | `55.9%` | 254 | `31` | `1.27` | `30R` | `-8.0R` | `3.92` |
| 2548 | XAGUSD | London | 15m | FADE_UP | BtwLowClose | `55.9%` | 254 | `31` | `1.27` | `30R` | `-11.0R` | `3.92` |
| 2549 | XAGUSD | London | 15m | SHAKEOUT_DOWN | BtwLowClose | `58.1%` | 129 | `17` | `1.39` | `21R` | `-5.0R` | `3.92` |
| 2550 | SP500 | NY Cash | 15m | FADE_UP | BtwCloseHigh | `55.9%` | 256 | `32` | `1.27` | `30R` | `-12.0R` | `3.92` |
| 2551 | AUDUSD | London | 15m | FADE_DOWN | RSI_50-70 | `55.6%` | 275 | `34` | `1.25` | `31R` | `-12.0R` | `3.92` |
| 2552 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | RSI_50-70 | `56.1%` | 239 | `29` | `1.28` | `29R` | `-15.0R` | `3.92` |
| 2553 | EURUSD | NY | 15m | FADE_DOWN | Tue | `57.5%` | 153 | `19` | `1.35` | `23R` | `-8.0R` | `3.92` |
| 2554 | EURJPY | London | 15m | FADE_UP | AbovePD | `57.5%` | 153 | `19` | `1.35` | `23R` | `-6.0R` | `3.92` |
| 2555 | SP500 | NY Cash | 15m | FADE_UP | Wed | `57.5%` | 153 | `19` | `1.35` | `23R` | `-6.0R` | `3.92` |
| 2556 | AUDUSD | London | 60m | FADE_DOWN | Fri | `57.0%` | 179 | `22` | `1.32` | `25R` | `-7.0R` | `3.92` |
| 2557 | SP500 | NY Cash | 60m | FADE_UP | OR_Q1_Tight | `57.0%` | 179 | `22` | `1.32` | `25R` | `-7.0R` | `3.92` |
| 2558 | GBPJPY | Tokyo | 30m | FADE_DOWN | Thu | `57.2%` | 166 | `20` | `1.34` | `24R` | `-12.0R` | `3.91` |
| 2559 | GBPAUD | London | 15m | FADE_DOWN | RSI_50-70 | `55.8%` | 260 | `32` | `1.26` | `30R` | `-13.0R` | `3.91` |
| 2560 | XAGUSD | London | 30m | FADE_UP | RSI_D<35 | `59.8%` | 82 | `11` | `1.48` | `16R` | `-9.0R` | `3.91` |
| 2561 | SP500 | NY Cash | 60m | FADE_DOWN | Mon | `59.0%` | 100 | `12` | `1.44` | `18R` | `-8.0R` | `3.91` |
| 2562 | VIX | NY Cash | 15m | FADE_UP | RSI_50-70 | `59.0%` | 100 | `29` | `1.44` | `18R` | `-6.0R` | `3.91` |
| 2563 | SP500 | Pre-Market | 45m | FADE_DOWN | BelowPD | `58.0%` | 131 | `16` | `1.38` | `21R` | `-6.0R` | `3.91` |
| 2564 | GBPJPY | London | 15m | FADE_DOWN | RSI<30 | `59.3%` | 91 | `11` | `1.46` | `17R` | `-4.0R` | `3.91` |
| 2565 | WTI | London Initial | 45m | FADE_UP | RSI>70 | `59.3%` | 91 | `11` | `1.46` | `17R` | `-6.0R` | `3.91` |
| 2566 | GBPJPY | London | 30m | FADE_UP | RSI_30-50 | `55.5%` | 281 | `34` | `1.25` | `31R` | `-12.0R` | `3.91` |
| 2567 | XAUUSD | London | 30m | FADE_DOWN | BtwLowClose | `55.5%` | 281 | `35` | `1.25` | `31R` | `-12.0R` | `3.91` |
| 2568 | BRENT | London | 30m | FADE_UP | RSI>70 | `60.6%` | 66 | `8` | `1.54` | `14R` | `-5.0R` | `3.91` |
| 2569 | SP500 | NY Cash | 60m | FADE_DOWN | RSI<30 | `60.6%` | 66 | `8` | `1.54` | `14R` | `-4.0R` | `3.91` |
| 2570 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | RSI_30-50 | `60.6%` | 66 | `8` | `1.54` | `14R` | `-4.0R` | `3.91` |
| 2571 | USDJPY | Tokyo | 15m | FADE_UP | Fri | `57.1%` | 168 | `21` | `1.33` | `24R` | `-8.0R` | `3.90` |
| 2572 | EURJPY | Tokyo | 15m | FADE_DOWN | Mon | `57.1%` | 168 | `21` | `1.33` | `24R` | `-8.0R` | `3.90` |
| 2573 | XAGUSD | London | 60m | FADE_DOWN | ATR+10% | `62.2%` | 45 | `6` | `1.65` | `11R` | `-3.0R` | `3.90` |
| 2574 | BRENT | London | 30m | FADE_UP | Mon | `57.6%` | 144 | `18` | `1.36` | `22R` | `-8.0R` | `3.90` |
| 2575 | GBPJPY | London | 45m | FADE_UP | Wed | `56.6%` | 198 | `25` | `1.30` | `26R` | `-8.0R` | `3.90` |
| 2576 | WTI | NY Main | 15m | FADE_UP | AbovePD | `56.6%` | 198 | `24` | `1.30` | `26R` | `-7.0R` | `3.90` |
| 2577 | VIX | NY Cash | 15m | FADE_UP | BASE | `56.1%` | 230 | `68` | `1.28` | `28R` | `-14.0R` | `3.90` |
| 2578 | XAGUSD | NY | 30m | FADE_UP | RSI_D<35 | `61.0%` | 59 | `8` | `1.57` | `13R` | `-10.0R` | `3.89` |
| 2579 | BRENT | NY | 15m | FADE_UP | RSI_D<35 | `61.0%` | 59 | `8` | `1.57` | `13R` | `-7.0R` | `3.89` |
| 2580 | SP500 | Pre-Market | 15m | FADE_DOWN | Mon | `61.0%` | 59 | `7` | `1.57` | `13R` | `-2.0R` | `3.89` |
| 2581 | EURUSD | NY | 45m | FADE_DOWN | BtwCloseHigh | `57.3%` | 157 | `19` | `1.34` | `23R` | `-7.0R` | `3.89` |
| 2582 | EURJPY | London | 30m | FADE_DOWN | BelowPD | `57.9%` | 133 | `17` | `1.38` | `21R` | `-9.0R` | `3.89` |
| 2583 | XAGUSD | NY | 15m | FADE_UP | BelowPD | `57.9%` | 133 | `17` | `1.38` | `21R` | `-9.0R` | `3.89` |
| 2584 | NATGAS | NY | 45m | FADE_DOWN | Wed | `57.9%` | 133 | `16` | `1.38` | `21R` | `-7.0R` | `3.89` |
| 2585 | GBPUSD | London | 30m | FADE_UP | RSI_30-50 | `55.2%` | 310 | `38` | `1.23` | `32R` | `-13.0R` | `3.89` |
| 2586 | XAGUSD | NY | 45m | FADE_DOWN | AbovePD | `58.2%` | 122 | `15` | `1.39` | `20R` | `-4.0R` | `3.89` |
| 2587 | BRENT | NY | 30m | FADE_DOWN | BelowPD | `58.2%` | 122 | `15` | `1.39` | `20R` | `-14.0R` | `3.89` |
| 2588 | NATGAS | NY | 45m | FADE_DOWN | Mon | `58.2%` | 122 | `15` | `1.39` | `20R` | `-3.0R` | `3.89` |
| 2589 | GBPUSD | London | 15m | FADE_DOWN | OR_Q4_Wide | `55.8%` | 249 | `31` | `1.26` | `29R` | `-8.0R` | `3.89` |
| 2590 | NATGAS | NY | 15m | FADE_DOWN | BtwLowClose | `55.8%` | 249 | `31` | `1.26` | `29R` | `-11.0R` | `3.89` |
| 2591 | BRENT | NY | 15m | FADE_DOWN | RSI_D<35 | `61.5%` | 52 | `7` | `1.60` | `12R` | `-4.0R` | `3.89` |
| 2592 | VIX | NY Cash | 30m | FADE_UP | BelowPD | `61.5%` | 52 | `16` | `1.60` | `12R` | `-4.0R` | `3.89` |
| 2593 | GBPUSD | NY | 30m | FADE_DOWN | RSI_D<35 | `58.8%` | 102 | `13` | `1.43` | `18R` | `-7.0R` | `3.89` |
| 2594 | USDJPY | NY | 45m | FADE_DOWN | Thu | `58.8%` | 102 | `13` | `1.43` | `18R` | `-3.0R` | `3.89` |
| 2595 | GBPAUD | Sydney | 15m | FADE_UP | RSI_30-50 | `60.0%` | 75 | `9` | `1.50` | `15R` | `-6.0R` | `3.89` |
| 2596 | WTI | London Initial | 45m | FADE_UP | RSI_D<35 | `60.0%` | 75 | `10` | `1.50` | `15R` | `-7.0R` | `3.89` |
| 2597 | EURUSD | NY | 30m | FADE_DOWN | Mon | `57.5%` | 146 | `18` | `1.35` | `22R` | `-7.0R` | `3.88` |
| 2598 | XAUUSD | NY | 15m | FADE_DOWN | RSI_D>65 | `57.5%` | 146 | `20` | `1.35` | `22R` | `-10.0R` | `3.88` |
| 2599 | XAUUSD | NY | 15m | FADE_DOWN | Fri | `57.5%` | 146 | `18` | `1.35` | `22R` | `-7.0R` | `3.88` |
| 2600 | BRENT | NY | 30m | FADE_DOWN | Fri | `57.0%` | 172 | `22` | `1.32` | `24R` | `-6.0R` | `3.88` |
| 2601 | NASDAQ100 | Pre-Market | 60m | FADE_UP | Thu | `57.2%` | 159 | `20` | `1.34` | `23R` | `-8.0R` | `3.88` |
| 2602 | GBPUSD | London | 30m | FADE_DOWN | Fri | `56.4%` | 202 | `25` | `1.30` | `26R` | `-11.0R` | `3.88` |
| 2603 | EURJPY | Tokyo | 30m | FADE_UP | Fri | `56.4%` | 202 | `25` | `1.30` | `26R` | `-10.0R` | `3.88` |
| 2604 | XAUUSD | London | 45m | FADE_UP | Fri | `56.4%` | 202 | `25` | `1.30` | `26R` | `-10.0R` | `3.88` |
| 2605 | AUDUSD | London | 45m | FADE_DOWN | RSI_D>65 | `59.1%` | 93 | `12` | `1.45` | `17R` | `-4.0R` | `3.88` |
| 2606 | WTI | London Initial | 15m | FADE_UP | Fri | `59.1%` | 93 | `12` | `1.45` | `17R` | `-6.0R` | `3.88` |
| 2607 | EURUSD | NY | 30m | FADE_UP | RSI_D>65 | `59.5%` | 84 | `10` | `1.47` | `16R` | `-6.0R` | `3.88` |
| 2608 | EURUSD | London | 45m | FADE_UP | RSI_D<35 | `58.4%` | 113 | `14` | `1.40` | `19R` | `-3.0R` | `3.88` |
| 2609 | USDJPY | NY | 30m | FADE_UP | OR_Q4_Wide | `58.1%` | 124 | `15` | `1.38` | `20R` | `-5.0R` | `3.88` |
| 2610 | GBPJPY | Tokyo | 15m | FADE_DOWN | Tue | `58.1%` | 124 | `15` | `1.38` | `20R` | `-4.0R` | `3.88` |
| 2611 | BRENT | London | 60m | FADE_UP | Mon | `56.9%` | 174 | `22` | `1.32` | `24R` | `-7.0R` | `3.87` |
| 2612 | NASDAQ100 | NY Cash | 15m | FADE_UP | BtwLowClose | `56.4%` | 204 | `25` | `1.29` | `26R` | `-8.0R` | `3.87` |
| 2613 | GBPAUD | London | 30m | FADE_UP | OR_Q4_Wide | `55.9%` | 238 | `29` | `1.27` | `28R` | `-8.0R` | `3.87` |
| 2614 | XAUUSD | London | 15m | FADE_UP | RSI_30-50 | `55.6%` | 257 | `31` | `1.25` | `29R` | `-7.0R` | `3.87` |
| 2615 | GBPJPY | London | 30m | FADE_UP | Wed | `56.6%` | 189 | `24` | `1.30` | `25R` | `-7.0R` | `3.87` |
| 2616 | XAUUSD | London | 45m | FADE_UP | Thu | `56.6%` | 189 | `23` | `1.30` | `25R` | `-8.0R` | `3.87` |
| 2617 | SP500 | Pre-Market | 15m | FADE_DOWN | RSI_30-50 | `56.6%` | 189 | `23` | `1.30` | `25R` | `-12.0R` | `3.87` |
| 2618 | USDJPY | NY | 30m | FADE_DOWN | Mon | `57.4%` | 148 | `18` | `1.35` | `22R` | `-8.0R` | `3.87` |
| 2619 | GBPAUD | London | 30m | FADE_DOWN | BelowPD | `57.4%` | 148 | `19` | `1.35` | `22R` | `-12.0R` | `3.87` |
| 2620 | USDJPY | NY | 30m | FADE_DOWN | Wed | `57.1%` | 161 | `20` | `1.33` | `23R` | `-6.0R` | `3.87` |
| 2621 | XAGUSD | NY | 15m | FADE_DOWN | Fri | `57.7%` | 137 | `17` | `1.36` | `21R` | `-6.0R` | `3.86` |
| 2622 | EURUSD | London | 15m | FADE_UP | Tue | `57.1%` | 163 | `20` | `1.33` | `23R` | `-5.0R` | `3.86` |
| 2623 | USDJPY | NY | 15m | FADE_DOWN | BtwCloseHigh | `57.1%` | 163 | `20` | `1.33` | `23R` | `-8.0R` | `3.86` |
| 2624 | USDJPY | NY | 45m | FADE_DOWN | Wed | `57.3%` | 150 | `18` | `1.34` | `22R` | `-6.0R` | `3.86` |
| 2625 | WTI | NY Main | 30m | FADE_UP | BtwLowClose | `56.0%` | 225 | `28` | `1.27` | `27R` | `-11.0R` | `3.86` |
| 2626 | GBPUSD | London | 60m | FADE_DOWN | RSI_50-70 | `55.5%` | 263 | `33` | `1.25` | `29R` | `-11.0R` | `3.86` |
| 2627 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | GapSmall | `55.5%` | 263 | `32` | `1.25` | `29R` | `-11.0R` | `3.86` |
| 2628 | WTI | London Initial | 60m | FADE_DOWN | BelowPD | `58.3%` | 115 | `15` | `1.40` | `19R` | `-5.0R` | `3.86` |
| 2629 | GBPAUD | London | 30m | FADE_UP | Thu | `56.7%` | 178 | `22` | `1.31` | `24R` | `-10.0R` | `3.86` |
| 2630 | WTI | NY Main | 15m | FADE_UP | Thu | `56.7%` | 178 | `22` | `1.31` | `24R` | `-6.0R` | `3.86` |
| 2631 | GBPJPY | London | 60m | FADE_DOWN | Tue | `57.0%` | 165 | `20` | `1.32` | `23R` | `-11.0R` | `3.85` |
| 2632 | BRENT | London | 15m | FADE_UP | Mon | `59.7%` | 77 | `9` | `1.48` | `15R` | `-5.0R` | `3.85` |
| 2633 | BRENT | NY | 30m | FADE_UP | RSI_30-50 | `55.2%` | 290 | `36` | `1.23` | `30R` | `-14.0R` | `3.85` |
| 2634 | XAUUSD | London | 45m | FADE_DOWN | Thu | `56.4%` | 195 | `24` | `1.29` | `25R` | `-6.0R` | `3.85` |
| 2635 | GBPJPY | Tokyo | 60m | FADE_DOWN | RSI_D>65 | `57.2%` | 152 | `20` | `1.34` | `22R` | `-4.0R` | `3.85` |
| 2636 | BRENT | NY | 60m | FADE_DOWN | Wed | `57.2%` | 152 | `19` | `1.34` | `22R` | `-7.0R` | `3.85` |
| 2637 | XAGUSD | NY | 45m | FADE_DOWN | RSI_50-70 | `56.7%` | 180 | `22` | `1.31` | `24R` | `-9.0R` | `3.85` |
| 2638 | NATGAS | NY | 15m | FADE_DOWN | Thu | `56.7%` | 180 | `22` | `1.31` | `24R` | `-10.0R` | `3.85` |
| 2639 | XAGUSD | London | 45m | FADE_DOWN | BelowPD | `57.8%` | 128 | `16` | `1.37` | `20R` | `-7.0R` | `3.84` |
| 2640 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | OR_Q4_Wide | `58.5%` | 106 | `14` | `1.41` | `18R` | `-8.0R` | `3.84` |
| 2641 | AUDUSD | Sydney | 60m | FADE_UP | GapSmall | `62.5%` | 40 | `5` | `1.67` | `10R` | `-3.0R` | `3.84` |
| 2642 | XAGUSD | London | 60m | FADE_UP | AbovePD+RSI_D>65 | `62.5%` | 40 | `5` | `1.67` | `10R` | `-6.0R` | `3.84` |
| 2643 | SP500 | Pre-Market | 60m | SHAKEOUT_DOWN | RSI_D<35 | `62.5%` | 40 | `6` | `1.67` | `10R` | `-3.0R` | `3.84` |
| 2644 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | OR_Q1_Tight | `62.5%` | 40 | `20` | `1.67` | `10R` | `-3.0R` | `3.84` |
| 2645 | NASDAQ100 | NY Cash | 45m | FADE_UP | RSI_D<35 | `62.5%` | 40 | `6` | `1.67` | `10R` | `-3.0R` | `3.84` |
| 2646 | XAGUSD | London | 60m | FADE_DOWN | Mon | `56.9%` | 167 | `21` | `1.32` | `23R` | `-8.0R` | `3.84` |
| 2647 | XAUUSD | NY | 45m | FADE_UP | Wed | `58.1%` | 117 | `14` | `1.39` | `19R` | `-7.0R` | `3.84` |
| 2648 | BRENT | NY | 60m | FADE_UP | BelowPD | `58.1%` | 117 | `14` | `1.39` | `19R` | `-6.0R` | `3.84` |
| 2649 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | GapSmall | `55.3%` | 273 | `33` | `1.24` | `29R` | `-10.0R` | `3.84` |
| 2650 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | Wed | `57.4%` | 141 | `17` | `1.35` | `21R` | `-6.0R` | `3.84` |
| 2651 | SP500 | Pre-Market | 60m | FADE_UP | Thu | `57.1%` | 154 | `19` | `1.33` | `22R` | `-17.0R` | `3.84` |
| 2652 | GBPUSD | NY | 15m | FADE_DOWN | RSI_D<35 | `58.8%` | 97 | `12` | `1.43` | `17R` | `-10.0R` | `3.83` |
| 2653 | GBPJPY | London | 15m | FADE_UP | RSI>70 | `58.8%` | 97 | `12` | `1.43` | `17R` | `-4.0R` | `3.83` |
| 2654 | EURUSD | NY | 60m | FADE_DOWN | RSI_D<35 | `61.1%` | 54 | `7` | `1.57` | `12R` | `-6.0R` | `3.83` |
| 2655 | GBPJPY | Tokyo | 30m | FADE_DOWN | ATR+10% | `61.1%` | 54 | `7` | `1.57` | `12R` | `-5.0R` | `3.83` |
| 2656 | GBPAUD | Sydney | 15m | FADE_UP | BtwLowClose | `61.1%` | 54 | `7` | `1.57` | `12R` | `-4.0R` | `3.83` |
| 2657 | WTI | NY Main | 60m | FADE_UP | RSI_D<35 | `61.1%` | 54 | `7` | `1.57` | `12R` | `-2.0R` | `3.83` |
| 2658 | EURUSD | London | 30m | FADE_UP | OR_Q1_Tight | `56.0%` | 218 | `29` | `1.27` | `26R` | `-10.0R` | `3.83` |
| 2659 | USDJPY | Tokyo | 60m | FADE_UP | OR_Q4_Wide | `56.0%` | 218 | `27` | `1.27` | `26R` | `-9.0R` | `3.83` |
| 2660 | SP500 | Pre-Market | 60m | FADE_DOWN | BelowPD | `57.7%` | 130 | `16` | `1.36` | `20R` | `-6.0R` | `3.83` |
| 2661 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | OR_Q1_Tight | `57.7%` | 130 | `24` | `1.36` | `20R` | `-9.0R` | `3.83` |
| 2662 | NASDAQ100 | NY Cash | 45m | FADE_UP | Wed | `57.7%` | 130 | `16` | `1.36` | `20R` | `-8.0R` | `3.83` |
| 2663 | EURJPY | Tokyo | 60m | FADE_DOWN | ATR+10% | `61.7%` | 47 | `6` | `1.61` | `11R` | `-3.0R` | `3.83` |
| 2664 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | Thu | `61.7%` | 47 | `6` | `1.61` | `11R` | `-7.0R` | `3.83` |
| 2665 | SP500 | Pre-Market | 30m | FADE_UP | RSI_D<35 | `61.7%` | 47 | `6` | `1.61` | `11R` | `-5.0R` | `3.83` |
| 2666 | NASDAQ100 | Pre-Market | 45m | FADE_UP | AbovePD+RSI_D>65 | `61.7%` | 47 | `6` | `1.61` | `11R` | `-4.0R` | `3.83` |
| 2667 | VIX | NY Cash | 15m | FADE_DOWN | Wed | `61.7%` | 47 | `14` | `1.61` | `11R` | `-7.0R` | `3.83` |
| 2668 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | BtwLowClose | `56.5%` | 186 | `23` | `1.30` | `24R` | `-11.0R` | `3.82` |
| 2669 | WTI | NY Main | 45m | FADE_DOWN | RSI_D>65 | `58.3%` | 108 | `13` | `1.40` | `18R` | `-11.0R` | `3.82` |
| 2670 | EURJPY | Tokyo | 30m | FADE_UP | RSI>70 | `60.0%` | 70 | `9` | `1.50` | `14R` | `-8.0R` | `3.82` |
| 2671 | WTI | London Initial | 15m | FADE_UP | RSI_D>65 | `60.0%` | 70 | `9` | `1.50` | `14R` | `-3.0R` | `3.82` |
| 2672 | NATGAS | NY | 60m | FADE_UP | RSI>70 | `60.0%` | 70 | `9` | `1.50` | `14R` | `-9.0R` | `3.82` |
| 2673 | EURUSD | NY | 15m | FADE_UP | BtwCloseHigh | `56.7%` | 171 | `21` | `1.31` | `23R` | `-8.0R` | `3.82` |
| 2674 | USDJPY | NY | 45m | FADE_DOWN | BtwLowClose | `56.7%` | 171 | `21` | `1.31` | `23R` | `-7.0R` | `3.82` |
| 2675 | EURJPY | London | 45m | FADE_UP | AbovePD | `56.7%` | 171 | `21` | `1.31` | `23R` | `-8.0R` | `3.82` |
| 2676 | EURUSD | London | 15m | SHAKEOUT_DOWN | RSI_30-50 | `56.2%` | 203 | `25` | `1.28` | `25R` | `-13.0R` | `3.82` |
| 2677 | XAUUSD | NY | 45m | FADE_DOWN | Fri | `59.1%` | 88 | `11` | `1.44` | `16R` | `-5.0R` | `3.82` |
| 2678 | XAGUSD | London | 60m | FADE_UP | RSI>70 | `59.1%` | 88 | `11` | `1.44` | `16R` | `-8.0R` | `3.82` |
| 2679 | EURJPY | Tokyo | 60m | FADE_UP | OR_Q1_Tight | `55.6%` | 241 | `30` | `1.25` | `27R` | `-8.0R` | `3.82` |
| 2680 | SP500 | Pre-Market | 15m | FADE_UP | Thu | `59.5%` | 79 | `10` | `1.47` | `15R` | `-4.0R` | `3.82` |
| 2681 | WTI | NY Main | 45m | FADE_DOWN | Wed | `57.0%` | 158 | `20` | `1.32` | `22R` | `-7.0R` | `3.82` |
| 2682 | SP500 | NY Cash | 15m | FADE_UP | RSI_D>65 | `57.0%` | 158 | `21` | `1.32` | `22R` | `-7.0R` | `3.82` |
| 2683 | GBPAUD | London | 30m | FADE_DOWN | Fri | `56.4%` | 188 | `23` | `1.29` | `24R` | `-10.0R` | `3.82` |
| 2684 | EURJPY | Tokyo | 45m | FADE_UP | Tue | `56.1%` | 205 | `25` | `1.28` | `25R` | `-6.0R` | `3.82` |
| 2685 | EURUSD | NY | 15m | FADE_UP | OR_Q1_Tight | `57.6%` | 132 | `18` | `1.36` | `20R` | `-8.0R` | `3.82` |
| 2686 | BRENT | NY | 60m | FADE_DOWN | Thu | `57.6%` | 132 | `16` | `1.36` | `20R` | `-6.0R` | `3.82` |
| 2687 | XAUUSD | London | 60m | FADE_DOWN | OR_Q1_Tight | `55.5%` | 245 | `35` | `1.25` | `27R` | `-10.0R` | `3.81` |
| 2688 | NASDAQ100 | Pre-Market | 45m | SHAKEOUT_DOWN | RSI_D>65 | `58.6%` | 99 | `13` | `1.41` | `17R` | `-9.0R` | `3.81` |
| 2689 | USDJPY | Tokyo | 45m | FADE_UP | Wed | `55.8%` | 226 | `28` | `1.26` | `26R` | `-6.0R` | `3.81` |
| 2690 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | AbovePD | `56.9%` | 160 | `20` | `1.32` | `22R` | `-7.0R` | `3.81` |
| 2691 | SP500 | Pre-Market | 15m | FADE_DOWN | BtwCloseHigh | `58.2%` | 110 | `14` | `1.39` | `18R` | `-7.0R` | `3.80` |
| 2692 | NATGAS | NY | 15m | FADE_DOWN | RSI_50-70 | `55.2%` | 270 | `33` | `1.23` | `28R` | `-16.0R` | `3.80` |
| 2693 | GBPAUD | London | 15m | FADE_UP | Mon | `57.5%` | 134 | `16` | `1.35` | `20R` | `-8.0R` | `3.80` |
| 2694 | NASDAQ100 | Pre-Market | 60m | FADE_UP | BtwLowClose | `55.1%` | 272 | `33` | `1.23` | `28R` | `-12.0R` | `3.80` |
| 2695 | XAGUSD | NY | 60m | FADE_DOWN | Fri | `60.3%` | 63 | `8` | `1.52` | `13R` | `-4.0R` | `3.80` |
| 2696 | WTI | London Initial | 30m | FADE_DOWN | RSI<30 | `60.3%` | 63 | `8` | `1.52` | `13R` | `-5.0R` | `3.80` |
| 2697 | SP500 | Pre-Market | 15m | FADE_DOWN | Wed | `60.3%` | 63 | `8` | `1.52` | `13R` | `-4.0R` | `3.80` |
| 2698 | SP500 | NY Cash | 15m | FADE_UP | RSI_30-50 | `55.9%` | 211 | `26` | `1.27` | `25R` | `-9.0R` | `3.80` |
| 2699 | GBPJPY | London | 60m | FADE_UP | AbovePD | `56.8%` | 162 | `20` | `1.31` | `22R` | `-6.0R` | `3.80` |
| 2700 | WTI | NY Main | 30m | FADE_DOWN | Fri | `56.8%` | 162 | `20` | `1.31` | `22R` | `-9.0R` | `3.80` |
| 2701 | NASDAQ100 | Pre-Market | 45m | FADE_UP | Fri | `56.8%` | 162 | `20` | `1.31` | `22R` | `-9.0R` | `3.80` |
| 2702 | AUDUSD | London | 15m | FADE_DOWN | RSI_D<35 | `58.9%` | 90 | `12` | `1.43` | `16R` | `-6.0R` | `3.80` |
| 2703 | NATGAS | NY | 30m | FADE_DOWN | RSI_D<35 | `58.9%` | 90 | `11` | `1.43` | `16R` | `-7.0R` | `3.80` |
| 2704 | VIX | NY Cash | 45m | FADE_UP | BtwLowClose | `58.9%` | 90 | `27` | `1.43` | `16R` | `-5.0R` | `3.80` |
| 2705 | GBPUSD | London | 15m | FADE_UP | OR_Q4_Wide | `55.3%` | 253 | `31` | `1.24` | `27R` | `-12.0R` | `3.79` |
| 2706 | XAGUSD | NY | 15m | FADE_UP | Thu | `57.0%` | 149 | `19` | `1.33` | `21R` | `-13.0R` | `3.79` |
| 2707 | NASDAQ100 | NY Cash | 45m | FADE_UP | OR_Q1_Tight | `57.0%` | 149 | `19` | `1.33` | `21R` | `-8.0R` | `3.79` |
| 2708 | AUDUSD | London | 15m | FADE_DOWN | Mon | `57.4%` | 136 | `17` | `1.34` | `20R` | `-7.0R` | `3.79` |
| 2709 | BRENT | NY | 45m | FADE_DOWN | OR_Q1_Tight | `56.1%` | 196 | `24` | `1.28` | `24R` | `-12.0R` | `3.79` |
| 2710 | WTI | NY Main | 15m | FADE_DOWN | Thu | `56.7%` | 164 | `20` | `1.31` | `22R` | `-9.0R` | `3.79` |
| 2711 | XAGUSD | London | 45m | FADE_UP | RSI>70 | `59.3%` | 81 | `11` | `1.45` | `15R` | `-8.0R` | `3.79` |
| 2712 | WTI | London Initial | 15m | SHAKEOUT_UP | RSI_30-50 | `59.3%` | 81 | `10` | `1.45` | `15R` | `-5.0R` | `3.79` |
| 2713 | BRENT | London | 15m | FADE_DOWN | Wed | `59.3%` | 81 | `10` | `1.45` | `15R` | `-5.0R` | `3.79` |
| 2714 | EURUSD | London | 15m | FADE_UP | AbovePD | `58.4%` | 101 | `13` | `1.40` | `17R` | `-8.0R` | `3.79` |
| 2715 | GBPUSD | NY | 45m | FADE_UP | Fri | `58.0%` | 112 | `14` | `1.38` | `18R` | `-6.0R` | `3.79` |
| 2716 | XAUUSD | London | 15m | FADE_UP | BelowPD | `58.0%` | 112 | `14` | `1.38` | `18R` | `-4.0R` | `3.79` |
| 2717 | USDJPY | Tokyo | 45m | FADE_DOWN | RSI_D<35 | `59.7%` | 72 | `9` | `1.48` | `14R` | `-3.0R` | `3.79` |
| 2718 | XAUUSD | NY | 60m | FADE_UP | Fri | `59.7%` | 72 | `9` | `1.48` | `14R` | `-6.0R` | `3.79` |
| 2719 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | BelowPD | `59.7%` | 72 | `9` | `1.48` | `14R` | `-3.0R` | `3.79` |
| 2720 | XAUUSD | London | 60m | FADE_UP | RSI_D>65 | `55.8%` | 215 | `27` | `1.26` | `25R` | `-9.0R` | `3.79` |
| 2721 | BRENT | NY | 30m | FADE_DOWN | OR_Q4_Wide | `56.1%` | 198 | `25` | `1.28` | `24R` | `-8.0R` | `3.78` |
| 2722 | USDJPY | Tokyo | 15m | FADE_UP | ATR-10% | `62.9%` | 35 | `5` | `1.69` | `9R` | `-4.0R` | `3.78` |
| 2723 | AUDUSD | Sydney | 60m | FADE_UP | RSI_50-70 | `62.9%` | 35 | `4` | `1.69` | `9R` | `-4.0R` | `3.78` |
| 2724 | GBPUSD | NY | 15m | FADE_DOWN | Fri | `57.0%` | 151 | `19` | `1.32` | `21R` | `-11.0R` | `3.78` |
| 2725 | GBPUSD | London | 30m | MOMENTUM_UP | ATR-10% | `56.7%` | 30 | `4` | `1.96` | `12R` | `-6.0R` | `3.78` |
| 2726 | USDJPY | Tokyo | 60m | FADE_DOWN | OR_Q1_Tight | `55.5%` | 238 | `31` | `1.25` | `26R` | `-8.0R` | `3.78` |
| 2727 | GBPJPY | London | 60m | FADE_UP | OR_Q1_Tight | `55.2%` | 261 | `33` | `1.23` | `27R` | `-10.0R` | `3.78` |
| 2728 | AUDUSD | London | 15m | FADE_DOWN | Wed | `57.2%` | 138 | `17` | `1.34` | `20R` | `-8.0R` | `3.78` |
| 2729 | GBPJPY | Tokyo | 30m | FADE_UP | RSI_D>65 | `57.2%` | 138 | `18` | `1.34` | `20R` | `-11.0R` | `3.78` |
| 2730 | WTI | NY Main | 45m | FADE_DOWN | Fri | `57.2%` | 138 | `17` | `1.34` | `20R` | `-12.0R` | `3.78` |
| 2731 | BRENT | NY | 60m | FADE_DOWN | AbovePD | `57.2%` | 138 | `17` | `1.34` | `20R` | `-10.0R` | `3.78` |
| 2732 | GBPUSD | NY | 30m | FADE_DOWN | BtwCloseHigh | `56.0%` | 200 | `25` | `1.27` | `24R` | `-6.0R` | `3.78` |
| 2733 | XAUUSD | London | 45m | FADE_DOWN | Tue | `56.0%` | 200 | `25` | `1.27` | `24R` | `-12.0R` | `3.78` |
| 2734 | USDJPY | Tokyo | 30m | FADE_UP | OR_Q4_Wide | `55.4%` | 242 | `30` | `1.24` | `26R` | `-9.0R` | `3.77` |
| 2735 | BRENT | NY | 45m | FADE_DOWN | BtwLowClose | `55.4%` | 242 | `30` | `1.24` | `26R` | `-8.0R` | `3.77` |
| 2736 | USDJPY | Tokyo | 30m | FADE_UP | Wed | `55.7%` | 221 | `27` | `1.26` | `25R` | `-11.0R` | `3.77` |
| 2737 | USDJPY | Tokyo | 45m | FADE_UP | Tue | `55.7%` | 221 | `27` | `1.26` | `25R` | `-13.0R` | `3.77` |
| 2738 | NATGAS | NY | 30m | FADE_UP | BelowPD | `56.5%` | 168 | `21` | `1.30` | `22R` | `-13.0R` | `3.77` |
| 2739 | GBPUSD | NY | 30m | FADE_DOWN | Thu | `56.9%` | 153 | `19` | `1.32` | `21R` | `-6.0R` | `3.77` |
| 2740 | VIX | NY Cash | 30m | FADE_UP | RSI_30-50 | `58.3%` | 103 | `31` | `1.40` | `17R` | `-8.0R` | `3.77` |
| 2741 | GBPJPY | Tokyo | 60m | FADE_UP | Wed | `55.9%` | 204 | `25` | `1.27` | `24R` | `-11.0R` | `3.76` |
| 2742 | GBPUSD | London | 15m | FADE_DOWN | RSI<30 | `57.5%` | 127 | `16` | `1.35` | `19R` | `-8.0R` | `3.76` |
| 2743 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | RSI_D>65 | `57.5%` | 127 | `16` | `1.35` | `19R` | `-5.0R` | `3.76` |
| 2744 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | Thu | `56.5%` | 170 | `21` | `1.30` | `22R` | `-7.0R` | `3.76` |
| 2745 | VIX | NY Cash | 15m | FADE_UP | BelowPD | `61.2%` | 49 | `15` | `1.58` | `11R` | `-3.0R` | `3.76` |
| 2746 | GBPAUD | London | 15m | FADE_UP | BtwCloseHigh | `56.1%` | 187 | `23` | `1.28` | `23R` | `-11.0R` | `3.76` |
| 2747 | AUDUSD | London | 45m | FADE_DOWN | ATR+10% | `61.9%` | 42 | `5` | `1.62` | `10R` | `-3.0R` | `3.76` |
| 2748 | EURJPY | London | 30m | FADE_UP | ATR+10% | `61.9%` | 42 | `5` | `1.62` | `10R` | `-5.0R` | `3.76` |
| 2749 | SP500 | Pre-Market | 15m | FADE_DOWN | ATR+10% | `61.9%` | 42 | `5` | `1.62` | `10R` | `-6.0R` | `3.76` |
| 2750 | GBPUSD | NY | 30m | FADE_DOWN | RSI<30 | `60.0%` | 65 | `8` | `1.50` | `13R` | `-6.0R` | `3.76` |
| 2751 | XAUUSD | NY | 30m | FADE_DOWN | RSI<30 | `60.0%` | 65 | `8` | `1.50` | `13R` | `-5.0R` | `3.76` |
| 2752 | NASDAQ100 | Pre-Market | 15m | FADE_UP | Mon | `60.0%` | 65 | `8` | `1.50` | `13R` | `-6.0R` | `3.76` |
| 2753 | GBPUSD | NY | 30m | FADE_UP | OR_Q1_Tight | `56.1%` | 189 | `23` | `1.28` | `23R` | `-13.0R` | `3.75` |
| 2754 | XAUUSD | London | 15m | FADE_DOWN | Thu | `57.8%` | 116 | `14` | `1.37` | `18R` | `-10.0R` | `3.75` |
| 2755 | XAGUSD | NY | 15m | FADE_DOWN | Thu | `57.0%` | 142 | `18` | `1.33` | `20R` | `-7.0R` | `3.75` |
| 2756 | VIX | NY Cash | 30m | FADE_UP | BtwCloseHigh | `59.5%` | 74 | `22` | `1.47` | `14R` | `-6.0R` | `3.75` |
| 2757 | SP500 | Pre-Market | 60m | FADE_UP | OR_Q1_Tight | `56.7%` | 157 | `20` | `1.31` | `21R` | `-10.0R` | `3.75` |
| 2758 | BRENT | London | 60m | FADE_DOWN | AbovePD | `57.4%` | 129 | `16` | `1.35` | `19R` | `-7.0R` | `3.75` |
| 2759 | SP500 | NY Cash | 60m | FADE_DOWN | OR_Q4_Wide | `58.5%` | 94 | `12` | `1.41` | `16R` | `-4.0R` | `3.75` |
| 2760 | EURUSD | London | 45m | FADE_DOWN | RSI_D>65 | `58.1%` | 105 | `13` | `1.39` | `17R` | `-8.0R` | `3.75` |
| 2761 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | BelowPD | `58.1%` | 105 | `13` | `1.39` | `17R` | `-8.0R` | `3.75` |
| 2762 | GBPAUD | London | 45m | FADE_UP | AbovePD | `56.3%` | 174 | `23` | `1.29` | `22R` | `-10.0R` | `3.75` |
| 2763 | NASDAQ100 | Pre-Market | 45m | FADE_UP | Thu | `56.3%` | 174 | `22` | `1.29` | `22R` | `-6.0R` | `3.75` |
| 2764 | GBPJPY | London | 30m | MOMENTUM_UP | RSI<30 | `55.9%` | 34 | `5` | `1.90` | `14R` | `-3.0R` | `3.74` |
| 2765 | EURJPY | London | 15m | MOMENTUM_DOWN | RSI>70 | `55.9%` | 34 | `5` | `1.90` | `14R` | `-4.0R` | `3.74` |
| 2766 | BRENT | London | 15m | MOMENTUM_DOWN | RSI<30 | `55.9%` | 34 | `5` | `1.90` | `14R` | `-3.0R` | `3.74` |
| 2767 | XAUUSD | NY | 30m | FADE_UP | Tue | `56.9%` | 144 | `18` | `1.32` | `20R` | `-10.0R` | `3.74` |
| 2768 | EURUSD | NY | 30m | FADE_DOWN | BelowPD | `56.6%` | 159 | `20` | `1.30` | `21R` | `-8.0R` | `3.74` |
| 2769 | USDJPY | Tokyo | 30m | FADE_DOWN | OR_Q1_Tight | `56.2%` | 176 | `28` | `1.29` | `22R` | `-7.0R` | `3.74` |
| 2770 | USDJPY | NY | 30m | FADE_UP | BelowPD | `57.3%` | 131 | `16` | `1.34` | `19R` | `-7.0R` | `3.74` |
| 2771 | WTI | NY Main | 15m | FADE_UP | RSI_D>65 | `57.3%` | 131 | `16` | `1.34` | `19R` | `-6.0R` | `3.74` |
| 2772 | BRENT | London | 15m | FADE_DOWN | OR_Q4_Wide | `55.9%` | 195 | `24` | `1.27` | `23R` | `-11.0R` | `3.74` |
| 2773 | USDJPY | NY | 45m | FADE_UP | BtwCloseHigh | `56.5%` | 161 | `20` | `1.30` | `21R` | `-10.0R` | `3.73` |
| 2774 | XAUUSD | London | 60m | FADE_DOWN | RSI_D>65 | `56.5%` | 161 | `20` | `1.30` | `21R` | `-12.0R` | `3.73` |
| 2775 | NATGAS | NY | 30m | FADE_DOWN | Wed | `56.5%` | 161 | `20` | `1.30` | `21R` | `-7.0R` | `3.73` |
| 2776 | GBPJPY | London | 45m | FADE_DOWN | RSI_D<35 | `58.8%` | 85 | `12` | `1.43` | `15R` | `-7.0R` | `3.73` |
| 2777 | BRENT | London | 15m | FADE_DOWN | BtwLowClose | `56.8%` | 146 | `18` | `1.32` | `20R` | `-6.0R` | `3.73` |
| 2778 | BRENT | NY | 15m | FADE_UP | Wed | `56.8%` | 146 | `18` | `1.32` | `20R` | `-12.0R` | `3.73` |
| 2779 | EURUSD | London | 30m | FADE_DOWN | Wed | `56.2%` | 178 | `22` | `1.28` | `22R` | `-11.0R` | `3.73` |
| 2780 | XAGUSD | London | 30m | FADE_UP | Wed | `56.2%` | 178 | `22` | `1.28` | `22R` | `-8.0R` | `3.73` |
| 2781 | XAGUSD | NY | 15m | FADE_DOWN | OR_Q1_Tight | `56.2%` | 178 | `27` | `1.28` | `22R` | `-7.0R` | `3.73` |
| 2782 | AUDUSD | London | 45m | FADE_DOWN | OR_Q1_Tight | `55.2%` | 241 | `31` | `1.23` | `25R` | `-12.0R` | `3.73` |
| 2783 | WTI | NY Main | 30m | FADE_UP | Tue | `56.4%` | 163 | `20` | `1.30` | `21R` | `-11.0R` | `3.73` |
| 2784 | SP500 | NY Cash | 45m | FADE_DOWN | OR_Q4_Wide | `57.5%` | 120 | `15` | `1.35` | `18R` | `-5.0R` | `3.72` |
| 2785 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | Thu | `57.5%` | 120 | `15` | `1.35` | `18R` | `-6.0R` | `3.72` |
| 2786 | WTI | NY Main | 30m | FADE_DOWN | BtwLowClose | `55.1%` | 243 | `30` | `1.23` | `25R` | `-7.0R` | `3.72` |
| 2787 | BRENT | NY | 30m | FADE_UP | BtwLowClose | `55.1%` | 243 | `30` | `1.23` | `25R` | `-7.0R` | `3.72` |
| 2788 | NASDAQ100 | NY Cash | 15m | FADE_UP | BtwCloseHigh | `55.1%` | 243 | `30` | `1.23` | `25R` | `-11.0R` | `3.72` |
| 2789 | WTI | London Initial | 45m | FADE_DOWN | RSI_D<35 | `59.2%` | 76 | `10` | `1.45` | `14R` | `-3.0R` | `3.72` |
| 2790 | GBPUSD | NY | 15m | FADE_UP | ATR+10% | `63.3%` | 30 | `4` | `1.73` | `8R` | `-3.0R` | `3.72` |
| 2791 | XAUUSD | NY | 45m | FADE_DOWN | ATR+10% | `63.3%` | 30 | `4` | `1.73` | `8R` | `-3.0R` | `3.72` |
| 2792 | SP500 | Pre-Market | 45m | FADE_UP | ATR-10% | `63.3%` | 30 | `4` | `1.73` | `8R` | `-2.0R` | `3.72` |
| 2793 | XAUUSD | London | 60m | FADE_UP | RSI_D<35 | `59.7%` | 67 | `9` | `1.48` | `13R` | `-7.0R` | `3.72` |
| 2794 | VIX | NY Cash | 45m | FADE_DOWN | BtwCloseHigh | `59.7%` | 67 | `20` | `1.48` | `13R` | `-5.0R` | `3.72` |
| 2795 | GBPAUD | London | 30m | FADE_UP | Fri | `56.0%` | 182 | `22` | `1.27` | `22R` | `-11.0R` | `3.72` |
| 2796 | EURJPY | London | 30m | FADE_UP | OR_Q1_Tight | `55.4%` | 224 | `28` | `1.24` | `24R` | `-10.0R` | `3.71` |
| 2797 | EURJPY | Tokyo | 15m | FADE_DOWN | Tue | `56.7%` | 150 | `19` | `1.31` | `20R` | `-6.0R` | `3.71` |
| 2798 | EURUSD | London | 60m | FADE_DOWN | Wed | `56.0%` | 184 | `23` | `1.27` | `22R` | `-8.0R` | `3.71` |
| 2799 | GBPUSD | London | 45m | FADE_UP | Tue | `56.0%` | 184 | `23` | `1.27` | `22R` | `-10.0R` | `3.71` |
| 2800 | USDJPY | Tokyo | 15m | FADE_UP | Wed | `56.0%` | 184 | `23` | `1.27` | `22R` | `-7.0R` | `3.71` |
| 2801 | GBPAUD | London | 60m | FADE_UP | Mon | `56.0%` | 184 | `23` | `1.27` | `22R` | `-5.0R` | `3.71` |
| 2802 | WTI | London Initial | 60m | FADE_UP | Tue | `56.0%` | 184 | `23` | `1.27` | `22R` | `-12.0R` | `3.71` |
| 2803 | XAGUSD | London | 15m | FADE_DOWN | BelowPD | `58.6%` | 87 | `11` | `1.42` | `15R` | `-4.0R` | `3.71` |
| 2804 | WTI | London Initial | 15m | SHAKEOUT_UP | BtwCloseHigh | `58.6%` | 87 | `11` | `1.42` | `15R` | `-7.0R` | `3.71` |
| 2805 | GBPAUD | London | 45m | FADE_DOWN | RSI<30 | `58.2%` | 98 | `12` | `1.39` | `16R` | `-6.0R` | `3.71` |
| 2806 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | OR_Q4_Wide | `58.2%` | 98 | `16` | `1.39` | `16R` | `-8.0R` | `3.71` |
| 2807 | GBPJPY | Tokyo | 60m | FADE_UP | OR_Q1_Tight | `55.3%` | 228 | `28` | `1.24` | `24R` | `-13.0R` | `3.71` |
| 2808 | BRENT | London | 15m | SHAKEOUT_DOWN | Mon | `60.8%` | 51 | `6` | `1.55` | `11R` | `-6.0R` | `3.70` |
| 2809 | GBPJPY | Tokyo | 30m | FADE_DOWN | Fri | `56.6%` | 152 | `19` | `1.30` | `20R` | `-7.0R` | `3.70` |
| 2810 | EURJPY | London | 30m | FADE_UP | BelowPD | `56.6%` | 152 | `19` | `1.30` | `20R` | `-7.0R` | `3.70` |
| 2811 | EURJPY | Tokyo | 45m | FADE_UP | OR_Q1_Tight | `55.2%` | 230 | `29` | `1.23` | `24R` | `-6.0R` | `3.70` |
| 2812 | USDJPY | Tokyo | 60m | FADE_DOWN | Wed | `56.2%` | 169 | `21` | `1.28` | `21R` | `-5.0R` | `3.70` |
| 2813 | EURUSD | London | 45m | FADE_UP | Mon | `55.9%` | 188 | `23` | `1.27` | `22R` | `-9.0R` | `3.70` |
| 2814 | WTI | NY Main | 60m | FADE_DOWN | OR_Q1_Tight | `55.5%` | 209 | `26` | `1.25` | `23R` | `-6.0R` | `3.70` |
| 2815 | GBPJPY | London | 30m | FADE_DOWN | BelowPD | `57.7%` | 111 | `14` | `1.36` | `17R` | `-5.0R` | `3.70` |
| 2816 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | RSI_D>65 | `57.7%` | 111 | `14` | `1.36` | `17R` | `-7.0R` | `3.70` |
| 2817 | XAUUSD | London | 30m | FADE_DOWN | Fri | `56.5%` | 154 | `19` | `1.30` | `20R` | `-8.0R` | `3.69` |
| 2818 | XAUUSD | London | 60m | FADE_DOWN | Thu | `55.8%` | 190 | `23` | `1.26` | `22R` | `-6.0R` | `3.69` |
| 2819 | USDJPY | NY | 15m | FADE_DOWN | AbovePD | `56.8%` | 139 | `17` | `1.32` | `19R` | `-7.0R` | `3.69` |
| 2820 | EURJPY | London | 45m | FADE_UP | RSI>70 | `58.0%` | 100 | `12` | `1.38` | `16R` | `-5.0R` | `3.69` |
| 2821 | USDJPY | NY | 45m | FADE_UP | OR_Q1_Tight | `55.7%` | 192 | `24` | `1.26` | `22R` | `-9.0R` | `3.69` |
| 2822 | AUDUSD | London | 45m | FADE_UP | Wed | `55.7%` | 192 | `24` | `1.26` | `22R` | `-8.0R` | `3.69` |
| 2823 | NASDAQ100 | NY Cash | 30m | FADE_UP | AbovePD+RSI_D>65 | `61.4%` | 44 | `6` | `1.59` | `10R` | `-3.0R` | `3.69` |
| 2824 | VIX | NY Cash | 45m | FADE_DOWN | Mon | `61.4%` | 44 | `13` | `1.59` | `10R` | `-4.0R` | `3.69` |
| 2825 | XAUUSD | London | 45m | FADE_UP | ATR-10% | `62.2%` | 37 | `5` | `1.64` | `9R` | `-2.0R` | `3.69` |
| 2826 | XAUUSD | NY | 45m | FADE_UP | RSI_D<35 | `62.2%` | 37 | `5` | `1.64` | `9R` | `-3.0R` | `3.69` |
| 2827 | VIX | NY Cash | 45m | FADE_UP | AbovePD | `62.2%` | 37 | `12` | `1.64` | `9R` | `-3.0R` | `3.69` |
| 2828 | GBPUSD | London | 15m | FADE_DOWN | Fri | `56.4%` | 156 | `19` | `1.29` | `20R` | `-16.0R` | `3.69` |
| 2829 | SP500 | NY Cash | 45m | FADE_DOWN | RSI<30 | `58.4%` | 89 | `11` | `1.41` | `15R` | `-4.0R` | `3.69` |
| 2830 | SP500 | NY Cash | 15m | FADE_DOWN | BelowPD | `57.1%` | 126 | `16` | `1.33` | `18R` | `-5.0R` | `3.68` |
| 2831 | XAGUSD | London | 15m | SHAKEOUT_UP | RSI_D>65 | `59.4%` | 69 | `9` | `1.46` | `13R` | `-4.0R` | `3.68` |
| 2832 | XAGUSD | NY | 60m | FADE_DOWN | Thu | `59.4%` | 69 | `8` | `1.46` | `13R` | `-6.0R` | `3.68` |
| 2833 | EURUSD | NY | 30m | FADE_DOWN | BtwCloseHigh | `55.7%` | 194 | `24` | `1.26` | `22R` | `-10.0R` | `3.68` |
| 2834 | XAUUSD | NY | 60m | FADE_DOWN | BtwLowClose | `57.5%` | 113 | `14` | `1.35` | `17R` | `-4.0R` | `3.68` |
| 2835 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | Wed | `57.5%` | 113 | `14` | `1.35` | `17R` | `-7.0R` | `3.68` |
| 2836 | VIX | NY Cash | 15m | FADE_UP | GapSmall | `55.9%` | 177 | `52` | `1.27` | `21R` | `-8.0R` | `3.67` |
| 2837 | XAUUSD | NY | 30m | FADE_DOWN | Mon | `57.0%` | 128 | `16` | `1.33` | `18R` | `-10.0R` | `3.67` |
| 2838 | XAUUSD | London | 15m | SHAKEOUT_UP | RSI_30-50 | `56.6%` | 143 | `18` | `1.31` | `19R` | `-6.0R` | `3.67` |
| 2839 | GBPAUD | London | 30m | FADE_DOWN | RSI_D>65 | `57.8%` | 102 | `13` | `1.37` | `16R` | `-4.0R` | `3.67` |
| 2840 | XAUUSD | London | 30m | FADE_UP | Thu | `55.9%` | 179 | `23` | `1.27` | `21R` | `-12.0R` | `3.67` |
| 2841 | EURUSD | NY | 30m | FADE_DOWN | OR_Q4_Wide | `57.4%` | 115 | `14` | `1.35` | `17R` | `-8.0R` | `3.67` |
| 2842 | WTI | London Initial | 15m | FADE_DOWN | Tue | `57.4%` | 115 | `14` | `1.35` | `17R` | `-10.0R` | `3.67` |
| 2843 | USDJPY | NY | 60m | FADE_DOWN | Fri | `58.8%` | 80 | `10` | `1.42` | `14R` | `-8.0R` | `3.67` |
| 2844 | EURUSD | NY | 60m | FADE_UP | Mon | `58.2%` | 91 | `11` | `1.39` | `15R` | `-6.0R` | `3.66` |
| 2845 | NASDAQ100 | NY Cash | 30m | FADE_UP | Fri | `56.9%` | 130 | `16` | `1.32` | `18R` | `-7.0R` | `3.66` |
| 2846 | WTI | NY Main | 15m | FADE_DOWN | OR_Q4_Wide | `55.1%` | 227 | `29` | `1.23` | `23R` | `-9.0R` | `3.66` |
| 2847 | EURUSD | NY | 30m | FADE_DOWN | BtwLowClose | `55.4%` | 204 | `25` | `1.24` | `22R` | `-11.0R` | `3.66` |
| 2848 | GBPJPY | London | 30m | FADE_UP | Tue | `55.7%` | 183 | `23` | `1.26` | `21R` | `-11.0R` | `3.66` |
| 2849 | EURJPY | Tokyo | 45m | FADE_DOWN | Fri | `56.1%` | 164 | `20` | `1.28` | `20R` | `-7.0R` | `3.66` |
| 2850 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | RSI_30-50 | `57.3%` | 117 | `14` | `1.34` | `17R` | `-7.0R` | `3.65` |
| 2851 | GBPUSD | NY | 30m | FADE_DOWN | Tue | `56.5%` | 147 | `18` | `1.30` | `19R` | `-7.0R` | `3.65` |
| 2852 | XAUUSD | London | 60m | FADE_DOWN | OR_Q4_Wide | `55.3%` | 206 | `31` | `1.24` | `22R` | `-10.0R` | `3.65` |
| 2853 | SP500 | NY Cash | 15m | FADE_UP | ATR+10% | `60.4%` | 53 | `7` | `1.52` | `11R` | `-6.0R` | `3.65` |
| 2854 | WTI | NY Main | 15m | FADE_DOWN | RSI_D<35 | `59.2%` | 71 | `9` | `1.45` | `13R` | `-5.0R` | `3.65` |
| 2855 | USDJPY | NY | 30m | FADE_DOWN | Thu | `56.8%` | 132 | `16` | `1.32` | `18R` | `-6.0R` | `3.65` |
| 2856 | GBPUSD | London | 45m | FADE_UP | OR_Q4_Wide | `55.3%` | 208 | `25` | `1.24` | `22R` | `-10.0R` | `3.65` |
| 2857 | EURJPY | London | 30m | FADE_DOWN | AbovePD | `56.0%` | 166 | `21` | `1.27` | `20R` | `-9.0R` | `3.65` |
| 2858 | AUDUSD | London | 15m | FADE_UP | RSI>70 | `59.7%` | 62 | `8` | `1.48` | `12R` | `-3.0R` | `3.65` |
| 2859 | WTI | London Initial | 15m | FADE_DOWN | BtwCloseHigh | `56.0%` | 168 | `21` | `1.27` | `20R` | `-5.0R` | `3.64` |
| 2860 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | Tue | `56.0%` | 168 | `21` | `1.27` | `20R` | `-16.0R` | `3.64` |
| 2861 | EURUSD | London | 60m | FADE_DOWN | BelowPD | `58.5%` | 82 | `10` | `1.41` | `14R` | `-5.0R` | `3.64` |
| 2862 | GBPJPY | Tokyo | 60m | FADE_DOWN | RSI_D<35 | `58.5%` | 82 | `12` | `1.41` | `14R` | `-5.0R` | `3.64` |
| 2863 | XAUUSD | NY | 60m | FADE_DOWN | Tue | `58.5%` | 82 | `10` | `1.41` | `14R` | `-4.0R` | `3.64` |
| 2864 | GBPUSD | NY | 15m | FADE_UP | BtwCloseHigh | `55.6%` | 189 | `23` | `1.25` | `21R` | `-12.0R` | `3.64` |
| 2865 | GBPUSD | London | 15m | FADE_DOWN | Thu | `56.3%` | 151 | `19` | `1.29` | `19R` | `-5.0R` | `3.64` |
| 2866 | GBPJPY | London | 15m | FADE_UP | AbovePD | `56.3%` | 151 | `19` | `1.29` | `19R` | `-8.0R` | `3.64` |
| 2867 | GBPJPY | London | 15m | FADE_DOWN | Thu | `56.3%` | 151 | `18` | `1.29` | `19R` | `-8.0R` | `3.64` |
| 2868 | XAUUSD | London | 60m | FADE_DOWN | Tue | `55.5%` | 191 | `23` | `1.25` | `21R` | `-12.0R` | `3.64` |
| 2869 | XAUUSD | NY | 15m | FADE_UP | AbovePD | `55.0%` | 218 | `27` | `1.22` | `22R` | `-8.0R` | `3.63` |
| 2870 | USDJPY | NY | 45m | FADE_UP | Mon | `57.0%` | 121 | `15` | `1.33` | `17R` | `-14.0R` | `3.63` |
| 2871 | XAGUSD | NY | 30m | FADE_UP | Fri | `57.0%` | 121 | `15` | `1.33` | `17R` | `-11.0R` | `3.63` |
| 2872 | SP500 | NY Cash | 60m | FADE_DOWN | RSI_D>65 | `57.0%` | 121 | `16` | `1.33` | `17R` | `-6.0R` | `3.63` |
| 2873 | XAUUSD | NY | 30m | FADE_DOWN | BtwCloseHigh | `55.4%` | 195 | `24` | `1.24` | `21R` | `-8.0R` | `3.63` |
| 2874 | GBPJPY | London | 15m | FADE_UP | ATR+10% | `60.9%` | 46 | `7` | `1.56` | `10R` | `-3.0R` | `3.63` |
| 2875 | XAGUSD | London | 60m | FADE_UP | ATR-10% | `60.9%` | 46 | `6` | `1.56` | `10R` | `-4.0R` | `3.63` |
| 2876 | GBPUSD | London | 15m | SHAKEOUT_UP | Fri | `57.9%` | 95 | `12` | `1.38` | `15R` | `-11.0R` | `3.63` |
| 2877 | NASDAQ100 | NY Cash | 15m | FADE_UP | Wed | `56.1%` | 155 | `19` | `1.28` | `19R` | `-6.0R` | `3.62` |
| 2878 | WTI | NY Main | 60m | FADE_DOWN | BtwCloseHigh | `55.3%` | 197 | `24` | `1.24` | `21R` | `-8.0R` | `3.62` |
| 2879 | GBPAUD | London | 30m | FADE_DOWN | RSI_D<35 | `58.3%` | 84 | `11` | `1.40` | `14R` | `-6.0R` | `3.62` |
| 2880 | GBPJPY | Tokyo | 15m | FADE_DOWN | Fri | `56.9%` | 123 | `15` | `1.32` | `17R` | `-9.0R` | `3.62` |
| 2881 | USDJPY | NY | 15m | FADE_UP | BtwLowClose | `55.6%` | 178 | `22` | `1.25` | `20R` | `-13.0R` | `3.61` |
| 2882 | EURJPY | Tokyo | 30m | FADE_UP | Mon | `55.6%` | 178 | `22` | `1.25` | `20R` | `-7.0R` | `3.61` |
| 2883 | GBPUSD | London | 45m | FADE_DOWN | ATR-10% | `62.5%` | 32 | `4` | `1.67` | `8R` | `-3.0R` | `3.61` |
| 2884 | XAGUSD | NY | 45m | FADE_UP | AbovePD+RSI_D>65 | `62.5%` | 32 | `4` | `1.67` | `8R` | `-3.0R` | `3.61` |
| 2885 | NASDAQ100 | Pre-Market | 45m | SHAKEOUT_DOWN | RSI_D<35 | `62.5%` | 32 | `4` | `1.67` | `8R` | `-2.0R` | `3.61` |
| 2886 | GBPUSD | NY | 45m | FADE_DOWN | RSI_D>65 | `59.4%` | 64 | `8` | `1.46` | `12R` | `-3.0R` | `3.61` |
| 2887 | EURJPY | Tokyo | 60m | FADE_DOWN | RSI<30 | `59.4%` | 64 | `8` | `1.46` | `12R` | `-6.0R` | `3.61` |
| 2888 | XAGUSD | London | 15m | SHAKEOUT_DOWN | AbovePD | `59.4%` | 64 | `8` | `1.46` | `12R` | `-5.0R` | `3.61` |
| 2889 | WTI | NY Main | 45m | FADE_UP | RSI_D<35 | `59.4%` | 64 | `8` | `1.46` | `12R` | `-6.0R` | `3.61` |
| 2890 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | Mon | `59.4%` | 64 | `8` | `1.46` | `12R` | `-4.0R` | `3.61` |
| 2891 | EURJPY | London | 15m | FADE_UP | Wed | `56.0%` | 159 | `20` | `1.27` | `19R` | `-9.0R` | `3.61` |
| 2892 | WTI | NY Main | 30m | FADE_DOWN | Thu | `56.0%` | 159 | `20` | `1.27` | `19R` | `-14.0R` | `3.61` |
| 2893 | EURJPY | London | 60m | FADE_UP | RSI>70 | `57.7%` | 97 | `12` | `1.37` | `15R` | `-8.0R` | `3.61` |
| 2894 | NATGAS | NY | 60m | FADE_UP | Mon | `57.7%` | 97 | `12` | `1.37` | `15R` | `-7.0R` | `3.61` |
| 2895 | EURJPY | Tokyo | 45m | FADE_UP | ATR+10% | `61.5%` | 39 | `5` | `1.60` | `9R` | `-3.0R` | `3.61` |
| 2896 | SP500 | NY Cash | 45m | FADE_UP | RSI_D<35 | `61.5%` | 39 | `5` | `1.60` | `9R` | `-3.0R` | `3.61` |
| 2897 | XAUUSD | London | 15m | FADE_UP | RSI_D<35 | `60.0%` | 55 | `7` | `1.50` | `11R` | `-7.0R` | `3.61` |
| 2898 | WTI | London Initial | 15m | SHAKEOUT_UP | Fri | `60.0%` | 55 | `7` | `1.50` | `11R` | `-3.0R` | `3.61` |
| 2899 | SP500 | Pre-Market | 15m | SHAKEOUT_UP | BelowPD | `60.0%` | 55 | `7` | `1.50` | `11R` | `-6.0R` | `3.61` |
| 2900 | EURJPY | London | 30m | FADE_DOWN | RSI_D>65 | `56.8%` | 125 | `17` | `1.31` | `17R` | `-6.0R` | `3.61` |
| 2901 | AUDUSD | London | 60m | FADE_DOWN | AbovePD | `55.1%` | 205 | `25` | `1.23` | `21R` | `-11.0R` | `3.60` |
| 2902 | XAUUSD | London | 15m | FADE_DOWN | RSI_50-70 | `55.1%` | 205 | `25` | `1.23` | `21R` | `-10.0R` | `3.60` |
| 2903 | AUDUSD | London | 60m | FADE_DOWN | RSI_D>65 | `58.1%` | 86 | `11` | `1.39` | `14R` | `-4.0R` | `3.60` |
| 2904 | XAUUSD | NY | 45m | FADE_UP | RSI_D>65 | `56.7%` | 127 | `16` | `1.31` | `17R` | `-7.0R` | `3.60` |
| 2905 | SP500 | Pre-Market | 15m | FADE_UP | Fri | `58.7%` | 75 | `9` | `1.42` | `13R` | `-6.0R` | `3.60` |
| 2906 | SP500 | NY Cash | 30m | FADE_UP | BelowPD | `57.1%` | 112 | `14` | `1.33` | `16R` | `-6.0R` | `3.60` |
| 2907 | BRENT | NY | 45m | FADE_DOWN | Tue | `56.2%` | 144 | `18` | `1.29` | `18R` | `-10.0R` | `3.59` |
| 2908 | NASDAQ100 | NY Cash | 15m | FADE_UP | Mon | `56.2%` | 144 | `18` | `1.29` | `18R` | `-10.0R` | `3.59` |
| 2909 | NASDAQ100 | NY Cash | 15m | FADE_UP | Thu | `56.2%` | 144 | `18` | `1.29` | `18R` | `-13.0R` | `3.59` |
| 2910 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | Tue | `56.2%` | 144 | `18` | `1.29` | `18R` | `-9.0R` | `3.59` |
| 2911 | EURJPY | Tokyo | 45m | FADE_DOWN | Thu | `55.4%` | 186 | `23` | `1.24` | `20R` | `-8.0R` | `3.59` |
| 2912 | WTI | London Initial | 60m | FADE_UP | Wed | `55.4%` | 186 | `23` | `1.24` | `20R` | `-7.0R` | `3.59` |
| 2913 | USDJPY | NY | 45m | FADE_DOWN | Fri | `57.6%` | 99 | `12` | `1.36` | `15R` | `-8.0R` | `3.59` |
| 2914 | EURJPY | London | 15m | FADE_UP | RSI>70 | `57.6%` | 99 | `12` | `1.36` | `15R` | `-6.0R` | `3.59` |
| 2915 | XAGUSD | London | 30m | FADE_DOWN | Wed | `55.8%` | 165 | `21` | `1.26` | `19R` | `-8.0R` | `3.59` |
| 2916 | EURUSD | NY | 30m | FADE_UP | AbovePD | `55.3%` | 188 | `23` | `1.24` | `20R` | `-12.0R` | `3.59` |
| 2917 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | BtwLowClose | `57.0%` | 114 | `14` | `1.33` | `16R` | `-4.0R` | `3.58` |
| 2918 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | RSI<30 | `57.0%` | 114 | `14` | `1.33` | `16R` | `-11.0R` | `3.58` |
| 2919 | AUDUSD | London | 60m | FADE_UP | Wed | `55.3%` | 190 | `23` | `1.24` | `20R` | `-12.0R` | `3.58` |
| 2920 | BRENT | NY | 15m | FADE_DOWN | Tue | `55.7%` | 167 | `21` | `1.26` | `19R` | `-7.0R` | `3.58` |
| 2921 | SP500 | Pre-Market | 45m | FADE_UP | Wed | `55.7%` | 167 | `21` | `1.26` | `19R` | `-5.0R` | `3.58` |
| 2922 | EURJPY | Tokyo | 15m | FADE_UP | Mon | `56.1%` | 148 | `18` | `1.28` | `18R` | `-11.0R` | `3.58` |
| 2923 | SP500 | NY Cash | 15m | FADE_DOWN | Fri | `56.1%` | 148 | `18` | `1.28` | `18R` | `-7.0R` | `3.58` |
| 2924 | BRENT | London | 45m | FADE_UP | RSI>70 | `58.0%` | 88 | `11` | `1.38` | `14R` | `-7.0R` | `3.58` |
| 2925 | GBPAUD | London | 15m | SHAKEOUT_UP | RSI_30-50 | `55.6%` | 169 | `21` | `1.25` | `19R` | `-9.0R` | `3.58` |
| 2926 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | BelowPD | `59.1%` | 66 | `8` | `1.44` | `12R` | `-5.0R` | `3.58` |
| 2927 | USDJPY | NY | 15m | FADE_UP | BelowPD | `56.5%` | 131 | `16` | `1.30` | `17R` | `-7.0R` | `3.58` |
| 2928 | USDJPY | NY | 60m | FADE_DOWN | BtwCloseHigh | `56.5%` | 131 | `16` | `1.30` | `17R` | `-6.0R` | `3.58` |
| 2929 | XAGUSD | NY | 45m | FADE_DOWN | BtwCloseHigh | `56.5%` | 131 | `16` | `1.30` | `17R` | `-12.0R` | `3.58` |
| 2930 | GBPJPY | Tokyo | 15m | FADE_UP | RSI_D>65 | `57.4%` | 101 | `13` | `1.35` | `15R` | `-9.0R` | `3.57` |
| 2931 | WTI | London Initial | 60m | SHAKEOUT_UP | OR_Q1_Tight | `57.4%` | 101 | `13` | `1.35` | `15R` | `-6.0R` | `3.57` |
| 2932 | AUDUSD | London | 30m | FADE_DOWN | Tue | `55.2%` | 194 | `24` | `1.23` | `20R` | `-10.0R` | `3.57` |
| 2933 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | BtwLowClose | `56.9%` | 116 | `14` | `1.32` | `16R` | `-8.0R` | `3.57` |
| 2934 | BRENT | London | 45m | FADE_DOWN | RSI<30 | `58.4%` | 77 | `10` | `1.41` | `13R` | `-11.0R` | `3.57` |
| 2935 | SP500 | NY Cash | 30m | FADE_UP | ATR+10% | `60.4%` | 48 | `6` | `1.53` | `10R` | `-5.0R` | `3.57` |
| 2936 | NASDAQ100 | Pre-Market | 60m | FADE_UP | BelowPD | `56.4%` | 133 | `17` | `1.29` | `17R` | `-5.0R` | `3.57` |
| 2937 | USDJPY | Tokyo | 30m | FADE_DOWN | Tue | `55.5%` | 173 | `21` | `1.25` | `19R` | `-6.0R` | `3.57` |
| 2938 | EURJPY | Tokyo | 60m | FADE_UP | Tue | `55.0%` | 200 | `25` | `1.22` | `20R` | `-7.0R` | `3.56` |
| 2939 | GBPUSD | London | 60m | FADE_UP | RSI>70 | `57.3%` | 103 | `13` | `1.34` | `15R` | `-7.0R` | `3.56` |
| 2940 | XAGUSD | London | 30m | FADE_DOWN | BelowPD | `56.8%` | 118 | `15` | `1.31` | `16R` | `-7.0R` | `3.56` |
| 2941 | EURUSD | NY | 30m | FADE_DOWN | Tue | `55.8%` | 154 | `19` | `1.26` | `18R` | `-10.0R` | `3.56` |
| 2942 | GBPUSD | NY | 45m | FADE_UP | BelowPD | `56.3%` | 135 | `17` | `1.29` | `17R` | `-13.0R` | `3.56` |
| 2943 | USDJPY | NY | 60m | FADE_UP | AbovePD | `56.3%` | 135 | `17` | `1.29` | `17R` | `-5.0R` | `3.56` |
| 2944 | BRENT | London | 30m | FADE_UP | Tue | `56.3%` | 135 | `17` | `1.29` | `17R` | `-8.0R` | `3.56` |
| 2945 | NATGAS | NY | 15m | FADE_DOWN | AbovePD | `55.4%` | 177 | `22` | `1.24` | `19R` | `-6.0R` | `3.56` |
| 2946 | USDJPY | NY | 30m | FADE_DOWN | AbovePD | `55.8%` | 156 | `19` | `1.26` | `18R` | `-9.0R` | `3.55` |
| 2947 | AUDUSD | London | 15m | FADE_UP | Fri | `56.2%` | 137 | `17` | `1.28` | `17R` | `-7.0R` | `3.55` |
| 2948 | SP500 | Pre-Market | 60m | FADE_UP | BelowPD | `56.2%` | 137 | `17` | `1.28` | `17R` | `-11.0R` | `3.55` |
| 2949 | XAUUSD | London | 15m | FADE_UP | Fri | `56.7%` | 120 | `15` | `1.31` | `16R` | `-6.0R` | `3.55` |
| 2950 | EURJPY | Tokyo | 45m | FADE_UP | RSI>70 | `58.2%` | 79 | `10` | `1.39` | `13R` | `-6.0R` | `3.55` |
| 2951 | AUDUSD | London | 60m | FADE_DOWN | RSI_D<35 | `57.1%` | 105 | `14` | `1.33` | `15R` | `-10.0R` | `3.55` |
| 2952 | XAGUSD | London | 15m | SHAKEOUT_DOWN | OR_Q1_Tight | `58.8%` | 68 | `33` | `1.43` | `12R` | `-6.0R` | `3.55` |
| 2953 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | BtwLowClose | `58.8%` | 68 | `8` | `1.43` | `12R` | `-4.0R` | `3.55` |
| 2954 | GBPJPY | London | 45m | FADE_DOWN | Thu | `55.2%` | 181 | `22` | `1.23` | `19R` | `-13.0R` | `3.55` |
| 2955 | GBPJPY | London | 30m | FADE_DOWN | Thu | `55.2%` | 183 | `22` | `1.23` | `19R` | `-10.0R` | `3.54` |
| 2956 | EURJPY | London | 45m | FADE_DOWN | RSI<30 | `57.6%` | 92 | `11` | `1.36` | `14R` | `-9.0R` | `3.54` |
| 2957 | NATGAS | NY | 15m | FADE_UP | Wed | `55.6%` | 160 | `20` | `1.25` | `18R` | `-15.0R` | `3.54` |
| 2958 | XAUUSD | NY | 30m | FADE_UP | ATR+10% | `61.0%` | 41 | `5` | `1.56` | `9R` | `-4.0R` | `3.54` |
| 2959 | WTI | London Initial | 15m | FADE_UP | RSI>70 | `61.0%` | 41 | `5` | `1.56` | `9R` | `-6.0R` | `3.54` |
| 2960 | NASDAQ100 | Pre-Market | 30m | FADE_UP | Mon | `56.6%` | 122 | `15` | `1.30` | `16R` | `-5.0R` | `3.54` |
| 2961 | GBPJPY | London | 15m | FADE_UP | Wed | `55.6%` | 162 | `20` | `1.25` | `18R` | `-8.0R` | `3.53` |
| 2962 | NATGAS | NY | 30m | FADE_DOWN | AbovePD | `55.5%` | 164 | `20` | `1.25` | `18R` | `-11.0R` | `3.53` |
| 2963 | GBPJPY | Tokyo | 60m | FADE_DOWN | RSI<30 | `59.3%` | 59 | `7` | `1.46` | `11R` | `-7.0R` | `3.53` |
| 2964 | SP500 | Pre-Market | 15m | FADE_UP | RSI_D>65 | `59.3%` | 59 | `8` | `1.46` | `11R` | `-8.0R` | `3.53` |
| 2965 | XAGUSD | London | 60m | FADE_DOWN | BelowPD | `56.5%` | 124 | `15` | `1.30` | `16R` | `-9.0R` | `3.53` |
| 2966 | BRENT | London | 30m | FADE_UP | Wed | `56.5%` | 124 | `15` | `1.30` | `16R` | `-6.0R` | `3.53` |
| 2967 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | Tue | `56.5%` | 124 | `15` | `1.30` | `16R` | `-7.0R` | `3.53` |
| 2968 | XAGUSD | London | 30m | FADE_DOWN | RSI_D<35 | `58.0%` | 81 | `12` | `1.38` | `13R` | `-6.0R` | `3.52` |
| 2969 | WTI | London Initial | 15m | FADE_DOWN | RSI_D>65 | `58.0%` | 81 | `10` | `1.38` | `13R` | `-10.0R` | `3.52` |
| 2970 | USDJPY | NY | 45m | FADE_DOWN | Tue | `56.9%` | 109 | `13` | `1.32` | `15R` | `-8.0R` | `3.52` |
| 2971 | WTI | London Initial | 45m | FADE_DOWN | BelowPD | `56.9%` | 109 | `14` | `1.32` | `15R` | `-7.0R` | `3.52` |
| 2972 | SP500 | NY Cash | 45m | FADE_DOWN | Tue | `55.9%` | 145 | `18` | `1.27` | `17R` | `-5.0R` | `3.52` |
| 2973 | EURJPY | Tokyo | 15m | FADE_DOWN | ATR-10% | `61.8%` | 34 | `4` | `1.62` | `8R` | `-6.0R` | `3.52` |
| 2974 | GBPAUD | Sydney | 15m | FADE_UP | Thu | `61.8%` | 34 | `4` | `1.62` | `8R` | `-4.0R` | `3.52` |
| 2975 | BRENT | London | 15m | SHAKEOUT_UP | Tue | `61.8%` | 34 | `5` | `1.62` | `8R` | `-3.0R` | `3.52` |
| 2976 | VIX | NY Cash | 30m | FADE_DOWN | RSI<30 | `61.8%` | 34 | `10` | `1.62` | `8R` | `-2.0R` | `3.52` |
| 2977 | USDJPY | Tokyo | 30m | FADE_DOWN | RSI_D<35 | `58.6%` | 70 | `9` | `1.41` | `12R` | `-4.0R` | `3.52` |
| 2978 | SP500 | Pre-Market | 45m | FADE_DOWN | RSI<30 | `58.6%` | 70 | `9` | `1.41` | `12R` | `-4.0R` | `3.52` |
| 2979 | NASDAQ100 | Pre-Market | 30m | FADE_UP | OR_Q1_Tight | `58.6%` | 70 | `20` | `1.41` | `12R` | `-5.0R` | `3.52` |
| 2980 | NASDAQ100 | NY Cash | 45m | FADE_UP | AbovePD | `56.3%` | 126 | `15` | `1.29` | `16R` | `-5.0R` | `3.52` |
| 2981 | GBPUSD | London | 45m | FADE_DOWN | AbovePD | `55.4%` | 168 | `21` | `1.24` | `18R` | `-8.0R` | `3.52` |
| 2982 | WTI | London Initial | 15m | FADE_UP | BtwLowClose | `55.4%` | 168 | `21` | `1.24` | `18R` | `-12.0R` | `3.52` |
| 2983 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | Tue | `55.4%` | 168 | `21` | `1.24` | `18R` | `-9.0R` | `3.52` |
| 2984 | WTI | NY Main | 30m | FADE_DOWN | Tue | `55.3%` | 170 | `21` | `1.24` | `18R` | `-7.0R` | `3.51` |
| 2985 | EURJPY | London | 15m | FADE_DOWN | Wed | `55.8%` | 147 | `18` | `1.26` | `17R` | `-8.0R` | `3.51` |
| 2986 | AUDUSD | London | 30m | FADE_DOWN | RSI_D<35 | `56.8%` | 111 | `15` | `1.31` | `15R` | `-8.0R` | `3.51` |
| 2987 | VIX | NY Cash | 15m | FADE_UP | RSI_30-50 | `57.3%` | 96 | `29` | `1.34` | `14R` | `-8.0R` | `3.51` |
| 2988 | NASDAQ100 | Pre-Market | 60m | FADE_UP | Fri | `55.2%` | 172 | `21` | `1.23` | `18R` | `-12.0R` | `3.51` |
| 2989 | XAUUSD | NY | 45m | FADE_DOWN | OR_Q4_Wide | `57.8%` | 83 | `14` | `1.37` | `13R` | `-8.0R` | `3.50` |
| 2990 | XAUUSD | London | 30m | FADE_UP | Fri | `55.2%` | 174 | `21` | `1.23` | `18R` | `-9.0R` | `3.50` |
| 2991 | NASDAQ100 | NY Cash | 15m | FADE_UP | RSI>70 | `56.2%` | 130 | `16` | `1.28` | `16R` | `-7.0R` | `3.50` |
| 2992 | EURUSD | NY | 30m | FADE_UP | Fri | `55.6%` | 153 | `19` | `1.25` | `17R` | `-7.0R` | `3.49` |
| 2993 | EURUSD | London | 15m | FADE_UP | RSI_D>65 | `58.3%` | 72 | `9` | `1.40` | `12R` | `-7.0R` | `3.49` |
| 2994 | EURJPY | Tokyo | 30m | FADE_UP | RSI_D<35 | `58.3%` | 72 | `10` | `1.40` | `12R` | `-4.0R` | `3.49` |
| 2995 | SP500 | Pre-Market | 15m | FADE_UP | Mon | `58.3%` | 72 | `9` | `1.40` | `12R` | `-7.0R` | `3.49` |
| 2996 | XAUUSD | London | 60m | FADE_DOWN | BelowPD | `56.1%` | 132 | `16` | `1.28` | `16R` | `-7.0R` | `3.49` |
| 2997 | GBPJPY | London | 60m | FADE_DOWN | Wed | `55.5%` | 155 | `19` | `1.25` | `17R` | `-11.0R` | `3.49` |
| 2998 | USDJPY | Tokyo | 30m | FADE_UP | RSI>70 | `57.6%` | 85 | `11` | `1.36` | `13R` | `-5.0R` | `3.49` |
| 2999 | GBPAUD | London | 30m | FADE_DOWN | RSI<30 | `57.0%` | 100 | `13` | `1.33` | `14R` | `-4.0R` | `3.48` |
| 3000 | SP500 | NY Cash | 15m | FADE_DOWN | RSI>70 | `60.5%` | 43 | `6` | `1.53` | `9R` | `-3.0R` | `3.48` |
| 3001 | XAGUSD | NY | 30m | FADE_DOWN | RSI_D<35 | `59.6%` | 52 | `8` | `1.48` | `10R` | `-5.0R` | `3.48` |
| 3002 | NASDAQ100 | NY Cash | 30m | FADE_UP | RSI_D<35 | `59.6%` | 52 | `7` | `1.48` | `10R` | `-5.0R` | `3.48` |
| 3003 | USDJPY | NY | 30m | FADE_DOWN | RSI_D>65 | `56.4%` | 117 | `15` | `1.29` | `15R` | `-7.0R` | `3.48` |
| 3004 | EURJPY | Tokyo | 15m | FADE_DOWN | Thu | `55.3%` | 161 | `20` | `1.24` | `17R` | `-9.0R` | `3.47` |
| 3005 | XAGUSD | London | 30m | FADE_UP | RSI>70 | `58.1%` | 74 | `10` | `1.39` | `12R` | `-6.0R` | `3.47` |
| 3006 | GBPUSD | London | 15m | SHAKEOUT_UP | Thu | `57.5%` | 87 | `11` | `1.35` | `13R` | `-7.0R` | `3.47` |
| 3007 | XAUUSD | NY | 60m | FADE_UP | OR_Q1_Tight | `55.2%` | 163 | `23` | `1.23` | `17R` | `-11.0R` | `3.47` |
| 3008 | BRENT | NY | 30m | FADE_UP | Tue | `55.2%` | 163 | `20` | `1.23` | `17R` | `-7.0R` | `3.47` |
| 3009 | GBPUSD | London | 15m | FADE_UP | AbovePD | `56.3%` | 119 | `15` | `1.29` | `15R` | `-8.0R` | `3.47` |
| 3010 | XAUUSD | NY | 30m | FADE_DOWN | RSI_D>65 | `56.3%` | 119 | `15` | `1.29` | `15R` | `-7.0R` | `3.47` |
| 3011 | GBPAUD | London | 15m | FADE_UP | BelowPD | `56.9%` | 102 | `13` | `1.32` | `14R` | `-10.0R` | `3.47` |
| 3012 | XAUUSD | NY | 15m | FADE_UP | Tue | `55.2%` | 165 | `21` | `1.23` | `17R` | `-11.0R` | `3.46` |
| 3013 | SP500 | Pre-Market | 60m | FADE_UP | AbovePD | `55.2%` | 165 | `21` | `1.23` | `17R` | `-10.0R` | `3.46` |
| 3014 | XAUUSD | NY | 60m | FADE_DOWN | OR_Q4_Wide | `58.7%` | 63 | `10` | `1.42` | `11R` | `-6.0R` | `3.46` |
| 3015 | BRENT | London | 60m | FADE_UP | RSI_D<35 | `58.7%` | 63 | `9` | `1.42` | `11R` | `-5.0R` | `3.46` |
| 3016 | NASDAQ100 | Pre-Market | 45m | FADE_UP | AbovePD | `55.1%` | 167 | `20` | `1.23` | `17R` | `-6.0R` | `3.46` |
| 3017 | EURUSD | London | 30m | FADE_UP | RSI_D<35 | `56.2%` | 121 | `15` | `1.28` | `15R` | `-6.0R` | `3.46` |
| 3018 | EURUSD | London | 30m | SHAKEOUT_UP | OR_Q1_Tight | `56.2%` | 121 | `16` | `1.28` | `15R` | `-10.0R` | `3.46` |
| 3019 | AUDUSD | London | 15m | FADE_DOWN | Fri | `55.6%` | 142 | `18` | `1.25` | `16R` | `-12.0R` | `3.46` |
| 3020 | WTI | London Initial | 30m | SHAKEOUT_UP | BtwCloseHigh | `55.6%` | 142 | `18` | `1.25` | `16R` | `-7.0R` | `3.46` |
| 3021 | SP500 | NY Cash | 60m | FADE_UP | Tue | `56.7%` | 104 | `13` | `1.31` | `14R` | `-4.0R` | `3.45` |
| 3022 | WTI | London Initial | 15m | SHAKEOUT_DOWN | RSI_50-70 | `57.3%` | 89 | `11` | `1.34` | `13R` | `-6.0R` | `3.45` |
| 3023 | EURUSD | NY | 60m | FADE_DOWN | Fri | `57.9%` | 76 | `9` | `1.38` | `12R` | `-6.0R` | `3.45` |
| 3024 | EURUSD | London | 60m | FADE_UP | ATR-10% | `61.1%` | 36 | `5` | `1.57` | `8R` | `-3.0R` | `3.44` |
| 3025 | EURUSD | London | 60m | FADE_DOWN | ATR-10% | `61.1%` | 36 | `5` | `1.57` | `8R` | `-3.0R` | `3.44` |
| 3026 | GBPAUD | London | 30m | FADE_UP | RSI<30 | `61.1%` | 36 | `5` | `1.57` | `8R` | `-3.0R` | `3.44` |
| 3027 | XAUUSD | London | 15m | FADE_DOWN | AbovePD+RSI_D>65 | `61.1%` | 36 | `5` | `1.57` | `8R` | `-5.0R` | `3.44` |
| 3028 | XAUUSD | NY | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `61.1%` | 36 | `5` | `1.57` | `8R` | `-3.0R` | `3.44` |
| 3029 | BRENT | London | 15m | FADE_DOWN | BtwCloseHigh | `55.4%` | 148 | `19` | `1.24` | `16R` | `-8.0R` | `3.44` |
| 3030 | WTI | London Initial | 15m | SHAKEOUT_DOWN | Fri | `59.3%` | 54 | `7` | `1.45` | `10R` | `-3.0R` | `3.44` |
| 3031 | GBPAUD | London | 15m | FADE_DOWN | Wed | `55.3%` | 150 | `19` | `1.24` | `16R` | `-9.0R` | `3.43` |
| 3032 | BRENT | NY | 45m | FADE_DOWN | RSI_D<35 | `58.5%` | 65 | `8` | `1.41` | `11R` | `-7.0R` | `3.43` |
| 3033 | SP500 | Pre-Market | 60m | FADE_UP | ATR+10% | `58.5%` | 65 | `8` | `1.41` | `11R` | `-9.0R` | `3.43` |
| 3034 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | BelowPD | `58.5%` | 65 | `8` | `1.41` | `11R` | `-3.0R` | `3.43` |
| 3035 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | BelowPD | `56.5%` | 108 | `13` | `1.30` | `14R` | `-5.0R` | `3.43` |
| 3036 | EURUSD | NY | 30m | FADE_UP | Mon | `55.3%` | 152 | `19` | `1.24` | `16R` | `-9.0R` | `3.43` |
| 3037 | XAUUSD | NY | 15m | FADE_DOWN | BelowPD | `55.3%` | 152 | `19` | `1.24` | `16R` | `-8.0R` | `3.43` |
| 3038 | EURUSD | London | 30m | FADE_DOWN | ATR+10% | `60.0%` | 45 | `6` | `1.50` | `9R` | `-4.0R` | `3.43` |
| 3039 | EURUSD | NY | 45m | FADE_UP | RSI>70 | `60.0%` | 45 | `6` | `1.50` | `9R` | `-5.0R` | `3.43` |
| 3040 | GBPJPY | London | 45m | FADE_DOWN | ATR+10% | `60.0%` | 45 | `6` | `1.50` | `9R` | `-4.0R` | `3.43` |
| 3041 | USDJPY | Tokyo | 15m | FADE_DOWN | Tue | `55.2%` | 154 | `19` | `1.23` | `16R` | `-11.0R` | `3.42` |
| 3042 | AUDUSD | London | 30m | FADE_DOWN | BelowPD | `55.2%` | 154 | `19` | `1.23` | `16R` | `-11.0R` | `3.42` |
| 3043 | XAGUSD | NY | 15m | FADE_UP | Fri | `55.2%` | 154 | `19` | `1.23` | `16R` | `-11.0R` | `3.42` |
| 3044 | WTI | London Initial | 45m | FADE_UP | BelowPD | `56.4%` | 110 | `14` | `1.29` | `14R` | `-5.0R` | `3.42` |
| 3045 | GBPAUD | London | 15m | FADE_DOWN | BelowPD | `56.2%` | 112 | `14` | `1.29` | `14R` | `-4.0R` | `3.41` |
| 3046 | WTI | London Initial | 30m | FADE_UP | AbovePD | `56.2%` | 112 | `15` | `1.29` | `14R` | `-6.0R` | `3.41` |
| 3047 | NASDAQ100 | NY Cash | 15m | FADE_UP | BelowPD | `56.2%` | 112 | `14` | `1.29` | `14R` | `-5.0R` | `3.41` |
| 3048 | SP500 | Pre-Market | 45m | FADE_UP | AbovePD | `55.0%` | 160 | `21` | `1.22` | `16R` | `-8.0R` | `3.41` |
| 3049 | EURJPY | London | 30m | FADE_DOWN | RSI_D<35 | `58.2%` | 67 | `10` | `1.39` | `11R` | `-3.0R` | `3.41` |
| 3050 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | BtwCloseHigh | `57.5%` | 80 | `10` | `1.35` | `12R` | `-7.0R` | `3.41` |
| 3051 | XAUUSD | London | 60m | FADE_UP | AbovePD+RSI_D>65 | `58.9%` | 56 | `7` | `1.43` | `10R` | `-7.0R` | `3.40` |
| 3052 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | AbovePD | `58.9%` | 56 | `7` | `1.43` | `10R` | `-5.0R` | `3.40` |
| 3053 | USDJPY | NY | 15m | FADE_DOWN | Mon | `56.1%` | 114 | `14` | `1.28` | `14R` | `-5.0R` | `3.40` |
| 3054 | XAUUSD | London | 15m | FADE_UP | RSI_D>65 | `55.5%` | 137 | `17` | `1.25` | `15R` | `-8.0R` | `3.40` |
| 3055 | EURJPY | Tokyo | 60m | FADE_DOWN | RSI_D>65 | `55.3%` | 141 | `19` | `1.24` | `15R` | `-6.0R` | `3.39` |
| 3056 | USDJPY | NY | 60m | FADE_UP | Wed | `55.9%` | 118 | `15` | `1.27` | `14R` | `-12.0R` | `3.39` |
| 3057 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | Mon | `58.0%` | 69 | `9` | `1.38` | `11R` | `-5.0R` | `3.39` |
| 3058 | SP500 | Pre-Market | 30m | FADE_DOWN | Fri | `56.6%` | 99 | `12` | `1.30` | `13R` | `-6.0R` | `3.39` |
| 3059 | GBPUSD | NY | 30m | FADE_UP | Fri | `55.2%` | 143 | `18` | `1.23` | `15R` | `-7.0R` | `3.38` |
| 3060 | WTI | London Initial | 15m | SHAKEOUT_UP | RSI_50-70 | `55.2%` | 143 | `18` | `1.23` | `15R` | `-10.0R` | `3.38` |
| 3061 | EURUSD | NY | 60m | FADE_UP | RSI_D>65 | `59.6%` | 47 | `6` | `1.47` | `9R` | `-4.0R` | `3.38` |
| 3062 | WTI | London Initial | 15m | SHAKEOUT_DOWN | RSI_D>65 | `59.6%` | 47 | `6` | `1.47` | `9R` | `-5.0R` | `3.38` |
| 3063 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | RSI_D<35 | `59.6%` | 47 | `6` | `1.47` | `9R` | `-4.0R` | `3.38` |
| 3064 | EURJPY | London | 45m | FADE_DOWN | RSI_D>65 | `55.8%` | 120 | `16` | `1.26` | `14R` | `-6.0R` | `3.38` |
| 3065 | NATGAS | NY | 30m | FADE_UP | RSI>70 | `55.8%` | 120 | `15` | `1.26` | `14R` | `-5.0R` | `3.38` |
| 3066 | EURUSD | London | 45m | FADE_DOWN | ATR-10% | `60.5%` | 38 | `5` | `1.53` | `8R` | `-2.0R` | `3.38` |
| 3067 | EURUSD | NY | 15m | FADE_DOWN | RSI>70 | `60.5%` | 38 | `5` | `1.53` | `8R` | `-3.0R` | `3.38` |
| 3068 | AUDUSD | Sydney | 15m | FADE_UP | BtwLowClose | `60.5%` | 38 | `5` | `1.53` | `8R` | `-3.0R` | `3.38` |
| 3069 | GBPJPY | Tokyo | 15m | FADE_DOWN | OR_Q1_Tight | `60.5%` | 38 | `5` | `1.53` | `8R` | `-5.0R` | `3.38` |
| 3070 | BRENT | NY | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `60.5%` | 38 | `5` | `1.53` | `8R` | `-6.0R` | `3.38` |
| 3071 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_DOWN | Fri | `60.5%` | 38 | `5` | `1.53` | `8R` | `-7.0R` | `3.38` |
| 3072 | VIX | NY Cash | 45m | FADE_UP | ATR+10% | `60.5%` | 38 | `13` | `1.53` | `8R` | `-2.0R` | `3.38` |
| 3073 | GBPUSD | NY | 60m | FADE_DOWN | Thu | `57.1%` | 84 | `10` | `1.33` | `12R` | `-7.0R` | `3.38` |
| 3074 | XAGUSD | London | 30m | SHAKEOUT_DOWN | Tue | `56.4%` | 101 | `13` | `1.30` | `13R` | `-8.0R` | `3.37` |
| 3075 | SP500 | NY Cash | 45m | FADE_UP | BelowPD | `56.4%` | 101 | `13` | `1.30` | `13R` | `-7.0R` | `3.37` |
| 3076 | BRENT | NY | 15m | SHAKEOUT_UP | OR_Q1_Tight | `58.6%` | 58 | `7` | `1.42` | `10R` | `-5.0R` | `3.37` |
| 3077 | NATGAS | NY | 60m | FADE_UP | RSI_D<35 | `58.6%` | 58 | `7` | `1.42` | `10R` | `-7.0R` | `3.37` |
| 3078 | VIX | NY Cash | 30m | FADE_DOWN | OR_Q1_Tight | `58.6%` | 58 | `19` | `1.42` | `10R` | `-5.0R` | `3.37` |
| 3079 | GBPJPY | London | 60m | FADE_DOWN | RSI_D>65 | `55.7%` | 122 | `15` | `1.26` | `14R` | `-7.0R` | `3.37` |
| 3080 | SP500 | Pre-Market | 30m | FADE_DOWN | Thu | `55.7%` | 122 | `15` | `1.26` | `14R` | `-17.0R` | `3.37` |
| 3081 | NASDAQ100 | NY Cash | 30m | FADE_UP | RSI_D>65 | `55.0%` | 149 | `19` | `1.22` | `15R` | `-7.0R` | `3.37` |
| 3082 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | Thu | `55.0%` | 149 | `18` | `1.22` | `15R` | `-7.0R` | `3.37` |
| 3083 | WTI | London Initial | 15m | FADE_UP | AbovePD | `57.7%` | 71 | `9` | `1.37` | `11R` | `-6.0R` | `3.36` |
| 3084 | NATGAS | NY | 15m | FADE_UP | RSI_D>65 | `56.3%` | 103 | `13` | `1.29` | `13R` | `-10.0R` | `3.36` |
| 3085 | NASDAQ100 | Pre-Market | 15m | FADE_UP | BtwCloseHigh | `57.0%` | 86 | `11` | `1.32` | `12R` | `-8.0R` | `3.36` |
| 3086 | WTI | NY Main | 30m | FADE_DOWN | RSI_D>65 | `55.6%` | 126 | `15` | `1.25` | `14R` | `-9.0R` | `3.36` |
| 3087 | SP500 | Pre-Market | 45m | FADE_UP | OR_Q1_Tight | `55.6%` | 126 | `16` | `1.25` | `14R` | `-13.0R` | `3.36` |
| 3088 | GBPUSD | London | 30m | FADE_DOWN | BelowPD | `55.5%` | 128 | `16` | `1.25` | `14R` | `-10.0R` | `3.35` |
| 3089 | XAGUSD | NY | 45m | FADE_DOWN | Fri | `56.8%` | 88 | `11` | `1.32` | `12R` | `-5.0R` | `3.35` |
| 3090 | BRENT | London | 15m | FADE_DOWN | Thu | `56.8%` | 88 | `11` | `1.32` | `12R` | `-6.0R` | `3.35` |
| 3091 | XAUUSD | NY | 60m | FADE_DOWN | BtwCloseHigh | `56.1%` | 107 | `13` | `1.28` | `13R` | `-8.0R` | `3.35` |
| 3092 | VIX | NY Cash | 15m | FADE_UP | BtwLowClose | `57.5%` | 73 | `22` | `1.35` | `11R` | `-5.0R` | `3.34` |
| 3093 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | Thu | `58.3%` | 60 | `8` | `1.40` | `10R` | `-3.0R` | `3.34` |
| 3094 | VIX | NY Cash | 60m | FADE_UP | BtwCloseHigh | `58.3%` | 60 | `18` | `1.40` | `10R` | `-6.0R` | `3.34` |
| 3095 | GBPJPY | Tokyo | 45m | FADE_DOWN | ATR-10% | `59.2%` | 49 | `6` | `1.45` | `9R` | `-6.0R` | `3.34` |
| 3096 | GBPUSD | London | 60m | FADE_DOWN | RSI_D>65 | `56.0%` | 109 | `14` | `1.27` | `13R` | `-7.0R` | `3.34` |
| 3097 | GBPJPY | London | 45m | FADE_UP | AbovePD+RSI_D>65 | `61.3%` | 31 | `4` | `1.58` | `7R` | `-4.0R` | `3.33` |
| 3098 | XAGUSD | London | 60m | FADE_DOWN | ATR-10% | `61.3%` | 31 | `4` | `1.58` | `7R` | `-4.0R` | `3.33` |
| 3099 | XAGUSD | NY | 15m | FADE_DOWN | ATR-10% | `61.3%` | 31 | `4` | `1.58` | `7R` | `-3.0R` | `3.33` |
| 3100 | BRENT | London | 15m | SHAKEOUT_DOWN | BelowPD | `61.3%` | 31 | `4` | `1.58` | `7R` | `-5.0R` | `3.33` |
| 3101 | VIX | NY Cash | 15m | FADE_DOWN | RSI<30 | `61.3%` | 31 | `9` | `1.58` | `7R` | `-3.0R` | `3.33` |
| 3102 | VIX | NY Cash | 45m | FADE_DOWN | AbovePD | `61.3%` | 31 | `9` | `1.58` | `7R` | `-2.0R` | `3.33` |
| 3103 | XAUUSD | London | 45m | FADE_UP | BelowPD | `55.1%` | 136 | `17` | `1.23` | `14R` | `-9.0R` | `3.33` |
| 3104 | GBPUSD | NY | 15m | FADE_DOWN | RSI<30 | `57.3%` | 75 | `9` | `1.34` | `11R` | `-6.0R` | `3.33` |
| 3105 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | RSI<30 | `57.3%` | 75 | `9` | `1.34` | `11R` | `-4.0R` | `3.33` |
| 3106 | USDJPY | NY | 60m | FADE_DOWN | RSI_D>65 | `56.5%` | 92 | `12` | `1.30` | `12R` | `-4.0R` | `3.32` |
| 3107 | SP500 | Pre-Market | 15m | FADE_DOWN | RSI_50-70 | `56.5%` | 92 | `11` | `1.30` | `12R` | `-10.0R` | `3.32` |
| 3108 | EURUSD | London | 15m | SHAKEOUT_DOWN | BtwCloseHigh | `55.0%` | 140 | `17` | `1.22` | `14R` | `-8.0R` | `3.32` |
| 3109 | USDJPY | NY | 15m | FADE_UP | Tue | `55.0%` | 140 | `17` | `1.22` | `14R` | `-8.0R` | `3.32` |
| 3110 | USDJPY | NY | 15m | FADE_UP | Thu | `55.0%` | 140 | `17` | `1.22` | `14R` | `-6.0R` | `3.32` |
| 3111 | WTI | London Initial | 30m | SHAKEOUT_UP | RSI_30-50 | `55.0%` | 140 | `18` | `1.22` | `14R` | `-11.0R` | `3.32` |
| 3112 | WTI | London Initial | 30m | FADE_UP | ATR+10% | `60.0%` | 40 | `5` | `1.50` | `8R` | `-4.0R` | `3.32` |
| 3113 | WTI | London Initial | 45m | FADE_DOWN | ATR+10% | `60.0%` | 40 | `5` | `1.50` | `8R` | `-4.0R` | `3.32` |
| 3114 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | BelowPD | `60.0%` | 40 | `5` | `1.50` | `8R` | `-3.0R` | `3.32` |
| 3115 | NASDAQ100 | NY Cash | 45m | FADE_DOWN | ATR+10% | `60.0%` | 40 | `5` | `1.50` | `8R` | `-7.0R` | `3.32` |
| 3116 | BRENT | London | 45m | FADE_UP | RSI_D<35 | `58.1%` | 62 | `9` | `1.38` | `10R` | `-6.0R` | `3.32` |
| 3117 | USDJPY | NY | 15m | FADE_DOWN | RSI_D>65 | `55.7%` | 115 | `15` | `1.25` | `13R` | `-6.0R` | `3.31` |
| 3118 | SP500 | NY Cash | 30m | FADE_DOWN | BelowPD | `55.7%` | 115 | `14` | `1.25` | `13R` | `-5.0R` | `3.31` |
| 3119 | BRENT | London | 60m | FADE_UP | BelowPD | `56.4%` | 94 | `12` | `1.29` | `12R` | `-8.0R` | `3.31` |
| 3120 | AUDUSD | Sydney | 15m | FADE_UP | OR_Q4_Wide | `57.1%` | 77 | `10` | `1.33` | `11R` | `-7.0R` | `3.31` |
| 3121 | XAUUSD | NY | 30m | FADE_UP | BelowPD | `55.6%` | 117 | `14` | `1.25` | `13R` | `-5.0R` | `3.31` |
| 3122 | AUDUSD | Sydney | 45m | FADE_UP | RSI_50-70 | `58.8%` | 51 | `6` | `1.43` | `9R` | `-4.0R` | `3.30` |
| 3123 | NASDAQ100 | NY Cash | 15m | FADE_DOWN | ATR+10% | `58.8%` | 51 | `6` | `1.43` | `9R` | `-5.0R` | `3.30` |
| 3124 | GBPJPY | Tokyo | 45m | FADE_UP | RSI_D<35 | `56.2%` | 96 | `13` | `1.29` | `12R` | `-15.0R` | `3.30` |
| 3125 | XAUUSD | NY | 45m | FADE_UP | AbovePD | `55.5%` | 119 | `15` | `1.25` | `13R` | `-12.0R` | `3.30` |
| 3126 | GBPUSD | London | 60m | FADE_UP | RSI_D>65 | `56.1%` | 98 | `12` | `1.28` | `12R` | `-5.0R` | `3.29` |
| 3127 | GBPJPY | Tokyo | 45m | FADE_DOWN | RSI_D>65 | `55.3%` | 123 | `16` | `1.24` | `13R` | `-7.0R` | `3.29` |
| 3128 | GBPUSD | London | 30m | SHAKEOUT_DOWN | OR_Q1_Tight | `55.2%` | 125 | `16` | `1.23` | `13R` | `-10.0R` | `3.28` |
| 3129 | XAGUSD | London | 15m | FADE_DOWN | Tue | `55.2%` | 125 | `16` | `1.23` | `13R` | `-7.0R` | `3.28` |
| 3130 | SP500 | NY Cash | 45m | FADE_DOWN | BelowPD | `56.0%` | 100 | `12` | `1.27` | `12R` | `-8.0R` | `3.28` |
| 3131 | BRENT | London | 60m | FADE_DOWN | RSI<30 | `56.8%` | 81 | `10` | `1.31` | `11R` | `-5.0R` | `3.28` |
| 3132 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | RSI_50-70 | `56.8%` | 81 | `10` | `1.31` | `11R` | `-6.0R` | `3.28` |
| 3133 | GBPJPY | London | 15m | FADE_DOWN | RSI_D>65 | `55.1%` | 127 | `16` | `1.23` | `13R` | `-8.0R` | `3.28` |
| 3134 | EURJPY | London | 15m | FADE_UP | BelowPD | `55.1%` | 127 | `16` | `1.23` | `13R` | `-6.0R` | `3.28` |
| 3135 | EURJPY | Tokyo | 60m | FADE_UP | RSI_D<35 | `57.6%` | 66 | `9` | `1.36` | `10R` | `-4.0R` | `3.27` |
| 3136 | BRENT | NY | 15m | SHAKEOUT_DOWN | OR_Q1_Tight | `57.6%` | 66 | `8` | `1.36` | `10R` | `-5.0R` | `3.27` |
| 3137 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | Fri | `57.6%` | 66 | `8` | `1.36` | `10R` | `-7.0R` | `3.27` |
| 3138 | VIX | NY Cash | 45m | FADE_DOWN | RSI_50-70 | `57.6%` | 66 | `20` | `1.36` | `10R` | `-5.0R` | `3.27` |
| 3139 | BRENT | London | 30m | FADE_DOWN | RSI<30 | `58.5%` | 53 | `7` | `1.41` | `9R` | `-3.0R` | `3.27` |
| 3140 | SP500 | Pre-Market | 30m | FADE_DOWN | RSI<30 | `58.5%` | 53 | `7` | `1.41` | `9R` | `-3.0R` | `3.27` |
| 3141 | GBPJPY | London | 15m | FADE_UP | RSI<30 | `59.5%` | 42 | `6` | `1.47` | `8R` | `-5.0R` | `3.27` |
| 3142 | EURJPY | London | 30m | FADE_DOWN | RSI>70 | `59.5%` | 42 | `5` | `1.47` | `8R` | `-7.0R` | `3.27` |
| 3143 | NASDAQ100 | Pre-Market | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `59.5%` | 42 | `6` | `1.47` | `8R` | `-5.0R` | `3.27` |
| 3144 | WTI | London Initial | 60m | FADE_DOWN | RSI_D<35 | `56.6%` | 83 | `11` | `1.31` | `11R` | `-9.0R` | `3.27` |
| 3145 | SP500 | Pre-Market | 45m | SHAKEOUT_DOWN | OR_Q1_Tight | `56.6%` | 83 | `12` | `1.31` | `11R` | `-9.0R` | `3.27` |
| 3146 | EURUSD | London | 15m | SHAKEOUT_UP | Wed | `55.8%` | 104 | `13` | `1.26` | `12R` | `-7.0R` | `3.27` |
| 3147 | EURUSD | NY | 60m | FADE_UP | RSI>70 | `60.6%` | 33 | `4` | `1.54` | `7R` | `-2.0R` | `3.26` |
| 3148 | GBPUSD | London | 30m | FADE_DOWN | ATR-10% | `60.6%` | 33 | `4` | `1.54` | `7R` | `-2.0R` | `3.26` |
| 3149 | XAUUSD | NY | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `60.6%` | 33 | `5` | `1.54` | `7R` | `-3.0R` | `3.26` |
| 3150 | BRENT | NY | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `60.6%` | 33 | `4` | `1.54` | `7R` | `-4.0R` | `3.26` |
| 3151 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `60.6%` | 33 | `4` | `1.54` | `7R` | `-5.0R` | `3.26` |
| 3152 | GBPJPY | Tokyo | 30m | FADE_DOWN | RSI_D<35 | `57.4%` | 68 | `10` | `1.34` | `10R` | `-10.0R` | `3.25` |
| 3153 | EURJPY | London | 15m | SHAKEOUT_UP | OR_Q1_Tight | `57.4%` | 68 | `9` | `1.34` | `10R` | `-5.0R` | `3.25` |
| 3154 | BRENT | London | 45m | FADE_DOWN | RSI_D<35 | `57.4%` | 68 | `9` | `1.34` | `10R` | `-6.0R` | `3.25` |
| 3155 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | BelowPD | `57.4%` | 68 | `8` | `1.34` | `10R` | `-7.0R` | `3.25` |
| 3156 | SP500 | Pre-Market | 60m | FADE_UP | RSI_D<35 | `58.2%` | 55 | `7` | `1.39` | `9R` | `-3.0R` | `3.24` |
| 3157 | GBPJPY | Tokyo | 15m | FADE_DOWN | RSI_D>65 | `56.3%` | 87 | `11` | `1.29` | `11R` | `-6.0R` | `3.24` |
| 3158 | GBPAUD | London | 60m | FADE_UP | RSI>70 | `57.1%` | 70 | `9` | `1.33` | `10R` | `-5.0R` | `3.24` |
| 3159 | NASDAQ100 | NY Cash | 60m | FADE_UP | RSI_D>65 | `55.3%` | 114 | `15` | `1.24` | `12R` | `-9.0R` | `3.23` |
| 3160 | WTI | London Initial | 45m | SHAKEOUT_DOWN | OR_Q1_Tight | `56.2%` | 89 | `11` | `1.28` | `11R` | `-7.0R` | `3.23` |
| 3161 | GBPJPY | London | 15m | FADE_DOWN | ATR+10% | `59.1%` | 44 | `6` | `1.44` | `8R` | `-5.0R` | `3.23` |
| 3162 | VIX | NY Cash | 15m | FADE_DOWN | BelowPD | `59.1%` | 44 | `14` | `1.44` | `8R` | `-3.0R` | `3.23` |
| 3163 | BRENT | NY | 15m | FADE_UP | RSI_D>65 | `55.2%` | 116 | `15` | `1.23` | `12R` | `-6.0R` | `3.23` |
| 3164 | WTI | London Initial | 15m | FADE_DOWN | Thu | `56.0%` | 91 | `11` | `1.27` | `11R` | `-7.0R` | `3.22` |
| 3165 | USDJPY | NY | 45m | FADE_UP | OR_Q4_Wide | `56.9%` | 72 | `10` | `1.32` | `10R` | `-7.0R` | `3.22` |
| 3166 | AUDUSD | London | 30m | FADE_UP | RSI>70 | `56.9%` | 72 | `9` | `1.32` | `10R` | `-5.0R` | `3.22` |
| 3167 | SP500 | Pre-Market | 30m | SHAKEOUT_DOWN | Wed | `56.9%` | 72 | `9` | `1.32` | `10R` | `-5.0R` | `3.22` |
| 3168 | EURJPY | London | 15m | FADE_UP | RSI_D<35 | `57.9%` | 57 | `8` | `1.38` | `9R` | `-3.0R` | `3.22` |
| 3169 | XAUUSD | NY | 15m | FADE_DOWN | RSI_D<35 | `57.9%` | 57 | `7` | `1.38` | `9R` | `-7.0R` | `3.22` |
| 3170 | XAUUSD | London | 45m | FADE_UP | RSI_D<35 | `56.8%` | 74 | `9` | `1.31` | `10R` | `-6.0R` | `3.21` |
| 3171 | GBPAUD | London | 45m | FADE_DOWN | RSI_D>65 | `55.8%` | 95 | `13` | `1.26` | `11R` | `-10.0R` | `3.21` |
| 3172 | SP500 | NY Cash | 15m | FADE_DOWN | OR_Q1_Tight | `55.8%` | 95 | `12` | `1.26` | `11R` | `-7.0R` | `3.21` |
| 3173 | GBPUSD | London | 60m | FADE_UP | ATR-10% | `60.0%` | 35 | `4` | `1.50` | `7R` | `-4.0R` | `3.20` |
| 3174 | WTI | London Initial | 15m | SHAKEOUT_UP | BelowPD | `60.0%` | 35 | `4` | `1.50` | `7R` | `-4.0R` | `3.20` |
| 3175 | WTI | NY Main | 15m | FADE_DOWN | RSI>70 | `60.0%` | 35 | `4` | `1.50` | `7R` | `-4.0R` | `3.20` |
| 3176 | WTI | NY Main | 15m | FADE_DOWN | RSI<30 | `55.7%` | 97 | `13` | `1.26` | `11R` | `-6.0R` | `3.20` |
| 3177 | SP500 | NY Cash | 15m | FADE_UP | OR_Q1_Tight | `55.7%` | 97 | `14` | `1.26` | `11R` | `-7.0R` | `3.20` |
| 3178 | EURUSD | NY | 30m | FADE_DOWN | RSI<30 | `57.6%` | 59 | `7` | `1.36` | `9R` | `-7.0R` | `3.20` |
| 3179 | XAUUSD | NY | 15m | FADE_UP | ATR+10% | `58.7%` | 46 | `6` | `1.42` | `8R` | `-3.0R` | `3.19` |
| 3180 | SP500 | NY Cash | 60m | FADE_UP | AbovePD+RSI_D>65 | `58.7%` | 46 | `6` | `1.42` | `8R` | `-4.0R` | `3.19` |
| 3181 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | Wed | `58.7%` | 46 | `6` | `1.42` | `8R` | `-5.0R` | `3.19` |
| 3182 | SP500 | Pre-Market | 60m | FADE_UP | RSI>70 | `56.6%` | 76 | `10` | `1.30` | `10R` | `-5.0R` | `3.19` |
| 3183 | XAGUSD | NY | 30m | FADE_DOWN | RSI_D>65 | `55.6%` | 99 | `13` | `1.25` | `11R` | `-9.0R` | `3.19` |
| 3184 | WTI | NY Main | 15m | SHAKEOUT_UP | OR_Q1_Tight | `56.4%` | 78 | `10` | `1.29` | `10R` | `-5.0R` | `3.18` |
| 3185 | XAUUSD | London | 30m | FADE_DOWN | ATR+10% | `57.4%` | 61 | `8` | `1.35` | `9R` | `-6.0R` | `3.18` |
| 3186 | XAUUSD | NY | 45m | FADE_UP | RSI>70 | `57.4%` | 61 | `8` | `1.35` | `9R` | `-6.0R` | `3.18` |
| 3187 | NASDAQ100 | NY Cash | 15m | FADE_UP | RSI_D<35 | `57.4%` | 61 | `9` | `1.35` | `9R` | `-4.0R` | `3.18` |
| 3188 | XAGUSD | NY | 60m | FADE_DOWN | BtwCloseHigh | `55.2%` | 105 | `13` | `1.23` | `11R` | `-8.0R` | `3.17` |
| 3189 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | BtwLowClose | `55.2%` | 105 | `13` | `1.23` | `11R` | `-5.0R` | `3.17` |
| 3190 | EURUSD | London | 45m | FADE_DOWN | RSI<30 | `55.1%` | 107 | `13` | `1.23` | `11R` | `-4.0R` | `3.17` |
| 3191 | GBPJPY | Tokyo | 30m | FADE_DOWN | RSI_D>65 | `55.0%` | 109 | `15` | `1.22` | `11R` | `-8.0R` | `3.16` |
| 3192 | SP500 | Pre-Market | 30m | FADE_UP | Thu | `55.0%` | 109 | `14` | `1.22` | `11R` | `-9.0R` | `3.16` |
| 3193 | SP500 | Pre-Market | 30m | SHAKEOUT_DOWN | BtwCloseHigh | `55.0%` | 109 | `13` | `1.22` | `11R` | `-6.0R` | `3.16` |
| 3194 | GBPUSD | London | 15m | SHAKEOUT_DOWN | Thu | `56.0%` | 84 | `10` | `1.27` | `10R` | `-5.0R` | `3.15` |
| 3195 | XAGUSD | London | 45m | FADE_DOWN | RSI_D<35 | `56.0%` | 84 | `12` | `1.27` | `10R` | `-4.0R` | `3.15` |
| 3196 | XAUUSD | London | 15m | SHAKEOUT_UP | RSI>70 | `59.5%` | 37 | `5` | `1.47` | `7R` | `-5.0R` | `3.15` |
| 3197 | XAUUSD | NY | 45m | FADE_DOWN | RSI_D<35 | `59.5%` | 37 | `6` | `1.47` | `7R` | `-2.0R` | `3.15` |
| 3198 | VIX | NY Cash | 30m | FADE_UP | ATR+10% | `59.5%` | 37 | `12` | `1.47` | `7R` | `-3.0R` | `3.15` |
| 3199 | EURJPY | London | 60m | FADE_DOWN | RSI<30 | `56.9%` | 65 | `8` | `1.32` | `9R` | `-6.0R` | `3.14` |
| 3200 | WTI | NY Main | 30m | FADE_DOWN | RSI_D<35 | `55.7%` | 88 | `11` | `1.26` | `10R` | `-5.0R` | `3.13` |
| 3201 | BRENT | NY | 30m | FADE_DOWN | RSI_D<35 | `56.7%` | 67 | `9` | `1.31` | `9R` | `-6.0R` | `3.12` |
| 3202 | BRENT | London | 60m | FADE_UP | RSI>70 | `55.4%` | 92 | `12` | `1.24` | `10R` | `-7.0R` | `3.12` |
| 3203 | BRENT | London | 45m | SHAKEOUT_UP | OR_Q1_Tight | `56.5%` | 69 | `9` | `1.30` | `9R` | `-9.0R` | `3.11` |
| 3204 | XAUUSD | London | 45m | FADE_UP | ATR+10% | `57.7%` | 52 | `6` | `1.36` | `8R` | `-9.0R` | `3.11` |
| 3205 | XAUUSD | NY | 30m | FADE_UP | RSI_D<35 | `57.7%` | 52 | `7` | `1.36` | `8R` | `-6.0R` | `3.11` |
| 3206 | EURUSD | London | 60m | FADE_DOWN | RSI_D<35 | `55.2%` | 96 | `12` | `1.23` | `10R` | `-8.0R` | `3.11` |
| 3207 | AUDUSD | London | 30m | FADE_UP | RSI_D<35 | `55.2%` | 96 | `14` | `1.23` | `10R` | `-6.0R` | `3.11` |
| 3208 | USDJPY | Tokyo | 15m | FADE_DOWN | RSI_D<35 | `56.3%` | 71 | `9` | `1.29` | `9R` | `-5.0R` | `3.10` |
| 3209 | XAUUSD | NY | 60m | FADE_DOWN | Mon | `56.3%` | 71 | `9` | `1.29` | `9R` | `-6.0R` | `3.10` |
| 3210 | XAGUSD | NY | 15m | FADE_UP | RSI>70 | `56.3%` | 71 | `9` | `1.29` | `9R` | `-6.0R` | `3.10` |
| 3211 | XAGUSD | NY | 15m | FADE_UP | RSI_D<35 | `56.3%` | 71 | `10` | `1.29` | `9R` | `-5.0R` | `3.10` |
| 3212 | NASDAQ100 | Pre-Market | 30m | FADE_DOWN | OR_Q1_Tight | `56.3%` | 71 | `21` | `1.29` | `9R` | `-8.0R` | `3.10` |
| 3213 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | Wed | `56.3%` | 71 | `9` | `1.29` | `9R` | `-6.0R` | `3.10` |
| 3214 | XAUUSD | London | 30m | SHAKEOUT_UP | OR_Q1_Tight | `55.0%` | 100 | `16` | `1.22` | `10R` | `-9.0R` | `3.10` |
| 3215 | XAUUSD | London | 60m | FADE_DOWN | RSI_D<35 | `56.2%` | 73 | `9` | `1.28` | `9R` | `-8.0R` | `3.09` |
| 3216 | XAGUSD | London | 15m | SHAKEOUT_UP | Wed | `56.2%` | 73 | `9` | `1.28` | `9R` | `-4.0R` | `3.09` |
| 3217 | USDJPY | NY | 30m | FADE_UP | AbovePD+RSI_D>65 | `58.5%` | 41 | `5` | `1.41` | `7R` | `-8.0R` | `3.07` |
| 3218 | XAGUSD | NY | 30m | FADE_UP | AbovePD+RSI_D>65 | `58.5%` | 41 | `5` | `1.41` | `7R` | `-3.0R` | `3.07` |
| 3219 | SP500 | Pre-Market | 60m | SHAKEOUT_DOWN | ATR+10% | `58.5%` | 41 | `6` | `1.41` | `7R` | `-4.0R` | `3.07` |
| 3220 | EURJPY | London | 30m | FADE_UP | RSI<30 | `60.0%` | 30 | `5` | `1.50` | `6R` | `-4.0R` | `3.06` |
| 3221 | XAUUSD | London | 15m | FADE_UP | ATR-10% | `60.0%` | 30 | `4` | `1.50` | `6R` | `-4.0R` | `3.06` |
| 3222 | XAGUSD | NY | 15m | FADE_UP | ATR-10% | `60.0%` | 30 | `4` | `1.50` | `6R` | `-3.0R` | `3.06` |
| 3223 | XAGUSD | NY | 60m | FADE_UP | AbovePD+RSI_D>65 | `60.0%` | 30 | `4` | `1.50` | `6R` | `-3.0R` | `3.06` |
| 3224 | WTI | NY Main | 30m | FADE_UP | RSI<30 | `60.0%` | 30 | `4` | `1.50` | `6R` | `-4.0R` | `3.06` |
| 3225 | WTI | NY Main | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `60.0%` | 30 | `4` | `1.50` | `6R` | `-4.0R` | `3.06` |
| 3226 | BRENT | London | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `60.0%` | 30 | `4` | `1.50` | `6R` | `-4.0R` | `3.06` |
| 3227 | SP500 | NY Cash | 30m | FADE_UP | ATR-10% | `60.0%` | 30 | `4` | `1.50` | `6R` | `-3.0R` | `3.06` |
| 3228 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | RSI>70 | `60.0%` | 30 | `4` | `1.50` | `6R` | `-2.0R` | `3.06` |
| 3229 | GBPUSD | NY | 30m | FADE_UP | RSI_D<35 | `55.6%` | 81 | `11` | `1.25` | `9R` | `-5.0R` | `3.05` |
| 3230 | GBPJPY | London | 15m | FADE_UP | RSI_D<35 | `55.6%` | 81 | `12` | `1.25` | `9R` | `-9.0R` | `3.05` |
| 3231 | GBPAUD | London | 15m | FADE_UP | RSI_D>65 | `55.6%` | 81 | `11` | `1.25` | `9R` | `-10.0R` | `3.05` |
| 3232 | SP500 | NY Cash | 15m | FADE_UP | RSI_D<35 | `56.9%` | 58 | `7` | `1.32` | `8R` | `-4.0R` | `3.05` |
| 3233 | BRENT | London | 45m | FADE_DOWN | BelowPD | `55.4%` | 83 | `10` | `1.24` | `9R` | `-11.0R` | `3.04` |
| 3234 | NATGAS | NY | 15m | FADE_DOWN | RSI_D<35 | `55.4%` | 83 | `10` | `1.24` | `9R` | `-8.0R` | `3.04` |
| 3235 | GBPJPY | London | 30m | FADE_DOWN | RSI_D<35 | `55.3%` | 85 | `12` | `1.24` | `9R` | `-9.0R` | `3.04` |
| 3236 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | BtwCloseHigh | `55.3%` | 85 | `11` | `1.24` | `9R` | `-7.0R` | `3.04` |
| 3237 | GBPUSD | London | 45m | FADE_DOWN | ATR+10% | `58.1%` | 43 | `5` | `1.39` | `7R` | `-6.0R` | `3.04` |
| 3238 | XAGUSD | London | 30m | FADE_DOWN | ATR+10% | `58.1%` | 43 | `5` | `1.39` | `7R` | `-4.0R` | `3.04` |
| 3239 | NASDAQ100 | NY Cash | 30m | FADE_UP | ATR+10% | `58.1%` | 43 | `5` | `1.39` | `7R` | `-6.0R` | `3.04` |
| 3240 | GBPJPY | Tokyo | 15m | FADE_DOWN | RSI_D<35 | `56.7%` | 60 | `9` | `1.31` | `8R` | `-9.0R` | `3.03` |
| 3241 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | Thu | `56.7%` | 60 | `8` | `1.31` | `8R` | `-7.0R` | `3.03` |
| 3242 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_UP | AbovePD | `56.7%` | 60 | `7` | `1.31` | `8R` | `-4.0R` | `3.03` |
| 3243 | GBPAUD | London | 60m | FADE_DOWN | RSI_D>65 | `55.2%` | 87 | `11` | `1.23` | `9R` | `-11.0R` | `3.03` |
| 3244 | WTI | London Initial | 15m | FADE_DOWN | Wed | `55.1%` | 89 | `11` | `1.23` | `9R` | `-5.0R` | `3.03` |
| 3245 | GBPUSD | London | 15m | FADE_UP | RSI<30 | `57.8%` | 45 | `6` | `1.37` | `7R` | `-4.0R` | `3.01` |
| 3246 | GBPUSD | London | 60m | FADE_UP | ATR+10% | `57.8%` | 45 | `6` | `1.37` | `7R` | `-3.0R` | `3.01` |
| 3247 | NASDAQ100 | Pre-Market | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `57.8%` | 45 | `6` | `1.37` | `7R` | `-8.0R` | `3.01` |
| 3248 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | ATR+10% | `57.8%` | 45 | `6` | `1.37` | `7R` | `-6.0R` | `3.01` |
| 3249 | NASDAQ100 | Pre-Market | 45m | FADE_UP | ATR+10% | `56.2%` | 64 | `8` | `1.29` | `8R` | `-5.0R` | `3.01` |
| 3250 | GBPJPY | London | 30m | FADE_DOWN | RSI>70 | `59.4%` | 32 | `4` | `1.46` | `6R` | `-4.0R` | `3.01` |
| 3251 | GBPJPY | London | 30m | FADE_DOWN | ATR-10% | `59.4%` | 32 | `4` | `1.46` | `6R` | `-5.0R` | `3.01` |
| 3252 | EURJPY | London | 30m | FADE_DOWN | ATR-10% | `59.4%` | 32 | `4` | `1.46` | `6R` | `-5.0R` | `3.01` |
| 3253 | GBPAUD | London | 30m | FADE_DOWN | ATR+10% | `59.4%` | 32 | `4` | `1.46` | `6R` | `-4.0R` | `3.01` |
| 3254 | XAUUSD | NY | 60m | FADE_DOWN | RSI_D<35 | `59.4%` | 32 | `5` | `1.46` | `6R` | `-4.0R` | `3.01` |
| 3255 | XAGUSD | NY | 45m | FADE_DOWN | ATR+10% | `59.4%` | 32 | `4` | `1.46` | `6R` | `-4.0R` | `3.01` |
| 3256 | WTI | London Initial | 30m | FADE_UP | RSI_D<35 | `56.1%` | 66 | `9` | `1.28` | `8R` | `-7.0R` | `3.00` |
| 3257 | GBPUSD | London | 45m | FADE_UP | ATR+10% | `57.4%` | 47 | `6` | `1.35` | `7R` | `-3.0R` | `2.99` |
| 3258 | AUDUSD | Sydney | 60m | FADE_DOWN | RSI_30-50 | `57.4%` | 47 | `6` | `1.35` | `7R` | `-7.0R` | `2.99` |
| 3259 | SP500 | NY Cash | 30m | FADE_UP | AbovePD+RSI_D>65 | `57.4%` | 47 | `7` | `1.35` | `7R` | `-4.0R` | `2.99` |
| 3260 | NASDAQ100 | Pre-Market | 30m | SHAKEOUT_DOWN | Tue | `55.7%` | 70 | `9` | `1.26` | `8R` | `-6.0R` | `2.98` |
| 3261 | GBPJPY | Tokyo | 45m | FADE_DOWN | RSI_D<35 | `55.6%` | 72 | `10` | `1.25` | `8R` | `-6.0R` | `2.97` |
| 3262 | GBPUSD | NY | 30m | FADE_DOWN | ATR-10% | `58.8%` | 34 | `4` | `1.43` | `6R` | `-7.0R` | `2.96` |
| 3263 | NASDAQ100 | NY Cash | 45m | FADE_UP | ATR+10% | `58.8%` | 34 | `4` | `1.43` | `6R` | `-4.0R` | `2.96` |
| 3264 | XAGUSD | NY | 15m | FADE_DOWN | RSI<30 | `55.4%` | 74 | `9` | `1.24` | `8R` | `-5.0R` | `2.96` |
| 3265 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | Tue | `55.1%` | 78 | `10` | `1.23` | `8R` | `-9.0R` | `2.95` |
| 3266 | GBPJPY | London | 30m | FADE_UP | ATR+10% | `56.9%` | 51 | `7` | `1.32` | `7R` | `-5.0R` | `2.95` |
| 3267 | GBPJPY | London | 60m | FADE_UP | ATR+10% | `56.9%` | 51 | `7` | `1.32` | `7R` | `-6.0R` | `2.95` |
| 3268 | XAUUSD | London | 15m | SHAKEOUT_UP | AbovePD | `56.9%` | 51 | `6` | `1.32` | `7R` | `-5.0R` | `2.95` |
| 3269 | XAUUSD | NY | 30m | FADE_DOWN | RSI_D<35 | `56.9%` | 51 | `6` | `1.32` | `7R` | `-6.0R` | `2.95` |
| 3270 | BRENT | London | 15m | SHAKEOUT_DOWN | RSI_D>65 | `56.9%` | 51 | `6` | `1.32` | `7R` | `-9.0R` | `2.95` |
| 3271 | XAGUSD | NY | 60m | FADE_DOWN | Tue | `55.0%` | 80 | `10` | `1.22` | `8R` | `-6.0R` | `2.95` |
| 3272 | BRENT | London | 15m | SHAKEOUT_UP | Fri | `56.6%` | 53 | `7` | `1.30` | `7R` | `-4.0R` | `2.93` |
| 3273 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | BtwLowClose | `56.6%` | 53 | `7` | `1.30` | `7R` | `-5.0R` | `2.93` |
| 3274 | NASDAQ100 | Pre-Market | 15m | FADE_UP | AbovePD | `56.6%` | 53 | `7` | `1.30` | `7R` | `-4.0R` | `2.93` |
| 3275 | GBPAUD | London | 45m | FADE_UP | ATR+10% | `58.3%` | 36 | `5` | `1.40` | `6R` | `-7.0R` | `2.93` |
| 3276 | GBPAUD | London | 60m | FADE_UP | ATR+10% | `58.3%` | 36 | `5` | `1.40` | `6R` | `-7.0R` | `2.93` |
| 3277 | WTI | London Initial | 30m | FADE_DOWN | ATR+10% | `58.3%` | 36 | `4` | `1.40` | `6R` | `-3.0R` | `2.93` |
| 3278 | WTI | NY Main | 45m | FADE_UP | ATR+10% | `58.3%` | 36 | `4` | `1.40` | `6R` | `-4.0R` | `2.93` |
| 3279 | BRENT | London | 15m | FADE_UP | RSI>70 | `58.3%` | 36 | `5` | `1.40` | `6R` | `-5.0R` | `2.93` |
| 3280 | SP500 | Pre-Market | 15m | FADE_DOWN | AbovePD | `58.3%` | 36 | `5` | `1.40` | `6R` | `-3.0R` | `2.93` |
| 3281 | SP500 | Pre-Market | 30m | SHAKEOUT_DOWN | AbovePD | `58.3%` | 36 | `5` | `1.40` | `6R` | `-3.0R` | `2.93` |
| 3282 | BRENT | London | 15m | FADE_DOWN | BelowPD | `56.4%` | 55 | `7` | `1.29` | `7R` | `-5.0R` | `2.92` |
| 3283 | GBPJPY | Tokyo | 15m | FADE_UP | ATR+10% | `57.9%` | 38 | `5` | `1.38` | `6R` | `-4.0R` | `2.90` |
| 3284 | SP500 | Pre-Market | 15m | SHAKEOUT_DOWN | Wed | `57.9%` | 38 | `5` | `1.38` | `6R` | `-5.0R` | `2.90` |
| 3285 | SP500 | Pre-Market | 45m | SHAKEOUT_DOWN | ATR+10% | `57.9%` | 38 | `5` | `1.38` | `6R` | `-5.0R` | `2.90` |
| 3286 | EURUSD | NY | 45m | FADE_DOWN | RSI_D>65 | `55.9%` | 59 | `7` | `1.27` | `7R` | `-7.0R` | `2.89` |
| 3287 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | Wed | `55.9%` | 59 | `7` | `1.27` | `7R` | `-6.0R` | `2.89` |
| 3288 | EURJPY | London | 45m | FADE_UP | RSI_D<35 | `55.6%` | 63 | `9` | `1.25` | `7R` | `-5.0R` | `2.88` |
| 3289 | XAGUSD | NY | 30m | FADE_UP | RSI>70 | `55.6%` | 63 | `8` | `1.25` | `7R` | `-4.0R` | `2.88` |
| 3290 | EURJPY | London | 30m | FADE_UP | RSI_D<35 | `55.4%` | 65 | `10` | `1.24` | `7R` | `-7.0R` | `2.87` |
| 3291 | XAGUSD | NY | 30m | FADE_UP | ATR+10% | `57.5%` | 40 | `5` | `1.35` | `6R` | `-4.0R` | `2.87` |
| 3292 | WTI | NY Main | 45m | FADE_DOWN | ATR+10% | `57.5%` | 40 | `5` | `1.35` | `6R` | `-5.0R` | `2.87` |
| 3293 | VIX | NY Cash | 15m | FADE_UP | BtwCloseHigh | `55.1%` | 69 | `21` | `1.23` | `7R` | `-4.0R` | `2.86` |
| 3294 | VIX | NY Cash | 30m | FADE_UP | AbovePD | `57.1%` | 42 | `13` | `1.33` | `6R` | `-3.0R` | `2.85` |
| 3295 | VIX | NY Cash | 60m | FADE_UP | Tue | `57.1%` | 42 | `13` | `1.33` | `6R` | `-3.0R` | `2.85` |
| 3296 | NASDAQ100 | Pre-Market | 30m | FADE_UP | ATR+10% | `56.8%` | 44 | `6` | `1.32` | `6R` | `-6.0R` | `2.83` |
| 3297 | USDJPY | Tokyo | 30m | FADE_DOWN | ATR+10% | `56.5%` | 46 | `6` | `1.30` | `6R` | `-6.0R` | `2.81` |
| 3298 | EURUSD | London | 15m | SHAKEOUT_UP | OR_Q1_Tight | `56.2%` | 48 | `7` | `1.29` | `6R` | `-4.0R` | `2.80` |
| 3299 | VIX | NY Cash | 30m | FADE_DOWN | Tue | `56.2%` | 48 | `14` | `1.29` | `6R` | `-6.0R` | `2.80` |
| 3300 | SP500 | NY Cash | 30m | FADE_UP | RSI_D<35 | `56.0%` | 50 | `6` | `1.27` | `6R` | `-4.0R` | `2.79` |
| 3301 | GBPUSD | London | 30m | FADE_UP | ATR+10% | `55.8%` | 52 | `6` | `1.26` | `6R` | `-7.0R` | `2.78` |
| 3302 | SP500 | Pre-Market | 30m | FADE_DOWN | RSI_D<35 | `55.6%` | 54 | `7` | `1.25` | `6R` | `-4.0R` | `2.77` |
| 3303 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | RSI_D>65 | `55.4%` | 56 | `7` | `1.24` | `6R` | `-6.0R` | `2.76` |
| 3304 | VIX | NY Cash | 15m | FADE_DOWN | BtwCloseHigh | `55.4%` | 56 | `16` | `1.24` | `6R` | `-5.0R` | `2.76` |
| 3305 | AUDUSD | London | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `58.1%` | 31 | `4` | `1.38` | `5R` | `-4.0R` | `2.76` |
| 3306 | EURJPY | London | 15m | FADE_UP | AbovePD+RSI_D>65 | `58.1%` | 31 | `4` | `1.38` | `5R` | `-2.0R` | `2.76` |
| 3307 | SP500 | Pre-Market | 30m | SHAKEOUT_UP | ATR+10% | `58.1%` | 31 | `4` | `1.38` | `5R` | `-2.0R` | `2.76` |
| 3308 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | Fri | `58.1%` | 31 | `4` | `1.38` | `5R` | `-3.0R` | `2.76` |
| 3309 | NASDAQ100 | NY Cash | 60m | FADE_UP | ATR+10% | `58.1%` | 31 | `4` | `1.38` | `5R` | `-4.0R` | `2.76` |
| 3310 | WTI | London Initial | 30m | SHAKEOUT_UP | BelowPD | `55.2%` | 58 | `7` | `1.23` | `6R` | `-4.0R` | `2.76` |
| 3311 | XAGUSD | London | 30m | FADE_UP | AbovePD+RSI_D>65 | `57.6%` | 33 | `4` | `1.36` | `5R` | `-3.0R` | `2.73` |
| 3312 | VIX | NY Cash | 30m | FADE_DOWN | AbovePD | `57.6%` | 33 | `10` | `1.36` | `5R` | `-3.0R` | `2.73` |
| 3313 | USDJPY | NY | 60m | FADE_UP | RSI_D<35 | `57.1%` | 35 | `4` | `1.33` | `5R` | `-4.0R` | `2.71` |
| 3314 | AUDUSD | London | 60m | FADE_DOWN | ATR+10% | `57.1%` | 35 | `4` | `1.33` | `5R` | `-4.0R` | `2.71` |
| 3315 | EURJPY | London | 60m | FADE_UP | ATR+10% | `57.1%` | 35 | `5` | `1.33` | `5R` | `-3.0R` | `2.71` |
| 3316 | XAUUSD | London | 30m | FADE_UP | ATR-10% | `57.1%` | 35 | `4` | `1.33` | `5R` | `-3.0R` | `2.71` |
| 3317 | WTI | NY Main | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `57.1%` | 35 | `5` | `1.33` | `5R` | `-5.0R` | `2.71` |
| 3318 | NASDAQ100 | NY Cash | 60m | FADE_DOWN | ATR+10% | `57.1%` | 35 | `4` | `1.33` | `5R` | `-5.0R` | `2.71` |
| 3319 | USDJPY | NY | 30m | FADE_DOWN | RSI>70 | `56.8%` | 37 | `5` | `1.31` | `5R` | `-5.0R` | `2.69` |
| 3320 | AUDUSD | London | 15m | FADE_DOWN | ATR+10% | `56.8%` | 37 | `5` | `1.31` | `5R` | `-7.0R` | `2.69` |
| 3321 | GBPJPY | Tokyo | 15m | FADE_UP | OR_Q1_Tight | `56.8%` | 37 | `7` | `1.31` | `5R` | `-7.0R` | `2.69` |
| 3322 | SP500 | NY Cash | 60m | FADE_DOWN | AbovePD+RSI_D>65 | `56.8%` | 37 | `5` | `1.31` | `5R` | `-3.0R` | `2.69` |
| 3323 | EURUSD | London | 30m | FADE_UP | ATR+10% | `56.4%` | 39 | `5` | `1.29` | `5R` | `-5.0R` | `2.67` |
| 3324 | GBPUSD | London | 30m | FADE_DOWN | ATR+10% | `56.4%` | 39 | `5` | `1.29` | `5R` | `-5.0R` | `2.67` |
| 3325 | USDJPY | Tokyo | 30m | FADE_UP | ATR+10% | `56.1%` | 41 | `5` | `1.28` | `5R` | `-4.0R` | `2.66` |
| 3326 | EURJPY | Tokyo | 15m | FADE_DOWN | ATR+10% | `56.1%` | 41 | `5` | `1.28` | `5R` | `-5.0R` | `2.66` |
| 3327 | EURJPY | London | 15m | FADE_UP | ATR+10% | `56.1%` | 41 | `5` | `1.28` | `5R` | `-6.0R` | `2.66` |
| 3328 | XAGUSD | London | 45m | FADE_DOWN | ATR+10% | `56.1%` | 41 | `5` | `1.28` | `5R` | `-4.0R` | `2.66` |
| 3329 | SP500 | NY Cash | 45m | FADE_DOWN | AbovePD+RSI_D>65 | `56.1%` | 41 | `5` | `1.28` | `5R` | `-4.0R` | `2.66` |
| 3330 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | Thu | `56.1%` | 41 | `5` | `1.28` | `5R` | `-7.0R` | `2.66` |
| 3331 | EURUSD | London | 60m | FADE_DOWN | ATR+10% | `55.8%` | 43 | `5` | `1.26` | `5R` | `-4.0R` | `2.65` |
| 3332 | USDJPY | Tokyo | 60m | FADE_UP | ATR+10% | `55.8%` | 43 | `5` | `1.26` | `5R` | `-4.0R` | `2.65` |
| 3333 | GBPAUD | Sydney | 15m | FADE_UP | AbovePD | `55.8%` | 43 | `6` | `1.26` | `5R` | `-5.0R` | `2.65` |
| 3334 | XAGUSD | London | 15m | FADE_UP | ATR+10% | `55.8%` | 43 | `5` | `1.26` | `5R` | `-5.0R` | `2.65` |
| 3335 | XAUUSD | London | 15m | FADE_DOWN | RSI_D<35 | `55.6%` | 45 | `6` | `1.25` | `5R` | `-5.0R` | `2.64` |
| 3336 | XAUUSD | London | 60m | FADE_UP | ATR+10% | `55.6%` | 45 | `6` | `1.25` | `5R` | `-6.0R` | `2.64` |
| 3337 | XAUUSD | NY | 30m | FADE_DOWN | ATR+10% | `55.3%` | 47 | `6` | `1.24` | `5R` | `-3.0R` | `2.64` |
| 3338 | SP500 | NY Cash | 15m | FADE_UP | AbovePD+RSI_D>65 | `55.3%` | 47 | `7` | `1.24` | `5R` | `-3.0R` | `2.64` |
| 3339 | AUDUSD | London | 15m | SHAKEOUT_UP | RSI_D>65 | `55.1%` | 49 | `7` | `1.23` | `5R` | `-5.0R` | `2.63` |
| 3340 | XAUUSD | London | 15m | SHAKEOUT_UP | OR_Q1_Tight | `55.1%` | 49 | `9` | `1.23` | `5R` | `-5.0R` | `2.63` |
| 3341 | GBPJPY | London | 15m | FADE_DOWN | AbovePD+RSI_D>65 | `56.7%` | 30 | `4` | `1.31` | `4R` | `-4.0R` | `2.52` |
| 3342 | GBPAUD | London | 45m | FADE_DOWN | ATR+10% | `56.7%` | 30 | `4` | `1.31` | `4R` | `-3.0R` | `2.52` |
| 3343 | BRENT | London | 15m | SHAKEOUT_UP | BelowPD | `56.7%` | 30 | `4` | `1.31` | `4R` | `-5.0R` | `2.52` |
| 3344 | NASDAQ100 | Pre-Market | 15m | FADE_DOWN | OR_Q4+ATR+ | `56.7%` | 30 | `4` | `1.31` | `4R` | `-4.0R` | `2.52` |
| 3345 | NASDAQ100 | Pre-Market | 15m | SHAKEOUT_UP | AbovePD | `56.7%` | 30 | `4` | `1.31` | `4R` | `-5.0R` | `2.52` |
| 3346 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | ATR-10% | `56.7%` | 30 | `4` | `1.31` | `4R` | `-3.0R` | `2.52` |
| 3347 | VIX | NY Cash | 60m | FADE_UP | AbovePD | `56.7%` | 30 | `10` | `1.31` | `4R` | `-4.0R` | `2.52` |
| 3348 | VIX | NY Cash | 60m | FADE_UP | ATR+10% | `56.2%` | 32 | `11` | `1.29` | `4R` | `-4.0R` | `2.51` |
| 3349 | AUDUSD | London | 15m | SHAKEOUT_UP | OR_Q1_Tight | `55.9%` | 34 | `4` | `1.27` | `4R` | `-6.0R` | `2.50` |
| 3350 | EURJPY | Tokyo | 15m | FADE_UP | ATR+10% | `55.9%` | 34 | `4` | `1.27` | `4R` | `-4.0R` | `2.50` |
| 3351 | EURJPY | Tokyo | 30m | FADE_UP | ATR+10% | `55.6%` | 36 | `5` | `1.25` | `4R` | `-3.0R` | `2.49` |
| 3352 | WTI | NY Main | 15m | FADE_DOWN | AbovePD+RSI_D>65 | `55.6%` | 36 | `5` | `1.25` | `4R` | `-4.0R` | `2.49` |
| 3353 | XAGUSD | NY | 15m | FADE_DOWN | AbovePD+RSI_D>65 | `55.3%` | 38 | `5` | `1.24` | `4R` | `-4.0R` | `2.48` |
| 3354 | XAGUSD | NY | 30m | FADE_DOWN | ATR+10% | `55.3%` | 38 | `5` | `1.24` | `4R` | `-4.0R` | `2.48` |
| 3355 | WTI | London Initial | 15m | FADE_UP | RSI_D<35 | `55.3%` | 38 | `5` | `1.24` | `4R` | `-7.0R` | `2.48` |
| 3356 | BRENT | London | 15m | FADE_DOWN | RSI_D<35 | `55.3%` | 38 | `5` | `1.24` | `4R` | `-2.0R` | `2.48` |
| 3357 | NASDAQ100 | NY Cash | 30m | FADE_DOWN | AbovePD+RSI_D>65 | `55.3%` | 38 | `5` | `1.24` | `4R` | `-3.0R` | `2.48` |
| 3358 | VIX | NY Cash | 45m | FADE_DOWN | Fri | `55.0%` | 40 | `12` | `1.22` | `4R` | `-5.0R` | `2.48` |

---
*Generado por KHA0SYS3 Discovery Pipeline*
