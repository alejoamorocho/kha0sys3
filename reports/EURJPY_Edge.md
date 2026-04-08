# 🌐 Matriz Probabilística Omnidireccional: EURJPY

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **Tokyo 15m**](#permutación-1-tokyo-15m)
- [Permutación #2: **Tokyo 30m**](#permutación-2-tokyo-30m)
- [Permutación #3: **Tokyo 45m**](#permutación-3-tokyo-45m)
- [Permutación #4: **Tokyo 60m**](#permutación-4-tokyo-60m)
- [Permutación #5: **London 15m**](#permutación-5-london-15m)
- [Permutación #6: **London 30m**](#permutación-6-london-30m)
- [Permutación #7: **London 45m**](#permutación-7-london-45m)
- [Permutación #8: **London 60m**](#permutación-8-london-60m)

---
## Permutación #1: Tokyo 15m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1578`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.32%`
- **Rotura Bajista (DOWN):** `47.91%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `82.24%` | `81.61%` |
| 1.5x Rango OR | `72.54%` | `73.41%` |
| 2.0x Rango OR | `64.61%` | `64.15%` |
| 1.0x Volatilidad ATR Diaria | `16.62%` | `17.72%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `56.42%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.47%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `89.35%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `68.57%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `47.88%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1202`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `38.44%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `29.28%` |
| Shakeout & Re-breakout UP (>=2x OR) | `21.30%` |
| Continuacion Bajista (>=1x OR) | `63.64%` |
| Extension media reversal UP | `1.16x OR` | Mediana: `0.56x` |
| Extension media continuacion DOWN | `2.10x OR` | Mediana: `1.51x` |
| Tiempo medio al re-breakout | `139 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1241`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `36.91%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `28.20%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `22.64%` |
| Continuacion Alcista (>=1x OR) | `64.22%` |
| Extension media reversal DOWN | `1.25x OR` | Mediana: `0.44x` |
| Extension media continuacion UP | `2.04x OR` | Mediana: `1.52x` |
| Tiempo medio al re-breakout | `135 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 55 | `22%` | `67%` ⭐ | `50%` | `65%` ⭐ | `29%` | `85%` ⭐ |
| RSI > 70 (Overbought) | 59 | `78%` ⭐ | `67%` ⭐ | `63%` ⭐ | `50%` | `40%` | `86%` ⭐ |
| RSI 30-70 (Neutro) | 1464 | `50%` | `73%` ⭐ | `56%` | `58%` | `39%` | `90%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1041 | `50%` | `70%` ⭐ | `59%` | `57%` | `36%` | `89%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 535 | `51%` | `78%` ⭐ | `51%` | `62%` ⭐ | `43%` | `90%` ⭐ |
| ATR Creciente (>10%) | 77 | `45%` | `77%` ⭐ | `54%` | `56%` | `36%` | `84%` ⭐ |
| ATR Decreciente (<-10%) | 60 | `43%` | `62%` ⭐ | `62%` ⭐ | `62%` ⭐ | `44%` | `97%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 429 | `49%` | `74%` ⭐ | `56%` | `58%` | `35%` | `88%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 352 | `49%` | `71%` ⭐ | `55%` | `54%` | `41%` | `89%` ⭐ |
| RSI Diario < 35 | 126 | `48%` | `80%` ⭐ | `51%` | `44%` | `27%` | `88%` ⭐ |
| RSI Diario > 65 | 211 | `48%` | `70%` ⭐ | `60%` | `54%` | `38%` | `87%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `311 min` | `285 min` | `495 min` |
| TP DOWN (desde entrada) | `317 min` | `225 min` | `555 min` |
| False Break UP → SL | `147 min` | - | - |
| False Break DOWN → SL | `132 min` | - | - |

---

## Permutación #2: Tokyo 30m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1902`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.52%`
- **Rotura Bajista (DOWN):** `46.06%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `76.08%` | `76.83%` |
| 1.5x Rango OR | `66.27%` | `66.78%` |
| 2.0x Rango OR | `55.26%` | `57.19%` |
| 1.0x Volatilidad ATR Diaria | `16.32%` | `16.10%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.56%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.45%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `87.91%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `67.67%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `48.03%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1415`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `30.74%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `20.14%` |
| Shakeout & Re-breakout UP (>=2x OR) | `13.71%` |
| Continuacion Bajista (>=1x OR) | `57.60%` |
| Extension media reversal UP | `0.84x OR` | Mediana: `0.27x` |
| Extension media continuacion DOWN | `1.81x OR` | Mediana: `1.26x` |
| Tiempo medio al re-breakout | `158 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1481`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `30.32%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `21.81%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `16.68%` |
| Continuacion Alcista (>=1x OR) | `58.14%` |
| Extension media reversal DOWN | `1.02x OR` | Mediana: `0.20x` |
| Extension media continuacion UP | `1.69x OR` | Mediana: `1.21x` |
| Tiempo medio al re-breakout | `151 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 69 | `26%` | `44%` | `61%` ⭐ | `63%` ⭐ | `25%` | `83%` ⭐ |
| RSI > 70 (Overbought) | 84 | `86%` ⭐ | `60%` | `58%` | `50%` | `24%` | `76%` ⭐ |
| RSI 30-70 (Neutro) | 1749 | `52%` | `67%` ⭐ | `57%` | `58%` | `31%` | `89%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1255 | `52%` | `65%` ⭐ | `59%` | `57%` | `29%` | `88%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 643 | `54%` | `69%` ⭐ | `55%` | `62%` ⭐ | `34%` | `88%` ⭐ |
| ATR Creciente (>10%) | 83 | `45%` | `68%` ⭐ | `54%` | `61%` ⭐ | `27%` | `83%` ⭐ |
| ATR Decreciente (<-10%) | 71 | `49%` | `60%` ⭐ | `63%` ⭐ | `69%` ⭐ | `31%` | `94%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 491 | `53%` | `64%` ⭐ | `58%` | `60%` ⭐ | `28%` | `87%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 456 | `51%` | `66%` ⭐ | `56%` | `57%` | `34%` | `87%` ⭐ |
| RSI Diario < 35 | 140 | `53%` | `65%` ⭐ | `57%` | `43%` | `21%` | `87%` ⭐ |
| RSI Diario > 65 | 254 | `52%` | `56%` | `62%` ⭐ | `50%` | `30%` | `87%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `358 min` | `345 min` | `555 min` |
| TP DOWN (desde entrada) | `354 min` | `315 min` | `630 min` |
| False Break UP → SL | `184 min` | - | - |
| False Break DOWN → SL | `183 min` | - | - |

---

## Permutación #3: Tokyo 45m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2028`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.97%`
- **Rotura Bajista (DOWN):** `46.06%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `71.82%` | `72.38%` |
| 1.5x Rango OR | `60.53%` | `60.81%` |
| 2.0x Rango OR | `50.76%` | `51.18%` |
| 1.0x Volatilidad ATR Diaria | `15.09%` | `15.85%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.16%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.71%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `87.03%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `67.06%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `47.14%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1487`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `24.21%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `15.87%` |
| Shakeout & Re-breakout UP (>=2x OR) | `9.68%` |
| Continuacion Bajista (>=1x OR) | `53.13%` |
| Extension media reversal UP | `0.67x OR` | Mediana: `0.07x` |
| Extension media continuacion DOWN | `1.60x OR` | Mediana: `1.08x` |
| Tiempo medio al re-breakout | `174 min` | Mediana: `135 min` |

**False Breakouts DOWN analizados:** `1542`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `25.29%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `17.51%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `13.10%` |
| Continuacion Alcista (>=1x OR) | `51.10%` |
| Extension media reversal DOWN | `0.82x OR` | Mediana: `0.03x` |
| Extension media continuacion UP | `1.45x OR` | Mediana: `1.03x` |
| Tiempo medio al re-breakout | `162 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 74 | `19%` | `50%` | `50%` | `65%` ⭐ | `14%` | `77%` ⭐ |
| RSI > 70 (Overbought) | 94 | `89%` ⭐ | `57%` | `55%` | `78%` ⭐ | `20%` | `71%` ⭐ |
| RSI 30-70 (Neutro) | 1860 | `51%` | `61%` ⭐ | `59%` | `57%` | `25%` | `88%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1333 | `51%` | `59%` | `59%` | `56%` | `23%` | `87%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 691 | `54%` | `63%` ⭐ | `57%` | `62%` ⭐ | `27%` | `87%` ⭐ |
| ATR Creciente (>10%) | 82 | `50%` | `59%` | `59%` | `63%` ⭐ | `23%` | `83%` ⭐ |
| ATR Decreciente (<-10%) | 79 | `39%` | `55%` | `61%` ⭐ | `64%` ⭐ | `29%` | `95%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 521 | `50%` | `60%` ⭐ | `57%` | `57%` | `22%` | `87%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 491 | `53%` | `58%` | `57%` | `56%` | `25%` | `86%` ⭐ |
| RSI Diario < 35 | 146 | `53%` | `56%` | `64%` ⭐ | `49%` | `20%` | `86%` ⭐ |
| RSI Diario > 65 | 267 | `51%` | `55%` | `63%` ⭐ | `50%` | `24%` | `85%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `391 min` | `360 min` | `645 min` |
| TP DOWN (desde entrada) | `371 min` | `345 min` | `645 min` |
| False Break UP → SL | `222 min` | - | - |
| False Break DOWN → SL | `230 min` | - | - |

---

## Permutación #4: Tokyo 60m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2083`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.58%`
- **Rotura Bajista (DOWN):** `50.22%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `67.69%` | `66.73%` |
| 1.5x Rango OR | `54.84%` | `54.59%` |
| 2.0x Rango OR | `45.16%` | `44.17%` |
| 1.0x Volatilidad ATR Diaria | `14.62%` | `16.35%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.05%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.55%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `84.54%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `66.15%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.57%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1449`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `16.08%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `9.80%` |
| Shakeout & Re-breakout UP (>=2x OR) | `6.35%` |
| Continuacion Bajista (>=1x OR) | `43.27%` |
| Extension media reversal UP | `0.47x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.29x OR` | Mediana: `0.84x` |
| Tiempo medio al re-breakout | `184 min` | Mediana: `165 min` |

**False Breakouts DOWN analizados:** `1461`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `16.70%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `10.88%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `8.01%` |
| Continuacion Alcista (>=1x OR) | `42.51%` |
| Extension media reversal DOWN | `0.52x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.19x OR` | Mediana: `0.84x` |
| Tiempo medio al re-breakout | `187 min` | Mediana: `165 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 95 | `14%` | `15%` | `62%` ⭐ | `49%` | `4%` | `65%` ⭐ |
| RSI > 70 (Overbought) | 117 | `82%` ⭐ | `38%` | `61%` ⭐ | `45%` | `7%` | `72%` ⭐ |
| RSI 30-70 (Neutro) | 1871 | `48%` | `57%` | `53%` | `58%` | `17%` | `86%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1371 | `47%` | `54%` | `55%` | `56%` | `14%` | `84%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 708 | `51%` | `56%` | `52%` | `60%` ⭐ | `19%` | `85%` ⭐ |
| ATR Creciente (>10%) | 82 | `39%` | `47%` | `50%` | `58%` | `20%` | `82%` ⭐ |
| ATR Decreciente (<-10%) | 82 | `43%` | `54%` | `60%` ⭐ | `67%` ⭐ | `17%` | `88%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 532 | `50%` | `57%` | `51%` | `53%` | `13%` | `85%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 514 | `49%` | `51%` | `55%` | `57%` | `17%` | `83%` ⭐ |
| RSI Diario < 35 | 145 | `50%` | `52%` | `52%` | `49%` | `13%` | `83%` ⭐ |
| RSI Diario > 65 | 274 | `46%` | `50%` | `55%` | `53%` | `16%` | `84%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `429 min` | `390 min` | `675 min` |
| TP DOWN (desde entrada) | `420 min` | `390 min` | `675 min` |
| False Break UP → SL | `285 min` | - | - |
| False Break DOWN → SL | `281 min` | - | - |

---

## Permutación #5: London 15m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1674`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.52%`
- **Rotura Bajista (DOWN):** `44.80%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `77.32%` | `77.07%` |
| 1.5x Rango OR | `67.79%` | `64.40%` |
| 2.0x Rango OR | `56.57%` | `54.00%` |
| 1.0x Volatilidad ATR Diaria | `10.25%` | `11.87%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `56.21%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.53%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `62.54%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `53.70%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.68%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1297`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `48.57%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `37.78%` |
| Shakeout & Re-breakout UP (>=2x OR) | `30.22%` |
| Continuacion Bajista (>=1x OR) | `69.62%` |
| Extension media reversal UP | `1.61x OR` | Mediana: `0.92x` |
| Extension media continuacion DOWN | `2.52x OR` | Mediana: `1.76x` |
| Tiempo medio al re-breakout | `110 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1355`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `46.42%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `37.12%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `30.33%` |
| Continuacion Alcista (>=1x OR) | `71.07%` |
| Extension media reversal DOWN | `1.73x OR` | Mediana: `0.80x` |
| Extension media continuacion UP | `2.39x OR` | Mediana: `1.87x` |
| Tiempo medio al re-breakout | `116 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 116 | `22%` | `77%` ⭐ | `42%` | `52%` | `36%` | `33%` |
| RSI > 70 (Overbought) | 143 | `74%` ⭐ | `62%` ⭐ | `54%` | `44%` | `43%` | `38%` |
| RSI 30-70 (Neutro) | 1415 | `49%` | `68%` ⭐ | `57%` | `60%` ⭐ | `50%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 303 | `52%` | `68%` ⭐ | `56%` | `52%` | `49%` | `51%` |
| OR BELOW_PD_LOW | 278 | `47%` | `70%` ⭐ | `54%` | `63%` ⭐ | `50%` | `45%` |
| OR BETWEEN_CLOSE_AND_HIGH | 529 | `49%` | `67%` ⭐ | `56%` | `65%` ⭐ | `49%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 564 | `51%` | `68%` ⭐ | `58%` | `53%` | `47%` | `70%` ⭐ |
| ATR Creciente (>10%) | 77 | `53%` | `71%` ⭐ | `56%` | `53%` | `46%` | `64%` ⭐ |
| ATR Decreciente (<-10%) | 59 | `51%` | `67%` ⭐ | `50%` | `59%` | `52%` | `68%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 441 | `50%` | `66%` ⭐ | `60%` ⭐ | `56%` | `46%` | `63%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 389 | `54%` | `64%` ⭐ | `57%` | `58%` | `47%` | `65%` ⭐ |
| RSI Diario < 35 | 124 | `46%` | `67%` ⭐ | `58%` | `67%` ⭐ | `52%` | `60%` ⭐ |
| RSI Diario > 65 | 231 | `46%` | `71%` ⭐ | `59%` | `54%` | `43%` | `55%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `190 min` | `120 min` | `345 min` |
| TP DOWN (desde entrada) | `185 min` | `105 min` | `345 min` |
| False Break UP → SL | `95 min` | - | - |
| False Break DOWN → SL | `97 min` | - | - |

---

## Permutación #6: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1979`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.00%`
- **Rotura Bajista (DOWN):** `45.68%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `70.85%` | `69.25%` |
| 1.5x Rango OR | `57.43%` | `54.98%` |
| 2.0x Rango OR | `45.68%` | `45.80%` |
| 1.0x Volatilidad ATR Diaria | `9.72%` | `12.72%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.73%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.19%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.39%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `53.46%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.57%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1513`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `36.75%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `27.10%` |
| Shakeout & Re-breakout UP (>=2x OR) | `19.50%` |
| Continuacion Bajista (>=1x OR) | `60.08%` |
| Extension media reversal UP | `1.11x OR` | Mediana: `0.44x` |
| Extension media continuacion DOWN | `2.01x OR` | Mediana: `1.34x` |
| Tiempo medio al re-breakout | `124 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1563`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `34.87%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `26.23%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `20.73%` |
| Continuacion Alcista (>=1x OR) | `63.53%` |
| Extension media reversal DOWN | `1.19x OR` | Mediana: `0.36x` |
| Extension media continuacion UP | `1.94x OR` | Mediana: `1.44x` |
| Tiempo medio al re-breakout | `133 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 120 | `28%` | `45%` | `55%` | `47%` | `21%` | `31%` |
| RSI > 70 (Overbought) | 168 | `71%` ⭐ | `50%` | `60%` ⭐ | `57%` | `34%` | `40%` |
| RSI 30-70 (Neutro) | 1691 | `52%` | `59%` | `58%` | `58%` | `38%` | `66%` ⭐ |
| OR ABOVE_PD_HIGH | 363 | `50%` | `53%` | `60%` ⭐ | `54%` | `39%` | `50%` |
| OR BELOW_PD_LOW | 307 | `53%` | `58%` | `53%` | `55%` | `37%` | `46%` |
| OR BETWEEN_CLOSE_AND_HIGH | 649 | `53%` | `59%` | `58%` | `62%` ⭐ | `37%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 660 | `52%` | `58%` | `58%` | `55%` | `35%` | `67%` ⭐ |
| ATR Creciente (>10%) | 84 | `54%` | `60%` ⭐ | `58%` | `46%` | `40%` | `55%` |
| ATR Decreciente (<-10%) | 76 | `54%` | `51%` | `49%` | `59%` | `37%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 511 | `50%` | `58%` | `62%` ⭐ | `57%` | `36%` | `61%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 470 | `55%` | `54%` | `55%` | `53%` | `35%` | `63%` ⭐ |
| RSI Diario < 35 | 142 | `49%` | `60%` ⭐ | `51%` | `57%` | `34%` | `57%` |
| RSI Diario > 65 | 262 | `48%` | `58%` | `64%` ⭐ | `55%` | `34%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `231 min` | `180 min` | `390 min` |
| TP DOWN (desde entrada) | `223 min` | `165 min` | `375 min` |
| False Break UP → SL | `136 min` | - | - |
| False Break DOWN → SL | `139 min` | - | - |

---

## Permutación #7: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2044`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.20%`
- **Rotura Bajista (DOWN):** `46.23%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `65.79%` | `64.97%` |
| 1.5x Rango OR | `49.20%` | `51.22%` |
| 2.0x Rango OR | `38.24%` | `39.58%` |
| 1.0x Volatilidad ATR Diaria | `10.22%` | `11.53%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.39%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.54%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.01%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `52.79%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.85%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1513`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `28.29%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `19.70%` |
| Shakeout & Re-breakout UP (>=2x OR) | `13.48%` |
| Continuacion Bajista (>=1x OR) | `55.39%` |
| Extension media reversal UP | `0.80x OR` | Mediana: `0.19x` |
| Extension media continuacion DOWN | `1.70x OR` | Mediana: `1.17x` |
| Tiempo medio al re-breakout | `135 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1562`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `27.46%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `19.85%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `15.30%` |
| Continuacion Alcista (>=1x OR) | `56.85%` |
| Extension media reversal DOWN | `0.90x OR` | Mediana: `0.14x` |
| Extension media continuacion UP | `1.61x OR` | Mediana: `1.17x` |
| Tiempo medio al re-breakout | `144 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 132 | `16%` | `29%` | `43%` | `49%` | `14%` | `34%` |
| RSI > 70 (Overbought) | 145 | `79%` ⭐ | `50%` | `51%` | `29%` | `22%` | `31%` |
| RSI 30-70 (Neutro) | 1767 | `53%` | `50%` | `56%` | `55%` | `30%` | `65%` ⭐ |
| OR ABOVE_PD_HIGH | 387 | `49%` | `53%` | `51%` | `51%` | `30%` | `50%` |
| OR BELOW_PD_LOW | 308 | `52%` | `48%` | `52%` | `55%` | `28%` | `46%` |
| OR BETWEEN_CLOSE_AND_HIGH | 666 | `55%` | `47%` | `59%` | `57%` | `29%` | `68%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 683 | `51%` | `50%` | `55%` | `51%` | `27%` | `67%` ⭐ |
| ATR Creciente (>10%) | 84 | `56%` | `43%` | `62%` ⭐ | `42%` | `27%` | `54%` |
| ATR Decreciente (<-10%) | 79 | `58%` | `52%` | `48%` | `50%` | `29%` | `63%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 528 | `49%` | `50%` | `59%` | `57%` | `29%` | `62%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 496 | `58%` | `47%` | `54%` | `48%` | `24%` | `62%` ⭐ |
| RSI Diario < 35 | 144 | `51%` | `47%` | `47%` | `59%` | `23%` | `58%` |
| RSI Diario > 65 | 268 | `48%` | `44%` | `67%` ⭐ | `50%` | `27%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `260 min` | `240 min` | `405 min` |
| TP DOWN (desde entrada) | `243 min` | `225 min` | `390 min` |
| False Break UP → SL | `172 min` | - | - |
| False Break DOWN → SL | `163 min` | - | - |

---

## Permutación #8: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2072`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.25%`
- **Rotura Bajista (DOWN):** `46.77%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `59.79%` | `60.89%` |
| 1.5x Rango OR | `43.60%` | `46.96%` |
| 2.0x Rango OR | `32.30%` | `35.09%` |
| 1.0x Volatilidad ATR Diaria | `9.79%` | `10.94%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `51.98%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `51.60%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `60.23%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `51.54%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.60%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1489`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `22.50%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `14.51%` |
| Shakeout & Re-breakout UP (>=2x OR) | `9.20%` |
| Continuacion Bajista (>=1x OR) | `50.17%` |
| Extension media reversal UP | `0.61x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.48x OR` | Mediana: `1.01x` |
| Tiempo medio al re-breakout | `140 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1538`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `21.91%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `15.34%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `10.92%` |
| Continuacion Alcista (>=1x OR) | `50.85%` |
| Extension media reversal DOWN | `0.68x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.37x OR` | Mediana: `1.02x` |
| Tiempo medio al re-breakout | `159 min` | Mediana: `135 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 111 | `17%` | `26%` | `47%` | `41%` | `9%` | `34%` |
| RSI > 70 (Overbought) | 153 | `79%` ⭐ | `39%` | `46%` | `44%` | `13%` | `33%` |
| RSI 30-70 (Neutro) | 1808 | `51%` | `45%` | `53%` | `53%` | `24%` | `64%` ⭐ |
| OR ABOVE_PD_HIGH | 394 | `46%` | `47%` | `46%` | `51%` | `25%` | `49%` |
| OR BELOW_PD_LOW | 306 | `52%` | `42%` | `51%` | `56%` | `19%` | `45%` |
| OR BETWEEN_CLOSE_AND_HIGH | 677 | `55%` | `44%` | `55%` | `53%` | `23%` | `67%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 695 | `50%` | `42%` | `52%` | `49%` | `22%` | `66%` ⭐ |
| ATR Creciente (>10%) | 83 | `51%` | `43%` | `48%` | `48%` | `16%` | `54%` |
| ATR Decreciente (<-10%) | 80 | `59%` | `49%` | `45%` | `44%` | `25%` | `60%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 531 | `46%` | `44%` | `56%` | `54%` | `23%` | `61%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 513 | `56%` | `41%` | `53%` | `46%` | `22%` | `61%` ⭐ |
| RSI Diario < 35 | 145 | `54%` | `46%` | `46%` | `59%` | `20%` | `58%` |
| RSI Diario > 65 | 271 | `48%` | `40%` | `61%` ⭐ | `51%` | `21%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `275 min` | `240 min` | `405 min` |
| TP DOWN (desde entrada) | `256 min` | `240 min` | `405 min` |
| False Break UP → SL | `196 min` | - | - |
| False Break DOWN → SL | `184 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: EURJPY

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] Tokyo (15m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `85.48%` (base: `73.41%`, +12%pp). N=126.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `62.54%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `61.39%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `61.01%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `60.23%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (15m)**: Imantación cíclica brutal. El `89.35%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (30m)**: Imantación cíclica brutal. El `87.91%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (45m)**: Imantación cíclica brutal. El `87.03%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (60m)**: Imantación cíclica brutal. El `84.54%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] Tokyo (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `68.57%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `67.67%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `67.06%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `66.15%` de los eventos evaluados.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `64.40%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (15m)**: Tasa de extensión polar bajista (1.5x) del `73.41%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (30m)**: Tasa de extensión polar bajista (1.5x) del `66.78%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (45m)**: Tasa de extensión polar bajista (1.5x) del `60.81%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `67.79%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `72.54%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `66.27%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.53%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Tokyo 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=403 | UP: `49%` | Ext 1.5 UP: `80%` | Falsa Ruptura DW: `61%` | Reversión a PD_Close: `93%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=395 | UP: `49%` | Ext 1.5 UP: `62%` | Falsa Ruptura DW: `58%` | Reversión a PD_Close: `86%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=124 | UP: `56%` | Ext 1.5 UP: `69%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `87%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1454 | UP: `50%` | Ext 1.5 UP: `73%` | Falsa Ruptura DW: `58%` | Reversión a PD_Close: `90%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*