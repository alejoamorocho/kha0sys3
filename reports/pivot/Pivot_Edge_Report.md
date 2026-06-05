# Pivot Point Edge Study — Resultados ejecutivos

**Eventos de transición:** 243,227 · **Símbolos:** 14 · **Período:** 2018-2026 (M1)

**Método:** ruptura = close M1 cruza el nivel. Destino = primer nivel DISTINTO alcanzado el mismo día UTC. Continuación = avanza al siguiente nivel en la dirección de la ruptura; Reversión = se devuelve.

## TL;DR — El edge es FADE (mean-reversion) de niveles intermedios

Las rupturas de niveles pivot intermedios **tienden a fallar (~58-75%)**. El efecto se intensifica en **horas asiáticas (00-08 UTC)**. Los niveles extremos S3/R3 se excluyen (su sesgo es artefacto geométrico).

## 1. Sesgo agregado por nivel/dirección (todos los símbolos)

| nivel | dir | n | CONT | REV | EOD | sesgo dominante |
|---|---|---|---|---|---|---|
| R2_W | UP | 2,012 | 9% | 73% | 18% | **REVERSIÓN 73%** |
| S2_D | DOWN | 7,561 | 7% | 71% | 22% | **REVERSIÓN 71%** |
| PP_D | UP | 24,423 | 18% | 70% | 12% | **REVERSIÓN 70%** |
| R1_D | UP | 15,349 | 21% | 68% | 11% | **REVERSIÓN 68%** |
| PP_W | UP | 10,737 | 23% | 67% | 10% | **REVERSIÓN 67%** |
| S2_W | DOWN | 1,769 | 3% | 67% | 30% | **REVERSIÓN 67%** |
| R1_W | UP | 5,970 | 19% | 65% | 15% | **REVERSIÓN 65%** |
| R2_D | UP | 7,890 | 29% | 59% | 12% | **REVERSIÓN 59%** |
| S1_W | DOWN | 5,242 | 23% | 54% | 23% | **neutro** |
| S1_D | DOWN | 14,674 | 39% | 47% | 14% | **neutro** |
| PP_W | DOWN | 10,775 | 45% | 45% | 10% | **neutro** |
| S1_W | UP | 4,999 | 33% | 44% | 22% | **neutro** |
| S1_D | UP | 13,780 | 41% | 43% | 16% | **neutro** |
| R1_W | DOWN | 5,671 | 50% | 35% | 15% | **neutro** |
| PP_D | DOWN | 24,309 | 58% | 31% | 12% | **CONTINUACIÓN 58%** |
| R2_D | DOWN | 7,300 | 62% | 25% | 13% | **CONTINUACIÓN 62%** |
| R1_D | DOWN | 14,287 | 64% | 24% | 12% | **CONTINUACIÓN 64%** |
| R2_W | DOWN | 1,891 | 64% | 18% | 18% | **CONTINUACIÓN 64%** |
| S2_W | UP | 1,690 | 54% | 16% | 30% | **neutro** |
| S2_D | UP | 7,040 | 67% | 11% | 21% | **CONTINUACIÓN 67%** |

## 2. EDGES tradeables y su mejor horario

Para cada edge fuerte, la probabilidad sube en ciertas horas UTC.

| nivel | dir | sesgo | global | mejores horas (UTC) |
|---|---|---|---|---|
| S2_D | DOWN | REV (FADE breakdown S2 → comprar) | 71% | 00h=93%, 05h=89%, 01h=88%, 02h=87% |
| PP_D | UP | REV (FADE breakout PP → vender) | 70% | 08h=78%, 03h=77%, 04h=76%, 05h=76% |
| R1_D | UP | REV (FADE breakout R1 → vender) | 68% | 05h=76%, 10h=75%, 11h=74%, 09h=74% |
| R2_D | UP | REV (FADE breakout R2 → vender) | 59% | 06h=68%, 09h=67%, 11h=66%, 07h=65% |
| S2_D | UP | CONT (Seguir rebote S2 → comprar) | 67% | 00h=93%, 01h=89%, 02h=87%, 06h=86% |
| PP_D | DOWN | CONT (Seguir breakdown PP → vender) | 58% | 00h=65%, 01h=62%, 08h=61%, 10h=61% |
| R1_D | DOWN | CONT (Seguir breakdown R1 → vender) | 64% | 01h=74%, 05h=74%, 07h=70%, 00h=70% |

## 3. FADE breakout PP/R1 al alza → reversión, por símbolo

Robustez del edge principal en cada activo (rompe PP/R1 arriba → se devuelve).

| símbolo | PP_D UP n | PP rev% | R1_D UP n | R1 rev% |
|---|---|---|---|---|
| AUDUSD | 1,794 | 68% | 1,140 | 70% |
| BRENT | 1,483 | 73% | 952 | 68% |
| EURJPY | 1,786 | 72% | 1,095 | 65% |
| EURUSD | 1,793 | 68% | 1,099 | 70% |
| GBPAUD | 1,884 | 71% | 1,047 | 72% |
| GBPJPY | 1,819 | 70% | 1,099 | 68% |
| GBPUSD | 1,812 | 70% | 1,099 | 67% |
| NASDAQ100 | 1,643 | 71% | 1,138 | 65% |
| NATGAS | 1,662 | 67% | 1,113 | 68% |
| SP500 | 1,666 | 71% | 1,160 | 67% |
| USDJPY | 1,775 | 69% | 1,098 | 66% |
| WTI | 1,737 | 70% | 1,114 | 67% |
| XAGUSD | 1,804 | 72% | 1,084 | 68% |
| XAUUSD | 1,765 | 67% | 1,111 | 67% |

## 4. EDGE ESTRELLA: S2_D breakdown en Asia (00-06 UTC) → rebote

Romper S2 hacia abajo en horas asiáticas rebota con altísima probabilidad.

| símbolo | n (00-06h) | rebote% |
|---|---|---|
| AUDUSD | 212 | 89% |
| EURJPY | 174 | 86% |
| EURUSD | 142 | 89% |
| GBPAUD | 150 | 84% |
| GBPJPY | 147 | 84% |
| GBPUSD | 126 | 88% |
| NASDAQ100 | 132 | 87% |
| NATGAS | 80 | 90% |
| SP500 | 143 | 90% |
| USDJPY | 216 | 86% |
| WTI | 154 | 91% |
| XAGUSD | 216 | 84% |
| XAUUSD | 200 | 92% |

## Nota metodológica

- S3/R3 excluidos del ranking: son niveles extremos, su dirección de transición es forzada (no hay nivel más allá).

- 'EOD' = no hubo otro cruce ese día (precio se quedó). ~12-22% de casos.

- Próximo paso sugerido: análisis de GESTIÓN — medir hasta qué nivel llega la reversión (TP) y cuánto avanza la ruptura antes de fallar (SL), en R-múltiplos.
