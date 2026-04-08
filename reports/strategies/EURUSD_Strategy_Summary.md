# Resumen de Estrategias: EURUSD

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 476
**Con WR >= 65%:** 16
**Mejor WR base (sin filtro):** `63.83%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | London 60m | BASE
- WR: `62.29%` | Trades: `952` | W/L: `593/359`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=952), Estrategia base (todas las condiciones)

**Estrategia #2:** FADE_DOWN | NY 60m | BelowPD
- WR: `65.04%` | Trades: `123` | W/L: `80/43`
- Razon: WR supera umbral 65%, Filtro contextual: BelowPD

**Estrategia #3:** SHAKEOUT_DOWN | London 15m | BASE
- WR: `50.98%` | Trades: `410` | W/L: `209/201`
- Razon: Alta significancia estadistica (N=410), Estrategia base (todas las condiciones)


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP London 60m | `62.3%` | `1.65` | `116` | `234.0R` | NO APROBADA |
| 2 | FADE_DOWN NY 60m | `66.7%` | `2.00` | `15` | `40.0R` | NO APROBADA |
| 3 | SHAKEOUT_DOWN London 15m | `51.0%` | `1.04` | `50` | `8.0R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `1482` |
| Trades/Ano | `181.2` |
| Win Rate | `59.51%` |
| Profit Factor | `1.47` |
| Net R | `282.00R` |
| Max Drawdown | `-10.00R` |
| Sharpe | `3.076` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP London 30m ATR-10% | `73.2%` | 41 | Duplicado/No complementaria |
| FADE_UP London 15m ATR+10% | `69.4%` | 36 | Duplicado/No complementaria |
| FADE_UP NY 60m BtwCloseHigh | `68.5%` | 127 | Duplicado/No complementaria |
| FADE_UP London 45m ATR-10% | `68.4%` | 38 | Duplicado/No complementaria |
| FADE_UP NY 60m RSI_D<35 | `68.4%` | 57 | Duplicado/No complementaria |
| FADE_UP London 45m RSI<30 | `68.2%` | 22 | Duplicado/No complementaria |
| FADE_UP NY 45m BtwCloseHigh | `68.2%` | 154 | Duplicado/No complementaria |
| FADE_UP NY 45m RSI_D<35 | `66.7%` | 63 | Duplicado/No complementaria |
| FADE_UP NY 60m ATR+10% | `66.7%` | 24 | Duplicado/No complementaria |
| FADE_UP London 30m RSI_D>65 | `65.1%` | 86 | Duplicado/No complementaria |

---
*Generado por KHA0SYS3 Strategy Pipeline*
