# Resumen de Estrategias: AUDUSD

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 312
**Con WR >= 65%:** 32
**Mejor WR base (sin filtro):** `73.58%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | London 45m | BASE
- WR: `61.53%` | Trades: `980` | W/L: `603/377`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=980), Estrategia base (todas las condiciones)

**Estrategia #2:** FADE_DOWN | Sydney 45m | BASE
- WR: `73.58%` | Trades: `106` | W/L: `78/28`
- Razon: WR supera umbral 65%, Estrategia base (todas las condiciones)

**Estrategia #3:** FADE_UP | London 60m | BelowPD
- WR: `68.10%` | Trades: `163` | W/L: `111/52`
- Razon: WR supera umbral 65%, Filtro contextual: BelowPD


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP London 45m | `61.5%` | `1.60` | `120` | `226.0R` | NO APROBADA |
| 2 | FADE_DOWN Sydney 45m | `73.6%` | `2.79` | `13` | `50.0R` | NO APROBADA |
| 3 | FADE_UP London 60m | `68.1%` | `2.13` | `20` | `59.0R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `1249` |
| Trades/Ano | `152.7` |
| Win Rate | `63.41%` |
| Profit Factor | `1.73` |
| Net R | `335.00R` |
| Max Drawdown | `-12.00R` |
| Sharpe | `4.418` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP Sydney 45m BelowPD | `87.0%` | 23 | Duplicado/No complementaria |
| FADE_DOWN Sydney 60m AbovePD | `85.7%` | 21 | Duplicado/No complementaria |
| FADE_UP Sydney 30m BelowPD | `82.1%` | 28 | Duplicado/No complementaria |
| FADE_DOWN Sydney 15m BtwLowClose | `80.8%` | 26 | Duplicado/No complementaria |
| FADE_DOWN Sydney 60m BtwCloseHigh | `80.0%` | 20 | Duplicado/No complementaria |
| FADE_UP London 30m RSI<30 | `78.3%` | 23 | Duplicado/No complementaria |
| FADE_UP Sydney 45m BtwLowClose | `77.1%` | 35 | Duplicado/No complementaria |
| FADE_DOWN Sydney 30m AbovePD | `75.0%` | 20 | Duplicado/No complementaria |
| FADE_DOWN Sydney 15m BtwCloseHigh | `74.3%` | 35 | Duplicado/No complementaria |
| FADE_DOWN Sydney 30m BtwCloseHigh | `74.2%` | 31 | Duplicado/No complementaria |

---
*Generado por KHA0SYS3 Strategy Pipeline*
