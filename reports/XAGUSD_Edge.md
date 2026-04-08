# 🌐 Matriz Probabilística Omnidireccional: XAGUSD

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
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1353`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.59%`
- **Rotura Bajista (DOWN):** `43.46%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.23%` | `79.93%` |
| 1.5x Rango OR | `68.05%` | `70.07%` |
| 2.0x Rango OR | `57.16%` | `62.59%` |
| 1.0x Volatilidad ATR Diaria | `12.46%` | `12.93%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `60.32%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `62.76%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `67.55%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.80%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.24%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1072`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `58.21%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `47.95%` |
| Shakeout & Re-breakout UP (>=2x OR) | `39.09%` |
| Continuacion Bajista (>=1x OR) | `74.53%` |
| Extension media reversal UP | `2.13x OR` | Mediana: `1.37x` |
| Extension media continuacion DOWN | `3.18x OR` | Mediana: `2.34x` |
| Tiempo medio al re-breakout | `122 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1133`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `55.96%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `47.84%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `40.07%` |
| Continuacion Alcista (>=1x OR) | `76.88%` |
| Extension media reversal DOWN | `2.23x OR` | Mediana: `1.36x` |
| Extension media continuacion UP | `2.90x OR` | Mediana: `2.22x` |
| Tiempo medio al re-breakout | `134 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 65 | `32%` | `76%` ⭐ | `62%` ⭐ | `68%` ⭐ | `59%` | `35%` |
| RSI > 70 (Overbought) | 89 | `70%` ⭐ | `61%` ⭐ | `68%` ⭐ | `77%` ⭐ | `64%` ⭐ | `39%` |
| RSI 30-70 (Neutro) | 1199 | `51%` | `68%` ⭐ | `60%` | `62%` ⭐ | `58%` | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 237 | `54%` | `67%` ⭐ | `68%` ⭐ | `69%` ⭐ | `64%` ⭐ | `55%` |
| OR BELOW_PD_LOW | 216 | `53%` | `66%` ⭐ | `65%` ⭐ | `59%` | `54%` | `48%` |
| OR BETWEEN_CLOSE_AND_HIGH | 412 | `48%` | `67%` ⭐ | `59%` | `64%` ⭐ | `59%` | `75%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 488 | `53%` | `70%` ⭐ | `55%` | `61%` ⭐ | `56%` | `77%` ⭐ |
| ATR Creciente (>10%) | 86 | `50%` | `81%` ⭐ | `56%` | `66%` ⭐ | `66%` ⭐ | `66%` ⭐ |
| ATR Decreciente (<-10%) | 51 | `59%` | `70%` ⭐ | `53%` | `53%` | `51%` | `71%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 376 | `52%` | `68%` ⭐ | `57%` | `61%` ⭐ | `56%` | `70%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 269 | `54%` | `65%` ⭐ | `57%` | `60%` | `50%` | `59%` |
| RSI Diario < 35 | 131 | `53%` | `67%` ⭐ | `63%` ⭐ | `62%` ⭐ | `51%` | `60%` ⭐ |
| RSI Diario > 65 | 240 | `50%` | `66%` ⭐ | `60%` | `55%` | `62%` ⭐ | `67%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `220 min` | `195 min` | `360 min` |
| TP DOWN (desde entrada) | `215 min` | `195 min` | `360 min` |
| False Break UP → SL | `105 min` | - | - |
| False Break DOWN → SL | `87 min` | - | - |

---

## Permutación #2: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1827`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `53.64%`
- **Rotura Bajista (DOWN):** `44.28%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `75.51%` | `76.02%` |
| 1.5x Rango OR | `63.16%` | `66.25%` |
| 2.0x Rango OR | `52.96%` | `56.86%` |
| 1.0x Volatilidad ATR Diaria | `12.45%` | `13.23%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.78%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `60.20%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `68.47%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `59.66%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.95%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1404`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `48.22%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `37.54%` |
| Shakeout & Re-breakout UP (>=2x OR) | `29.34%` |
| Continuacion Bajista (>=1x OR) | `70.30%` |
| Extension media reversal UP | `1.58x OR` | Mediana: `0.92x` |
| Extension media continuacion DOWN | `2.63x OR` | Mediana: `1.97x` |
| Tiempo medio al re-breakout | `140 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1501`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `49.23%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `41.04%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `33.64%` |
| Continuacion Alcista (>=1x OR) | `71.15%` |
| Extension media reversal DOWN | `1.77x OR` | Mediana: `0.93x` |
| Extension media continuacion UP | `2.41x OR` | Mediana: `1.82x` |
| Tiempo medio al re-breakout | `155 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 78 | `31%` | `62%` ⭐ | `50%` | `50%` | `25%` | `36%` |
| RSI > 70 (Overbought) | 102 | `74%` ⭐ | `63%` ⭐ | `57%` | `73%` ⭐ | `52%` | `45%` |
| RSI 30-70 (Neutro) | 1647 | `53%` | `63%` ⭐ | `59%` | `61%` ⭐ | `49%` | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 310 | `54%` | `60%` | `63%` ⭐ | `61%` ⭐ | `49%` | `57%` |
| OR BELOW_PD_LOW | 264 | `54%` | `63%` ⭐ | `62%` ⭐ | `56%` | `45%` | `50%` |
| OR BETWEEN_CLOSE_AND_HIGH | 578 | `54%` | `66%` ⭐ | `58%` | `62%` ⭐ | `51%` | `74%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 675 | `53%` | `63%` ⭐ | `56%` | `60%` ⭐ | `47%` | `76%` ⭐ |
| ATR Creciente (>10%) | 98 | `54%` | `57%` | `68%` ⭐ | `58%` | `56%` | `64%` ⭐ |
| ATR Decreciente (<-10%) | 71 | `51%` | `67%` ⭐ | `53%` | `67%` ⭐ | `50%` | `72%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 474 | `54%` | `65%` ⭐ | `56%` | `56%` | `46%` | `69%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 397 | `58%` | `54%` | `63%` ⭐ | `61%` ⭐ | `41%` | `61%` ⭐ |
| RSI Diario < 35 | 173 | `49%` | `61%` ⭐ | `58%` | `58%` | `42%` | `62%` ⭐ |
| RSI Diario > 65 | 298 | `52%` | `62%` ⭐ | `57%` | `64%` ⭐ | `51%` | `67%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `232 min` | `225 min` | `360 min` |
| TP DOWN (desde entrada) | `232 min` | `225 min` | `360 min` |
| False Break UP → SL | `146 min` | - | - |
| False Break DOWN → SL | `125 min` | - | - |

---

## Permutación #3: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2007`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `53.46%`
- **Rotura Bajista (DOWN):** `45.49%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.31%` | `74.59%` |
| 1.5x Rango OR | `56.20%` | `62.54%` |
| 2.0x Rango OR | `45.29%` | `51.59%` |
| 1.0x Volatilidad ATR Diaria | `11.46%` | `13.25%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.83%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.16%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `67.61%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `58.50%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.76%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1546`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `39.78%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `29.69%` |
| Shakeout & Re-breakout UP (>=2x OR) | `22.96%` |
| Continuacion Bajista (>=1x OR) | `66.75%` |
| Extension media reversal UP | `1.26x OR` | Mediana: `0.58x` |
| Extension media continuacion DOWN | `2.24x OR` | Mediana: `1.66x` |
| Tiempo medio al re-breakout | `147 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1618`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `42.65%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `32.32%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `24.10%` |
| Continuacion Alcista (>=1x OR) | `63.16%` |
| Extension media reversal DOWN | `1.36x OR` | Mediana: `0.65x` |
| Extension media continuacion UP | `2.03x OR` | Mediana: `1.46x` |
| Tiempo medio al re-breakout | `162 min` | Mediana: `135 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 86 | `22%` | `32%` | `63%` ⭐ | `48%` | `27%` | `35%` |
| RSI > 70 (Overbought) | 112 | `75%` ⭐ | `58%` | `57%` | `58%` | `37%` | `44%` |
| RSI 30-70 (Neutro) | 1809 | `54%` | `56%` | `60%` ⭐ | `59%` | `41%` | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 342 | `54%` | `52%` | `66%` ⭐ | `61%` ⭐ | `40%` | `56%` |
| OR BELOW_PD_LOW | 283 | `52%` | `52%` | `61%` ⭐ | `57%` | `39%` | `51%` |
| OR BETWEEN_CLOSE_AND_HIGH | 655 | `53%` | `60%` ⭐ | `57%` | `59%` | `42%` | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 727 | `54%` | `56%` | `59%` | `57%` | `38%` | `75%` ⭐ |
| ATR Creciente (>10%) | 102 | `56%` | `51%` | `65%` ⭐ | `55%` | `44%` | `63%` ⭐ |
| ATR Decreciente (<-10%) | 82 | `52%` | `49%` | `63%` ⭐ | `64%` ⭐ | `44%` | `63%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 517 | `53%` | `58%` | `57%` | `56%` | `40%` | `69%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 461 | `57%` | `52%` | `62%` ⭐ | `55%` | `31%` | `59%` |
| RSI Diario < 35 | 183 | `51%` | `56%` | `63%` ⭐ | `55%` | `34%` | `62%` ⭐ |
| RSI Diario > 65 | 320 | `55%` | `56%` | `55%` | `62%` ⭐ | `41%` | `65%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `259 min` | `270 min` | `360 min` |
| TP DOWN (desde entrada) | `243 min` | `255 min` | `360 min` |
| False Break UP → SL | `172 min` | - | - |
| False Break DOWN → SL | `146 min` | - | - |

---

## Permutación #4: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2058`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.67%`
- **Rotura Bajista (DOWN):** `45.92%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `65.22%` | `70.79%` |
| 1.5x Rango OR | `52.03%` | `56.83%` |
| 2.0x Rango OR | `40.87%` | `45.61%` |
| 1.0x Volatilidad ATR Diaria | `11.25%` | `13.65%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.67%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.14%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `67.40%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `58.02%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.70%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1568`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `32.84%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `24.30%` |
| Shakeout & Re-breakout UP (>=2x OR) | `18.18%` |
| Continuacion Bajista (>=1x OR) | `62.05%` |
| Extension media reversal UP | `1.01x OR` | Mediana: `0.38x` |
| Extension media continuacion DOWN | `1.96x OR` | Mediana: `1.42x` |
| Tiempo medio al re-breakout | `154 min` | Mediana: `120 min` |

**False Breakouts DOWN analizados:** `1638`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `36.75%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `26.56%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `20.39%` |
| Continuacion Alcista (>=1x OR) | `57.08%` |
| Extension media reversal DOWN | `1.11x OR` | Mediana: `0.40x` |
| Extension media continuacion UP | `1.76x OR` | Mediana: `1.23x` |
| Tiempo medio al re-breakout | `167 min` | Mediana: `150 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 86 | `17%` | `33%` | `73%` ⭐ | `46%` | `21%` | `38%` |
| RSI > 70 (Overbought) | 118 | `81%` ⭐ | `49%` | `55%` | `67%` ⭐ | `24%` | `42%` |
| RSI 30-70 (Neutro) | 1854 | `53%` | `53%` | `59%` | `58%` | `34%` | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 348 | `54%` | `51%` | `63%` ⭐ | `58%` | `33%` | `57%` |
| OR BELOW_PD_LOW | 286 | `54%` | `46%` | `58%` | `55%` | `31%` | `52%` |
| OR BETWEEN_CLOSE_AND_HIGH | 678 | `50%` | `58%` | `56%` | `59%` | `35%` | `72%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 746 | `54%` | `50%` | `59%` | `55%` | `32%` | `74%` ⭐ |
| ATR Creciente (>10%) | 104 | `53%` | `55%` | `58%` | `60%` | `37%` | `63%` ⭐ |
| ATR Decreciente (<-10%) | 86 | `58%` | `48%` | `56%` | `54%` | `33%` | `63%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 523 | `52%` | `53%` | `54%` | `54%` | `30%` | `68%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 486 | `58%` | `46%` | `62%` ⭐ | `56%` | `26%` | `60%` ⭐ |
| RSI Diario < 35 | 187 | `49%` | `51%` | `59%` | `53%` | `27%` | `62%` ⭐ |
| RSI Diario > 65 | 323 | `58%` | `55%` | `55%` | `61%` ⭐ | `35%` | `65%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `270 min` | `270 min` | `375 min` |
| TP DOWN (desde entrada) | `246 min` | `255 min` | `360 min` |
| False Break UP → SL | `192 min` | - | - |
| False Break DOWN → SL | `167 min` | - | - |

---

## Permutación #5: NY 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1992`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.99%`
- **Rotura Bajista (DOWN):** `44.93%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `55.65%` | `58.88%` |
| 1.5x Rango OR | `40.59%` | `42.46%` |
| 2.0x Rango OR | `28.14%` | `32.85%` |
| 1.0x Volatilidad ATR Diaria | `6.38%` | `7.49%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `48.74%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `47.37%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `46.29%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `40.31%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `35.37%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1482`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `25.37%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `17.81%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.88%` |
| Continuacion Bajista (>=1x OR) | `54.18%` |
| Extension media reversal UP | `0.76x OR` | Mediana: `0.09x` |
| Extension media continuacion DOWN | `1.64x OR` | Mediana: `1.13x` |
| Tiempo medio al re-breakout | `82 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1504`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `27.33%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `19.22%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `14.76%` |
| Continuacion Alcista (>=1x OR) | `51.99%` |
| Extension media reversal DOWN | `0.89x OR` | Mediana: `0.09x` |
| Extension media continuacion UP | `1.55x OR` | Mediana: `1.07x` |
| Tiempo medio al re-breakout | `82 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 155 | `29%` | `44%` | `38%` | `40%` | `19%` | `17%` |
| RSI > 70 (Overbought) | 147 | `65%` ⭐ | `38%` | `42%` | `47%` | `27%` | `21%` |
| RSI 30-70 (Neutro) | 1690 | `48%` | `41%` | `50%` | `48%` | `26%` | `51%` |
| OR ABOVE_PD_HIGH | 489 | `45%` | `43%` | `47%` | `46%` | `26%` | `33%` |
| OR BELOW_PD_LOW | 403 | `45%` | `37%` | `42%` | `48%` | `25%` | `29%` |
| OR BETWEEN_CLOSE_AND_HIGH | 526 | `51%` | `41%` | `56%` | `52%` | `28%` | `60%` |
| OR BETWEEN_LOW_AND_CLOSE | 574 | `50%` | `41%` | `48%` | `45%` | `22%` | `57%` |
| ATR Creciente (>10%) | 101 | `49%` | `51%` | `47%` | `48%` | `30%` | `48%` |
| ATR Decreciente (<-10%) | 77 | `49%` | `32%` | `47%` | `58%` | `22%` | `36%` |
| ATR Q1 (Baja Vol Historica) | 503 | `51%` | `42%` | `52%` | `48%` | `27%` | `46%` |
| ATR Q4 (Alta Vol Historica) | 470 | `49%` | `44%` | `55%` | `51%` | `28%` | `44%` |
| RSI Diario < 35 | 185 | `44%` | `43%` | `49%` | `57%` | `28%` | `43%` |
| RSI Diario > 65 | 320 | `53%` | `47%` | `51%` | `45%` | `29%` | `48%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `103 min` | `60 min` | `180 min` |
| TP DOWN (desde entrada) | `96 min` | `60 min` | `165 min` |
| False Break UP → SL | `76 min` | - | - |
| False Break DOWN → SL | `78 min` | - | - |

---

## Permutación #6: NY 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2034`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.77%`
- **Rotura Bajista (DOWN):** `47.00%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `43.15%` | `47.70%` |
| 1.5x Rango OR | `28.02%` | `30.54%` |
| 2.0x Rango OR | `18.04%` | `20.50%` |
| 1.0x Volatilidad ATR Diaria | `5.04%` | `5.96%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `41.94%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `39.54%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `44.64%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `38.50%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `33.65%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1404`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `15.53%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `9.97%` |
| Shakeout & Re-breakout UP (>=2x OR) | `6.27%` |
| Continuacion Bajista (>=1x OR) | `44.30%` |
| Extension media reversal UP | `0.44x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.23x OR` | Mediana: `0.84x` |
| Tiempo medio al re-breakout | `98 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1413`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `17.48%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `11.18%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `7.29%` |
| Continuacion Alcista (>=1x OR) | `40.06%` |
| Extension media reversal DOWN | `0.53x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.13x OR` | Mediana: `0.75x` |
| Tiempo medio al re-breakout | `97 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 141 | `20%` | `32%` | `18%` | `34%` | `12%` | `18%` |
| RSI > 70 (Overbought) | 147 | `73%` ⭐ | `28%` | `32%` | `34%` | `10%` | `20%` |
| RSI 30-70 (Neutro) | 1746 | `49%` | `28%` | `44%` | `40%` | `16%` | `49%` |
| OR ABOVE_PD_HIGH | 499 | `45%` | `33%` | `43%` | `38%` | `17%` | `32%` |
| OR BELOW_PD_LOW | 405 | `50%` | `24%` | `33%` | `40%` | `14%` | `29%` |
| OR BETWEEN_CLOSE_AND_HIGH | 542 | `50%` | `30%` | `47%` | `41%` | `18%` | `58%` |
| OR BETWEEN_LOW_AND_CLOSE | 588 | `50%` | `26%` | `43%` | `39%` | `13%` | `54%` |
| ATR Creciente (>10%) | 105 | `47%` | `45%` | `47%` | `44%` | `23%` | `48%` |
| ATR Decreciente (<-10%) | 82 | `52%` | `23%` | `40%` | `57%` | `14%` | `39%` |
| ATR Q1 (Baja Vol Historica) | 517 | `48%` | `27%` | `46%` | `43%` | `16%` | `45%` |
| ATR Q4 (Alta Vol Historica) | 501 | `50%` | `29%` | `47%` | `45%` | `20%` | `42%` |
| RSI Diario < 35 | 185 | `49%` | `30%` | `40%` | `36%` | `15%` | `41%` |
| RSI Diario > 65 | 322 | `52%` | `33%` | `44%` | `39%` | `21%` | `45%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `136 min` | `90 min` | `255 min` |
| TP DOWN (desde entrada) | `119 min` | `60 min` | `210 min` |
| False Break UP → SL | `102 min` | - | - |
| False Break DOWN → SL | `101 min` | - | - |

---

## Permutación #7: NY 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2002`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.35%`
- **Rotura Bajista (DOWN):** `46.75%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `32.79%` | `37.50%` |
| 1.5x Rango OR | `18.32%` | `22.76%` |
| 2.0x Rango OR | `10.93%` | `13.89%` |
| 1.0x Volatilidad ATR Diaria | `3.95%` | `5.13%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `33.60%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `31.09%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `42.16%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `37.01%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `32.12%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1260`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `9.76%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `5.71%` |
| Shakeout & Re-breakout UP (>=2x OR) | `3.65%` |
| Continuacion Bajista (>=1x OR) | `34.52%` |
| Extension media reversal UP | `0.28x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.97x OR` | Mediana: `0.63x` |
| Tiempo medio al re-breakout | `111 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1287`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `11.03%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `6.37%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `4.35%` |
| Continuacion Alcista (>=1x OR) | `30.61%` |
| Extension media reversal DOWN | `0.33x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.86x OR` | Mediana: `0.56x` |
| Tiempo medio al re-breakout | `112 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 132 | `17%` | `14%` | `14%` | `30%` | `7%` | `17%` |
| RSI > 70 (Overbought) | 139 | `83%` ⭐ | `16%` | `34%` | `19%` | `12%` | `19%` |
| RSI 30-70 (Neutro) | 1731 | `49%` | `19%` | `34%` | `32%` | `10%` | `46%` |
| OR ABOVE_PD_HIGH | 487 | `47%` | `23%` | `36%` | `30%` | `12%` | `31%` |
| OR BELOW_PD_LOW | 398 | `51%` | `13%` | `25%` | `33%` | `8%` | `28%` |
| OR BETWEEN_CLOSE_AND_HIGH | 538 | `51%` | `20%` | `36%` | `29%` | `10%` | `54%` |
| OR BETWEEN_LOW_AND_CLOSE | 579 | `49%` | `17%` | `35%` | `32%` | `8%` | `50%` |
| ATR Creciente (>10%) | 104 | `46%` | `29%` | `35%` | `40%` | `13%` | `46%` |
| ATR Decreciente (<-10%) | 82 | `59%` | `19%` | `33%` | `48%` | `2%` | `38%` |
| ATR Q1 (Baja Vol Historica) | 512 | `50%` | `21%` | `37%` | `36%` | `9%` | `43%` |
| ATR Q4 (Alta Vol Historica) | 504 | `51%` | `20%` | `38%` | `36%` | `13%` | `40%` |
| RSI Diario < 35 | 184 | `52%` | `16%` | `33%` | `28%` | `11%` | `38%` |
| RSI Diario > 65 | 313 | `53%` | `21%` | `36%` | `31%` | `14%` | `42%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `147 min` | `105 min` | `255 min` |
| TP DOWN (desde entrada) | `141 min` | `90 min` | `255 min` |
| False Break UP → SL | `123 min` | - | - |
| False Break DOWN → SL | `117 min` | - | - |

---

## Permutación #8: NY 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1961`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.39%`
- **Rotura Bajista (DOWN):** `45.54%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `27.61%` | `32.03%` |
| 1.5x Rango OR | `14.01%` | `18.70%` |
| 2.0x Rango OR | `8.64%` | `10.75%` |
| 1.0x Volatilidad ATR Diaria | `3.27%` | `3.92%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `28.24%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `25.64%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `39.88%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `35.59%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `30.78%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1142`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `7.09%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `4.29%` |
| Shakeout & Re-breakout UP (>=2x OR) | `2.45%` |
| Continuacion Bajista (>=1x OR) | `29.25%` |
| Extension media reversal UP | `0.21x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.84x OR` | Mediana: `0.55x` |
| Tiempo medio al re-breakout | `117 min` | Mediana: `98 min` |

**False Breakouts DOWN analizados:** `1182`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `7.78%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `4.06%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `2.62%` |
| Continuacion Alcista (>=1x OR) | `26.14%` |
| Extension media reversal DOWN | `0.23x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.75x OR` | Mediana: `0.49x` |
| Tiempo medio al re-breakout | `121 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 129 | `14%` | `6%` | `22%` | `25%` | `3%` | `13%` |
| RSI > 70 (Overbought) | 128 | `81%` ⭐ | `11%` | `29%` | `21%` | `5%` | `20%` |
| RSI 30-70 (Neutro) | 1704 | `49%` | `15%` | `28%` | `26%` | `8%` | `43%` |
| OR ABOVE_PD_HIGH | 477 | `45%` | `20%` | `28%` | `25%` | `10%` | `30%` |
| OR BELOW_PD_LOW | 383 | `52%` | `8%` | `23%` | `27%` | `6%` | `26%` |
| OR BETWEEN_CLOSE_AND_HIGH | 533 | `50%` | `14%` | `29%` | `23%` | `7%` | `51%` |
| OR BETWEEN_LOW_AND_CLOSE | 568 | `47%` | `14%` | `31%` | `27%` | `6%` | `48%` |
| ATR Creciente (>10%) | 102 | `49%` | `16%` | `38%` | `33%` | `9%` | `44%` |
| ATR Decreciente (<-10%) | 78 | `59%` | `17%` | `30%` | `46%` | `0%` | `36%` |
| ATR Q1 (Baja Vol Historica) | 507 | `49%` | `14%` | `34%` | `30%` | `6%` | `42%` |
| ATR Q4 (Alta Vol Historica) | 497 | `51%` | `18%` | `32%` | `28%` | `9%` | `38%` |
| RSI Diario < 35 | 181 | `50%` | `12%` | `24%` | `22%` | `8%` | `36%` |
| RSI Diario > 65 | 308 | `53%` | `19%` | `33%` | `25%` | `9%` | `39%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `164 min` | `135 min` | `270 min` |
| TP DOWN (desde entrada) | `152 min` | `105 min` | `270 min` |
| False Break UP → SL | `138 min` | - | - |
| False Break DOWN → SL | `127 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: XAGUSD

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST UP] London (15m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `81.40%` (base: `68.05%`, +13%pp). N=86. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE FADE-BREAKOUT] London (15m)**: Trampa de Liquidez Alcista del `60.32%`. Cada vez que rompe al alza, termina invalidándose devorando el OR Low. Sugerencia Algo: Stop-Limit en contra de falsos quiebres (Atrapar inversores manuales).

- **[EDGE FADE-BREAKOUT] London (15m)**: Trampa de Liquidez Bajista del `62.76%`. Sugerencia Algo: Colocar orden de compra ciega si el activo cruza brevemente el piso y titubea.

- **[EDGE FADE-BREAKOUT] London (30m)**: Trampa de Liquidez Bajista del `60.20%`. Sugerencia Algo: Colocar orden de compra ciega si el activo cruza brevemente el piso y titubea.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `67.55%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `68.47%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `67.61%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `67.40%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE RSI-CONDITIONAL] London (15m) | RSI > 70 (Overbought)**: Shakeout UP post-fade al `63.77%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=89.

- **[EDGE RSI-CONDITIONAL] London (15m) | RSI Diario > 65**: Shakeout UP post-fade al `62.11%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=240.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `70.07%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `66.25%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (45m)**: Tasa de extensión polar bajista (1.5x) del `62.54%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `68.05%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `63.16%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=343 | UP: `48%` | Ext 1.5 UP: `71%` | Falsa Ruptura DW: `63%` | Reversión a PD_Close: `71%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=346 | UP: `55%` | Ext 1.5 UP: `58%` | Falsa Ruptura DW: `61%` | Reversión a PD_Close: `58%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=113 | UP: `46%` | Ext 1.5 UP: `73%` | Falsa Ruptura DW: `62%` | Reversión a PD_Close: `72%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1240 | UP: `52%` | Ext 1.5 UP: `68%` | Falsa Ruptura DW: `63%` | Reversión a PD_Close: `67%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*