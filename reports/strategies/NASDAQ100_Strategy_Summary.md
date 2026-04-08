# Resumen de Estrategias: NASDAQ100

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 462
**Con WR >= 65%:** 24
**Mejor WR base (sin filtro):** `63.79%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | NY Cash 45m | BASE
- WR: `62.01%` | Trades: `558` | W/L: `346/212`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=558), Estrategia base (todas las condiciones)

**Estrategia #2:** SHAKEOUT_DOWN | Pre-Market 15m | BtwLowClose
- WR: `66.67%` | Trades: `66` | W/L: `44/22`
- Razon: WR supera umbral 65%, Filtro contextual: BtwLowClose

**Estrategia #3:** SHAKEOUT_UP | Pre-Market 15m | BelowPD
- WR: `68.09%` | Trades: `47` | W/L: `32/15`
- Razon: WR supera umbral 65%, Filtro contextual: BelowPD


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP NY Cash 45m | `62.0%` | `1.63` | `68` | `134.0R` | NO APROBADA |
| 2 | SHAKEOUT_DOWN Pre-Market 15m | `66.7%` | `2.00` | `8` | `22.0R` | NO APROBADA |
| 3 | SHAKEOUT_UP Pre-Market 15m | `68.1%` | `2.13` | `6` | `17.0R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `671` |
| Trades/Ano | `82.2` |
| Win Rate | `62.89%` |
| Profit Factor | `1.69` |
| Net R | `173.00R` |
| Max Drawdown | `-8.00R` |
| Sharpe | `4.233` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP Pre-Market 30m ATR-10% | `80.0%` | 20 | Duplicado/No complementaria |
| SHAKEOUT_UP Pre-Market 30m RSI_D<35 | `77.3%` | 22 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m RSI>70 | `75.0%` | 24 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m RSI<30 | `70.0%` | 20 | Duplicado/No complementaria |
| FADE_DOWN NY Cash 45m RSI_D<35 | `70.0%` | 40 | Duplicado/No complementaria |
| FADE_UP NY Cash 60m RSI>70 | `69.6%` | 56 | Duplicado/No complementaria |
| FADE_DOWN NY Cash 60m RSI_D<35 | `68.6%` | 35 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m RSI_D>65 | `68.3%` | 63 | Duplicado/No complementaria |
| SHAKEOUT_DOWN Pre-Market 30m RSI_D<35 | `67.9%` | 28 | Duplicado/No complementaria |
| FADE_UP Pre-Market 60m ATR-10% | `67.7%` | 31 | Duplicado/No complementaria |

---
*Generado por KHA0SYS3 Strategy Pipeline*
