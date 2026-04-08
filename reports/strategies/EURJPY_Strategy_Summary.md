# Resumen de Estrategias: EURJPY

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 423
**Con WR >= 65%:** 11
**Mejor WR base (sin filtro):** `61.05%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | London 45m | BASE
- WR: `61.05%` | Trades: `968` | W/L: `591/377`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=968), Estrategia base (todas las condiciones)

**Estrategia #2:** FADE_DOWN | Tokyo 60m | BASE
- WR: `51.32%` | Trades: `1173` | W/L: `602/571`
- Razon: Alta significancia estadistica (N=1173), Estrategia base (todas las condiciones)

**Estrategia #3:** MOMENTUM_DOWN | London 45m | RSI>70
- WR: `65.22%` | Trades: `23` | W/L: `15/8`
- Razon: WR supera umbral 65%, Filtro contextual: RSI>70


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP London 45m | `61.1%` | `1.57` | `118` | `214.0R` | NO APROBADA |
| 2 | FADE_DOWN Tokyo 60m | `60.5%` | `1.53` | `122` | `209.0R` | NO APROBADA |
| 3 | MOMENTUM_DOWN London 45m | `65.2%` | `2.81` | `3` | `14.5R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `1986` |
| Trades/Ano | `242.8` |
| Win Rate | `60.83%` |
| Profit Factor | `1.56` |
| Net R | `437.50R` |
| Max Drawdown | `-9.00R` |
| Sharpe | `3.567` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP Tokyo 60m RSI>70 | `69.4%` | 85 | Duplicado/No complementaria |
| FADE_UP London 60m RSI_D>65 | `69.0%` | 116 | Duplicado/No complementaria |
| FADE_UP Tokyo 60m ATR-10% | `67.7%` | 31 | Duplicado/No complementaria |
| FADE_UP Tokyo 30m ATR-10% | `66.7%` | 33 | Duplicado/No complementaria |
| FADE_UP Tokyo 45m RSI_D<35 | `66.2%` | 74 | Duplicado/No complementaria |
| FADE_UP London 30m RSI>70 | `66.1%` | 109 | Duplicado/No complementaria |
| FADE_UP London 30m RSI_D>65 | `65.6%` | 122 | Duplicado/No complementaria |
| FADE_UP Tokyo 45m ATR-10% | `65.5%` | 29 | Duplicado/No complementaria |
| FADE_UP Tokyo 45m RSI_D>65 | `64.7%` | 133 | Menor WR |
| FADE_UP Tokyo 30m RSI_D>65 | `64.3%` | 129 | Menor WR |

---
*Generado por KHA0SYS3 Strategy Pipeline*
