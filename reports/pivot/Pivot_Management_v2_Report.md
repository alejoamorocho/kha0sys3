# Pivot Management v2 — TP pequeños + fricción REAL por símbolo

**Trades:** 2,241,174 · R:R 2:1 · fricción = spread round-turn real / SL_dist · SL-first

Con TP pequeños (5-10%) el SL es minúsculo → la fricción real (spread) puede superar el riesgo. Por eso se mide exacta, no fija.

## 1. Por TP% — WR bruto vs fricción (todos los setups/símbolos)

| TP% | n | WR bruto | fric_R medio | SL(atr) | exp_R neto |
|---|---|---|---|---|---|
| 5% | 373,529 | 30% | 146129557546.53R | 0.39 | -146129557546.625 |
| 10% | 373,529 | 32% | 73064778773.27R | 0.77 | -73064778773.292 |
| 15% | 373,529 | 32% | 48709852515.51R | 1.16 | -48709852515.525 |
| 20% | 373,529 | 32% | 36532389386.63R | 1.54 | -36532389386.651 |
| 25% | 373,529 | 31% | 29225911509.31R | 1.93 | -29225911509.329 |
| 50% | 373,529 | 27% | 14612955754.65R | 3.86 | -14612955754.724 |

## 2. Mejores setups por expectancy NETO (n>=300)

| period | nivel | rup | tipo | TP% | n | WR bruto | fric_R | exp_R neto | PF bruto |
|---|---|---|---|---|---|---|---|---|---|
| W | S2 | DOWN | TREND | 50% | 1,729 | 4% | 0.35 | -0.572 | 0.27 |
| W | S2 | UP | FADE | 50% | 1,671 | 4% | 0.37 | -0.587 | 0.29 |
| W | S2 | DOWN | TREND | 25% | 1,729 | 15% | 0.69 | -0.861 | 0.64 |
| W | S2 | UP | FADE | 25% | 1,671 | 15% | 0.73 | -0.904 | 0.63 |
| W | S2 | DOWN | TREND | 20% | 1,729 | 20% | 0.86 | -0.980 | 0.78 |
| W | S2 | UP | FADE | 20% | 1,671 | 20% | 0.92 | -1.035 | 0.77 |
| W | PP | UP | FADE | 50% | 10,634 | 17% | 0.98 | -1.166 | 0.65 |
| W | PP | DOWN | FADE | 50% | 10,676 | 16% | 0.99 | -1.181 | 0.63 |
| W | S2 | DOWN | TREND | 15% | 1,729 | 26% | 1.15 | -1.211 | 0.90 |
| W | PP | DOWN | TREND | 50% | 10,676 | 18% | 1.05 | -1.226 | 0.68 |
| W | PP | UP | TREND | 50% | 10,634 | 17% | 1.06 | -1.264 | 0.63 |
| W | S1 | DOWN | FADE | 50% | 5,164 | 18% | 1.09 | -1.273 | 0.66 |
| W | R1 | UP | FADE | 50% | 5,887 | 16% | 1.08 | -1.273 | 0.63 |
| W | R2 | DOWN | FADE | 50% | 1,862 | 20% | 1.15 | -1.277 | 0.75 |
| W | R1 | DOWN | TREND | 50% | 5,616 | 17% | 1.11 | -1.284 | 0.66 |
| W | S2 | DOWN | FADE | 50% | 1,729 | 22% | 1.14 | -1.294 | 0.75 |
| W | S2 | UP | FADE | 15% | 1,671 | 25% | 1.22 | -1.298 | 0.87 |
| W | S1 | UP | TREND | 50% | 4,953 | 18% | 1.13 | -1.307 | 0.67 |
| W | R1 | DOWN | FADE | 50% | 5,616 | 19% | 1.20 | -1.346 | 0.73 |
| W | S1 | UP | FADE | 50% | 4,953 | 20% | 1.24 | -1.395 | 0.73 |
| W | R2 | UP | TREND | 50% | 1,960 | 19% | 1.23 | -1.408 | 0.68 |
| W | S2 | UP | TREND | 50% | 1,671 | 21% | 1.26 | -1.427 | 0.71 |
| W | S1 | DOWN | TREND | 50% | 5,164 | 22% | 1.32 | -1.457 | 0.77 |
| W | R1 | UP | TREND | 50% | 5,887 | 21% | 1.36 | -1.480 | 0.77 |
| W | R2 | UP | FADE | 50% | 1,960 | 22% | 1.41 | -1.531 | 0.79 |
| W | R2 | DOWN | TREND | 50% | 1,862 | 23% | 1.53 | -1.663 | 0.77 |
| W | S2 | DOWN | TREND | 10% | 1,729 | 29% | 1.73 | -1.791 | 0.90 |
| W | S2 | UP | FADE | 10% | 1,671 | 28% | 1.84 | -1.888 | 0.92 |
| W | PP | DOWN | FADE | 25% | 10,676 | 30% | 1.98 | -2.009 | 0.95 |
| W | PP | UP | FADE | 25% | 10,634 | 28% | 1.96 | -2.029 | 0.89 |

## 3. Ranking por WR BRUTO (ignora fricción) — ¿hay sesgo?

Break-even bruto a 2:1 = 33%. Si WR bruto >> 33% hay sesgo direccional real.

| period | nivel | rup | tipo | TP% | n | WR bruto |
|---|---|---|---|---|---|---|
| 🟡 D | S1 | DOWN | FADE | 15% | 14,674 | 36% |
| 🔴 W | S2 | DOWN | FADE | 10% | 1,729 | 36% |
| 🔴 D | PP | UP | FADE | 10% | 24,423 | 36% |
| 🔴 D | S1 | DOWN | FADE | 20% | 14,674 | 36% |
| 🔴 W | R2 | UP | FADE | 5% | 1,960 | 36% |
| 🔴 D | PP | DOWN | FADE | 10% | 24,309 | 35% |
| 🔴 W | PP | UP | FADE | 5% | 10,634 | 35% |
| 🔴 D | PP | DOWN | FADE | 5% | 24,309 | 35% |
| 🔴 D | PP | DOWN | FADE | 15% | 24,309 | 35% |
| 🔴 W | S2 | DOWN | FADE | 5% | 1,729 | 35% |
| 🔴 D | S1 | DOWN | FADE | 10% | 14,674 | 35% |
| 🔴 D | R2 | DOWN | FADE | 25% | 7,300 | 35% |
| 🔴 D | PP | UP | FADE | 15% | 24,423 | 35% |
| 🔴 D | S2 | DOWN | FADE | 15% | 7,561 | 35% |
| 🔴 D | R2 | DOWN | FADE | 15% | 7,300 | 35% |
| 🔴 D | R2 | UP | FADE | 20% | 7,890 | 35% |
| 🔴 W | R1 | DOWN | FADE | 10% | 5,616 | 35% |
| 🔴 D | R2 | DOWN | FADE | 20% | 7,300 | 35% |
| 🔴 W | S1 | DOWN | FADE | 5% | 5,164 | 35% |
| 🔴 W | PP | DOWN | FADE | 5% | 10,676 | 35% |

## 4. Setups con expectancy NETO positivo: 0

_Ninguno._ El WR bruto no supera lo suficiente el 33% para pagar la fricción.
