# 🌐 Matriz Probabilística Omnidireccional: SP500

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **Pre-Market 15m**](#permutación-1-pre-market-15m)
- [Permutación #2: **Pre-Market 30m**](#permutación-2-pre-market-30m)
- [Permutación #3: **Pre-Market 45m**](#permutación-3-pre-market-45m)
- [Permutación #4: **Pre-Market 60m**](#permutación-4-pre-market-60m)
- [Permutación #5: **NY Cash 15m**](#permutación-5-ny-cash-15m)
- [Permutación #6: **NY Cash 30m**](#permutación-6-ny-cash-30m)
- [Permutación #7: **NY Cash 45m**](#permutación-7-ny-cash-45m)
- [Permutación #8: **NY Cash 60m**](#permutación-8-ny-cash-60m)

---
## Permutación #1: Pre-Market 15m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `729`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.48%`
- **Rotura Bajista (DOWN):** `44.86%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `83.42%` | `83.49%` |
| 1.5x Rango OR | `73.37%` | `74.01%` |
| 2.0x Rango OR | `65.49%` | `65.44%` |
| 1.0x Volatilidad ATR Diaria | `16.03%` | `21.10%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `61.68%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.43%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.80%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `55.01%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.31%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `586`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `65.19%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `57.17%` |
| Shakeout & Re-breakout UP (>=2x OR) | `50.17%` |
| Continuacion Bajista (>=1x OR) | `81.06%` |
| Extension media reversal UP | `2.91x OR` | Mediana: `2.04x` |
| Extension media continuacion DOWN | `4.25x OR` | Mediana: `3.14x` |
| Tiempo medio al re-breakout | `82 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `580`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `65.00%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `56.72%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `50.52%` |
| Continuacion Alcista (>=1x OR) | `81.21%` |
| Extension media reversal DOWN | `3.41x OR` | Mediana: `2.10x` |
| Extension media continuacion UP | `3.75x OR` | Mediana: `3.12x` |
| Tiempo medio al re-breakout | `79 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 62 | `32%` | `80%` ⭐ | `70%` ⭐ | `40%` | `57%` | `42%` |
| RSI > 70 (Overbought) | 36 | `83%` ⭐ | `63%` ⭐ | `67%` ⭐ | `60%` ⭐ | `50%` | `47%` |
| RSI 30-70 (Neutro) | 631 | `50%` | `74%` ⭐ | `61%` ⭐ | `56%` | `67%` ⭐ | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 97 | `56%` | `74%` ⭐ | `52%` | `55%` | `60%` ⭐ | `53%` |
| OR BELOW_PD_LOW | 173 | `51%` | `70%` ⭐ | `62%` ⭐ | `55%` | `64%` ⭐ | `49%` |
| OR BETWEEN_CLOSE_AND_HIGH | 215 | `44%` | `77%` ⭐ | `60%` | `58%` | `68%` ⭐ | `76%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 244 | `54%` | `73%` ⭐ | `67%` ⭐ | `50%` | `66%` ⭐ | `77%` ⭐ |
| ATR Creciente (>10%) | 96 | `48%` | `80%` ⭐ | `74%` ⭐ | `60%` ⭐ | `76%` ⭐ | `78%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 195 | `53%` | `71%` ⭐ | `57%` | `55%` | `64%` ⭐ | `65%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 176 | `45%` | `66%` ⭐ | `68%` ⭐ | `51%` | `58%` | `66%` ⭐ |
| RSI Diario < 35 | 79 | `47%` | `68%` ⭐ | `70%` ⭐ | `50%` | `68%` ⭐ | `72%` ⭐ |
| RSI Diario > 65 | 119 | `50%` | `68%` ⭐ | `59%` | `45%` | `55%` | `69%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `119 min` | `90 min` | `165 min` |
| TP DOWN (desde entrada) | `114 min` | `82 min` | `165 min` |
| False Break UP → SL | `63 min` | - | - |
| False Break DOWN → SL | `58 min` | - | - |

---

## Permutación #2: Pre-Market 30m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1272`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.62%`
- **Rotura Bajista (DOWN):** `45.99%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.27%` | `78.97%` |
| 1.5x Rango OR | `71.50%` | `69.23%` |
| 2.0x Rango OR | `63.58%` | `61.20%` |
| 1.0x Volatilidad ATR Diaria | `12.65%` | `17.44%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.65%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.19%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `67.92%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.23%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.44%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `995`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `59.60%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `51.76%` |
| Shakeout & Re-breakout UP (>=2x OR) | `43.22%` |
| Continuacion Bajista (>=1x OR) | `75.58%` |
| Extension media reversal UP | `2.31x OR` | Mediana: `1.58x` |
| Extension media continuacion DOWN | `3.46x OR` | Mediana: `2.49x` |
| Tiempo medio al re-breakout | `82 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `989`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `56.02%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `47.42%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `42.06%` |
| Continuacion Alcista (>=1x OR) | `78.97%` |
| Extension media reversal DOWN | `2.57x OR` | Mediana: `1.37x` |
| Extension media continuacion UP | `3.21x OR` | Mediana: `2.53x` |
| Tiempo medio al re-breakout | `85 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 74 | `19%` | `86%` ⭐ | `50%` | `56%` | `53%` | `45%` |
| RSI > 70 (Overbought) | 63 | `73%` ⭐ | `70%` ⭐ | `52%` | `50%` | `51%` | `52%` |
| RSI 30-70 (Neutro) | 1135 | `47%` | `71%` ⭐ | `56%` | `54%` | `60%` ⭐ | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 212 | `57%` | `70%` ⭐ | `52%` | `46%` | `51%` | `54%` |
| OR BELOW_PD_LOW | 247 | `47%` | `70%` ⭐ | `58%` | `53%` | `59%` | `52%` |
| OR BETWEEN_CLOSE_AND_HIGH | 401 | `41%` | `75%` ⭐ | `52%` | `54%` | `62%` ⭐ | `76%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 412 | `46%` | `71%` ⭐ | `60%` | `58%` | `61%` ⭐ | `77%` ⭐ |
| ATR Creciente (>10%) | 120 | `38%` | `67%` ⭐ | `69%` ⭐ | `70%` ⭐ | `65%` ⭐ | `79%` ⭐ |
| ATR Decreciente (<-10%) | 40 | `50%` | `65%` ⭐ | `60%` ⭐ | `69%` ⭐ | `58%` | `60%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 337 | `48%` | `72%` ⭐ | `57%` | `60%` | `59%` | `69%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 303 | `43%` | `70%` ⭐ | `57%` | `47%` | `56%` | `68%` ⭐ |
| RSI Diario < 35 | 105 | `45%` | `74%` ⭐ | `62%` ⭐ | `56%` | `62%` ⭐ | `69%` ⭐ |
| RSI Diario > 65 | 243 | `49%` | `68%` ⭐ | `60%` ⭐ | `52%` | `52%` | `73%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `119 min` | `82 min` | `165 min` |
| TP DOWN (desde entrada) | `120 min` | `90 min` | `165 min` |
| False Break UP → SL | `71 min` | - | - |
| False Break DOWN → SL | `63 min` | - | - |

---

## Permutación #3: Pre-Market 45m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1685`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.91%`
- **Rotura Bajista (DOWN):** `47.30%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `71.34%` | `72.27%` |
| 1.5x Rango OR | `60.29%` | `58.47%` |
| 2.0x Rango OR | `50.18%` | `49.31%` |
| 1.0x Volatilidad ATR Diaria | `10.46%` | `14.68%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.65%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.60%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.65%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `56.26%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.50%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1308`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `47.48%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `39.22%` |
| Shakeout & Re-breakout UP (>=2x OR) | `32.26%` |
| Continuacion Bajista (>=1x OR) | `70.49%` |
| Extension media reversal UP | `1.64x OR` | Mediana: `0.90x` |
| Extension media continuacion DOWN | `2.91x OR` | Mediana: `1.96x` |
| Tiempo medio al re-breakout | `89 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1361`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `47.61%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `38.72%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `32.55%` |
| Continuacion Alcista (>=1x OR) | `70.10%` |
| Extension media reversal DOWN | `1.94x OR` | Mediana: `0.87x` |
| Extension media continuacion UP | `2.45x OR` | Mediana: `1.89x` |
| Tiempo medio al re-breakout | `87 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 94 | `16%` | `53%` | `53%` | `52%` | `32%` | `38%` |
| RSI > 70 (Overbought) | 118 | `81%` ⭐ | `44%` | `53%` | `50%` | `36%` | `46%` |
| RSI 30-70 (Neutro) | 1473 | `50%` | `63%` ⭐ | `56%` | `61%` ⭐ | `49%` | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 334 | `50%` | `63%` ⭐ | `53%` | `47%` | `45%` | `56%` |
| OR BELOW_PD_LOW | 282 | `49%` | `63%` ⭐ | `60%` ⭐ | `57%` | `49%` | `51%` |
| OR BETWEEN_CLOSE_AND_HIGH | 551 | `51%` | `58%` | `55%` | `67%` ⭐ | `47%` | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 518 | `50%` | `60%` | `56%` | `61%` ⭐ | `49%` | `75%` ⭐ |
| ATR Creciente (>10%) | 130 | `58%` | `61%` ⭐ | `59%` | `70%` ⭐ | `48%` | `78%` ⭐ |
| ATR Decreciente (<-10%) | 75 | `41%` | `52%` | `61%` ⭐ | `68%` ⭐ | `56%` | `63%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 449 | `50%` | `63%` ⭐ | `53%` | `60%` ⭐ | `47%` | `69%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 405 | `46%` | `62%` ⭐ | `56%` | `57%` | `47%` | `66%` ⭐ |
| RSI Diario < 35 | 118 | `47%` | `64%` ⭐ | `61%` ⭐ | `67%` ⭐ | `54%` | `67%` ⭐ |
| RSI Diario > 65 | 359 | `49%` | `60%` | `56%` | `55%` | `44%` | `72%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `141 min` | `105 min` | `225 min` |
| TP DOWN (desde entrada) | `137 min` | `90 min` | `225 min` |
| False Break UP → SL | `72 min` | - | - |
| False Break DOWN → SL | `72 min` | - | - |

---

## Permutación #4: Pre-Market 60m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1809`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.81%`
- **Rotura Bajista (DOWN):** `46.32%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.15%` | `70.17%` |
| 1.5x Rango OR | `57.71%` | `56.32%` |
| 2.0x Rango OR | `48.06%` | `48.33%` |
| 1.0x Volatilidad ATR Diaria | `9.77%` | `15.04%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `52.94%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.64%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `65.67%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `56.05%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.81%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1376`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `42.44%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `34.01%` |
| Shakeout & Re-breakout UP (>=2x OR) | `26.82%` |
| Continuacion Bajista (>=1x OR) | `68.68%` |
| Extension media reversal UP | `1.35x OR` | Mediana: `0.70x` |
| Extension media continuacion DOWN | `2.70x OR` | Mediana: `1.79x` |
| Tiempo medio al re-breakout | `89 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1448`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `43.99%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `34.74%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `28.87%` |
| Continuacion Alcista (>=1x OR) | `66.09%` |
| Extension media reversal DOWN | `1.66x OR` | Mediana: `0.63x` |
| Extension media continuacion UP | `2.17x OR` | Mediana: `1.69x` |
| Tiempo medio al re-breakout | `85 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 98 | `18%` | `50%` | `33%` | `56%` | `20%` | `43%` |
| RSI > 70 (Overbought) | 121 | `79%` ⭐ | `45%` | `45%` | `22%` | `26%` | `46%` |
| RSI 30-70 (Neutro) | 1590 | `49%` | `59%` | `54%` | `59%` | `45%` | `69%` ⭐ |
| OR ABOVE_PD_HIGH | 375 | `47%` | `60%` | `52%` | `48%` | `42%` | `56%` |
| OR BELOW_PD_LOW | 291 | `49%` | `61%` ⭐ | `53%` | `56%` | `43%` | `50%` |
| OR BETWEEN_CLOSE_AND_HIGH | 593 | `51%` | `57%` | `52%` | `63%` ⭐ | `42%` | `72%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 550 | `51%` | `56%` | `54%` | `61%` ⭐ | `43%` | `73%` ⭐ |
| ATR Creciente (>10%) | 131 | `53%` | `58%` | `55%` | `69%` ⭐ | `46%` | `77%` ⭐ |
| ATR Decreciente (<-10%) | 86 | `45%` | `49%` | `62%` ⭐ | `67%` ⭐ | `52%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 482 | `50%` | `55%` | `52%` | `56%` | `44%` | `67%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 431 | `45%` | `57%` | `53%` | `57%` | `40%` | `65%` ⭐ |
| RSI Diario < 35 | 118 | `47%` | `62%` ⭐ | `57%` | `68%` ⭐ | `50%` | `66%` ⭐ |
| RSI Diario > 65 | 390 | `51%` | `57%` | `54%` | `51%` | `38%` | `72%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `140 min` | `90 min` | `240 min` |
| TP DOWN (desde entrada) | `132 min` | `90 min` | `225 min` |
| False Break UP → SL | `67 min` | - | - |
| False Break DOWN → SL | `74 min` | - | - |

---

## Permutación #5: NY Cash 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1733`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.97%`
- **Rotura Bajista (DOWN):** `46.39%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.18%` | `68.78%` |
| 1.5x Rango OR | `54.79%` | `54.10%` |
| 2.0x Rango OR | `42.87%` | `44.15%` |
| 1.0x Volatilidad ATR Diaria | `9.58%` | `15.55%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `48.77%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.98%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.57%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `52.22%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.89%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1309`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `37.05%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `28.04%` |
| Shakeout & Re-breakout UP (>=2x OR) | `21.54%` |
| Continuacion Bajista (>=1x OR) | `64.32%` |
| Extension media reversal UP | `1.20x OR` | Mediana: `0.46x` |
| Extension media continuacion DOWN | `2.39x OR` | Mediana: `1.50x` |
| Tiempo medio al re-breakout | `95 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1353`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `36.22%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `27.27%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `21.73%` |
| Continuacion Alcista (>=1x OR) | `62.31%` |
| Extension media reversal DOWN | `1.37x OR` | Mediana: `0.34x` |
| Extension media continuacion UP | `1.95x OR` | Mediana: `1.46x` |
| Tiempo medio al re-breakout | `91 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 147 | `20%` | `41%` | `59%` | `52%` | `28%` | `41%` |
| RSI > 70 (Overbought) | 187 | `70%` ⭐ | `53%` | `44%` | `57%` | `20%` | `36%` |
| RSI 30-70 (Neutro) | 1399 | `47%` | `56%` | `49%` | `54%` | `40%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 402 | `48%` | `52%` | `50%` | `52%` | `33%` | `52%` |
| OR BELOW_PD_LOW | 272 | `47%` | `62%` ⭐ | `39%` | `55%` | `40%` | `45%` |
| OR BETWEEN_CLOSE_AND_HIGH | 549 | `49%` | `55%` | `53%` | `49%` | `38%` | `68%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 510 | `44%` | `53%` | `48%` | `60%` | `38%` | `71%` ⭐ |
| ATR Creciente (>10%) | 123 | `46%` | `57%` | `57%` | `51%` | `49%` | `74%` ⭐ |
| ATR Decreciente (<-10%) | 79 | `41%` | `53%` | `44%` | `65%` ⭐ | `34%` | `58%` |
| ATR Q1 (Baja Vol Historica) | 451 | `47%` | `50%` | `53%` | `54%` | `32%` | `63%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 423 | `44%` | `55%` | `46%` | `57%` | `43%` | `60%` |
| RSI Diario < 35 | 122 | `50%` | `56%` | `54%` | `47%` | `43%` | `66%` ⭐ |
| RSI Diario > 65 | 366 | `47%` | `51%` | `53%` | `59%` | `30%` | `67%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `139 min` | `90 min` | `270 min` |
| TP DOWN (desde entrada) | `109 min` | `60 min` | `195 min` |
| False Break UP → SL | `84 min` | - | - |
| False Break DOWN → SL | `91 min` | - | - |

---

## Permutación #6: NY Cash 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1874`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.15%`
- **Rotura Bajista (DOWN):** `47.44%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `56.35%` | `59.51%` |
| 1.5x Rango OR | `42.35%` | `44.99%` |
| 2.0x Rango OR | `29.10%` | `34.87%` |
| 1.0x Volatilidad ATR Diaria | `7.38%` | `14.29%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `46.36%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `50.84%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `60.57%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `50.96%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `40.66%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1365`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `28.79%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `20.88%` |
| Shakeout & Re-breakout UP (>=2x OR) | `15.46%` |
| Continuacion Bajista (>=1x OR) | `55.60%` |
| Extension media reversal UP | `0.94x OR` | Mediana: `0.17x` |
| Extension media continuacion DOWN | `1.97x OR` | Mediana: `1.16x` |
| Tiempo medio al re-breakout | `104 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1426`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `27.70%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `20.41%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `16.20%` |
| Continuacion Alcista (>=1x OR) | `52.95%` |
| Extension media reversal DOWN | `1.03x OR` | Mediana: `0.02x` |
| Extension media continuacion UP | `1.62x OR` | Mediana: `1.10x` |
| Tiempo medio al re-breakout | `101 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 148 | `16%` | `46%` | `33%` | `45%` | `18%` | `41%` |
| RSI > 70 (Overbought) | 212 | `83%` ⭐ | `38%` | `38%` | `39%` | `14%` | `29%` |
| RSI 30-70 (Neutro) | 1514 | `48%` | `43%` | `49%` | `52%` | `31%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 451 | `49%` | `41%` | `47%` | `47%` | `25%` | `50%` |
| OR BELOW_PD_LOW | 285 | `52%` | `44%` | `43%` | `48%` | `34%` | `45%` |
| OR BETWEEN_CLOSE_AND_HIGH | 590 | `48%` | `46%` | `50%` | `51%` | `30%` | `67%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 548 | `49%` | `39%` | `44%` | `55%` | `29%` | `70%` ⭐ |
| ATR Creciente (>10%) | 126 | `43%` | `50%` | `54%` | `61%` ⭐ | `44%` | `72%` ⭐ |
| ATR Decreciente (<-10%) | 87 | `47%` | `37%` | `44%` | `55%` | `20%` | `59%` |
| ATR Q1 (Baja Vol Historica) | 482 | `47%` | `42%` | `45%` | `51%` | `27%` | `62%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 458 | `49%` | `40%` | `42%` | `52%` | `32%` | `59%` |
| RSI Diario < 35 | 125 | `48%` | `43%` | `47%` | `48%` | `35%` | `65%` ⭐ |
| RSI Diario > 65 | 399 | `49%` | `40%` | `51%` | `51%` | `25%` | `65%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `162 min` | `120 min` | `285 min` |
| TP DOWN (desde entrada) | `131 min` | `90 min` | `240 min` |
| False Break UP → SL | `111 min` | - | - |
| False Break DOWN → SL | `101 min` | - | - |

---

## Permutación #7: NY Cash 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1911`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.70%`
- **Rotura Bajista (DOWN):** `45.53%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `48.58%` | `53.22%` |
| 1.5x Rango OR | `31.48%` | `37.93%` |
| 2.0x Rango OR | `20.45%` | `28.97%` |
| 1.0x Volatilidad ATR Diaria | `6.48%` | `13.56%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `43.22%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `46.44%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `58.77%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `48.67%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `39.32%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1327`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `24.72%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `17.33%` |
| Shakeout & Re-breakout UP (>=2x OR) | `12.28%` |
| Continuacion Bajista (>=1x OR) | `51.24%` |
| Extension media reversal UP | `0.76x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.73x OR` | Mediana: `1.03x` |
| Tiempo medio al re-breakout | `105 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1421`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `23.57%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `17.17%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `13.44%` |
| Continuacion Alcista (>=1x OR) | `47.43%` |
| Extension media reversal DOWN | `0.83x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.39x OR` | Mediana: `0.94x` |
| Tiempo medio al re-breakout | `103 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 157 | `17%` | `26%` | `41%` | `41%` | `13%` | `38%` |
| RSI > 70 (Overbought) | 230 | `85%` ⭐ | `24%` | `34%` | `38%` | `9%` | `32%` |
| RSI 30-70 (Neutro) | 1524 | `50%` | `34%` | `46%` | `48%` | `28%` | `65%` ⭐ |
| OR ABOVE_PD_HIGH | 473 | `51%` | `30%` | `44%` | `43%` | `22%` | `48%` |
| OR BELOW_PD_LOW | 284 | `53%` | `37%` | `38%` | `44%` | `33%` | `45%` |
| OR BETWEEN_CLOSE_AND_HIGH | 599 | `51%` | `31%` | `48%` | `47%` | `24%` | `65%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 555 | `53%` | `30%` | `40%` | `49%` | `24%` | `68%` ⭐ |
| ATR Creciente (>10%) | 125 | `46%` | `31%` | `52%` | `56%` | `35%` | `74%` ⭐ |
| ATR Decreciente (<-10%) | 92 | `50%` | `26%` | `37%` | `52%` | `19%` | `58%` |
| ATR Q1 (Baja Vol Historica) | 488 | `49%` | `32%` | `44%` | `49%` | `24%` | `60%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 480 | `51%` | `31%` | `36%` | `44%` | `28%` | `57%` |
| RSI Diario < 35 | 123 | `47%` | `31%` | `41%` | `47%` | `27%` | `63%` ⭐ |
| RSI Diario > 65 | 413 | `52%` | `31%` | `50%` | `47%` | `21%` | `63%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `174 min` | `150 min` | `300 min` |
| TP DOWN (desde entrada) | `137 min` | `90 min` | `240 min` |
| False Break UP → SL | `112 min` | - | - |
| False Break DOWN → SL | `113 min` | - | - |

---

## Permutación #8: NY Cash 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1902`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.10%`
- **Rotura Bajista (DOWN):** `42.64%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `44.14%` | `50.43%` |
| 1.5x Rango OR | `27.06%` | `33.66%` |
| 2.0x Rango OR | `17.80%` | `25.77%` |
| 1.0x Volatilidad ATR Diaria | `6.38%` | `13.81%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `37.55%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `40.07%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `57.47%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `47.27%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `38.28%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1260`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `20.79%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `13.73%` |
| Shakeout & Re-breakout UP (>=2x OR) | `10.08%` |
| Continuacion Bajista (>=1x OR) | `47.54%` |
| Extension media reversal UP | `0.63x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.56x OR` | Mediana: `0.93x` |
| Tiempo medio al re-breakout | `111 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1380`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `20.58%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `15.36%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `11.81%` |
| Continuacion Alcista (>=1x OR) | `43.04%` |
| Extension media reversal DOWN | `0.71x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.25x OR` | Mediana: `0.84x` |
| Tiempo medio al re-breakout | `106 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 135 | `15%` | `30%` | `45%` | `36%` | `11%` | `34%` |
| RSI > 70 (Overbought) | 208 | `85%` ⭐ | `18%` | `33%` | `24%` | `10%` | `32%` |
| RSI 30-70 (Neutro) | 1559 | `50%` | `29%` | `38%` | `41%` | `23%` | `63%` ⭐ |
| OR ABOVE_PD_HIGH | 477 | `49%` | `26%` | `39%` | `37%` | `19%` | `48%` |
| OR BELOW_PD_LOW | 279 | `52%` | `34%` | `32%` | `37%` | `26%` | `45%` |
| OR BETWEEN_CLOSE_AND_HIGH | 599 | `50%` | `27%` | `40%` | `43%` | `19%` | `62%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 547 | `53%` | `25%` | `37%` | `41%` | `22%` | `67%` ⭐ |
| ATR Creciente (>10%) | 122 | `48%` | `24%` | `47%` | `53%` | `34%` | `75%` ⭐ |
| ATR Decreciente (<-10%) | 92 | `51%` | `17%` | `34%` | `42%` | `17%` | `58%` |
| ATR Q1 (Baja Vol Historica) | 479 | `50%` | `28%` | `38%` | `44%` | `20%` | `59%` |
| ATR Q4 (Alta Vol Historica) | 484 | `49%` | `27%` | `32%` | `38%` | `24%` | `56%` |
| RSI Diario < 35 | 120 | `49%` | `27%` | `39%` | `46%` | `24%` | `63%` ⭐ |
| RSI Diario > 65 | 413 | `52%` | `29%` | `43%` | `39%` | `17%` | `63%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `171 min` | `150 min` | `300 min` |
| TP DOWN (desde entrada) | `140 min` | `105 min` | `255 min` |
| False Break UP → SL | `125 min` | - | - |
| False Break DOWN → SL | `134 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: SP500

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] NY Cash (15m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `67.80%` (base: `54.10%`, +14%pp). N=123.

- **[EDGE CONTEXT-BOOST DOWN] NY Cash (15m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `69.09%` (base: `54.10%`, +15%pp). N=122.

- **[EDGE CONTEXT-BOOST DOWN] NY Cash (30m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `60.94%` (base: `44.99%`, +16%pp). N=125.

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (15m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `91.67%` (base: `74.01%`, +18%pp). N=79.

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (30m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `87.04%` (base: `69.23%`, +18%pp). N=105.

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (45m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `68.85%` (base: `58.47%`, +10%pp). N=118.

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (60m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `67.80%` (base: `56.32%`, +11%pp). N=118.

- **[EDGE CONTEXT-BOOST UP] Pre-Market (30m) | RSI < 30 (Oversold)**: Extension 1.5x UP sube a `85.71%` (base: `71.50%`, +14%pp). N=74. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE FADE-BREAKOUT] Pre-Market (15m)**: Trampa de Liquidez Alcista del `61.68%`. Cada vez que rompe al alza, termina invalidándose devorando el OR Low. Sugerencia Algo: Stop-Limit en contra de falsos quiebres (Atrapar inversores manuales).

- **[EDGE MAGNET PD_CLOSE] NY Cash (15m)**: Imantación cíclica brutal. El `61.57%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] NY Cash (30m)**: Imantación cíclica brutal. El `60.57%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (15m)**: Imantación cíclica brutal. El `66.80%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (30m)**: Imantación cíclica brutal. El `67.92%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (45m)**: Imantación cíclica brutal. El `66.65%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (60m)**: Imantación cíclica brutal. El `65.67%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE RSI-CONDITIONAL] Pre-Market (15m) | RSI 30-70 (Neutro)**: Shakeout UP post-fade al `66.87%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=631.

- **[EDGE RSI-CONDITIONAL] Pre-Market (15m) | RSI Diario < 35**: Shakeout UP post-fade al `67.65%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=79.

- **[EDGE RSI-CONDITIONAL] Pre-Market (30m) | RSI 30-70 (Neutro)**: Shakeout UP post-fade al `60.47%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=1135.

- **[EDGE RSI-CONDITIONAL] Pre-Market (30m) | RSI Diario < 35**: Shakeout UP post-fade al `61.63%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=105.

- **[EDGE SHAKEOUT-REVERSAL DOWN] Pre-Market (15m)**: Despues de un falso rompimiento bajista, el `65.00%` retoma direccion DOWN con extension >=1x OR. Media reversal: `3.41x OR` | Tiempo medio al re-breakout: 79 min. Sugerencia Algo: Orden limite de VENTA en OR_High tras primer rompimiento DOWN.

- **[EDGE SHAKEOUT-REVERSAL UP] Pre-Market (15m)**: Despues de un falso rompimiento alcista, el `65.19%` de las veces el precio retoma la direccion UP con extension >=1x OR. Media reversal: `2.91x OR` | Tiempo medio al re-breakout: 82 min. Sugerencia Algo: Orden limite de COMPRA en OR_Low tras primer rompimiento UP. El mercado barre stops y luego arranca.

- **[EDGE TENDENCIAL DOWN] Pre-Market (15m)**: Tasa de extensión polar bajista (1.5x) del `74.01%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Pre-Market (30m)**: Tasa de extensión polar bajista (1.5x) del `69.23%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] Pre-Market (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `73.37%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `71.50%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.29%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Pre-Market 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=183 | UP: `52%` | Ext 1.5 UP: `77%` | Falsa Ruptura DW: `52%` | Reversión a PD_Close: `66%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=183 | UP: `43%` | Ext 1.5 UP: `65%` | Falsa Ruptura DW: `48%` | Reversión a PD_Close: `64%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=32 | UP: `59%` | Ext 1.5 UP: `79%` | Falsa Ruptura DW: `15%` | Reversión a PD_Close: `50%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=697 | UP: `50%` | Ext 1.5 UP: `73%` | Falsa Ruptura DW: `56%` | Reversión a PD_Close: `68%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*