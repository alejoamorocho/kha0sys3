# Resumen de Estrategias: WTI

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 456
**Con WR >= 65%:** 14
**Mejor WR base (sin filtro):** `64.15%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | NY Main 45m | BASE
- WR: `63.44%` | Trades: `807` | W/L: `512/295`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=807), Estrategia base (todas las condiciones)

**Estrategia #2:** FADE_DOWN | London Initial 60m | BASE
- WR: `48.10%` | Trades: `1133` | W/L: `545/588`
- Razon: Alta significancia estadistica (N=1133), Estrategia base (todas las condiciones)

**Estrategia #3:** FADE_UP | NY Main 60m | AbovePD
- WR: `70.00%` | Trades: `180` | W/L: `126/54`
- Razon: WR supera umbral 65%, Filtro contextual: AbovePD


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP NY Main 45m | `63.4%` | `1.74` | `99` | `217.0R` | NO APROBADA |
| 2 | FADE_DOWN London Initial 60m | `59.0%` | `1.44` | `113` | `166.0R` | NO APROBADA |
| 3 | FADE_UP NY Main 60m | `70.0%` | `2.33` | `22` | `72.0R` | APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `1911` |
| Trades/Ano | `233.6` |
| Win Rate | `61.90%` |
| Profit Factor | `1.62` |
| Net R | `455.00R` |
| Max Drawdown | `-14.00R` |
| Sharpe | `3.891` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP NY Main 15m ATR-10% | `71.4%` | 21 | Duplicado/No complementaria |
| FADE_UP London Initial 60m ATR+10% | `70.0%` | 40 | Duplicado/No complementaria |
| FADE_UP London Initial 45m ATR+10% | `68.3%` | 41 | Duplicado/No complementaria |
| FADE_UP NY Main 15m RSI>70 | `67.4%` | 95 | Duplicado/No complementaria |
| FADE_UP NY Main 15m RSI_D<35 | `67.1%` | 73 | Duplicado/No complementaria |
| FADE_UP NY Main 30m AbovePD | `65.9%` | 217 | Duplicado/No complementaria |
| FADE_UP NY Main 30m RSI>70 | `65.4%` | 104 | Duplicado/No complementaria |
| FADE_UP NY Main 30m RSI_D<35 | `64.3%` | 70 | Menor WR |
| FADE_DOWN NY Main 60m BelowPD | `64.2%` | 134 | Menor WR |
| FADE_UP London Initial 60m RSI_D<35 | `64.0%` | 75 | Menor WR |

---
*Generado por KHA0SYS3 Strategy Pipeline*
