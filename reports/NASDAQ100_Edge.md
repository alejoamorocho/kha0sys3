# 🌐 Matriz Probabilística Omnidireccional: NASDAQ100

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
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `675`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.15%`
- **Rotura Bajista (DOWN):** `48.44%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `84.62%` | `86.85%` |
| 1.5x Rango OR | `74.77%` | `76.15%` |
| 2.0x Rango OR | `68.00%` | `66.06%` |
| 1.0x Volatilidad ATR Diaria | `17.85%` | `17.13%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.69%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.21%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `68.89%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `56.59%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.89%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `543`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `67.40%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `60.22%` |
| Shakeout & Re-breakout UP (>=2x OR) | `53.04%` |
| Continuacion Bajista (>=1x OR) | `82.87%` |
| Extension media reversal UP | `2.95x OR` | Mediana: `2.27x` |
| Extension media continuacion DOWN | `4.05x OR` | Mediana: `3.09x` |
| Tiempo medio al re-breakout | `77 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `520`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `66.73%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `58.85%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `52.69%` |
| Continuacion Alcista (>=1x OR) | `85.00%` |
| Extension media reversal DOWN | `3.32x OR` | Mediana: `2.21x` |
| Extension media continuacion UP | `3.89x OR` | Mediana: `2.99x` |
| Tiempo medio al re-breakout | `79 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 64 | `31%` | `65%` ⭐ | `70%` ⭐ | `49%` | `60%` ⭐ | `56%` |
| RSI > 70 (Overbought) | 31 | `77%` ⭐ | `58%` | `75%` ⭐ | `67%` ⭐ | `56%` | `48%` |
| RSI 30-70 (Neutro) | 580 | `48%` | `77%` ⭐ | `58%` | `54%` | `69%` ⭐ | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 100 | `53%` | `74%` ⭐ | `57%` | `47%` | `61%` ⭐ | `61%` ⭐ |
| OR BELOW_PD_LOW | 155 | `47%` | `71%` ⭐ | `64%` ⭐ | `60%` | `73%` ⭐ | `54%` |
| OR BETWEEN_CLOSE_AND_HIGH | 186 | `46%` | `79%` ⭐ | `57%` | `47%` | `68%` ⭐ | `75%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 234 | `48%` | `74%` ⭐ | `60%` ⭐ | `56%` | `66%` ⭐ | `77%` ⭐ |
| ATR Creciente (>10%) | 79 | `43%` | `79%` ⭐ | `68%` ⭐ | `51%` | `74%` ⭐ | `75%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 173 | `51%` | `72%` ⭐ | `61%` ⭐ | `53%` | `71%` ⭐ | `65%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 176 | `43%` | `70%` ⭐ | `63%` ⭐ | `55%` | `66%` ⭐ | `65%` ⭐ |
| RSI Diario < 35 | 67 | `42%` | `79%` ⭐ | `54%` | `54%` | `74%` ⭐ | `72%` ⭐ |
| RSI Diario > 65 | 123 | `51%` | `60%` ⭐ | `68%` ⭐ | `55%` | `56%` | `66%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `116 min` | `90 min` | `150 min` |
| TP DOWN (desde entrada) | `109 min` | `75 min` | `150 min` |
| False Break UP → SL | `64 min` | - | - |
| False Break DOWN → SL | `58 min` | - | - |

---

## Permutación #2: Pre-Market 30m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1278`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.24%`
- **Rotura Bajista (DOWN):** `46.71%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `82.06%` | `79.73%` |
| 1.5x Rango OR | `71.91%` | `70.18%` |
| 2.0x Rango OR | `63.28%` | `60.13%` |
| 1.0x Volatilidad ATR Diaria | `13.37%` | `18.09%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.15%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.77%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `68.00%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `56.57%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.05%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1001`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `61.74%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `53.95%` |
| Shakeout & Re-breakout UP (>=2x OR) | `44.76%` |
| Continuacion Bajista (>=1x OR) | `77.62%` |
| Extension media reversal UP | `2.46x OR` | Mediana: `1.69x` |
| Extension media continuacion DOWN | `3.61x OR` | Mediana: `2.50x` |
| Tiempo medio al re-breakout | `75 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `993`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `58.21%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `50.76%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `44.21%` |
| Continuacion Alcista (>=1x OR) | `80.97%` |
| Extension media reversal DOWN | `2.72x OR` | Mediana: `1.56x` |
| Extension media continuacion UP | `3.39x OR` | Mediana: `2.84x` |
| Tiempo medio al re-breakout | `77 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 86 | `21%` | `61%` ⭐ | `61%` ⭐ | `60%` ⭐ | `59%` | `60%` ⭐ |
| RSI > 70 (Overbought) | 70 | `69%` ⭐ | `69%` ⭐ | `62%` ⭐ | `28%` | `52%` | `53%` |
| RSI 30-70 (Neutro) | 1122 | `47%` | `73%` ⭐ | `53%` | `55%` | `63%` ⭐ | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 240 | `49%` | `75%` ⭐ | `51%` | `51%` | `60%` | `59%` |
| OR BELOW_PD_LOW | 235 | `48%` | `70%` ⭐ | `59%` | `58%` | `64%` ⭐ | `56%` |
| OR BETWEEN_CLOSE_AND_HIGH | 387 | `42%` | `74%` ⭐ | `49%` | `54%` | `64%` ⭐ | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 416 | `48%` | `70%` ⭐ | `58%` | `56%` | `60%` | `76%` ⭐ |
| ATR Creciente (>10%) | 113 | `39%` | `75%` ⭐ | `57%` | `64%` ⭐ | `69%` ⭐ | `73%` ⭐ |
| ATR Decreciente (<-10%) | 42 | `48%` | `65%` ⭐ | `80%` ⭐ | `53%` | `68%` ⭐ | `74%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 317 | `47%` | `70%` ⭐ | `58%` | `53%` | `62%` ⭐ | `64%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 313 | `46%` | `70%` ⭐ | `58%` | `53%` | `60%` ⭐ | `68%` ⭐ |
| RSI Diario < 35 | 97 | `44%` | `86%` ⭐ | `51%` | `60%` | `74%` ⭐ | `72%` ⭐ |
| RSI Diario > 65 | 251 | `42%` | `64%` ⭐ | `60%` ⭐ | `57%` | `55%` | `66%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `107 min` | `75 min` | `135 min` |
| TP DOWN (desde entrada) | `107 min` | `75 min` | `150 min` |
| False Break UP → SL | `67 min` | - | - |
| False Break DOWN → SL | `60 min` | - | - |

---

## Permutación #3: Pre-Market 45m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1687`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.33%`
- **Rotura Bajista (DOWN):** `46.47%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `75.15%` | `74.11%` |
| 1.5x Rango OR | `63.02%` | `60.84%` |
| 2.0x Rango OR | `51.71%` | `52.17%` |
| 1.0x Volatilidad ATR Diaria | `11.66%` | `16.07%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.30%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.40%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.69%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `56.55%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.72%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1297`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `50.58%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `39.71%` |
| Shakeout & Re-breakout UP (>=2x OR) | `31.53%` |
| Continuacion Bajista (>=1x OR) | `71.70%` |
| Extension media reversal UP | `1.68x OR` | Mediana: `1.02x` |
| Extension media continuacion DOWN | `3.00x OR` | Mediana: `2.03x` |
| Tiempo medio al re-breakout | `79 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1344`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `49.33%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `41.44%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `34.97%` |
| Continuacion Alcista (>=1x OR) | `73.74%` |
| Extension media reversal DOWN | `2.07x OR` | Mediana: `0.96x` |
| Extension media continuacion UP | `2.61x OR` | Mediana: `1.98x` |
| Tiempo medio al re-breakout | `75 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 111 | `19%` | `38%` | `48%` | `50%` | `41%` | `51%` |
| RSI > 70 (Overbought) | 121 | `70%` ⭐ | `47%` | `58%` | `31%` | `35%` | `51%` |
| RSI 30-70 (Neutro) | 1455 | `51%` | `66%` ⭐ | `54%` | `60%` | `53%` | `69%` ⭐ |
| OR ABOVE_PD_HIGH | 349 | `49%` | `66%` ⭐ | `54%` | `55%` | `54%` | `59%` |
| OR BELOW_PD_LOW | 270 | `51%` | `62%` ⭐ | `57%` | `61%` ⭐ | `53%` | `56%` |
| OR BETWEEN_CLOSE_AND_HIGH | 544 | `51%` | `60%` ⭐ | `53%` | `56%` | `50%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 524 | `50%` | `64%` ⭐ | `54%` | `59%` | `48%` | `74%` ⭐ |
| ATR Creciente (>10%) | 121 | `55%` | `56%` | `55%` | `68%` ⭐ | `52%` | `71%` ⭐ |
| ATR Decreciente (<-10%) | 57 | `46%` | `62%` ⭐ | `58%` | `61%` ⭐ | `59%` | `67%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 425 | `50%` | `65%` ⭐ | `58%` | `52%` | `50%` | `64%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 408 | `49%` | `62%` ⭐ | `54%` | `59%` | `49%` | `66%` ⭐ |
| RSI Diario < 35 | 106 | `50%` | `75%` ⭐ | `51%` | `63%` ⭐ | `64%` ⭐ | `67%` ⭐ |
| RSI Diario > 65 | 353 | `47%` | `59%` | `58%` | `57%` | `44%` | `68%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `121 min` | `75 min` | `165 min` |
| TP DOWN (desde entrada) | `116 min` | `75 min` | `165 min` |
| False Break UP → SL | `64 min` | - | - |
| False Break DOWN → SL | `69 min` | - | - |

---

## Permutación #4: Pre-Market 60m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1819`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.41%`
- **Rotura Bajista (DOWN):** `43.76%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `73.94%` | `72.36%` |
| 1.5x Rango OR | `59.76%` | `57.54%` |
| 2.0x Rango OR | `49.40%` | `48.49%` |
| 1.0x Volatilidad ATR Diaria | `11.45%` | `16.08%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `52.45%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.53%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.41%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `55.63%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.21%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1376`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `45.78%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `35.03%` |
| Shakeout & Re-breakout UP (>=2x OR) | `27.18%` |
| Continuacion Bajista (>=1x OR) | `70.13%` |
| Extension media reversal UP | `1.43x OR` | Mediana: `0.79x` |
| Extension media continuacion DOWN | `2.78x OR` | Mediana: `1.86x` |
| Tiempo medio al re-breakout | `77 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1450`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `46.55%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `36.90%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `30.21%` |
| Continuacion Alcista (>=1x OR) | `71.24%` |
| Extension media reversal DOWN | `1.76x OR` | Mediana: `0.77x` |
| Extension media continuacion UP | `2.36x OR` | Mediana: `1.78x` |
| Tiempo medio al re-breakout | `73 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 117 | `15%` | `39%` | `33%` | `53%` | `34%` | `48%` |
| RSI > 70 (Overbought) | 132 | `77%` ⭐ | `41%` | `54%` | `30%` | `28%` | `48%` |
| RSI 30-70 (Neutro) | 1570 | `51%` | `63%` ⭐ | `53%` | `57%` | `48%` | `69%` ⭐ |
| OR ABOVE_PD_HIGH | 391 | `48%` | `60%` ⭐ | `53%` | `50%` | `48%` | `59%` |
| OR BELOW_PD_LOW | 282 | `50%` | `59%` | `53%` | `60%` ⭐ | `49%` | `55%` |
| OR BETWEEN_CLOSE_AND_HIGH | 584 | `51%` | `59%` | `53%` | `54%` | `46%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 562 | `52%` | `60%` ⭐ | `52%` | `59%` | `43%` | `74%` ⭐ |
| ATR Creciente (>10%) | 124 | `56%` | `52%` | `58%` | `65%` ⭐ | `49%` | `72%` ⭐ |
| ATR Decreciente (<-10%) | 67 | `48%` | `47%` | `66%` ⭐ | `65%` ⭐ | `46%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 466 | `51%` | `59%` | `56%` | `52%` | `47%` | `64%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 438 | `48%` | `59%` | `53%` | `58%` | `45%` | `66%` ⭐ |
| RSI Diario < 35 | 109 | `51%` | `73%` ⭐ | `52%` | `63%` ⭐ | `59%` | `67%` ⭐ |
| RSI Diario > 65 | 390 | `51%` | `57%` | `57%` | `55%` | `39%` | `68%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `117 min` | `75 min` | `180 min` |
| TP DOWN (desde entrada) | `106 min` | `60 min` | `150 min` |
| False Break UP → SL | `62 min` | - | - |
| False Break DOWN → SL | `68 min` | - | - |

---

## Permutación #5: NY Cash 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1746`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.57%`
- **Rotura Bajista (DOWN):** `46.85%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `63.09%` | `62.10%` |
| 1.5x Rango OR | `47.64%` | `50.24%` |
| 2.0x Rango OR | `36.32%` | `38.51%` |
| 1.0x Volatilidad ATR Diaria | `10.02%` | `15.28%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `47.17%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `49.27%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `60.65%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `51.83%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.12%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1292`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `31.81%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `22.14%` |
| Shakeout & Re-breakout UP (>=2x OR) | `15.71%` |
| Continuacion Bajista (>=1x OR) | `58.13%` |
| Extension media reversal UP | `0.99x OR` | Mediana: `0.31x` |
| Extension media continuacion DOWN | `2.12x OR` | Mediana: `1.31x` |
| Tiempo medio al re-breakout | `93 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1322`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `29.35%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `22.77%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `18.23%` |
| Continuacion Alcista (>=1x OR) | `58.25%` |
| Extension media reversal DOWN | `1.18x OR` | Mediana: `0.17x` |
| Extension media continuacion UP | `1.77x OR` | Mediana: `1.26x` |
| Tiempo medio al re-breakout | `89 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 171 | `17%` | `24%` | `45%` | `48%` | `28%` | `40%` |
| RSI > 70 (Overbought) | 224 | `74%` ⭐ | `40%` | `44%` | `44%` | `19%` | `39%` |
| RSI 30-70 (Neutro) | 1351 | `48%` | `51%` | `48%` | `50%` | `34%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 382 | `51%` | `52%` | `45%` | `43%` | `26%` | `51%` |
| OR BELOW_PD_LOW | 281 | `49%` | `47%` | `45%` | `43%` | `33%` | `49%` |
| OR BETWEEN_CLOSE_AND_HIGH | 579 | `47%` | `48%` | `49%` | `53%` | `34%` | `65%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 504 | `47%` | `45%` | `48%` | `54%` | `33%` | `69%` ⭐ |
| ATR Creciente (>10%) | 116 | `45%` | `46%` | `60%` | `51%` | `46%` | `69%` ⭐ |
| ATR Decreciente (<-10%) | 68 | `51%` | `57%` | `51%` | `45%` | `31%` | `62%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 439 | `49%` | `46%` | `48%` | `41%` | `30%` | `60%` |
| ATR Q4 (Alta Vol Historica) | 428 | `44%` | `51%` | `49%` | `57%` | `39%` | `62%` ⭐ |
| RSI Diario < 35 | 117 | `56%` | `52%` | `54%` | `67%` ⭐ | `45%` | `63%` ⭐ |
| RSI Diario > 65 | 371 | `48%` | `52%` | `48%` | `45%` | `28%` | `62%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `141 min` | `90 min` | `255 min` |
| TP DOWN (desde entrada) | `118 min` | `60 min` | `225 min` |
| False Break UP → SL | `88 min` | - | - |
| False Break DOWN → SL | `91 min` | - | - |

---

## Permutación #6: NY Cash 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1859`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.67%`
- **Rotura Bajista (DOWN):** `46.10%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `52.97%` | `54.49%` |
| 1.5x Rango OR | `37.58%` | `41.89%` |
| 2.0x Rango OR | `24.84%` | `30.46%` |
| 1.0x Volatilidad ATR Diaria | `8.28%` | `15.52%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `42.78%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `44.11%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `58.80%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `50.19%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `40.05%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1299`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `25.02%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `17.09%` |
| Shakeout & Re-breakout UP (>=2x OR) | `13.32%` |
| Continuacion Bajista (>=1x OR) | `51.73%` |
| Extension media reversal UP | `0.83x OR` | Mediana: `0.04x` |
| Extension media continuacion DOWN | `1.86x OR` | Mediana: `1.06x` |
| Tiempo medio al re-breakout | `100 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1360`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `23.53%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `17.57%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `13.53%` |
| Continuacion Alcista (>=1x OR) | `49.56%` |
| Extension media reversal DOWN | `0.89x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.50x OR` | Mediana: `0.99x` |
| Tiempo medio al re-breakout | `98 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 179 | `15%` | `33%` | `37%` | `41%` | `19%` | `41%` |
| RSI > 70 (Overbought) | 259 | `85%` ⭐ | `30%` | `36%` | `35%` | `18%` | `31%` |
| RSI 30-70 (Neutro) | 1421 | `49%` | `40%` | `45%` | `45%` | `27%` | `66%` ⭐ |
| OR ABOVE_PD_HIGH | 418 | `52%` | `36%` | `42%` | `39%` | `21%` | `50%` |
| OR BELOW_PD_LOW | 284 | `49%` | `36%` | `41%` | `44%` | `27%` | `49%` |
| OR BETWEEN_CLOSE_AND_HIGH | 622 | `51%` | `40%` | `44%` | `43%` | `25%` | `62%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 535 | `50%` | `37%` | `43%` | `50%` | `28%` | `68%` ⭐ |
| ATR Creciente (>10%) | 115 | `46%` | `49%` | `47%` | `46%` | `41%` | `68%` ⭐ |
| ATR Decreciente (<-10%) | 73 | `52%` | `37%` | `42%` | `49%` | `24%` | `56%` |
| ATR Q1 (Baja Vol Historica) | 468 | `48%` | `36%` | `42%` | `40%` | `25%` | `58%` |
| ATR Q4 (Alta Vol Historica) | 466 | `49%` | `37%` | `46%` | `50%` | `30%` | `59%` |
| RSI Diario < 35 | 115 | `53%` | `46%` | `51%` | `52%` | `34%` | `61%` ⭐ |
| RSI Diario > 65 | 405 | `49%` | `42%` | `41%` | `40%` | `23%` | `60%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `170 min` | `135 min` | `300 min` |
| TP DOWN (desde entrada) | `120 min` | `75 min` | `225 min` |
| False Break UP → SL | `110 min` | - | - |
| False Break DOWN → SL | `106 min` | - | - |

---

## Permutación #7: NY Cash 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1877`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.24%`
- **Rotura Bajista (DOWN):** `45.66%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `45.28%` | `48.89%` |
| 1.5x Rango OR | `28.31%` | `34.07%` |
| 2.0x Rango OR | `18.13%` | `24.50%` |
| 1.0x Volatilidad ATR Diaria | `6.26%` | `12.60%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `36.69%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `42.36%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `56.47%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `48.22%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `39.18%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1243`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `22.69%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `16.17%` |
| Shakeout & Re-breakout UP (>=2x OR) | `12.47%` |
| Continuacion Bajista (>=1x OR) | `47.95%` |
| Extension media reversal UP | `0.74x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.70x OR` | Mediana: `0.95x` |
| Tiempo medio al re-breakout | `95 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1350`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `20.37%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `15.33%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.37%` |
| Continuacion Alcista (>=1x OR) | `43.85%` |
| Extension media reversal DOWN | `0.77x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.36x OR` | Mediana: `0.85x` |
| Tiempo medio al re-breakout | `96 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 187 | `18%` | `15%` | `35%` | `31%` | `13%` | `39%` |
| RSI > 70 (Overbought) | 250 | `86%` ⭐ | `20%` | `33%` | `41%` | `9%` | `32%` |
| RSI 30-70 (Neutro) | 1440 | `48%` | `32%` | `38%` | `45%` | `26%` | `63%` ⭐ |
| OR ABOVE_PD_HIGH | 439 | `48%` | `32%` | `33%` | `41%` | `20%` | `48%` |
| OR BELOW_PD_LOW | 284 | `50%` | `28%` | `36%` | `41%` | `28%` | `48%` |
| OR BETWEEN_CLOSE_AND_HIGH | 616 | `52%` | `27%` | `39%` | `41%` | `23%` | `59%` |
| OR BETWEEN_LOW_AND_CLOSE | 538 | `50%` | `27%` | `36%` | `46%` | `22%` | `66%` ⭐ |
| ATR Creciente (>10%) | 113 | `44%` | `36%` | `40%` | `44%` | `35%` | `67%` ⭐ |
| ATR Decreciente (<-10%) | 78 | `50%` | `23%` | `36%` | `51%` | `27%` | `55%` |
| ATR Q1 (Baja Vol Historica) | 462 | `49%` | `28%` | `35%` | `40%` | `23%` | `56%` |
| ATR Q4 (Alta Vol Historica) | 478 | `51%` | `27%` | `43%` | `46%` | `27%` | `57%` |
| RSI Diario < 35 | 114 | `51%` | `36%` | `43%` | `57%` | `29%` | `61%` ⭐ |
| RSI Diario > 65 | 414 | `46%` | `38%` | `34%` | `41%` | `21%` | `57%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `163 min` | `105 min` | `300 min` |
| TP DOWN (desde entrada) | `124 min` | `75 min` | `240 min` |
| False Break UP → SL | `119 min` | - | - |
| False Break DOWN → SL | `106 min` | - | - |

---

## Permutación #8: NY Cash 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1859`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.93%`
- **Rotura Bajista (DOWN):** `42.28%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `41.30%` | `45.17%` |
| 1.5x Rango OR | `25.59%` | `30.79%` |
| 2.0x Rango OR | `17.28%` | `21.76%` |
| 1.0x Volatilidad ATR Diaria | `6.29%` | `12.47%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `30.08%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `35.75%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `55.35%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `47.07%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `38.11%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1181`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `20.49%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `14.48%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.09%` |
| Continuacion Bajista (>=1x OR) | `45.05%` |
| Extension media reversal UP | `0.63x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.55x OR` | Mediana: `0.86x` |
| Tiempo medio al re-breakout | `96 min` | Mediana: `52 min` |

**False Breakouts DOWN analizados:** `1299`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `19.63%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `14.86%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `11.86%` |
| Continuacion Alcista (>=1x OR) | `39.65%` |
| Extension media reversal DOWN | `0.69x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.27x OR` | Mediana: `0.77x` |
| Tiempo medio al re-breakout | `96 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 150 | `11%` | `29%` | `29%` | `27%` | `13%` | `33%` |
| RSI > 70 (Overbought) | 216 | `80%` ⭐ | `10%` | `23%` | `25%` | `7%` | `27%` |
| RSI 30-70 (Neutro) | 1493 | `47%` | `29%` | `32%` | `38%` | `23%` | `62%` ⭐ |
| OR ABOVE_PD_HIGH | 442 | `45%` | `29%` | `27%` | `33%` | `18%` | `47%` |
| OR BELOW_PD_LOW | 276 | `49%` | `26%` | `26%` | `34%` | `19%` | `48%` |
| OR BETWEEN_CLOSE_AND_HIGH | 613 | `48%` | `23%` | `32%` | `38%` | `23%` | `57%` |
| OR BETWEEN_LOW_AND_CLOSE | 528 | `49%` | `25%` | `32%` | `37%` | `20%` | `64%` ⭐ |
| ATR Creciente (>10%) | 112 | `46%` | `29%` | `35%` | `42%` | `28%` | `65%` ⭐ |
| ATR Decreciente (<-10%) | 77 | `51%` | `23%` | `26%` | `40%` | `24%` | `52%` |
| ATR Q1 (Baja Vol Historica) | 454 | `46%` | `27%` | `30%` | `34%` | `22%` | `55%` |
| ATR Q4 (Alta Vol Historica) | 485 | `47%` | `27%` | `34%` | `39%` | `24%` | `56%` |
| RSI Diario < 35 | 112 | `46%` | `31%` | `31%` | `50%` | `25%` | `59%` |
| RSI Diario > 65 | 406 | `45%` | `33%` | `34%` | `36%` | `19%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `145 min` | `90 min` | `285 min` |
| TP DOWN (desde entrada) | `124 min` | `75 min` | `240 min` |
| False Break UP → SL | `140 min` | - | - |
| False Break DOWN → SL | `130 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: NASDAQ100

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (15m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `88.37%` (base: `76.15%`, +12%pp). N=79.

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (30m) | RSI Diario < 35**: Extension 1.5x DOWN sube a `80.85%` (base: `70.18%`, +11%pp). N=97.

- **[EDGE CONTEXT-BOOST DOWN] Pre-Market (45m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `74.00%` (base: `60.84%`, +13%pp). N=121.

- **[EDGE CONTEXT-BOOST UP] Pre-Market (30m) | RSI Diario < 35**: Extension 1.5x UP sube a `86.05%` (base: `71.91%`, +14%pp). N=97. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] Pre-Market (45m) | RSI Diario < 35**: Extension 1.5x UP sube a `75.47%` (base: `63.02%`, +12%pp). N=106. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] Pre-Market (60m) | RSI Diario < 35**: Extension 1.5x UP sube a `73.21%` (base: `59.76%`, +13%pp). N=109. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] NY Cash (15m)**: Imantación cíclica brutal. El `60.65%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (15m)**: Imantación cíclica brutal. El `68.89%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (30m)**: Imantación cíclica brutal. El `68.00%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (45m)**: Imantación cíclica brutal. El `66.69%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (60m)**: Imantación cíclica brutal. El `66.41%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE RSI-CONDITIONAL] Pre-Market (15m) | RSI 30-70 (Neutro)**: Shakeout UP post-fade al `68.91%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=580.

- **[EDGE RSI-CONDITIONAL] Pre-Market (15m) | RSI < 30 (Oversold)**: Shakeout UP post-fade al `60.34%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=64.

- **[EDGE RSI-CONDITIONAL] Pre-Market (15m) | RSI Diario < 35**: Shakeout UP post-fade al `74.07%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=67.

- **[EDGE RSI-CONDITIONAL] Pre-Market (30m) | RSI 30-70 (Neutro)**: Shakeout UP post-fade al `62.53%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=1122.

- **[EDGE RSI-CONDITIONAL] Pre-Market (30m) | RSI Diario < 35**: Shakeout UP post-fade al `73.68%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=97.

- **[EDGE RSI-CONDITIONAL] Pre-Market (45m) | RSI Diario < 35**: Shakeout UP post-fade al `63.75%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=106.

- **[EDGE SHAKEOUT-REVERSAL DOWN] Pre-Market (15m)**: Despues de un falso rompimiento bajista, el `66.73%` retoma direccion DOWN con extension >=1x OR. Media reversal: `3.32x OR` | Tiempo medio al re-breakout: 79 min. Sugerencia Algo: Orden limite de VENTA en OR_High tras primer rompimiento DOWN.

- **[EDGE SHAKEOUT-REVERSAL UP] Pre-Market (15m)**: Despues de un falso rompimiento alcista, el `67.40%` de las veces el precio retoma la direccion UP con extension >=1x OR. Media reversal: `2.95x OR` | Tiempo medio al re-breakout: 77 min. Sugerencia Algo: Orden limite de COMPRA en OR_Low tras primer rompimiento UP. El mercado barre stops y luego arranca.

- **[EDGE SHAKEOUT-REVERSAL UP] Pre-Market (30m)**: Despues de un falso rompimiento alcista, el `61.74%` de las veces el precio retoma la direccion UP con extension >=1x OR. Media reversal: `2.46x OR` | Tiempo medio al re-breakout: 75 min. Sugerencia Algo: Orden limite de COMPRA en OR_Low tras primer rompimiento UP. El mercado barre stops y luego arranca.

- **[EDGE TENDENCIAL DOWN] Pre-Market (15m)**: Tasa de extensión polar bajista (1.5x) del `76.15%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Pre-Market (30m)**: Tasa de extensión polar bajista (1.5x) del `70.18%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Pre-Market (45m)**: Tasa de extensión polar bajista (1.5x) del `60.84%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] Pre-Market (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `74.77%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `71.91%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `63.02%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Pre-Market 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=170 | UP: `53%` | Ext 1.5 UP: `76%` | Falsa Ruptura DW: `60%` | Reversión a PD_Close: `66%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=169 | UP: `44%` | Ext 1.5 UP: `68%` | Falsa Ruptura DW: `57%` | Reversión a PD_Close: `66%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=31 | UP: `32%` | Ext 1.5 UP: `80%` | Falsa Ruptura DW: `58%` | Reversión a PD_Close: `52%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=644 | UP: `49%` | Ext 1.5 UP: `75%` | Falsa Ruptura DW: `53%` | Reversión a PD_Close: `70%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*