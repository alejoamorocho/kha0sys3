# 🌐 Matriz Probabilística Omnidireccional: USDJPY

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **Tokyo 15m**](#permutación-1-tokyo-15m)
- [Permutación #2: **Tokyo 30m**](#permutación-2-tokyo-30m)
- [Permutación #3: **Tokyo 45m**](#permutación-3-tokyo-45m)
- [Permutación #4: **Tokyo 60m**](#permutación-4-tokyo-60m)
- [Permutación #5: **NY 15m**](#permutación-5-ny-15m)
- [Permutación #6: **NY 30m**](#permutación-6-ny-30m)
- [Permutación #7: **NY 45m**](#permutación-7-ny-45m)
- [Permutación #8: **NY 60m**](#permutación-8-ny-60m)

---
## Permutación #1: Tokyo 15m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1693`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.09%`
- **Rotura Bajista (DOWN):** `46.25%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.12%` | `81.35%` |
| 1.5x Rango OR | `71.10%` | `71.26%` |
| 2.0x Rango OR | `60.92%` | `61.56%` |
| 1.0x Volatilidad ATR Diaria | `15.38%` | `18.77%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.57%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.15%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `88.54%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `69.70%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.31%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1266`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `35.07%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `24.96%` |
| Shakeout & Re-breakout UP (>=2x OR) | `17.69%` |
| Continuacion Bajista (>=1x OR) | `64.69%` |
| Extension media reversal UP | `0.96x OR` | Mediana: `0.31x` |
| Extension media continuacion DOWN | `2.03x OR` | Mediana: `1.53x` |
| Tiempo medio al re-breakout | `134 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1298`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `34.90%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `26.73%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `20.34%` |
| Continuacion Alcista (>=1x OR) | `64.87%` |
| Extension media reversal DOWN | `1.12x OR` | Mediana: `0.31x` |
| Extension media continuacion UP | `1.89x OR` | Mediana: `1.49x` |
| Tiempo medio al re-breakout | `127 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 86 | `26%` | `64%` ⭐ | `59%` | `51%` | `34%` | `84%` ⭐ |
| RSI > 70 (Overbought) | 83 | `77%` ⭐ | `66%` ⭐ | `61%` ⭐ | `38%` | `23%` | `83%` ⭐ |
| RSI 30-70 (Neutro) | 1524 | `51%` | `72%` ⭐ | `54%` | `55%` | `36%` | `89%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1098 | `52%` | `69%` ⭐ | `55%` | `53%` | `35%` | `88%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 594 | `50%` | `74%` ⭐ | `53%` | `56%` | `36%` | `89%` ⭐ |
| ATR Creciente (>10%) | 87 | `48%` | `69%` ⭐ | `50%` | `51%` | `39%` | `87%` ⭐ |
| ATR Decreciente (<-10%) | 64 | `55%` | `74%` ⭐ | `63%` ⭐ | `64%` ⭐ | `26%` | `94%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 454 | `51%` | `71%` ⭐ | `53%` | `52%` | `34%` | `87%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 378 | `53%` | `73%` ⭐ | `50%` | `46%` | `34%` | `88%` ⭐ |
| RSI Diario < 35 | 146 | `46%` | `73%` ⭐ | `54%` | `56%` | `37%` | `88%` ⭐ |
| RSI Diario > 65 | 266 | `47%` | `74%` ⭐ | `49%` | `60%` | `38%` | `90%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `324 min` | `225 min` | `645 min` |
| TP DOWN (desde entrada) | `315 min` | `195 min` | `615 min` |
| False Break UP → SL | `140 min` | - | - |
| False Break DOWN → SL | `138 min` | - | - |

---

## Permutación #2: Tokyo 30m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1952`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.87%`
- **Rotura Bajista (DOWN):** `45.03%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `76.36%` | `75.77%` |
| 1.5x Rango OR | `64.73%` | `64.62%` |
| 2.0x Rango OR | `54.75%` | `54.27%` |
| 1.0x Volatilidad ATR Diaria | `13.76%` | `18.54%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.36%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.36%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `86.78%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `68.80%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.13%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1422`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `25.60%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `17.09%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.39%` |
| Continuacion Bajista (>=1x OR) | `57.59%` |
| Extension media reversal UP | `0.69x OR` | Mediana: `0.01x` |
| Extension media continuacion DOWN | `1.68x OR` | Mediana: `1.20x` |
| Tiempo medio al re-breakout | `151 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1461`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `26.63%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `19.71%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `13.69%` |
| Continuacion Alcista (>=1x OR) | `56.54%` |
| Extension media reversal DOWN | `0.85x OR` | Mediana: `0.06x` |
| Extension media continuacion UP | `1.56x OR` | Mediana: `1.18x` |
| Tiempo medio al re-breakout | `140 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 107 | `21%` | `59%` | `68%` ⭐ | `52%` | `22%` | `83%` ⭐ |
| RSI > 70 (Overbought) | 107 | `82%` ⭐ | `55%` | `56%` | `32%` | `13%` | `81%` ⭐ |
| RSI 30-70 (Neutro) | 1738 | `53%` | `66%` ⭐ | `57%` | `54%` | `26%` | `87%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1261 | `54%` | `64%` ⭐ | `58%` | `54%` | `26%` | `87%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 690 | `51%` | `66%` ⭐ | `57%` | `52%` | `26%` | `87%` ⭐ |
| ATR Creciente (>10%) | 89 | `46%` | `66%` ⭐ | `56%` | `55%` | `24%` | `83%` ⭐ |
| ATR Decreciente (<-10%) | 74 | `54%` | `60%` ⭐ | `65%` ⭐ | `52%` | `19%` | `91%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 508 | `53%` | `68%` ⭐ | `55%` | `49%` | `25%` | `85%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 468 | `52%` | `65%` ⭐ | `56%` | `50%` | `27%` | `87%` ⭐ |
| RSI Diario < 35 | 160 | `54%` | `66%` ⭐ | `53%` | `58%` | `26%` | `85%` ⭐ |
| RSI Diario > 65 | 315 | `52%` | `59%` | `54%` | `54%` | `25%` | `88%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `388 min` | `330 min` | `720 min` |
| TP DOWN (desde entrada) | `356 min` | `285 min` | `690 min` |
| False Break UP → SL | `201 min` | - | - |
| False Break DOWN → SL | `217 min` | - | - |

---

## Permutación #3: Tokyo 45m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2041`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.18%`
- **Rotura Bajista (DOWN):** `45.12%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `72.30%` | `72.64%` |
| 1.5x Rango OR | `60.09%` | `59.83%` |
| 2.0x Rango OR | `49.67%` | `49.73%` |
| 1.0x Volatilidad ATR Diaria | `13.62%` | `18.02%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `56.06%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `52.88%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `85.06%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `68.59%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.69%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1441`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `19.71%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `12.56%` |
| Shakeout & Re-breakout UP (>=2x OR) | `8.33%` |
| Continuacion Bajista (>=1x OR) | `51.15%` |
| Extension media reversal UP | `0.53x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.45x OR` | Mediana: `1.03x` |
| Tiempo medio al re-breakout | `170 min` | Mediana: `135 min` |

**False Breakouts DOWN analizados:** `1464`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `20.15%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `14.69%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `9.49%` |
| Continuacion Alcista (>=1x OR) | `49.59%` |
| Extension media reversal DOWN | `0.65x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.34x OR` | Mediana: `0.98x` |
| Tiempo medio al re-breakout | `154 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 111 | `27%` | `43%` | `57%` | `58%` | `9%` | `84%` ⭐ |
| RSI > 70 (Overbought) | 121 | `88%` ⭐ | `51%` | `54%` | `36%` | `8%` | `72%` ⭐ |
| RSI 30-70 (Neutro) | 1809 | `51%` | `62%` ⭐ | `56%` | `53%` | `21%` | `86%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1317 | `52%` | `59%` | `57%` | `54%` | `20%` | `85%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 722 | `52%` | `61%` ⭐ | `55%` | `51%` | `19%` | `85%` ⭐ |
| ATR Creciente (>10%) | 89 | `48%` | `56%` | `63%` ⭐ | `49%` | `21%` | `83%` ⭐ |
| ATR Decreciente (<-10%) | 81 | `43%` | `54%` | `57%` | `63%` ⭐ | `11%` | `88%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 524 | `51%` | `59%` | `53%` | `49%` | `18%` | `83%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 498 | `52%` | `62%` ⭐ | `54%` | `50%` | `22%` | `85%` ⭐ |
| RSI Diario < 35 | 166 | `52%` | `63%` ⭐ | `51%` | `57%` | `17%` | `84%` ⭐ |
| RSI Diario > 65 | 324 | `55%` | `52%` | `57%` | `48%` | `18%` | `86%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `424 min` | `375 min` | `720 min` |
| TP DOWN (desde entrada) | `391 min` | `330 min` | `705 min` |
| False Break UP → SL | `249 min` | - | - |
| False Break DOWN → SL | `295 min` | - | - |

---

## Permutación #4: Tokyo 60m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2087`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.78%`
- **Rotura Bajista (DOWN):** `49.07%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `67.58%` | `65.23%` |
| 1.5x Rango OR | `53.83%` | `52.83%` |
| 2.0x Rango OR | `41.94%` | `41.70%` |
| 1.0x Volatilidad ATR Diaria | `14.44%` | `16.50%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `51.08%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.22%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `81.60%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `67.13%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.07%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1381`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `12.31%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `7.53%` |
| Shakeout & Re-breakout UP (>=2x OR) | `4.20%` |
| Continuacion Bajista (>=1x OR) | `40.70%` |
| Extension media reversal UP | `0.35x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.12x OR` | Mediana: `0.78x` |
| Tiempo medio al re-breakout | `187 min` | Mediana: `180 min` |

**False Breakouts DOWN analizados:** `1364`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `12.32%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `8.06%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `4.91%` |
| Continuacion Alcista (>=1x OR) | `40.18%` |
| Extension media reversal DOWN | `0.39x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.08x OR` | Mediana: `0.79x` |
| Tiempo medio al re-breakout | `181 min` | Mediana: `150 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 123 | `17%` | `24%` | `76%` ⭐ | `56%` | `6%` | `74%` ⭐ |
| RSI > 70 (Overbought) | 146 | `88%` ⭐ | `50%` | `46%` | `50%` | `6%` | `65%` ⭐ |
| RSI 30-70 (Neutro) | 1818 | `48%` | `55%` | `51%` | `53%` | `13%` | `83%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1347 | `48%` | `52%` | `52%` | `54%` | `12%` | `82%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 738 | `49%` | `57%` | `50%` | `52%` | `12%` | `81%` ⭐ |
| ATR Creciente (>10%) | 88 | `52%` | `54%` | `52%` | `38%` | `12%` | `81%` ⭐ |
| ATR Decreciente (<-10%) | 85 | `45%` | `47%` | `58%` | `64%` ⭐ | `8%` | `84%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 526 | `47%` | `55%` | `50%` | `49%` | `11%` | `79%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 519 | `50%` | `52%` | `48%` | `53%` | `13%` | `81%` ⭐ |
| RSI Diario < 35 | 167 | `53%` | `57%` | `42%` | `57%` | `10%` | `81%` ⭐ |
| RSI Diario > 65 | 334 | `50%` | `57%` | `49%` | `49%` | `11%` | `83%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `469 min` | `420 min` | `750 min` |
| TP DOWN (desde entrada) | `464 min` | `420 min` | `765 min` |
| False Break UP → SL | `314 min` | - | - |
| False Break DOWN → SL | `352 min` | - | - |

---

## Permutación #5: NY 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1617`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.06%`
- **Rotura Bajista (DOWN):** `47.50%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `62.29%` | `63.54%` |
| 1.5x Rango OR | `49.93%` | `47.66%` |
| 2.0x Rango OR | `38.76%` | `37.24%` |
| 1.0x Volatilidad ATR Diaria | `3.29%` | `5.21%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `47.17%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `47.01%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `36.12%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `35.06%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `34.17%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1206`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `30.35%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `22.72%` |
| Shakeout & Re-breakout UP (>=2x OR) | `16.58%` |
| Continuacion Bajista (>=1x OR) | `60.45%` |
| Extension media reversal UP | `0.91x OR` | Mediana: `0.15x` |
| Extension media continuacion DOWN | `2.03x OR` | Mediana: `1.35x` |
| Tiempo medio al re-breakout | `82 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1198`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `32.05%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `24.04%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `18.36%` |
| Continuacion Alcista (>=1x OR) | `58.51%` |
| Extension media reversal DOWN | `1.09x OR` | Mediana: `0.19x` |
| Extension media continuacion UP | `1.78x OR` | Mediana: `1.29x` |
| Tiempo medio al re-breakout | `78 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 132 | `27%` | `56%` | `31%` | `34%` | `20%` | `18%` |
| RSI > 70 (Overbought) | 155 | `72%` ⭐ | `49%` | `44%` | `42%` | `22%` | `10%` |
| RSI 30-70 (Neutro) | 1330 | `46%` | `50%` | `49%` | `49%` | `32%` | `41%` |
| OR ABOVE_PD_HIGH | 393 | `53%` | `50%` | `47%` | `48%` | `30%` | `20%` |
| OR BELOW_PD_LOW | 359 | `42%` | `50%` | `49%` | `48%` | `30%` | `19%` |
| OR BETWEEN_CLOSE_AND_HIGH | 431 | `47%` | `51%` | `44%` | `47%` | `34%` | `51%` |
| OR BETWEEN_LOW_AND_CLOSE | 434 | `47%` | `49%` | `49%` | `45%` | `27%` | `50%` |
| ATR Creciente (>10%) | 74 | `42%` | `58%` | `55%` | `46%` | `41%` | `39%` |
| ATR Decreciente (<-10%) | 57 | `51%` | `72%` ⭐ | `31%` | `50%` | `30%` | `35%` |
| ATR Q1 (Baja Vol Historica) | 450 | `44%` | `53%` | `48%` | `46%` | `30%` | `38%` |
| ATR Q4 (Alta Vol Historica) | 354 | `48%` | `42%` | `51%` | `48%` | `26%` | `36%` |
| RSI Diario < 35 | 136 | `45%` | `48%` | `48%` | `54%` | `36%` | `46%` |
| RSI Diario > 65 | 266 | `48%` | `50%` | `48%` | `50%` | `30%` | `33%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `115 min` | `60 min` | `165 min` |
| TP DOWN (desde entrada) | `98 min` | `60 min` | `165 min` |
| False Break UP → SL | `70 min` | - | - |
| False Break DOWN → SL | `81 min` | - | - |

---

## Permutación #6: NY 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1942`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.63%`
- **Rotura Bajista (DOWN):** `48.51%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `56.00%` | `54.56%` |
| 1.5x Rango OR | `38.81%` | `39.49%` |
| 2.0x Rango OR | `28.54%` | `29.30%` |
| 1.0x Volatilidad ATR Diaria | `3.78%` | `4.67%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `40.65%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `42.46%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `35.22%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `33.57%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `32.60%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1364`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `21.19%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `14.15%` |
| Shakeout & Re-breakout UP (>=2x OR) | `10.12%` |
| Continuacion Bajista (>=1x OR) | `48.39%` |
| Extension media reversal UP | `0.62x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.52x OR` | Mediana: `0.96x` |
| Tiempo medio al re-breakout | `94 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1368`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `19.44%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `13.67%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `9.21%` |
| Continuacion Alcista (>=1x OR) | `50.07%` |
| Extension media reversal DOWN | `0.64x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.42x OR` | Mediana: `1.00x` |
| Tiempo medio al re-breakout | `95 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 148 | `20%` | `34%` | `24%` | `31%` | `15%` | `18%` |
| RSI > 70 (Overbought) | 191 | `70%` ⭐ | `32%` | `34%` | `41%` | `18%` | `10%` |
| RSI 30-70 (Neutro) | 1603 | `48%` | `40%` | `42%` | `44%` | `22%` | `40%` |
| OR ABOVE_PD_HIGH | 502 | `53%` | `38%` | `41%` | `40%` | `22%` | `21%` |
| OR BELOW_PD_LOW | 403 | `45%` | `36%` | `41%` | `45%` | `20%` | `21%` |
| OR BETWEEN_CLOSE_AND_HIGH | 518 | `47%` | `45%` | `38%` | `45%` | `23%` | `47%` |
| OR BETWEEN_LOW_AND_CLOSE | 519 | `45%` | `36%` | `44%` | `40%` | `20%` | `49%` |
| ATR Creciente (>10%) | 85 | `47%` | `48%` | `38%` | `38%` | `30%` | `32%` |
| ATR Decreciente (<-10%) | 70 | `53%` | `43%` | `46%` | `31%` | `22%` | `36%` |
| ATR Q1 (Baja Vol Historica) | 504 | `45%` | `39%` | `41%` | `40%` | `23%` | `36%` |
| ATR Q4 (Alta Vol Historica) | 465 | `47%` | `38%` | `39%` | `43%` | `16%` | `34%` |
| RSI Diario < 35 | 156 | `43%` | `36%` | `49%` | `57%` | `29%` | `46%` |
| RSI Diario > 65 | 315 | `51%` | `42%` | `40%` | `47%` | `21%` | `33%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `142 min` | `90 min` | `255 min` |
| TP DOWN (desde entrada) | `118 min` | `60 min` | `210 min` |
| False Break UP → SL | `106 min` | - | - |
| False Break DOWN → SL | `112 min` | - | - |

---

## Permutación #7: NY 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1979`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.37%`
- **Rotura Bajista (DOWN):** `48.05%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `44.63%` | `42.69%` |
| 1.5x Rango OR | `27.64%` | `28.50%` |
| 2.0x Rango OR | `16.58%` | `18.61%` |
| 1.0x Volatilidad ATR Diaria | `2.76%` | `4.84%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `33.88%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `36.80%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `33.05%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `31.88%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `30.77%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1274`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `14.21%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `9.50%` |
| Shakeout & Re-breakout UP (>=2x OR) | `6.28%` |
| Continuacion Bajista (>=1x OR) | `40.27%` |
| Extension media reversal UP | `0.42x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.17x OR` | Mediana: `0.76x` |
| Tiempo medio al re-breakout | `110 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1326`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `14.25%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `9.58%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `6.33%` |
| Continuacion Alcista (>=1x OR) | `40.35%` |
| Extension media reversal DOWN | `0.44x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.09x OR` | Mediana: `0.74x` |
| Tiempo medio al re-breakout | `108 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 161 | `14%` | `22%` | `13%` | `31%` | `10%` | `22%` |
| RSI > 70 (Overbought) | 182 | `79%` ⭐ | `20%` | `22%` | `42%` | `12%` | `8%` |
| RSI 30-70 (Neutro) | 1636 | `50%` | `29%` | `37%` | `38%` | `15%` | `37%` |
| OR ABOVE_PD_HIGH | 516 | `53%` | `29%` | `34%` | `38%` | `15%` | `20%` |
| OR BELOW_PD_LOW | 397 | `46%` | `25%` | `34%` | `38%` | `13%` | `20%` |
| OR BETWEEN_CLOSE_AND_HIGH | 537 | `52%` | `29%` | `33%` | `35%` | `15%` | `43%` |
| OR BETWEEN_LOW_AND_CLOSE | 529 | `45%` | `27%` | `35%` | `36%` | `13%` | `46%` |
| ATR Creciente (>10%) | 85 | `46%` | `33%` | `26%` | `35%` | `18%` | `31%` |
| ATR Decreciente (<-10%) | 70 | `54%` | `32%` | `42%` | `35%` | `14%` | `31%` |
| ATR Q1 (Baja Vol Historica) | 509 | `47%` | `32%` | `35%` | `36%` | `17%` | `34%` |
| ATR Q4 (Alta Vol Historica) | 487 | `50%` | `24%` | `33%` | `34%` | `10%` | `31%` |
| RSI Diario < 35 | 158 | `40%` | `32%` | `41%` | `47%` | `23%` | `44%` |
| RSI Diario > 65 | 319 | `50%` | `25%` | `33%` | `43%` | `15%` | `32%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `179 min` | `135 min` | `300 min` |
| TP DOWN (desde entrada) | `149 min` | `105 min` | `225 min` |
| False Break UP → SL | `132 min` | - | - |
| False Break DOWN → SL | `130 min` | - | - |

---

## Permutación #8: NY 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1982`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.44%`
- **Rotura Bajista (DOWN):** `47.02%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `38.75%` | `37.66%` |
| 1.5x Rango OR | `20.94%` | `23.61%` |
| 2.0x Rango OR | `11.98%` | `15.67%` |
| 1.0x Volatilidad ATR Diaria | `2.81%` | `4.29%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `29.58%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `32.40%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `32.09%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `31.08%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `29.77%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1206`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `11.28%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `7.21%` |
| Shakeout & Re-breakout UP (>=2x OR) | `4.81%` |
| Continuacion Bajista (>=1x OR) | `35.16%` |
| Extension media reversal UP | `0.33x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.03x OR` | Mediana: `0.63x` |
| Tiempo medio al re-breakout | `115 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1267`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `10.73%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `6.71%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `4.26%` |
| Continuacion Alcista (>=1x OR) | `34.73%` |
| Extension media reversal DOWN | `0.33x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.95x OR` | Mediana: `0.65x` |
| Tiempo medio al re-breakout | `116 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 135 | `7%` | `10%` | `0%` | `24%` | `7%` | `17%` |
| RSI > 70 (Overbought) | 171 | `80%` ⭐ | `18%` | `18%` | `26%` | `12%` | `6%` |
| RSI 30-70 (Neutro) | 1676 | `49%` | `21%` | `32%` | `34%` | `12%` | `36%` |
| OR ABOVE_PD_HIGH | 522 | `52%` | `25%` | `28%` | `30%` | `12%` | `20%` |
| OR BELOW_PD_LOW | 395 | `45%` | `17%` | `29%` | `36%` | `12%` | `19%` |
| OR BETWEEN_CLOSE_AND_HIGH | 539 | `52%` | `21%` | `30%` | `32%` | `11%` | `41%` |
| OR BETWEEN_LOW_AND_CLOSE | 526 | `45%` | `19%` | `31%` | `32%` | `10%` | `45%` |
| ATR Creciente (>10%) | 84 | `43%` | `22%` | `28%` | `30%` | `14%` | `31%` |
| ATR Decreciente (<-10%) | 75 | `51%` | `18%` | `42%` | `35%` | `8%` | `28%` |
| ATR Q1 (Baja Vol Historica) | 502 | `47%` | `23%` | `33%` | `32%` | `13%` | `33%` |
| ATR Q4 (Alta Vol Historica) | 497 | `49%` | `17%` | `29%` | `31%` | `7%` | `30%` |
| RSI Diario < 35 | 155 | `41%` | `27%` | `31%` | `45%` | `20%` | `43%` |
| RSI Diario > 65 | 317 | `50%` | `18%` | `28%` | `36%` | `12%` | `32%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `186 min` | `150 min` | `300 min` |
| TP DOWN (desde entrada) | `150 min` | `105 min` | `240 min` |
| False Break UP → SL | `152 min` | - | - |
| False Break DOWN → SL | `140 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: USDJPY

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] Tokyo (15m) | RSI > 70 (Overbought)**: Extension 1.5x DOWN sube a `87.50%` (base: `71.26%`, +16%pp). N=83.

- **[EDGE CONTEXT-BOOST DOWN] Tokyo (45m) | RSI > 70 (Overbought)**: Extension 1.5x DOWN sube a `85.71%` (base: `59.83%`, +26%pp). N=121.

- **[EDGE CONTEXT-BOOST UP] NY (15m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `72.41%` (base: `49.93%`, +22%pp). N=57. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] Tokyo (15m)**: Imantación cíclica brutal. El `88.54%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (30m)**: Imantación cíclica brutal. El `86.78%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (45m)**: Imantación cíclica brutal. El `85.06%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (60m)**: Imantación cíclica brutal. El `81.60%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] Tokyo (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `69.70%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `68.80%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `68.59%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `67.13%` de los eventos evaluados.

- **[EDGE TENDENCIAL DOWN] Tokyo (15m)**: Tasa de extensión polar bajista (1.5x) del `71.26%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (30m)**: Tasa de extensión polar bajista (1.5x) del `64.62%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] Tokyo (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `71.10%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `64.73%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.09%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Tokyo 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=424 | UP: `50%` | Ext 1.5 UP: `77%` | Falsa Ruptura DW: `53%` | Reversión a PD_Close: `91%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=427 | UP: `51%` | Ext 1.5 UP: `66%` | Falsa Ruptura DW: `50%` | Reversión a PD_Close: `86%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=147 | UP: `46%` | Ext 1.5 UP: `75%` | Falsa Ruptura DW: `54%` | Reversión a PD_Close: `84%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1546 | UP: `52%` | Ext 1.5 UP: `71%` | Falsa Ruptura DW: `54%` | Reversión a PD_Close: `89%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*