# Resumen de Estrategias: SP500

## Seleccion del Equipo Quant

**Estrategias escaneadas:** 473
**Con WR >= 65%:** 20
**Mejor WR base (sin filtro):** `64.32%`
**Seleccionadas:** 3

**Estrategia #1:** FADE_UP | NY Cash 45m | BASE
- WR: `63.45%` | Trades: `673` | W/L: `427/246`
- Razon: Mejor score volumen-calidad, Alta significancia estadistica (N=673), Estrategia base (todas las condiciones)

**Estrategia #2:** SHAKEOUT_DOWN | Pre-Market 30m | RSI_D<35
- WR: `80.00%` | Trades: `30` | W/L: `24/6`
- Razon: WR supera umbral 65%, Filtro contextual: RSI_D<35

**Estrategia #3:** SHAKEOUT_UP | Pre-Market 15m | ATR+10%
- WR: `82.35%` | Trades: `34` | W/L: `28/6`
- Razon: WR supera umbral 65%, Filtro contextual: ATR+10%


## Resultados Individuales

| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FADE_UP NY Cash 45m | `63.4%` | `1.74` | `82` | `181.0R` | NO APROBADA |
| 2 | SHAKEOUT_DOWN Pre-Market 30m | `80.0%` | `4.00` | `4` | `18.0R` | NO APROBADA |
| 3 | SHAKEOUT_UP Pre-Market 15m | `82.4%` | `4.67` | `4` | `22.0R` | NO APROBADA |

## Resultado Grupal (todas las estrategias combinadas)

| Metrica | Valor |
| --- | --- |
| Total Trades | `737` |
| Trades/Ano | `90.3` |
| Win Rate | `64.99%` |
| Profit Factor | `1.86` |
| Net R | `221.00R` |
| Max Drawdown | `-8.00R` |
| Sharpe | `4.986` |

## Top 10 Candidatos Descartados

| Estrategia | WR | Trades | Razon |
| --- | --- | --- | --- |
| FADE_UP NY Cash 60m ATR+10% | `77.1%` | 35 | Duplicado/No complementaria |
| SHAKEOUT_DOWN Pre-Market 15m ATR+10% | `76.9%` | 26 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m ATR+10% | `73.9%` | 46 | Duplicado/No complementaria |
| FADE_UP NY Cash 60m ATR-10% | `72.7%` | 22 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m RSI_D<35 | `70.3%` | 37 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m RSI<30 | `70.0%` | 20 | Duplicado/No complementaria |
| FADE_UP Pre-Market 30m ATR+10% | `68.9%` | 45 | Duplicado/No complementaria |
| FADE_UP NY Cash 15m RSI<30 | `68.0%` | 25 | Duplicado/No complementaria |
| FADE_UP NY Cash 60m RSI>70 | `67.0%` | 88 | Duplicado/No complementaria |
| FADE_UP Pre-Market 15m RSI>70 | `66.7%` | 30 | Duplicado/No complementaria |

---
*Generado por KHA0SYS3 Strategy Pipeline*
