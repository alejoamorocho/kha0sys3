# Resumen de Estrategias: USDJPY

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 411
**Con WR >= 65%:** 11
**Mejor WR base (sin filtro):** `61.61%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | Tokyo 30m | BASE
- WR: `58.50%` | Trades: `1012` | W/L: `592/420`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=1012), Estrategia base (todas las condiciones)

**Estrategia #2:** FADE_DOWN | NY 30m | RSI_D<35
- WR: `65.79%` | Trades: `76` | W/L: `50/26`
- Razon: WR supera umbral 65%, Filtro contextual: RSI_D<35

**Estrategia #3:** MOMENTUM_DOWN | Tokyo 30m | BASE
- WR: `45.35%` | Trades: `860` | W/L: `390/470`
- Razon: Alta significancia estadistica (N=860), Estrategia base (todas las condiciones)


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP Tokyo 30m | `58.5%` | `1.41` | `124` | `172.0R` | NO APROBADA |
| 2 | FADE_DOWN NY 30m | `72.5%` | `2.63` | `9` | `31.0R` | NO APROBADA |
| 3 | MOMENTUM_DOWN Tokyo 30m | `45.3%` | `1.24` | `105` | `115.0R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `1941` |
| Trades/Ano | `237.3` |
| Win Rate | `53.17%` |
| Profit Factor | `1.35` |
| Net R | `318.00R` |
| Max Drawdown | `-16.50R` |
| Sharpe | `2.350` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP NY 60m ATR-10% | `76.2%` | 21 | Duplicado/No complementaria |
| FADE_UP Tokyo 60m ATR-10% | `71.0%` | 31 | Duplicado/No complementaria |
| FADE_UP NY 45m ATR-10% | `66.7%` | 24 | Duplicado/No complementaria |
| FADE_DOWN NY 60m RSI_D<35 | `66.7%` | 57 | Duplicado/No complementaria |
| FADE_UP NY 60m BelowPD | `66.2%` | 77 | Duplicado/No complementaria |
| FADE_UP NY 30m RSI_D<35 | `66.0%` | 50 | Duplicado/No complementaria |
| FADE_UP Tokyo 45m ATR+10% | `65.9%` | 41 | Duplicado/No complementaria |
| FADE_UP NY 45m RSI_D<35 | `65.0%` | 40 | Duplicado/No complementaria |
| FADE_UP NY 60m BtwLowClose | `64.6%` | 113 | Menor WR |
| FADE_UP Tokyo 45m ATR-10% | `64.5%` | 31 | Menor WR |

---
*Generado por KHA0SYS3 Strategy Pipeline*
