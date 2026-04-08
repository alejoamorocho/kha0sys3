# 🌐 Matriz Probabilística Omnidireccional: GBPJPY

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
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1355`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.00%`
- **Rotura Bajista (DOWN):** `48.41%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `81.63%` | `82.77%` |
| 1.5x Rango OR | `71.69%` | `75.30%` |
| 2.0x Rango OR | `64.76%` | `64.48%` |
| 1.0x Volatilidad ATR Diaria | `17.32%` | `17.68%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.08%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.47%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `88.93%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `70.26%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `47.38%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1047`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `37.73%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `28.27%` |
| Shakeout & Re-breakout UP (>=2x OR) | `20.92%` |
| Continuacion Bajista (>=1x OR) | `64.95%` |
| Extension media reversal UP | `1.13x OR` | Mediana: `0.51x` |
| Extension media continuacion DOWN | `2.14x OR` | Mediana: `1.58x` |
| Tiempo medio al re-breakout | `141 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1051`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `38.63%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `29.88%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `22.74%` |
| Continuacion Alcista (>=1x OR) | `65.08%` |
| Extension media reversal DOWN | `1.32x OR` | Mediana: `0.51x` |
| Extension media continuacion UP | `2.09x OR` | Mediana: `1.51x` |
| Tiempo medio al re-breakout | `146 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 51 | `25%` | `69%` ⭐ | `46%` | `53%` | `23%` | `82%` ⭐ |
| RSI > 70 (Overbought) | 49 | `82%` ⭐ | `70%` ⭐ | `65%` ⭐ | `56%` | `27%` | `84%` ⭐ |
| RSI 30-70 (Neutro) | 1255 | `49%` | `72%` ⭐ | `57%` | `58%` | `39%` | `89%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 810 | `48%` | `73%` ⭐ | `57%` | `56%` | `37%` | `89%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 544 | `50%` | `69%` ⭐ | `57%` | `59%` | `38%` | `89%` ⭐ |
| ATR Creciente (>10%) | 89 | `43%` | `74%` ⭐ | `58%` | `51%` | `32%` | `92%` ⭐ |
| ATR Decreciente (<-10%) | 60 | `47%` | `71%` ⭐ | `61%` ⭐ | `50%` | `42%` | `88%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 374 | `49%` | `70%` ⭐ | `59%` | `52%` | `35%` | `89%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 320 | `49%` | `71%` ⭐ | `51%` | `60%` | `38%` | `87%` ⭐ |
| RSI Diario < 35 | 130 | `51%` | `77%` ⭐ | `53%` | `57%` | `30%` | `89%` ⭐ |
| RSI Diario > 65 | 198 | `51%` | `74%` ⭐ | `57%` | `56%` | `38%` | `89%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `333 min` | `315 min` | `525 min` |
| TP DOWN (desde entrada) | `313 min` | `240 min` | `540 min` |
| False Break UP → SL | `153 min` | - | - |
| False Break DOWN → SL | `137 min` | - | - |

---

## Permutación #2: Tokyo 30m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1749`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.09%`
- **Rotura Bajista (DOWN):** `46.26%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `77.61%` | `78.74%` |
| 1.5x Rango OR | `66.08%` | `67.49%` |
| 2.0x Rango OR | `56.75%` | `57.85%` |
| 1.0x Volatilidad ATR Diaria | `15.92%` | `15.70%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.60%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.84%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `88.22%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `69.87%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `47.34%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1325`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `30.26%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `20.91%` |
| Shakeout & Re-breakout UP (>=2x OR) | `14.79%` |
| Continuacion Bajista (>=1x OR) | `58.87%` |
| Extension media reversal UP | `0.85x OR` | Mediana: `0.29x` |
| Extension media continuacion DOWN | `1.86x OR` | Mediana: `1.30x` |
| Tiempo medio al re-breakout | `163 min` | Mediana: `120 min` |

**False Breakouts DOWN analizados:** `1363`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `32.21%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `24.14%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `18.05%` |
| Continuacion Alcista (>=1x OR) | `58.11%` |
| Extension media reversal DOWN | `1.07x OR` | Mediana: `0.29x` |
| Extension media continuacion UP | `1.70x OR` | Mediana: `1.23x` |
| Tiempo medio al re-breakout | `159 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 53 | `17%` | `44%` | `67%` ⭐ | `48%` | `22%` | `77%` ⭐ |
| RSI > 70 (Overbought) | 68 | `87%` ⭐ | `64%` ⭐ | `66%` ⭐ | `67%` ⭐ | `26%` | `78%` ⭐ |
| RSI 30-70 (Neutro) | 1628 | `52%` | `66%` ⭐ | `59%` | `59%` | `31%` | `89%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1032 | `53%` | `68%` ⭐ | `59%` | `59%` | `30%` | `88%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 715 | `51%` | `63%` ⭐ | `60%` ⭐ | `59%` | `31%` | `88%` ⭐ |
| ATR Creciente (>10%) | 100 | `45%` | `76%` ⭐ | `53%` | `61%` ⭐ | `22%` | `89%` ⭐ |
| ATR Decreciente (<-10%) | 71 | `35%` | `60%` ⭐ | `60%` ⭐ | `53%` | `33%` | `89%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 471 | `54%` | `65%` ⭐ | `60%` | `55%` | `28%` | `88%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 416 | `51%` | `64%` ⭐ | `58%` | `58%` | `27%` | `87%` ⭐ |
| RSI Diario < 35 | 165 | `57%` | `68%` ⭐ | `53%` | `57%` | `24%` | `88%` ⭐ |
| RSI Diario > 65 | 256 | `54%` | `69%` ⭐ | `57%` | `54%` | `27%` | `87%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `378 min` | `345 min` | `600 min` |
| TP DOWN (desde entrada) | `354 min` | `330 min` | `585 min` |
| False Break UP → SL | `186 min` | - | - |
| False Break DOWN → SL | `190 min` | - | - |

---

## Permutación #3: Tokyo 45m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1936`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.50%`
- **Rotura Bajista (DOWN):** `46.44%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `74.22%` | `75.08%` |
| 1.5x Rango OR | `61.18%` | `63.40%` |
| 2.0x Rango OR | `52.36%` | `54.17%` |
| 1.0x Volatilidad ATR Diaria | `15.15%` | `14.57%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.18%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.73%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `87.45%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `69.78%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.85%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1448`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `25.62%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `16.44%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.40%` |
| Continuacion Bajista (>=1x OR) | `54.14%` |
| Extension media reversal UP | `0.71x OR` | Mediana: `0.12x` |
| Extension media continuacion DOWN | `1.66x OR` | Mediana: `1.13x` |
| Tiempo medio al re-breakout | `177 min` | Mediana: `135 min` |

**False Breakouts DOWN analizados:** `1494`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `27.78%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `20.01%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `14.73%` |
| Continuacion Alcista (>=1x OR) | `53.15%` |
| Extension media reversal DOWN | `0.88x OR` | Mediana: `0.12x` |
| Extension media continuacion UP | `1.49x OR` | Mediana: `1.08x` |
| Tiempo medio al re-breakout | `167 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 61 | `16%` | `50%` | `50%` | `65%` ⭐ | `12%` | `79%` ⭐ |
| RSI > 70 (Overbought) | 77 | `90%` ⭐ | `61%` ⭐ | `62%` ⭐ | `75%` ⭐ | `18%` | `74%` ⭐ |
| RSI 30-70 (Neutro) | 1798 | `51%` | `61%` ⭐ | `59%` | `59%` | `26%` | `88%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1147 | `50%` | `63%` ⭐ | `59%` | `61%` ⭐ | `26%` | `87%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 787 | `53%` | `58%` | `59%` | `58%` | `25%` | `88%` ⭐ |
| ATR Creciente (>10%) | 102 | `47%` | `71%` ⭐ | `50%` | `65%` ⭐ | `17%` | `87%` ⭐ |
| ATR Decreciente (<-10%) | 79 | `34%` | `56%` | `52%` | `58%` | `28%` | `90%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 506 | `50%` | `61%` ⭐ | `61%` ⭐ | `56%` | `26%` | `88%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 466 | `53%` | `57%` | `57%` | `57%` | `23%` | `86%` ⭐ |
| RSI Diario < 35 | 175 | `55%` | `64%` ⭐ | `56%` | `54%` | `22%` | `87%` ⭐ |
| RSI Diario > 65 | 289 | `53%` | `63%` ⭐ | `58%` | `54%` | `21%` | `87%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `397 min` | `375 min` | `615 min` |
| TP DOWN (desde entrada) | `374 min` | `360 min` | `600 min` |
| False Break UP → SL | `213 min` | - | - |
| False Break DOWN → SL | `227 min` | - | - |

---

## Permutación #4: Tokyo 60m
**Configuración:** Inicia a las `00:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2053`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.27%`
- **Rotura Bajista (DOWN):** `48.95%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `70.83%` | `71.14%` |
| 1.5x Rango OR | `59.21%` | `58.41%` |
| 2.0x Rango OR | `50.39%` | `48.56%` |
| 1.0x Volatilidad ATR Diaria | `15.02%` | `14.83%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.33%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.10%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `85.68%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `69.02%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.91%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1448`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `17.96%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `10.22%` |
| Shakeout & Re-breakout UP (>=2x OR) | `6.84%` |
| Continuacion Bajista (>=1x OR) | `48.34%` |
| Extension media reversal UP | `0.49x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.38x OR` | Mediana: `0.97x` |
| Tiempo medio al re-breakout | `192 min` | Mediana: `180 min` |

**False Breakouts DOWN analizados:** `1483`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `20.09%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `13.35%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `9.24%` |
| Continuacion Alcista (>=1x OR) | `46.86%` |
| Extension media reversal DOWN | `0.59x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.25x OR` | Mediana: `0.92x` |
| Tiempo medio al re-breakout | `183 min` | Mediana: `165 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 78 | `21%` | `38%` | `56%` | `56%` | `4%` | `76%` ⭐ |
| RSI > 70 (Overbought) | 90 | `87%` ⭐ | `54%` | `59%` | `67%` ⭐ | `8%` | `71%` ⭐ |
| RSI 30-70 (Neutro) | 1885 | `50%` | `60%` ⭐ | `55%` | `59%` | `19%` | `87%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 1220 | `49%` | `62%` ⭐ | `54%` | `61%` ⭐ | `19%` | `85%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 831 | `52%` | `55%` | `56%` | `57%` | `16%` | `86%` ⭐ |
| ATR Creciente (>10%) | 106 | `42%` | `71%` ⭐ | `47%` | `64%` ⭐ | `9%` | `86%` ⭐ |
| ATR Decreciente (<-10%) | 83 | `33%` | `52%` | `48%` | `64%` ⭐ | `15%` | `86%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 530 | `46%` | `61%` ⭐ | `54%` | `59%` | `19%` | `87%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 497 | `50%` | `54%` | `54%` | `56%` | `15%` | `84%` ⭐ |
| RSI Diario < 35 | 182 | `51%` | `64%` ⭐ | `50%` | `55%` | `14%` | `85%` ⭐ |
| RSI Diario > 65 | 307 | `48%` | `65%` ⭐ | `52%` | `55%` | `15%` | `86%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `415 min` | `375 min` | `630 min` |
| TP DOWN (desde entrada) | `402 min` | `375 min` | `600 min` |
| False Break UP → SL | `262 min` | - | - |
| False Break DOWN → SL | `283 min` | - | - |

---

## Permutación #5: London 15m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1718`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.44%`
- **Rotura Bajista (DOWN):** `48.25%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `76.56%` | `74.67%` |
| 1.5x Rango OR | `65.89%` | `62.85%` |
| 2.0x Rango OR | `56.93%` | `53.32%` |
| 1.0x Volatilidad ATR Diaria | `11.53%` | `13.51%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.58%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.21%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `65.83%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.33%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.18%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1337`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `46.45%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `36.28%` |
| Shakeout & Re-breakout UP (>=2x OR) | `29.92%` |
| Continuacion Bajista (>=1x OR) | `70.98%` |
| Extension media reversal UP | `1.59x OR` | Mediana: `0.77x` |
| Extension media continuacion DOWN | `2.62x OR` | Mediana: `1.95x` |
| Tiempo medio al re-breakout | `110 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1339`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `46.53%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `38.01%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `31.07%` |
| Continuacion Alcista (>=1x OR) | `70.28%` |
| Extension media reversal DOWN | `1.69x OR` | Mediana: `0.82x` |
| Extension media continuacion UP | `2.47x OR` | Mediana: `1.88x` |
| Tiempo medio al re-breakout | `114 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 146 | `29%` | `63%` ⭐ | `58%` | `56%` | `46%` | `42%` |
| RSI > 70 (Overbought) | 142 | `70%` ⭐ | `59%` | `57%` | `63%` ⭐ | `40%` | `39%` |
| RSI 30-70 (Neutro) | 1430 | `47%` | `67%` ⭐ | `55%` | `56%` | `47%` | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 322 | `48%` | `68%` ⭐ | `55%` | `54%` | `42%` | `52%` |
| OR BELOW_PD_LOW | 251 | `47%` | `76%` ⭐ | `43%` | `53%` | `50%` | `51%` |
| OR BETWEEN_CLOSE_AND_HIGH | 538 | `47%` | `64%` ⭐ | `59%` | `59%` | `47%` | `74%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 607 | `47%` | `62%` ⭐ | `58%` | `57%` | `47%` | `72%` ⭐ |
| ATR Creciente (>10%) | 102 | `45%` | `63%` ⭐ | `61%` ⭐ | `55%` | `44%` | `67%` ⭐ |
| ATR Decreciente (<-10%) | 64 | `53%` | `76%` ⭐ | `47%` | `52%` | `47%` | `70%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 472 | `44%` | `68%` ⭐ | `51%` | `52%` | `45%` | `67%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 385 | `51%` | `62%` ⭐ | `57%` | `62%` ⭐ | `44%` | `64%` ⭐ |
| RSI Diario < 35 | 159 | `52%` | `66%` ⭐ | `55%` | `63%` ⭐ | `47%` | `63%` ⭐ |
| RSI Diario > 65 | 259 | `45%` | `66%` ⭐ | `59%` | `53%` | `47%` | `63%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `192 min` | `120 min` | `345 min` |
| TP DOWN (desde entrada) | `170 min` | `90 min` | `315 min` |
| False Break UP → SL | `101 min` | - | - |
| False Break DOWN → SL | `103 min` | - | - |

---

## Permutación #6: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1979`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.62%`
- **Rotura Bajista (DOWN):** `48.21%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `70.06%` | `69.81%` |
| 1.5x Rango OR | `57.54%` | `55.77%` |
| 2.0x Rango OR | `46.54%` | `46.65%` |
| 1.0x Volatilidad ATR Diaria | `10.90%` | `13.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.05%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.39%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `64.93%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.10%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.28%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1484`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `35.18%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `26.55%` |
| Shakeout & Re-breakout UP (>=2x OR) | `20.15%` |
| Continuacion Bajista (>=1x OR) | `63.75%` |
| Extension media reversal UP | `1.11x OR` | Mediana: `0.37x` |
| Extension media continuacion DOWN | `2.07x OR` | Mediana: `1.51x` |
| Tiempo medio al re-breakout | `125 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1531`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `36.45%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `28.35%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `21.49%` |
| Continuacion Alcista (>=1x OR) | `62.44%` |
| Extension media reversal DOWN | `1.20x OR` | Mediana: `0.37x` |
| Extension media continuacion UP | `1.97x OR` | Mediana: `1.40x` |
| Tiempo medio al re-breakout | `131 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 161 | `24%` | `56%` | `38%` | `57%` | `28%` | `45%` |
| RSI > 70 (Overbought) | 167 | `76%` ⭐ | `44%` | `58%` | `54%` | `36%` | `35%` |
| RSI 30-70 (Neutro) | 1651 | `49%` | `60%` | `53%` | `56%` | `36%` | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 361 | `50%` | `59%` | `58%` | `51%` | `33%` | `52%` |
| OR BELOW_PD_LOW | 274 | `55%` | `56%` | `47%` | `54%` | `34%` | `50%` |
| OR BETWEEN_CLOSE_AND_HIGH | 645 | `48%` | `56%` | `56%` | `60%` ⭐ | `39%` | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 699 | `49%` | `59%` | `51%` | `56%` | `34%` | `70%` ⭐ |
| ATR Creciente (>10%) | 111 | `48%` | `62%` ⭐ | `55%` | `57%` | `38%` | `64%` ⭐ |
| ATR Decreciente (<-10%) | 76 | `54%` | `59%` | `49%` | `56%` | `39%` | `72%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 530 | `49%` | `58%` | `51%` | `53%` | `34%` | `67%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 458 | `55%` | `53%` | `53%` | `62%` ⭐ | `33%` | `62%` ⭐ |
| RSI Diario < 35 | 179 | `51%` | `66%` ⭐ | `44%` | `55%` | `36%` | `63%` ⭐ |
| RSI Diario > 65 | 301 | `50%` | `60%` ⭐ | `56%` | `58%` | `34%` | `62%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `222 min` | `165 min` | `360 min` |
| TP DOWN (desde entrada) | `201 min` | `135 min` | `345 min` |
| False Break UP → SL | `137 min` | - | - |
| False Break DOWN → SL | `138 min` | - | - |

---

## Permutación #7: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2067`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.38%`
- **Rotura Bajista (DOWN):** `46.88%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `65.73%` | `65.22%` |
| 1.5x Rango OR | `50.56%` | `50.77%` |
| 2.0x Rango OR | `38.79%` | `41.38%` |
| 1.0x Volatilidad ATR Diaria | `10.92%` | `13.42%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `50.75%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.08%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `63.18%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `55.97%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.28%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1480`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `27.30%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `18.31%` |
| Shakeout & Re-breakout UP (>=2x OR) | `13.65%` |
| Continuacion Bajista (>=1x OR) | `58.38%` |
| Extension media reversal UP | `0.77x OR` | Mediana: `0.09x` |
| Extension media continuacion DOWN | `1.76x OR` | Mediana: `1.27x` |
| Tiempo medio al re-breakout | `133 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1569`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `28.74%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `20.91%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `15.36%` |
| Continuacion Alcista (>=1x OR) | `57.17%` |
| Extension media reversal DOWN | `0.87x OR` | Mediana: `0.09x` |
| Extension media continuacion UP | `1.64x OR` | Mediana: `1.20x` |
| Tiempo medio al re-breakout | `142 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 163 | `17%` | `37%` | `30%` | `53%` | `17%` | `42%` |
| RSI > 70 (Overbought) | 161 | `80%` ⭐ | `40%` | `51%` | `39%` | `22%` | `34%` |
| RSI 30-70 (Neutro) | 1743 | `52%` | `53%` | `51%` | `55%` | `29%` | `68%` ⭐ |
| OR ABOVE_PD_HIGH | 379 | `49%` | `52%` | `53%` | `49%` | `26%` | `51%` |
| OR BELOW_PD_LOW | 277 | `56%` | `46%` | `42%` | `53%` | `26%` | `49%` |
| OR BETWEEN_CLOSE_AND_HIGH | 679 | `52%` | `51%` | `53%` | `59%` | `29%` | `71%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 732 | `51%` | `51%` | `51%` | `52%` | `26%` | `67%` ⭐ |
| ATR Creciente (>10%) | 111 | `50%` | `53%` | `56%` | `52%` | `26%` | `61%` ⭐ |
| ATR Decreciente (<-10%) | 84 | `57%` | `54%` | `50%` | `51%` | `33%` | `71%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 536 | `52%` | `51%` | `49%` | `51%` | `25%` | `65%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 493 | `57%` | `48%` | `53%` | `57%` | `23%` | `61%` ⭐ |
| RSI Diario < 35 | 185 | `51%` | `59%` | `41%` | `56%` | `26%` | `59%` |
| RSI Diario > 65 | 312 | `50%` | `52%` | `50%` | `47%` | `26%` | `60%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `239 min` | `210 min` | `375 min` |
| TP DOWN (desde entrada) | `231 min` | `195 min` | `375 min` |
| False Break UP → SL | `171 min` | - | - |
| False Break DOWN → SL | `163 min` | - | - |

---

## Permutación #8: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2087`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.99%`
- **Rotura Bajista (DOWN):** `44.85%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `60.67%` | `61.11%` |
| 1.5x Rango OR | `45.12%` | `46.79%` |
| 2.0x Rango OR | `33.09%` | `35.79%` |
| 1.0x Volatilidad ATR Diaria | `10.49%` | `12.71%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `49.28%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `49.89%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `62.48%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `54.96%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.76%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1444`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `20.29%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `13.02%` |
| Shakeout & Re-breakout UP (>=2x OR) | `8.86%` |
| Continuacion Bajista (>=1x OR) | `54.16%` |
| Extension media reversal UP | `0.57x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.53x OR` | Mediana: `1.13x` |
| Tiempo medio al re-breakout | `148 min` | Mediana: `120 min` |

**False Breakouts DOWN analizados:** `1553`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `23.50%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `15.90%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `11.27%` |
| Continuacion Alcista (>=1x OR) | `51.00%` |
| Extension media reversal DOWN | `0.68x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.40x OR` | Mediana: `1.02x` |
| Tiempo medio al re-breakout | `152 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 147 | `14%` | `33%` | `24%` | `50%` | `13%` | `36%` |
| RSI > 70 (Overbought) | 156 | `84%` ⭐ | `37%` | `47%` | `29%` | `21%` | `34%` |
| RSI 30-70 (Neutro) | 1784 | `53%` | `47%` | `50%` | `50%` | `21%` | `67%` ⭐ |
| OR ABOVE_PD_HIGH | 383 | `49%` | `46%` | `49%` | `46%` | `20%` | `51%` |
| OR BELOW_PD_LOW | 273 | `57%` | `42%` | `41%` | `50%` | `19%` | `50%` |
| OR BETWEEN_CLOSE_AND_HIGH | 689 | `54%` | `46%` | `54%` | `55%` | `22%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 742 | `52%` | `45%` | `49%` | `47%` | `20%` | `66%` ⭐ |
| ATR Creciente (>10%) | 110 | `51%` | `48%` | `52%` | `43%` | `19%` | `63%` ⭐ |
| ATR Decreciente (<-10%) | 85 | `52%` | `55%` | `43%` | `55%` | `23%` | `69%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 533 | `52%` | `44%` | `49%` | `48%` | `20%` | `64%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 506 | `58%` | `42%` | `51%` | `48%` | `16%` | `60%` ⭐ |
| RSI Diario < 35 | 184 | `53%` | `55%` | `42%` | `50%` | `21%` | `60%` |
| RSI Diario > 65 | 315 | `52%` | `46%` | `52%` | `48%` | `21%` | `59%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `263 min` | `240 min` | `405 min` |
| TP DOWN (desde entrada) | `248 min` | `210 min` | `390 min` |
| False Break UP → SL | `194 min` | - | - |
| False Break DOWN → SL | `193 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: GBPJPY

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST UP] London (15m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `76.47%` (base: `65.89%`, +11%pp). N=64. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (15m) | OR BELOW_PD_LOW**: Extension 1.5x UP sube a `76.47%` (base: `65.89%`, +11%pp). N=251. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] Tokyo (60m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `71.11%` (base: `59.21%`, +12%pp). N=106. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `65.83%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `64.93%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `63.18%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `62.48%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (15m)**: Imantación cíclica brutal. El `88.93%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (30m)**: Imantación cíclica brutal. El `88.22%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (45m)**: Imantación cíclica brutal. El `87.45%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Tokyo (60m)**: Imantación cíclica brutal. El `85.68%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] Tokyo (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `70.26%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `69.87%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `69.78%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Tokyo (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `69.02%` de los eventos evaluados.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `62.85%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (15m)**: Tasa de extensión polar bajista (1.5x) del `75.30%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (30m)**: Tasa de extensión polar bajista (1.5x) del `67.49%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Tokyo (45m)**: Tasa de extensión polar bajista (1.5x) del `63.40%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `65.89%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `71.69%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `66.08%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Tokyo (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `61.18%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Tokyo 30m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=438 | UP: `52%` | Ext 1.5 UP: `74%` | Falsa Ruptura DW: `58%` | Reversión a PD_Close: `92%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=438 | UP: `50%` | Ext 1.5 UP: `53%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `84%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=183 | UP: `54%` | Ext 1.5 UP: `67%` | Falsa Ruptura DW: `61%` | Reversión a PD_Close: `92%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1566 | UP: `52%` | Ext 1.5 UP: `66%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `88%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*