# 🌐 Matriz Probabilística Omnidireccional: GBPUSD

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **London 15m**](#permutación-1-london-15m)
- [Permutación #2: **London 30m**](#permutación-2-london-30m)
- [Permutación #3: **London 45m**](#permutación-3-london-45m)
- [Permutación #4: **London 60m**](#permutación-4-london-60m)
- [Permutación #5: **NY 15m**](#permutación-5-ny-15m)
- [Permutación #6: **NY 30m**](#permutación-6-ny-30m)
- [Permutación #7: **NY 45m**](#permutación-7-ny-45m)
- [Permutación #8: **NY 60m**](#permutación-8-ny-60m)

---
## Permutación #1: London 15m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1710`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.36%`
- **Rotura Bajista (DOWN):** `47.25%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `79.32%` | `79.70%` |
| 1.5x Rango OR | `69.41%` | `68.07%` |
| 2.0x Rango OR | `58.89%` | `58.17%` |
| 1.0x Volatilidad ATR Diaria | `14.15%` | `15.10%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.90%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.58%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `73.16%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `62.46%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.26%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1334`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `51.12%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `42.05%` |
| Shakeout & Re-breakout UP (>=2x OR) | `34.56%` |
| Continuacion Bajista (>=1x OR) | `75.11%` |
| Extension media reversal UP | `1.80x OR` | Mediana: `1.08x` |
| Extension media continuacion DOWN | `2.83x OR` | Mediana: `2.14x` |
| Tiempo medio al re-breakout | `119 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1335`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `51.99%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `42.77%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `35.13%` |
| Continuacion Alcista (>=1x OR) | `74.83%` |
| Extension media reversal DOWN | `1.89x OR` | Mediana: `1.09x` |
| Extension media continuacion UP | `2.75x OR` | Mediana: `2.12x` |
| Tiempo medio al re-breakout | `110 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 178 | `26%` | `65%` ⭐ | `57%` | `57%` | `46%` | `49%` |
| RSI > 70 (Overbought) | 132 | `75%` ⭐ | `64%` ⭐ | `59%` | `50%` | `46%` | `47%` |
| RSI 30-70 (Neutro) | 1400 | `49%` | `71%` ⭐ | `54%` | `54%` | `52%` | `79%` ⭐ |
| OR ABOVE_PD_HIGH | 266 | `45%` | `73%` ⭐ | `56%` | `46%` | `49%` | `64%` ⭐ |
| OR BELOW_PD_LOW | 247 | `51%` | `70%` ⭐ | `49%` | `52%` | `48%` | `65%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 570 | `49%` | `68%` ⭐ | `59%` | `57%` | `53%` | `76%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 627 | `48%` | `69%` ⭐ | `54%` | `58%` | `52%` | `78%` ⭐ |
| ATR Creciente (>10%) | 89 | `44%` | `72%` ⭐ | `44%` | `51%` | `49%` | `71%` ⭐ |
| ATR Decreciente (<-10%) | 54 | `48%` | `81%` ⭐ | `58%` | `52%` | `56%` | `76%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 461 | `49%` | `72%` ⭐ | `52%` | `59%` | `52%` | `71%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 387 | `53%` | `67%` ⭐ | `56%` | `51%` | `49%` | `74%` ⭐ |
| RSI Diario < 35 | 216 | `49%` | `70%` ⭐ | `48%` | `64%` ⭐ | `54%` | `74%` ⭐ |
| RSI Diario > 65 | 190 | `42%` | `69%` ⭐ | `54%` | `48%` | `44%` | `68%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `178 min` | `105 min` | `315 min` |
| TP DOWN (desde entrada) | `173 min` | `105 min` | `315 min` |
| False Break UP → SL | `76 min` | - | - |
| False Break DOWN → SL | `97 min` | - | - |

---

## Permutación #2: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2007`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.03%`
- **Rotura Bajista (DOWN):** `49.73%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `75.41%` | `73.65%` |
| 1.5x Rango OR | `63.49%` | `62.32%` |
| 2.0x Rango OR | `48.76%` | `51.30%` |
| 1.0x Volatilidad ATR Diaria | `14.11%` | `13.53%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `52.18%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.21%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `73.09%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `62.08%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.86%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1531`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `41.87%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `32.07%` |
| Shakeout & Re-breakout UP (>=2x OR) | `23.38%` |
| Continuacion Bajista (>=1x OR) | `67.60%` |
| Extension media reversal UP | `1.32x OR` | Mediana: `0.59x` |
| Extension media continuacion DOWN | `2.24x OR` | Mediana: `1.69x` |
| Tiempo medio al re-breakout | `134 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1542`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `41.37%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `32.04%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `25.23%` |
| Continuacion Alcista (>=1x OR) | `68.42%` |
| Extension media reversal DOWN | `1.31x OR` | Mediana: `0.58x` |
| Extension media continuacion UP | `2.21x OR` | Mediana: `1.64x` |
| Tiempo medio al re-breakout | `129 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 174 | `18%` | `68%` ⭐ | `45%` | `50%` | `31%` | `43%` |
| RSI > 70 (Overbought) | 162 | `73%` ⭐ | `58%` | `47%` | `42%` | `34%` | `44%` |
| RSI 30-70 (Neutro) | 1671 | `49%` | `64%` ⭐ | `53%` | `57%` | `44%` | `79%` ⭐ |
| OR ABOVE_PD_HIGH | 312 | `44%` | `66%` ⭐ | `49%` | `50%` | `40%` | `65%` ⭐ |
| OR BELOW_PD_LOW | 271 | `50%` | `66%` ⭐ | `44%` | `55%` | `37%` | `64%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 690 | `49%` | `64%` ⭐ | `53%` | `57%` | `45%` | `75%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 734 | `48%` | `61%` ⭐ | `56%` | `57%` | `42%` | `78%` ⭐ |
| ATR Creciente (>10%) | 94 | `55%` | `60%` | `56%` | `54%` | `39%` | `70%` ⭐ |
| ATR Decreciente (<-10%) | 66 | `47%` | `84%` ⭐ | `42%` | `57%` | `46%` | `76%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 529 | `50%` | `63%` ⭐ | `51%` | `53%` | `44%` | `71%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 474 | `51%` | `59%` | `54%` | `55%` | `36%` | `73%` ⭐ |
| RSI Diario < 35 | 238 | `56%` | `63%` ⭐ | `53%` | `61%` ⭐ | `38%` | `73%` ⭐ |
| RSI Diario > 65 | 226 | `42%` | `65%` ⭐ | `53%` | `50%` | `41%` | `69%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `208 min` | `165 min` | `360 min` |
| TP DOWN (desde entrada) | `208 min` | `165 min` | `360 min` |
| False Break UP → SL | `114 min` | - | - |
| False Break DOWN → SL | `131 min` | - | - |

---

## Permutación #3: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2084`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.70%`
- **Rotura Bajista (DOWN):** `50.91%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `69.72%` | `68.61%` |
| 1.5x Rango OR | `55.63%` | `55.70%` |
| 2.0x Rango OR | `41.85%` | `43.45%` |
| 1.0x Volatilidad ATR Diaria | `15.79%` | `13.48%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `50.20%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.89%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `72.07%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `60.84%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.27%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1557`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `31.86%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `23.06%` |
| Shakeout & Re-breakout UP (>=2x OR) | `16.76%` |
| Continuacion Bajista (>=1x OR) | `61.66%` |
| Extension media reversal UP | `0.98x OR` | Mediana: `0.30x` |
| Extension media continuacion DOWN | `1.86x OR` | Mediana: `1.42x` |
| Tiempo medio al re-breakout | `141 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1587`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `32.77%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `25.65%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `17.45%` |
| Continuacion Alcista (>=1x OR) | `60.68%` |
| Extension media reversal DOWN | `0.97x OR` | Mediana: `0.24x` |
| Extension media continuacion UP | `1.83x OR` | Mediana: `1.32x` |
| Tiempo medio al re-breakout | `141 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 185 | `18%` | `39%` | `58%` | `55%` | `25%` | `48%` |
| RSI > 70 (Overbought) | 163 | `83%` ⭐ | `47%` | `43%` | `58%` | `24%` | `42%` |
| RSI 30-70 (Neutro) | 1736 | `48%` | `58%` | `51%` | `56%` | `33%` | `77%` ⭐ |
| OR ABOVE_PD_HIGH | 328 | `43%` | `61%` ⭐ | `43%` | `52%` | `30%` | `64%` ⭐ |
| OR BELOW_PD_LOW | 275 | `51%` | `58%` | `47%` | `61%` ⭐ | `29%` | `64%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 714 | `48%` | `54%` | `50%` | `58%` | `36%` | `74%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 767 | `48%` | `54%` | `54%` | `55%` | `30%` | `77%` ⭐ |
| ATR Creciente (>10%) | 96 | `50%` | `48%` | `56%` | `53%` | `32%` | `68%` ⭐ |
| ATR Decreciente (<-10%) | 74 | `51%` | `68%` ⭐ | `53%` | `57%` | `39%` | `74%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 538 | `50%` | `57%` | `49%` | `53%` | `34%` | `70%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 503 | `49%` | `50%` | `52%` | `56%` | `26%` | `72%` ⭐ |
| RSI Diario < 35 | 246 | `53%` | `58%` | `50%` | `60%` | `32%` | `72%` ⭐ |
| RSI Diario > 65 | 233 | `41%` | `53%` | `51%` | `48%` | `26%` | `69%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `232 min` | `195 min` | `360 min` |
| TP DOWN (desde entrada) | `227 min` | `195 min` | `375 min` |
| False Break UP → SL | `150 min` | - | - |
| False Break DOWN → SL | `150 min` | - | - |

---

## Permutación #4: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2105`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.79%`
- **Rotura Bajista (DOWN):** `49.41%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `64.36%` | `65.29%` |
| 1.5x Rango OR | `48.78%` | `50.29%` |
| 2.0x Rango OR | `37.29%` | `38.17%` |
| 1.0x Volatilidad ATR Diaria | `14.70%` | `12.98%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `49.56%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.56%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `70.50%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `60.00%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.51%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1533`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `25.83%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `18.20%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.87%` |
| Continuacion Bajista (>=1x OR) | `56.75%` |
| Extension media reversal UP | `0.77x OR` | Mediana: `0.12x` |
| Extension media continuacion DOWN | `1.59x OR` | Mediana: `1.20x` |
| Tiempo medio al re-breakout | `148 min` | Mediana: `120 min` |

**False Breakouts DOWN analizados:** `1582`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `27.31%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `19.60%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.96%` |
| Continuacion Alcista (>=1x OR) | `54.61%` |
| Extension media reversal DOWN | `0.77x OR` | Mediana: `0.06x` |
| Extension media continuacion UP | `1.57x OR` | Mediana: `1.12x` |
| Tiempo medio al re-breakout | `147 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 183 | `19%` | `29%` | `60%` ⭐ | `51%` | `16%` | `42%` |
| RSI > 70 (Overbought) | 164 | `88%` ⭐ | `34%` | `41%` | `65%` ⭐ | `16%` | `44%` |
| RSI 30-70 (Neutro) | 1758 | `48%` | `52%` | `51%` | `54%` | `28%` | `76%` ⭐ |
| OR ABOVE_PD_HIGH | 330 | `44%` | `52%` | `42%` | `52%` | `22%` | `63%` ⭐ |
| OR BELOW_PD_LOW | 275 | `54%` | `43%` | `51%` | `60%` ⭐ | `23%` | `64%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 726 | `49%` | `52%` | `50%` | `54%` | `31%` | `72%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 774 | `49%` | `46%` | `51%` | `51%` | `23%` | `74%` ⭐ |
| ATR Creciente (>10%) | 96 | `51%` | `45%` | `53%` | `45%` | `27%` | `67%` ⭐ |
| ATR Decreciente (<-10%) | 77 | `52%` | `52%` | `52%` | `59%` | `31%` | `75%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 544 | `50%` | `52%` | `49%` | `52%` | `28%` | `69%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 511 | `51%` | `42%` | `51%` | `52%` | `21%` | `70%` ⭐ |
| RSI Diario < 35 | 247 | `54%` | `49%` | `47%` | `60%` | `23%` | `69%` ⭐ |
| RSI Diario > 65 | 233 | `45%` | `47%` | `52%` | `49%` | `22%` | `68%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `248 min` | `225 min` | `360 min` |
| TP DOWN (desde entrada) | `241 min` | `225 min` | `375 min` |
| False Break UP → SL | `174 min` | - | - |
| False Break DOWN → SL | `167 min` | - | - |

---

## Permutación #5: NY 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1807`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.04%`
- **Rotura Bajista (DOWN):** `45.66%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `66.95%` | `65.70%` |
| 1.5x Rango OR | `53.25%` | `52.61%` |
| 2.0x Rango OR | `41.35%` | `41.33%` |
| 1.0x Volatilidad ATR Diaria | `4.21%` | `4.85%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `47.96%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `52.24%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `41.89%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `38.74%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `34.53%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1370`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `34.89%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `25.47%` |
| Shakeout & Re-breakout UP (>=2x OR) | `19.49%` |
| Continuacion Bajista (>=1x OR) | `63.07%` |
| Extension media reversal UP | `1.11x OR` | Mediana: `0.38x` |
| Extension media continuacion DOWN | `2.02x OR` | Mediana: `1.53x` |
| Tiempo medio al re-breakout | `73 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1404`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `35.90%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `28.28%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `22.22%` |
| Continuacion Alcista (>=1x OR) | `61.18%` |
| Extension media reversal DOWN | `1.12x OR` | Mediana: `0.38x` |
| Extension media continuacion UP | `1.97x OR` | Mediana: `1.42x` |
| Tiempo medio al re-breakout | `72 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 134 | `27%` | `44%` | `42%` | `49%` | `37%` | `11%` |
| RSI > 70 (Overbought) | 112 | `66%` ⭐ | `51%` | `45%` | `58%` | `31%` | `15%` |
| RSI 30-70 (Neutro) | 1561 | `46%` | `54%` | `49%` | `52%` | `35%` | `46%` |
| OR ABOVE_PD_HIGH | 421 | `45%` | `53%` | `51%` | `51%` | `31%` | `28%` |
| OR BELOW_PD_LOW | 416 | `47%` | `57%` | `41%` | `49%` | `35%` | `24%` |
| OR BETWEEN_CLOSE_AND_HIGH | 444 | `48%` | `50%` | `50%` | `53%` | `39%` | `55%` |
| OR BETWEEN_LOW_AND_CLOSE | 526 | `45%` | `53%` | `50%` | `55%` | `35%` | `56%` |
| ATR Creciente (>10%) | 85 | `39%` | `48%` | `58%` | `62%` ⭐ | `38%` | `35%` |
| ATR Decreciente (<-10%) | 59 | `44%` | `58%` | `50%` | `55%` | `37%` | `49%` |
| ATR Q1 (Baja Vol Historica) | 484 | `48%` | `50%` | `52%` | `50%` | `34%` | `43%` |
| ATR Q4 (Alta Vol Historica) | 406 | `50%` | `58%` | `43%` | `52%` | `37%` | `43%` |
| RSI Diario < 35 | 222 | `46%` | `56%` | `46%` | `57%` | `36%` | `44%` |
| RSI Diario > 65 | 207 | `47%` | `58%` | `48%` | `60%` | `37%` | `42%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `89 min` | `60 min` | `120 min` |
| TP DOWN (desde entrada) | `87 min` | `60 min` | `135 min` |
| False Break UP → SL | `70 min` | - | - |
| False Break DOWN → SL | `68 min` | - | - |

---

## Permutación #6: NY 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2047`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.39%`
- **Rotura Bajista (DOWN):** `47.68%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `54.23%` | `57.07%` |
| 1.5x Rango OR | `37.73%` | `40.98%` |
| 2.0x Rango OR | `27.11%` | `29.10%` |
| 1.0x Volatilidad ATR Diaria | `4.02%` | `3.38%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `44.43%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `47.03%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `39.57%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `36.05%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `32.88%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1493`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `21.70%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `15.47%` |
| Shakeout & Re-breakout UP (>=2x OR) | `10.98%` |
| Continuacion Bajista (>=1x OR) | `52.98%` |
| Extension media reversal UP | `0.65x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.47x OR` | Mediana: `1.10x` |
| Tiempo medio al re-breakout | `88 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1513`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `23.86%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `16.39%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `11.30%` |
| Continuacion Alcista (>=1x OR) | `48.58%` |
| Extension media reversal DOWN | `0.68x OR` | Mediana: `0.02x` |
| Extension media continuacion UP | `1.41x OR` | Mediana: `0.97x` |
| Tiempo medio al re-breakout | `87 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 141 | `27%` | `37%` | `29%` | `42%` | `19%` | `13%` |
| RSI > 70 (Overbought) | 130 | `71%` ⭐ | `25%` | `37%` | `56%` | `24%` | `13%` |
| RSI 30-70 (Neutro) | 1776 | `47%` | `39%` | `46%` | `47%` | `22%` | `44%` |
| OR ABOVE_PD_HIGH | 495 | `46%` | `35%` | `48%` | `49%` | `22%` | `26%` |
| OR BELOW_PD_LOW | 471 | `49%` | `40%` | `40%` | `44%` | `19%` | `23%` |
| OR BETWEEN_CLOSE_AND_HIGH | 503 | `45%` | `38%` | `44%` | `46%` | `26%` | `53%` |
| OR BETWEEN_LOW_AND_CLOSE | 578 | `49%` | `38%` | `46%` | `48%` | `20%` | `53%` |
| ATR Creciente (>10%) | 95 | `46%` | `36%` | `50%` | `62%` ⭐ | `23%` | `37%` |
| ATR Decreciente (<-10%) | 74 | `43%` | `31%` | `56%` | `50%` | `20%` | `45%` |
| ATR Q1 (Baja Vol Historica) | 530 | `46%` | `40%` | `45%` | `48%` | `21%` | `40%` |
| ATR Q4 (Alta Vol Historica) | 487 | `51%` | `36%` | `42%` | `49%` | `23%` | `42%` |
| RSI Diario < 35 | 242 | `44%` | `41%` | `42%` | `50%` | `21%` | `43%` |
| RSI Diario > 65 | 225 | `51%` | `38%` | `49%` | `45%` | `19%` | `38%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `120 min` | `75 min` | `210 min` |
| TP DOWN (desde entrada) | `112 min` | `75 min` | `180 min` |
| False Break UP → SL | `98 min` | - | - |
| False Break DOWN → SL | `93 min` | - | - |

---

## Permutación #7: NY 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2068`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.94%`
- **Rotura Bajista (DOWN):** `48.94%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `42.39%` | `43.58%` |
| 1.5x Rango OR | `27.67%` | `28.46%` |
| 2.0x Rango OR | `16.90%` | `17.49%` |
| 1.0x Volatilidad ATR Diaria | `2.77%` | `3.26%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `38.44%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `38.24%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `37.77%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `34.86%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `30.75%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1417`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `13.62%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `8.47%` |
| Shakeout & Re-breakout UP (>=2x OR) | `5.15%` |
| Continuacion Bajista (>=1x OR) | `41.50%` |
| Extension media reversal UP | `0.40x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.13x OR` | Mediana: `0.80x` |
| Tiempo medio al re-breakout | `102 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1408`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `15.20%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `9.73%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `5.68%` |
| Continuacion Alcista (>=1x OR) | `38.49%` |
| Extension media reversal DOWN | `0.43x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.06x OR` | Mediana: `0.74x` |
| Tiempo medio al re-breakout | `99 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 148 | `15%` | `18%` | `27%` | `34%` | `8%` | `10%` |
| RSI > 70 (Overbought) | 120 | `72%` ⭐ | `11%` | `36%` | `34%` | `10%` | `13%` |
| RSI 30-70 (Neutro) | 1800 | `50%` | `29%` | `39%` | `39%` | `14%` | `42%` |
| OR ABOVE_PD_HIGH | 503 | `46%` | `27%` | `39%` | `40%` | `13%` | `25%` |
| OR BELOW_PD_LOW | 474 | `48%` | `27%` | `33%` | `38%` | `10%` | `22%` |
| OR BETWEEN_CLOSE_AND_HIGH | 510 | `48%` | `28%` | `40%` | `39%` | `18%` | `51%` |
| OR BETWEEN_LOW_AND_CLOSE | 581 | `52%` | `28%` | `41%` | `35%` | `13%` | `50%` |
| ATR Creciente (>10%) | 97 | `48%` | `32%` | `49%` | `49%` | `16%` | `36%` |
| ATR Decreciente (<-10%) | 74 | `38%` | `18%` | `46%` | `45%` | `12%` | `42%` |
| ATR Q1 (Baja Vol Historica) | 526 | `48%` | `25%` | `41%` | `37%` | `13%` | `38%` |
| ATR Q4 (Alta Vol Historica) | 500 | `51%` | `26%` | `41%` | `45%` | `15%` | `40%` |
| RSI Diario < 35 | 244 | `48%` | `32%` | `34%` | `38%` | `15%` | `42%` |
| RSI Diario > 65 | 229 | `48%` | `31%` | `42%` | `33%` | `14%` | `38%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `150 min` | `105 min` | `240 min` |
| TP DOWN (desde entrada) | `134 min` | `90 min` | `210 min` |
| False Break UP → SL | `107 min` | - | - |
| False Break DOWN → SL | `110 min` | - | - |

---

## Permutación #8: NY 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2048`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.27%`
- **Rotura Bajista (DOWN):** `47.75%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `34.59%` | `37.63%` |
| 1.5x Rango OR | `21.31%` | `19.43%` |
| 2.0x Rango OR | `12.49%` | `11.66%` |
| 1.0x Volatilidad ATR Diaria | `2.38%` | `2.45%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `33.10%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `32.52%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `36.87%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `33.54%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `29.69%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1317`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `9.72%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `5.69%` |
| Shakeout & Re-breakout UP (>=2x OR) | `3.26%` |
| Continuacion Bajista (>=1x OR) | `35.46%` |
| Extension media reversal UP | `0.29x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.94x OR` | Mediana: `0.68x` |
| Tiempo medio al re-breakout | `108 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1322`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `10.97%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `6.20%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `3.48%` |
| Continuacion Alcista (>=1x OR) | `31.69%` |
| Extension media reversal DOWN | `0.31x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.91x OR` | Mediana: `0.63x` |
| Tiempo medio al re-breakout | `106 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 146 | `18%` | `4%` | `31%` | `25%` | `4%` | `6%` |
| RSI > 70 (Overbought) | 128 | `80%` ⭐ | `7%` | `31%` | `15%` | `4%` | `12%` |
| RSI 30-70 (Neutro) | 1774 | `50%` | `24%` | `33%` | `34%` | `11%` | `41%` |
| OR ABOVE_PD_HIGH | 496 | `49%` | `23%` | `32%` | `33%` | `9%` | `23%` |
| OR BELOW_PD_LOW | 471 | `49%` | `19%` | `27%` | `31%` | `6%` | `22%` |
| OR BETWEEN_CLOSE_AND_HIGH | 503 | `47%` | `23%` | `34%` | `34%` | `13%` | `51%` |
| OR BETWEEN_LOW_AND_CLOSE | 578 | `52%` | `20%` | `38%` | `32%` | `10%` | `48%` |
| ATR Creciente (>10%) | 94 | `46%` | `23%` | `44%` | `43%` | `10%` | `35%` |
| ATR Decreciente (<-10%) | 73 | `45%` | `15%` | `36%` | `39%` | `4%` | `41%` |
| ATR Q1 (Baja Vol Historica) | 516 | `48%` | `20%` | `33%` | `32%` | `9%` | `37%` |
| ATR Q4 (Alta Vol Historica) | 498 | `51%` | `22%` | `38%` | `40%` | `13%` | `39%` |
| RSI Diario < 35 | 239 | `51%` | `28%` | `30%` | `33%` | `7%` | `41%` |
| RSI Diario > 65 | 224 | `48%` | `20%` | `37%` | `31%` | `9%` | `37%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `151 min` | `105 min` | `255 min` |
| TP DOWN (desde entrada) | `148 min` | `120 min` | `225 min` |
| False Break UP → SL | `118 min` | - | - |
| False Break DOWN → SL | `129 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: GBPUSD

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST UP] London (15m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `80.77%` (base: `69.41%`, +11%pp). N=54. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (30m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `83.87%` (base: `63.49%`, +20%pp). N=66. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (45m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `68.42%` (base: `55.63%`, +13%pp). N=74. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `73.16%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `73.09%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `72.07%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `70.50%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] London (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `62.46%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `62.08%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `60.84%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `60.00%` de los eventos evaluados.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `68.07%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `62.32%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `69.41%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `63.49%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=428 | UP: `50%` | Ext 1.5 UP: `79%` | Falsa Ruptura DW: `54%` | Reversión a PD_Close: `75%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=429 | UP: `49%` | Ext 1.5 UP: `58%` | Falsa Ruptura DW: `53%` | Reversión a PD_Close: `68%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=158 | UP: `49%` | Ext 1.5 UP: `69%` | Falsa Ruptura DW: `55%` | Reversión a PD_Close: `77%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1552 | UP: `48%` | Ext 1.5 UP: `69%` | Falsa Ruptura DW: `55%` | Reversión a PD_Close: `73%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*