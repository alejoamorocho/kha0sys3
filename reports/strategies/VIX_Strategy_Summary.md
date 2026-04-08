# Resumen de Estrategias: VIX

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 168
**Con WR >= 65%:** 11
**Mejor WR base (sin filtro):** `61.81%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_DOWN | NY Cash 45m | BASE
- WR: `61.81%` | Trades: `254` | W/L: `157/97`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=254), Estrategia base (todas las condiciones)

**Estrategia #2:** FADE_UP | NY Cash 45m | BtwCloseHigh
- WR: `67.12%` | Trades: `73` | W/L: `49/24`
- Razon: WR supera umbral 65%, Filtro contextual: BtwCloseHigh

**Estrategia #3:** FADE_DOWN | NY Cash 60m | BtwLowClose
- WR: `71.88%` | Trades: `64` | W/L: `46/18`
- Razon: WR supera umbral 65%, Filtro contextual: BtwLowClose


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_DOWN NY Cash 45m | `67.1%` | `2.04` | `69` | `80.0R` | APROBADA |
| 2 | FADE_UP NY Cash 45m | `67.1%` | `2.04` | `22` | `25.0R` | APROBADA |
| 3 | FADE_DOWN NY Cash 60m | `73.0%` | `2.71` | `19` | `29.0R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `370` |
| Trades/Ano | `108.7` |
| Win Rate | `68.11%` |
| Profit Factor | `2.14` |
| Net R | `134.00R` |
| Max Drawdown | `-7.00R` |
| Sharpe | `6.160` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_DOWN NY Cash 30m RSI_D<35 | `75.0%` | 20 | Duplicado/No complementaria |
| FADE_UP NY Cash 30m RSI_D>65 | `72.7%` | 22 | Duplicado/No complementaria |
| FADE_DOWN NY Cash 30m ATR-10% | `65.4%` | 26 | Duplicado/No complementaria |
| FADE_DOWN NY Cash 30m BtwLowClose | `63.4%` | 93 | Menor WR |
| FADE_DOWN NY Cash 30m ATR+10% | `63.3%` | 30 | Menor WR |
| FADE_UP NY Cash 30m BtwLowClose | `62.2%` | 90 | Menor WR |
| MOMENTUM_UP NY Cash 60m ATR-10% | `61.9%` | 21 | Menor WR |
| FADE_DOWN NY Cash 30m RSI<30 | `61.8%` | 34 | Menor WR |
| FADE_UP NY Cash 60m BtwLowClose | `61.7%` | 81 | Menor WR |
| FADE_UP NY Cash 30m BelowPD | `61.5%` | 52 | Menor WR |

---
*Generado por KHA0SYS3 Strategy Pipeline*
