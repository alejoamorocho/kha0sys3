# 🌐 Matriz Probabilística Omnidireccional: GBPAUD

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **Sydney 15m**](#permutación-1-sydney-15m)
- [Permutación #2: **Sydney 30m**](#permutación-2-sydney-30m)
- [Permutación #3: **Sydney 45m**](#permutación-3-sydney-45m)
- [Permutación #4: **Sydney 60m**](#permutación-4-sydney-60m)
- [Permutación #5: **London 15m**](#permutación-5-london-15m)
- [Permutación #6: **London 30m**](#permutación-6-london-30m)
- [Permutación #7: **London 45m**](#permutación-7-london-45m)
- [Permutación #8: **London 60m**](#permutación-8-london-60m)

---
## Permutación #1: Sydney 15m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1068`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `61.99%`
- **Rotura Bajista (DOWN):** `29.49%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `21.60%` | `16.83%` |
| 1.5x Rango OR | `8.91%` | `5.08%` |
| 2.0x Rango OR | `5.89%` | `1.90%` |
| 1.0x Volatilidad ATR Diaria | `0.15%` | `0.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `17.07%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `34.29%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `23.31%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `15.36%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `13.20%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `447`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `9.17%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `4.25%` |
| Shakeout & Re-breakout UP (>=2x OR) | `2.24%` |
| Continuacion Bajista (>=1x OR) | `14.32%` |
| Extension media reversal UP | `0.28x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.47x OR` | Mediana: `0.31x` |
| Tiempo medio al re-breakout | `32 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `789`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `2.53%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `0.76%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `0.25%` |
| Continuacion Alcista (>=1x OR) | `21.42%` |
| Extension media reversal DOWN | `0.10x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.69x OR` | Mediana: `0.49x` |
| Tiempo medio al re-breakout | `40 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 26 | `58%` | `13%` | `0%` | `40%` | `27%` | `23%` |
| RSI > 70 (Overbought) | 21 | `48%` | `20%` | `30%` | `38%` | `0%` | `5%` |
| RSI 30-70 (Neutro) | 1021 | `62%` ⭐ | `9%` | `17%` | `34%` | `9%` | `24%` |
| OR ABOVE_PD_HIGH | 243 | `61%` ⭐ | `13%` | `16%` | `32%` | `8%` | `4%` |
| OR BELOW_PD_LOW | 233 | `69%` ⭐ | `6%` | `16%` | `46%` | `9%` | `7%` |
| OR BETWEEN_CLOSE_AND_HIGH | 286 | `55%` | `6%` | `20%` | `33%` | `11%` | `32%` |
| OR BETWEEN_LOW_AND_CLOSE | 306 | `64%` ⭐ | `11%` | `17%` | `30%` | `9%` | `43%` |
| ATR Creciente (>10%) | 33 | `55%` | `11%` | `28%` | `27%` | `12%` | `24%` |
| ATR Decreciente (<-10%) | 23 | `78%` ⭐ | `11%` | `6%` | `25%` | `0%` | `22%` |
| ATR Q1 (Baja Vol Historica) | 316 | `61%` ⭐ | `12%` | `12%` | `36%` | `14%` | `26%` |
| ATR Q4 (Alta Vol Historica) | 227 | `58%` | `5%` | `18%` | `34%` | `9%` | `25%` |
| RSI Diario < 35 | 99 | `67%` ⭐ | `8%` | `15%` | `31%` | `8%` | `22%` |
| RSI Diario > 65 | 118 | `58%` | `10%` | `21%` | `29%` | `7%` | `24%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `47 min` | `45 min` | `75 min` |
| TP DOWN (desde entrada) | `35 min` | `30 min` | `75 min` |
| False Break UP → SL | `46 min` | - | - |
| False Break DOWN → SL | `38 min` | - | - |

---

## Permutación #2: Sydney 30m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1390`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `60.14%`
- **Rotura Bajista (DOWN):** `28.49%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `14.00%` | `11.62%` |
| 1.5x Rango OR | `5.50%` | `2.27%` |
| 2.0x Rango OR | `2.99%` | `0.76%` |
| 1.0x Volatilidad ATR Diaria | `0.12%` | `0.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `11.84%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `23.74%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `21.37%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `13.81%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `12.63%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `486`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `3.70%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `1.65%` |
| Shakeout & Re-breakout UP (>=2x OR) | `0.21%` |
| Continuacion Bajista (>=1x OR) | `12.55%` |
| Extension media reversal UP | `0.16x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.43x OR` | Mediana: `0.29x` |
| Tiempo medio al re-breakout | `32 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `924`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `2.49%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `0.54%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `0.32%` |
| Continuacion Alcista (>=1x OR) | `13.96%` |
| Extension media reversal DOWN | `0.07x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.55x OR` | Mediana: `0.41x` |
| Tiempo medio al re-breakout | `36 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 30 | `57%` | `12%` | `6%` | `22%` | `9%` | `13%` |
| RSI 30-70 (Neutro) | 1343 | `60%` ⭐ | `5%` | `12%` | `23%` | `4%` | `22%` |
| OR ABOVE_PD_HIGH | 308 | `60%` ⭐ | `6%` | `11%` | `22%` | `4%` | `3%` |
| OR BELOW_PD_LOW | 321 | `68%` ⭐ | `6%` | `11%` | `25%` | `3%` | `7%` |
| OR BETWEEN_CLOSE_AND_HIGH | 347 | `50%` | `4%` | `13%` | `23%` | `4%` | `29%` |
| OR BETWEEN_LOW_AND_CLOSE | 414 | `63%` ⭐ | `6%` | `13%` | `25%` | `4%` | `40%` |
| ATR Creciente (>10%) | 49 | `57%` | `7%` | `21%` | `22%` | `16%` | `16%` |
| ATR Decreciente (<-10%) | 37 | `73%` ⭐ | `0%` | `7%` | `25%` | `0%` | `22%` |
| ATR Q1 (Baja Vol Historica) | 380 | `62%` ⭐ | `7%` | `8%` | `24%` | `3%` | `23%` |
| ATR Q4 (Alta Vol Historica) | 306 | `56%` | `5%` | `11%` | `25%` | `4%` | `23%` |
| RSI Diario < 35 | 144 | `61%` ⭐ | `5%` | `11%` | `28%` | `8%` | `19%` |
| RSI Diario > 65 | 149 | `58%` | `10%` | `17%` | `20%` | `4%` | `21%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `40 min` | `45 min` | `60 min` |
| TP DOWN (desde entrada) | `47 min` | `60 min` | `75 min` |
| False Break UP → SL | `40 min` | - | - |
| False Break DOWN → SL | `35 min` | - | - |

---

## Permutación #3: Sydney 45m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1630`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `57.24%`
- **Rotura Bajista (DOWN):** `27.55%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `8.90%` | `9.35%` |
| 1.5x Rango OR | `3.32%` | `2.90%` |
| 2.0x Rango OR | `1.71%` | `0.89%` |
| 1.0x Volatilidad ATR Diaria | `0.00%` | `0.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `8.47%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `14.92%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `18.77%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `12.27%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `11.50%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `485`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `1.86%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `0.00%` |
| Shakeout & Re-breakout UP (>=2x OR) | `0.00%` |
| Continuacion Bajista (>=1x OR) | `10.10%` |
| Extension media reversal UP | `0.09x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.39x OR` | Mediana: `0.26x` |
| Tiempo medio al re-breakout | `29 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `957`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `1.25%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `0.21%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `0.21%` |
| Continuacion Alcista (>=1x OR) | `8.88%` |
| Extension media reversal DOWN | `0.04x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.43x OR` | Mediana: `0.31x` |
| Tiempo medio al re-breakout | `37 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI 30-70 (Neutro) | 1597 | `57%` | `3%` | `9%` | `15%` | `2%` | `19%` |
| OR ABOVE_PD_HIGH | 363 | `57%` | `5%` | `6%` | `15%` | `2%` | `2%` |
| OR BELOW_PD_LOW | 397 | `62%` ⭐ | `4%` | `9%` | `15%` | `0%` | `6%` |
| OR BETWEEN_CLOSE_AND_HIGH | 404 | `50%` | `2%` | `9%` | `14%` | `2%` | `25%` |
| OR BETWEEN_LOW_AND_CLOSE | 466 | `59%` | `2%` | `9%` | `16%` | `3%` | `37%` |
| ATR Creciente (>10%) | 58 | `52%` | `0%` | `13%` | `17%` | `9%` | `14%` |
| ATR Decreciente (<-10%) | 45 | `73%` ⭐ | `0%` | `15%` | `11%` | `0%` | `24%` |
| ATR Q1 (Baja Vol Historica) | 447 | `60%` | `5%` | `4%` | `19%` | `2%` | `18%` |
| ATR Q4 (Alta Vol Historica) | 372 | `55%` | `2%` | `7%` | `13%` | `2%` | `20%` |
| RSI Diario < 35 | 171 | `58%` | `5%` | `9%` | `14%` | `6%` | `16%` |
| RSI Diario > 65 | 169 | `54%` | `1%` | `10%` | `16%` | `0%` | `18%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `32 min` | `30 min` | `45 min` |
| TP DOWN (desde entrada) | `30 min` | `30 min` | `60 min` |
| False Break UP → SL | `39 min` | - | - |
| False Break DOWN → SL | `32 min` | - | - |

---

## Permutación #4: Sydney 60m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1759`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.82%`
- **Rotura Bajista (DOWN):** `25.41%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `4.70%` | `7.16%` |
| 1.5x Rango OR | `2.13%` | `1.12%` |
| 2.0x Rango OR | `1.12%` | `0.00%` |
| 1.0x Volatilidad ATR Diaria | `0.00%` | `0.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `5.37%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `8.28%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `15.80%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `10.63%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `9.89%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `423`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `1.42%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `0.47%` |
| Shakeout & Re-breakout UP (>=2x OR) | `0.00%` |
| Continuacion Bajista (>=1x OR) | `8.51%` |
| Extension media reversal UP | `0.05x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.37x OR` | Mediana: `0.26x` |
| Tiempo medio al re-breakout | `28 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `831`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `0.60%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `0.24%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `0.00%` |
| Continuacion Alcista (>=1x OR) | `5.42%` |
| Extension media reversal DOWN | `0.02x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.34x OR` | Mediana: `0.21x` |
| Tiempo medio al re-breakout | `30 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI 30-70 (Neutro) | 1733 | `51%` | `2%` | `5%` | `8%` | `1%` | `16%` |
| OR ABOVE_PD_HIGH | 389 | `54%` | `4%` | `5%` | `9%` | `2%` | `2%` |
| OR BELOW_PD_LOW | 436 | `52%` | `2%` | `3%` | `8%` | `0%` | `4%` |
| OR BETWEEN_CLOSE_AND_HIGH | 433 | `48%` | `1%` | `6%` | `6%` | `2%` | `21%` |
| OR BETWEEN_LOW_AND_CLOSE | 501 | `50%` | `2%` | `7%` | `10%` | `2%` | `32%` |
| ATR Creciente (>10%) | 62 | `48%` | `0%` | `10%` | `14%` | `6%` | `10%` |
| ATR Decreciente (<-10%) | 50 | `58%` | `0%` | `0%` | `8%` | `0%` | `20%` |
| ATR Q1 (Baja Vol Historica) | 473 | `54%` | `3%` | `5%` | `12%` | `2%` | `16%` |
| ATR Q4 (Alta Vol Historica) | 409 | `48%` | `2%` | `4%` | `7%` | `0%` | `16%` |
| RSI Diario < 35 | 182 | `49%` | `3%` | `6%` | `9%` | `7%` | `16%` |
| RSI Diario > 65 | 190 | `51%` | `1%` | `9%` | `11%` | `2%` | `14%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `28 min` | `30 min` | `45 min` |
| TP DOWN (desde entrada) | `30 min` | `30 min` | `45 min` |
| False Break UP → SL | `32 min` | - | - |
| False Break DOWN → SL | `30 min` | - | - |

---

## Permutación #5: London 15m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1632`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.02%`
- **Rotura Bajista (DOWN):** `47.49%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `79.63%` | `79.35%` |
| 1.5x Rango OR | `70.04%` | `68.26%` |
| 2.0x Rango OR | `58.99%` | `58.19%` |
| 1.0x Volatilidad ATR Diaria | `10.12%` | `9.94%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.66%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.97%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `63.54%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `55.76%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.55%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1275`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `49.33%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `39.84%` |
| Shakeout & Re-breakout UP (>=2x OR) | `30.98%` |
| Continuacion Bajista (>=1x OR) | `73.18%` |
| Extension media reversal UP | `1.71x OR` | Mediana: `0.95x` |
| Extension media continuacion DOWN | `2.58x OR` | Mediana: `2.02x` |
| Tiempo medio al re-breakout | `111 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1271`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `49.72%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `40.44%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `32.49%` |
| Continuacion Alcista (>=1x OR) | `72.70%` |
| Extension media reversal DOWN | `1.66x OR` | Mediana: `0.99x` |
| Extension media continuacion UP | `2.64x OR` | Mediana: `1.99x` |
| Tiempo medio al re-breakout | `109 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 103 | `22%` | `65%` ⭐ | `57%` | `60%` | `42%` | `39%` |
| RSI > 70 (Overbought) | 101 | `68%` ⭐ | `65%` ⭐ | `49%` | `41%` | `42%` | `38%` |
| RSI 30-70 (Neutro) | 1428 | `46%` | `71%` ⭐ | `54%` | `55%` | `50%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 318 | `46%` | `67%` ⭐ | `52%` | `53%` | `49%` | `48%` |
| OR BELOW_PD_LOW | 231 | `44%` | `67%` ⭐ | `57%` | `56%` | `45%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 483 | `39%` | `70%` ⭐ | `55%` | `52%` | `50%` | `76%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 600 | `52%` | `73%` ⭐ | `52%` | `59%` | `51%` | `70%` ⭐ |
| ATR Creciente (>10%) | 64 | `52%` | `79%` ⭐ | `45%` | `57%` | `59%` | `62%` ⭐ |
| ATR Decreciente (<-10%) | 40 | `38%` | `100%` ⭐ | `33%` | `59%` | `63%` ⭐ | `75%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 456 | `46%` | `74%` ⭐ | `51%` | `53%` | `51%` | `64%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 335 | `47%` | `74%` ⭐ | `48%` | `56%` | `49%` | `65%` ⭐ |
| RSI Diario < 35 | 166 | `41%` | `74%` ⭐ | `54%` | `58%` | `47%` | `64%` ⭐ |
| RSI Diario > 65 | 172 | `47%` | `72%` ⭐ | `56%` | `47%` | `47%` | `59%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `179 min` | `105 min` | `330 min` |
| TP DOWN (desde entrada) | `182 min` | `105 min` | `315 min` |
| False Break UP → SL | `84 min` | - | - |
| False Break DOWN → SL | `96 min` | - | - |

---

## Permutación #6: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1993`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.62%`
- **Rotura Bajista (DOWN):** `49.62%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `75.45%` | `72.70%` |
| 1.5x Rango OR | `62.59%` | `60.87%` |
| 2.0x Rango OR | `50.47%` | `48.63%` |
| 1.0x Volatilidad ATR Diaria | `9.38%` | `10.11%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `52.48%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.12%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `62.57%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `54.84%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.05%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1521`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `38.07%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `29.06%` |
| Shakeout & Re-breakout UP (>=2x OR) | `22.16%` |
| Continuacion Bajista (>=1x OR) | `66.27%` |
| Extension media reversal UP | `1.22x OR` | Mediana: `0.50x` |
| Extension media continuacion DOWN | `2.08x OR` | Mediana: `1.60x` |
| Tiempo medio al re-breakout | `130 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1531`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `39.39%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `30.44%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `23.19%` |
| Continuacion Alcista (>=1x OR) | `66.95%` |
| Extension media reversal DOWN | `1.19x OR` | Mediana: `0.49x` |
| Extension media continuacion UP | `2.13x OR` | Mediana: `1.57x` |
| Tiempo medio al re-breakout | `124 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 142 | `25%` | `61%` ⭐ | `61%` ⭐ | `54%` | `30%` | `32%` |
| RSI > 70 (Overbought) | 111 | `76%` ⭐ | `56%` | `50%` | `59%` | `32%` | `25%` |
| RSI 30-70 (Neutro) | 1740 | `48%` | `63%` ⭐ | `52%` | `56%` | `39%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 362 | `46%` | `60%` ⭐ | `52%` | `57%` | `36%` | `46%` |
| OR BELOW_PD_LOW | 306 | `46%` | `62%` ⭐ | `49%` | `56%` | `36%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 588 | `44%` | `64%` ⭐ | `55%` | `56%` | `39%` | `74%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 737 | `51%` | `63%` ⭐ | `52%` | `56%` | `39%` | `69%` ⭐ |
| ATR Creciente (>10%) | 72 | `49%` | `49%` | `63%` ⭐ | `56%` | `51%` | `64%` ⭐ |
| ATR Decreciente (<-10%) | 51 | `43%` | `77%` ⭐ | `32%` | `56%` | `43%` | `71%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 528 | `47%` | `65%` ⭐ | `49%` | `56%` | `38%` | `62%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 447 | `49%` | `65%` ⭐ | `53%` | `56%` | `37%` | `65%` ⭐ |
| RSI Diario < 35 | 195 | `51%` | `69%` ⭐ | `50%` | `55%` | `36%` | `61%` ⭐ |
| RSI Diario > 65 | 206 | `46%` | `56%` | `52%` | `56%` | `36%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `210 min` | `150 min` | `360 min` |
| TP DOWN (desde entrada) | `224 min` | `150 min` | `375 min` |
| False Break UP → SL | `123 min` | - | - |
| False Break DOWN → SL | `126 min` | - | - |

---

## Permutación #7: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2087`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.44%`
- **Rotura Bajista (DOWN):** `50.84%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.59%` | `65.69%` |
| 1.5x Rango OR | `55.15%` | `51.65%` |
| 2.0x Rango OR | `43.33%` | `39.30%` |
| 1.0x Volatilidad ATR Diaria | `8.59%` | `8.58%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `51.82%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.80%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.86%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `54.38%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.57%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1574`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `29.67%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `22.05%` |
| Shakeout & Re-breakout UP (>=2x OR) | `15.76%` |
| Continuacion Bajista (>=1x OR) | `58.96%` |
| Extension media reversal UP | `0.92x OR` | Mediana: `0.25x` |
| Extension media continuacion DOWN | `1.65x OR` | Mediana: `1.27x` |
| Tiempo medio al re-breakout | `139 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1573`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `31.09%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `22.38%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `15.58%` |
| Continuacion Alcista (>=1x OR) | `59.12%` |
| Extension media reversal DOWN | `0.86x OR` | Mediana: `0.21x` |
| Extension media continuacion UP | `1.77x OR` | Mediana: `1.32x` |
| Tiempo medio al re-breakout | `135 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 139 | `16%` | `59%` | `68%` ⭐ | `50%` | `21%` | `32%` |
| RSI > 70 (Overbought) | 110 | `82%` ⭐ | `53%` | `41%` | `35%` | `19%` | `21%` |
| RSI 30-70 (Neutro) | 1838 | `48%` | `55%` | `53%` | `57%` | `31%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 369 | `50%` | `55%` | `53%` | `51%` | `28%` | `46%` |
| OR BELOW_PD_LOW | 322 | `48%` | `49%` | `50%` | `54%` | `24%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 618 | `42%` | `54%` | `55%` | `57%` | `33%` | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 778 | `50%` | `58%` | `50%` | `58%` | `31%` | `68%` ⭐ |
| ATR Creciente (>10%) | 74 | `53%` | `46%` | `54%` | `52%` | `30%` | `64%` ⭐ |
| ATR Decreciente (<-10%) | 55 | `44%` | `58%` | `50%` | `67%` ⭐ | `34%` | `73%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 536 | `49%` | `57%` | `51%` | `55%` | `30%` | `61%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 505 | `48%` | `58%` | `52%` | `54%` | `30%` | `65%` ⭐ |
| RSI Diario < 35 | 204 | `47%` | `64%` ⭐ | `42%` | `60%` | `30%` | `60%` |
| RSI Diario > 65 | 213 | `49%` | `51%` | `60%` | `50%` | `29%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `234 min` | `180 min` | `390 min` |
| TP DOWN (desde entrada) | `246 min` | `195 min` | `390 min` |
| False Break UP → SL | `154 min` | - | - |
| False Break DOWN → SL | `150 min` | - | - |

---

## Permutación #8: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2102`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.14%`
- **Rotura Bajista (DOWN):** `48.38%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `63.95%` | `63.13%` |
| 1.5x Rango OR | `48.29%` | `44.94%` |
| 2.0x Rango OR | `35.67%` | `34.12%` |
| 1.0x Volatilidad ATR Diaria | `8.16%` | `8.55%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `51.80%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.69%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `60.94%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `53.76%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.08%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1526`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `23.92%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `17.10%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.53%` |
| Continuacion Bajista (>=1x OR) | `52.95%` |
| Extension media reversal UP | `0.70x OR` | Mediana: `0.05x` |
| Extension media continuacion DOWN | `1.41x OR` | Mediana: `1.08x` |
| Tiempo medio al re-breakout | `149 min` | Mediana: `120 min` |

**False Breakouts DOWN analizados:** `1565`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `24.92%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `16.87%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `11.44%` |
| Continuacion Alcista (>=1x OR) | `53.93%` |
| Extension media reversal DOWN | `0.66x OR` | Mediana: `0.06x` |
| Extension media continuacion UP | `1.49x OR` | Mediana: `1.11x` |
| Tiempo medio al re-breakout | `143 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 145 | `13%` | `42%` | `47%` | `54%` | `19%` | `33%` |
| RSI > 70 (Overbought) | 105 | `90%` ⭐ | `38%` | `43%` | `64%` ⭐ | `17%` | `27%` |
| RSI 30-70 (Neutro) | 1852 | `51%` | `49%` | `53%` | `54%` | `25%` | `65%` ⭐ |
| OR ABOVE_PD_HIGH | 370 | `52%` | `50%` | `52%` | `52%` | `24%` | `46%` |
| OR BELOW_PD_LOW | 323 | `52%` | `41%` | `53%` | `51%` | `17%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 622 | `47%` | `49%` | `53%` | `53%` | `24%` | `71%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 787 | `51%` | `50%` | `50%` | `56%` | `26%` | `67%` ⭐ |
| ATR Creciente (>10%) | 74 | `55%` | `44%` | `51%` | `50%` | `28%` | `62%` ⭐ |
| ATR Decreciente (<-10%) | 56 | `54%` | `50%` | `53%` | `56%` | `24%` | `73%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 537 | `51%` | `47%` | `52%` | `56%` | `24%` | `61%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 516 | `52%` | `49%` | `53%` | `51%` | `23%` | `64%` ⭐ |
| RSI Diario < 35 | 205 | `51%` | `57%` | `42%` | `56%` | `24%` | `58%` |
| RSI Diario > 65 | 214 | `52%` | `47%` | `58%` | `48%` | `22%` | `55%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `243 min` | `210 min` | `390 min` |
| TP DOWN (desde entrada) | `263 min` | `225 min` | `390 min` |
| False Break UP → SL | `188 min` | - | - |
| False Break DOWN → SL | `186 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: GBPAUD

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST UP] London (15m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `100.00%` (base: `70.04%`, +30%pp). N=40. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (30m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `77.27%` (base: `62.59%`, +15%pp). N=51. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `63.54%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `62.57%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `61.86%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `60.94%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `68.26%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `60.87%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `70.04%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `62.59%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=414 | UP: `45%` | Ext 1.5 UP: `81%` | Falsa Ruptura DW: `54%` | Reversión a PD_Close: `63%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=410 | UP: `46%` | Ext 1.5 UP: `66%` | Falsa Ruptura DW: `57%` | Reversión a PD_Close: `65%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=157 | UP: `39%` | Ext 1.5 UP: `74%` | Falsa Ruptura DW: `67%` | Reversión a PD_Close: `68%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1475 | UP: `47%` | Ext 1.5 UP: `70%` | Falsa Ruptura DW: `53%` | Reversión a PD_Close: `63%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*