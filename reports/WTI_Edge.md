# 🌐 Matriz Probabilística Omnidireccional: WTI

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **London Initial 15m**](#permutación-1-london-initial-15m)
- [Permutación #2: **London Initial 30m**](#permutación-2-london-initial-30m)
- [Permutación #3: **London Initial 45m**](#permutación-3-london-initial-45m)
- [Permutación #4: **London Initial 60m**](#permutación-4-london-initial-60m)
- [Permutación #5: **NY Main 15m**](#permutación-5-ny-main-15m)
- [Permutación #6: **NY Main 30m**](#permutación-6-ny-main-30m)
- [Permutación #7: **NY Main 45m**](#permutación-7-ny-main-45m)
- [Permutación #8: **NY Main 60m**](#permutación-8-ny-main-60m)

---
## Permutación #1: London Initial 15m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `966`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `45.65%`
- **Rotura Bajista (DOWN):** `51.55%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `81.63%` | `81.73%` |
| 1.5x Rango OR | `73.47%` | `74.90%` |
| 2.0x Rango OR | `65.31%` | `69.08%` |
| 1.0x Volatilidad ATR Diaria | `14.29%` | `17.07%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.05%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.03%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `78.57%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `63.66%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.60%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `779`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `60.21%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `49.94%` |
| Shakeout & Re-breakout UP (>=2x OR) | `44.29%` |
| Continuacion Bajista (>=1x OR) | `75.48%` |
| Extension media reversal UP | `2.28x OR` | Mediana: `1.48x` |
| Extension media continuacion DOWN | `3.28x OR` | Mediana: `2.44x` |
| Tiempo medio al re-breakout | `124 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `757`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `54.16%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `47.16%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `40.55%` |
| Continuacion Alcista (>=1x OR) | `78.73%` |
| Extension media reversal DOWN | `2.24x OR` | Mediana: `1.33x` |
| Extension media continuacion UP | `3.09x OR` | Mediana: `2.52x` |
| Tiempo medio al re-breakout | `128 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 56 | `21%` | `83%` ⭐ | `50%` | `45%` | `58%` | `59%` |
| RSI > 70 (Overbought) | 61 | `69%` ⭐ | `55%` | `60%` | `63%` ⭐ | `44%` | `62%` ⭐ |
| RSI 30-70 (Neutro) | 849 | `46%` | `75%` ⭐ | `58%` | `59%` | `61%` ⭐ | `81%` ⭐ |
| OR ABOVE_PD_HIGH | 152 | `47%` | `68%` ⭐ | `57%` | `64%` ⭐ | `58%` | `64%` ⭐ |
| OR BELOW_PD_LOW | 135 | `41%` | `80%` ⭐ | `62%` ⭐ | `53%` | `63%` ⭐ | `67%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 324 | `45%` | `77%` ⭐ | `60%` ⭐ | `56%` | `61%` ⭐ | `85%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 355 | `47%` | `71%` ⭐ | `55%` | `60%` | `59%` | `83%` ⭐ |
| ATR Creciente (>10%) | 61 | `48%` | `69%` ⭐ | `59%` | `50%` | `39%` | `79%` ⭐ |
| ATR Decreciente (<-10%) | 27 | `37%` | `50%` | `90%` ⭐ | `44%` | `50%` | `78%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 259 | `46%` | `76%` ⭐ | `59%` | `65%` ⭐ | `59%` | `78%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 230 | `45%` | `76%` ⭐ | `58%` | `60%` ⭐ | `61%` ⭐ | `77%` ⭐ |
| RSI Diario < 35 | 84 | `45%` | `79%` ⭐ | `55%` | `64%` ⭐ | `63%` ⭐ | `75%` ⭐ |
| RSI Diario > 65 | 158 | `45%` | `73%` ⭐ | `59%` | `58%` | `59%` | `79%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `205 min` | `135 min` | `360 min` |
| TP DOWN (desde entrada) | `191 min` | `120 min` | `360 min` |
| False Break UP → SL | `89 min` | - | - |
| False Break DOWN → SL | `77 min` | - | - |

---

## Permutación #2: London Initial 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1506`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.14%`
- **Rotura Bajista (DOWN):** `50.13%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.55%` | `80.26%` |
| 1.5x Rango OR | `72.55%` | `67.95%` |
| 2.0x Rango OR | `63.59%` | `59.34%` |
| 1.0x Volatilidad ATR Diaria | `15.17%` | `15.63%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.66%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.87%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `78.22%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `64.48%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.12%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1191`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `53.74%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `44.84%` |
| Shakeout & Re-breakout UP (>=2x OR) | `36.86%` |
| Continuacion Bajista (>=1x OR) | `73.22%` |
| Extension media reversal UP | `1.89x OR` | Mediana: `1.20x` |
| Extension media continuacion DOWN | `2.82x OR` | Mediana: `2.05x` |
| Tiempo medio al re-breakout | `129 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1195`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `48.12%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `40.50%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `32.80%` |
| Continuacion Alcista (>=1x OR) | `75.65%` |
| Extension media reversal DOWN | `1.86x OR` | Mediana: `0.88x` |
| Extension media continuacion UP | `2.73x OR` | Mediana: `2.20x` |
| Tiempo medio al re-breakout | `129 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 82 | `20%` | `62%` ⭐ | `69%` ⭐ | `58%` | `51%` | `65%` ⭐ |
| RSI > 70 (Overbought) | 95 | `78%` ⭐ | `68%` ⭐ | `61%` ⭐ | `80%` ⭐ | `56%` | `55%` |
| RSI 30-70 (Neutro) | 1329 | `48%` | `73%` ⭐ | `57%` | `59%` | `54%` | `81%` ⭐ |
| OR ABOVE_PD_HIGH | 226 | `50%` | `72%` ⭐ | `56%` | `69%` ⭐ | `55%` | `65%` ⭐ |
| OR BELOW_PD_LOW | 198 | `48%` | `76%` ⭐ | `60%` ⭐ | `59%` | `56%` | `69%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 540 | `47%` | `74%` ⭐ | `58%` | `57%` | `55%` | `84%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 542 | `49%` | `70%` ⭐ | `57%` | `59%` | `51%` | `82%` ⭐ |
| ATR Creciente (>10%) | 80 | `51%` | `63%` ⭐ | `59%` | `58%` | `35%` | `79%` ⭐ |
| ATR Decreciente (<-10%) | 36 | `31%` | `64%` ⭐ | `73%` ⭐ | `42%` | `42%` | `75%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 396 | `49%` | `73%` ⭐ | `60%` ⭐ | `65%` ⭐ | `54%` | `79%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 349 | `50%` | `69%` ⭐ | `60%` | `61%` ⭐ | `51%` | `76%` ⭐ |
| RSI Diario < 35 | 133 | `50%` | `70%` ⭐ | `56%` | `62%` ⭐ | `52%` | `70%` ⭐ |
| RSI Diario > 65 | 242 | `50%` | `74%` ⭐ | `60%` | `59%` | `50%` | `80%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `214 min` | `150 min` | `360 min` |
| TP DOWN (desde entrada) | `213 min` | `135 min` | `375 min` |
| False Break UP → SL | `102 min` | - | - |
| False Break DOWN → SL | `104 min` | - | - |

---

## Permutación #3: London Initial 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1789`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.64%`
- **Rotura Bajista (DOWN):** `49.30%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `75.56%` | `75.74%` |
| 1.5x Rango OR | `66.67%` | `63.49%` |
| 2.0x Rango OR | `56.98%` | `56.35%` |
| 1.0x Volatilidad ATR Diaria | `13.18%` | `16.33%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.80%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.18%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `77.53%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `64.23%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.95%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1416`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `46.33%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `36.16%` |
| Shakeout & Re-breakout UP (>=2x OR) | `29.17%` |
| Continuacion Bajista (>=1x OR) | `68.01%` |
| Extension media reversal UP | `1.49x OR` | Mediana: `0.79x` |
| Extension media continuacion DOWN | `2.49x OR` | Mediana: `1.76x` |
| Tiempo medio al re-breakout | `135 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1414`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `42.79%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `33.66%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `26.94%` |
| Continuacion Alcista (>=1x OR) | `69.45%` |
| Extension media reversal DOWN | `1.53x OR` | Mediana: `0.67x` |
| Extension media continuacion UP | `2.29x OR` | Mediana: `1.78x` |
| Tiempo medio al re-breakout | `131 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 101 | `16%` | `75%` ⭐ | `38%` | `51%` | `37%` | `61%` ⭐ |
| RSI > 70 (Overbought) | 110 | `85%` ⭐ | `63%` ⭐ | `57%` | `56%` | `39%` | `48%` |
| RSI 30-70 (Neutro) | 1578 | `49%` | `67%` ⭐ | `61%` ⭐ | `60%` ⭐ | `47%` | `81%` ⭐ |
| OR ABOVE_PD_HIGH | 264 | `52%` | `64%` ⭐ | `61%` ⭐ | `66%` ⭐ | `50%` | `66%` ⭐ |
| OR BELOW_PD_LOW | 225 | `49%` | `70%` ⭐ | `56%` | `55%` | `48%` | `68%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 650 | `49%` | `69%` ⭐ | `61%` ⭐ | `60%` | `49%` | `82%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 650 | `50%` | `64%` ⭐ | `59%` | `58%` | `42%` | `81%` ⭐ |
| ATR Creciente (>10%) | 84 | `50%` | `55%` | `67%` ⭐ | `59%` | `29%` | `76%` ⭐ |
| ATR Decreciente (<-10%) | 41 | `34%` | `79%` ⭐ | `71%` ⭐ | `46%` | `46%` | `78%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 458 | `50%` | `70%` ⭐ | `62%` ⭐ | `62%` ⭐ | `49%` | `78%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 440 | `51%` | `61%` ⭐ | `59%` | `56%` | `41%` | `75%` ⭐ |
| RSI Diario < 35 | 153 | `49%` | `64%` ⭐ | `60%` ⭐ | `58%` | `44%` | `71%` ⭐ |
| RSI Diario > 65 | 277 | `50%` | `72%` ⭐ | `62%` ⭐ | `63%` ⭐ | `44%` | `79%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `243 min` | `218 min` | `390 min` |
| TP DOWN (desde entrada) | `221 min` | `165 min` | `375 min` |
| False Break UP → SL | `124 min` | - | - |
| False Break DOWN → SL | `123 min` | - | - |

---

## Permutación #4: London Initial 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1926`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.60%`
- **Rotura Bajista (DOWN):** `48.96%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `74.47%` | `73.81%` |
| 1.5x Rango OR | `62.82%` | `62.25%` |
| 2.0x Rango OR | `53.63%` | `54.29%` |
| 1.0x Volatilidad ATR Diaria | `12.50%` | `17.39%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.37%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.79%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `76.79%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `63.55%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `46.34%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1497`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `41.35%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `31.06%` |
| Shakeout & Re-breakout UP (>=2x OR) | `23.65%` |
| Continuacion Bajista (>=1x OR) | `64.66%` |
| Extension media reversal UP | `1.21x OR` | Mediana: `0.56x` |
| Extension media continuacion DOWN | `2.29x OR` | Mediana: `1.60x` |
| Tiempo medio al re-breakout | `142 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1502`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `38.22%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `29.69%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `22.90%` |
| Continuacion Alcista (>=1x OR) | `65.78%` |
| Extension media reversal DOWN | `1.27x OR` | Mediana: `0.46x` |
| Extension media continuacion UP | `2.04x OR` | Mediana: `1.56x` |
| Tiempo medio al re-breakout | `138 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 109 | `16%` | `59%` | `53%` | `56%` | `29%` | `59%` |
| RSI > 70 (Overbought) | 126 | `84%` ⭐ | `63%` ⭐ | `49%` | `68%` ⭐ | `32%` | `48%` |
| RSI 30-70 (Neutro) | 1691 | `48%` | `63%` ⭐ | `59%` | `58%` | `43%` | `80%` ⭐ |
| OR ABOVE_PD_HIGH | 289 | `50%` | `61%` ⭐ | `57%` | `61%` ⭐ | `43%` | `64%` ⭐ |
| OR BELOW_PD_LOW | 239 | `48%` | `63%` ⭐ | `58%` | `56%` | `44%` | `68%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 709 | `47%` | `62%` ⭐ | `60%` | `59%` | `44%` | `81%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 689 | `49%` | `64%` ⭐ | `55%` | `56%` | `37%` | `80%` ⭐ |
| ATR Creciente (>10%) | 88 | `47%` | `56%` | `68%` ⭐ | `47%` | `27%` | `75%` ⭐ |
| ATR Decreciente (<-10%) | 43 | `40%` | `71%` ⭐ | `65%` ⭐ | `36%` | `43%` | `77%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 488 | `49%` | `66%` ⭐ | `58%` | `60%` ⭐ | `44%` | `77%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 471 | `50%` | `60%` ⭐ | `57%` | `55%` | `36%` | `76%` ⭐ |
| RSI Diario < 35 | 162 | `46%` | `57%` | `64%` ⭐ | `55%` | `42%` | `73%` ⭐ |
| RSI Diario > 65 | 294 | `47%` | `67%` ⭐ | `59%` | `60%` ⭐ | `39%` | `78%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `247 min` | `225 min` | `390 min` |
| TP DOWN (desde entrada) | `230 min` | `195 min` | `375 min` |
| False Break UP → SL | `144 min` | - | - |
| False Break DOWN → SL | `144 min` | - | - |

---

## Permutación #5: NY Main 15m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1859`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.36%`
- **Rotura Bajista (DOWN):** `46.75%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `69.97%` | `69.74%` |
| 1.5x Rango OR | `55.51%` | `55.58%` |
| 2.0x Rango OR | `45.16%` | `45.11%` |
| 1.0x Volatilidad ATR Diaria | `7.23%` | `10.47%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.62%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.81%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `55.51%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `48.47%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.15%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1456`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `41.62%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `33.04%` |
| Shakeout & Re-breakout UP (>=2x OR) | `26.30%` |
| Continuacion Bajista (>=1x OR) | `64.97%` |
| Extension media reversal UP | `1.37x OR` | Mediana: `0.65x` |
| Extension media continuacion DOWN | `2.31x OR` | Mediana: `1.63x` |
| Tiempo medio al re-breakout | `73 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1469`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `40.57%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `32.27%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `26.14%` |
| Continuacion Alcista (>=1x OR) | `66.85%` |
| Extension media reversal DOWN | `1.45x OR` | Mediana: `0.57x` |
| Extension media continuacion UP | `2.19x OR` | Mediana: `1.60x` |
| Tiempo medio al re-breakout | `78 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 161 | `29%` | `51%` | `49%` | `51%` | `31%` | `34%` |
| RSI > 70 (Overbought) | 142 | `71%` ⭐ | `49%` | `63%` ⭐ | `54%` | `29%` | `23%` |
| RSI 30-70 (Neutro) | 1556 | `48%` | `57%` | `55%` | `57%` | `44%` | `61%` ⭐ |
| OR ABOVE_PD_HIGH | 442 | `46%` | `60%` | `55%` | `57%` | `39%` | `43%` |
| OR BELOW_PD_LOW | 382 | `50%` | `54%` | `58%` | `56%` | `41%` | `43%` |
| OR BETWEEN_CLOSE_AND_HIGH | 508 | `50%` | `54%` | `58%` | `54%` | `43%` | `65%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 527 | `47%` | `55%` | `52%` | `56%` | `43%` | `66%` ⭐ |
| ATR Creciente (>10%) | 88 | `42%` | `73%` ⭐ | `43%` | `39%` | `43%` | `51%` |
| ATR Decreciente (<-10%) | 44 | `50%` | `45%` | `68%` ⭐ | `60%` ⭐ | `36%` | `50%` |
| ATR Q1 (Baja Vol Historica) | 466 | `48%` | `64%` ⭐ | `51%` | `53%` | `47%` | `56%` |
| ATR Q4 (Alta Vol Historica) | 446 | `49%` | `53%` | `57%` | `52%` | `39%` | `53%` |
| RSI Diario < 35 | 161 | `48%` | `51%` | `64%` ⭐ | `58%` | `52%` | `55%` |
| RSI Diario > 65 | 272 | `49%` | `62%` ⭐ | `56%` | `50%` | `43%` | `61%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `107 min` | `75 min` | `165 min` |
| TP DOWN (desde entrada) | `102 min` | `75 min` | `165 min` |
| False Break UP → SL | `66 min` | - | - |
| False Break DOWN → SL | `66 min` | - | - |

---

## Permutación #6: NY Main 30m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2028`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.87%`
- **Rotura Bajista (DOWN):** `46.01%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `61.45%` | `64.84%` |
| 1.5x Rango OR | `45.11%` | `49.30%` |
| 2.0x Rango OR | `32.90%` | `38.69%` |
| 1.0x Volatilidad ATR Diaria | `6.56%` | `10.61%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.88%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `51.13%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `54.98%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `47.93%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `40.46%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1562`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `32.27%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `24.46%` |
| Shakeout & Re-breakout UP (>=2x OR) | `18.18%` |
| Continuacion Bajista (>=1x OR) | `58.71%` |
| Extension media reversal UP | `1.00x OR` | Mediana: `0.29x` |
| Extension media continuacion DOWN | `1.89x OR` | Mediana: `1.33x` |
| Tiempo medio al re-breakout | `77 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1563`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `33.01%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `24.57%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `18.68%` |
| Continuacion Alcista (>=1x OR) | `58.16%` |
| Extension media reversal DOWN | `1.06x OR` | Mediana: `0.30x` |
| Extension media continuacion UP | `1.72x OR` | Mediana: `1.25x` |
| Tiempo medio al re-breakout | `86 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 140 | `27%` | `37%` | `47%` | `43%` | `24%` | `31%` |
| RSI > 70 (Overbought) | 166 | `78%` ⭐ | `43%` | `53%` | `48%` | `27%` | `24%` |
| RSI 30-70 (Neutro) | 1722 | `48%` | `46%` | `54%` | `52%` | `33%` | `60%` |
| OR ABOVE_PD_HIGH | 487 | `51%` | `43%` | `58%` | `54%` | `32%` | `44%` |
| OR BELOW_PD_LOW | 404 | `51%` | `45%` | `54%` | `52%` | `32%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 560 | `50%` | `45%` | `55%` | `51%` | `34%` | `63%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 577 | `45%` | `47%` | `49%` | `49%` | `31%` | `64%` ⭐ |
| ATR Creciente (>10%) | 90 | `44%` | `62%` ⭐ | `52%` | `43%` | `31%` | `51%` |
| ATR Decreciente (<-10%) | 47 | `45%` | `33%` | `67%` ⭐ | `65%` ⭐ | `26%` | `51%` |
| ATR Q1 (Baja Vol Historica) | 515 | `50%` | `54%` | `49%` | `47%` | `38%` | `55%` |
| ATR Q4 (Alta Vol Historica) | 498 | `49%` | `42%` | `58%` | `50%` | `31%` | `52%` |
| RSI Diario < 35 | 177 | `45%` | `44%` | `57%` | `54%` | `40%` | `53%` |
| RSI Diario > 65 | 299 | `49%` | `49%` | `56%` | `50%` | `32%` | `58%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `123 min` | `90 min` | `195 min` |
| TP DOWN (desde entrada) | `107 min` | `75 min` | `165 min` |
| False Break UP → SL | `85 min` | - | - |
| False Break DOWN → SL | `79 min` | - | - |

---

## Permutación #7: NY Main 45m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2065`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.04%`
- **Rotura Bajista (DOWN):** `46.05%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `50.95%` | `56.15%` |
| 1.5x Rango OR | `35.67%` | `39.54%` |
| 2.0x Rango OR | `24.67%` | `28.60%` |
| 1.0x Volatilidad ATR Diaria | `6.07%` | `10.30%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `48.58%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `43.64%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `52.74%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `46.59%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `38.62%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1506`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `23.04%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `16.27%` |
| Shakeout & Re-breakout UP (>=2x OR) | `10.82%` |
| Continuacion Bajista (>=1x OR) | `51.00%` |
| Extension media reversal UP | `0.66x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.49x OR` | Mediana: `1.04x` |
| Tiempo medio al re-breakout | `89 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1515`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `23.89%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `16.04%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.01%` |
| Continuacion Alcista (>=1x OR) | `48.78%` |
| Extension media reversal DOWN | `0.72x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.37x OR` | Mediana: `0.97x` |
| Tiempo medio al re-breakout | `94 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 147 | `22%` | `25%` | `31%` | `32%` | `12%` | `28%` |
| RSI > 70 (Overbought) | 180 | `78%` ⭐ | `26%` | `46%` | `32%` | `15%` | `28%` |
| RSI 30-70 (Neutro) | 1738 | `51%` | `38%` | `50%` | `46%` | `25%` | `57%` |
| OR ABOVE_PD_HIGH | 501 | `54%` | `34%` | `54%` | `45%` | `21%` | `42%` |
| OR BELOW_PD_LOW | 404 | `51%` | `34%` | `47%` | `49%` | `24%` | `42%` |
| OR BETWEEN_CLOSE_AND_HIGH | 576 | `49%` | `36%` | `47%` | `44%` | `26%` | `61%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 584 | `51%` | `38%` | `46%` | `39%` | `21%` | `61%` ⭐ |
| ATR Creciente (>10%) | 89 | `46%` | `44%` | `51%` | `49%` | `23%` | `49%` |
| ATR Decreciente (<-10%) | 48 | `54%` | `27%` | `81%` ⭐ | `62%` ⭐ | `22%` | `48%` |
| ATR Q1 (Baja Vol Historica) | 524 | `51%` | `46%` | `46%` | `40%` | `30%` | `51%` |
| ATR Q4 (Alta Vol Historica) | 511 | `48%` | `28%` | `53%` | `44%` | `23%` | `51%` |
| RSI Diario < 35 | 184 | `46%` | `40%` | `45%` | `46%` | `30%` | `52%` |
| RSI Diario > 65 | 301 | `50%` | `40%` | `47%` | `45%` | `25%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `129 min` | `105 min` | `210 min` |
| TP DOWN (desde entrada) | `119 min` | `90 min` | `210 min` |
| False Break UP → SL | `97 min` | - | - |
| False Break DOWN → SL | `91 min` | - | - |

---

## Permutación #8: NY Main 60m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2051`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.93%`
- **Rotura Bajista (DOWN):** `46.81%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `44.14%` | `47.60%` |
| 1.5x Rango OR | `28.71%` | `32.50%` |
| 2.0x Rango OR | `19.53%` | `22.08%` |
| 1.0x Volatilidad ATR Diaria | `6.25%` | `9.06%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `43.16%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `39.90%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `51.68%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `45.39%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `37.81%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1445`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `17.79%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `11.97%` |
| Shakeout & Re-breakout UP (>=2x OR) | `8.10%` |
| Continuacion Bajista (>=1x OR) | `44.91%` |
| Extension media reversal UP | `0.48x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.26x OR` | Mediana: `0.87x` |
| Tiempo medio al re-breakout | `94 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1454`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `18.50%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `12.17%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `7.63%` |
| Continuacion Alcista (>=1x OR) | `42.16%` |
| Extension media reversal DOWN | `0.54x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.16x OR` | Mediana: `0.81x` |
| Tiempo medio al re-breakout | `101 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 142 | `15%` | `18%` | `27%` | `29%` | `9%` | `23%` |
| RSI > 70 (Overbought) | 151 | `82%` ⭐ | `16%` | `38%` | `27%` | `11%` | `23%` |
| RSI 30-70 (Neutro) | 1758 | `50%` | `31%` | `44%` | `42%` | `19%` | `56%` |
| OR ABOVE_PD_HIGH | 497 | `52%` | `25%` | `49%` | `40%` | `16%` | `42%` |
| OR BELOW_PD_LOW | 400 | `50%` | `28%` | `42%` | `46%` | `18%` | `42%` |
| OR BETWEEN_CLOSE_AND_HIGH | 578 | `48%` | `32%` | `40%` | `39%` | `20%` | `58%` |
| OR BETWEEN_LOW_AND_CLOSE | 576 | `50%` | `29%` | `42%` | `36%` | `17%` | `60%` |
| ATR Creciente (>10%) | 89 | `39%` | `40%` | `46%` | `47%` | `16%` | `49%` |
| ATR Decreciente (<-10%) | 48 | `48%` | `9%` | `78%` ⭐ | `59%` | `20%` | `48%` |
| ATR Q1 (Baja Vol Historica) | 518 | `49%` | `40%` | `41%` | `38%` | `24%` | `50%` |
| ATR Q4 (Alta Vol Historica) | 514 | `47%` | `22%` | `43%` | `39%` | `18%` | `50%` |
| RSI Diario < 35 | 185 | `44%` | `30%` | `41%` | `47%` | `20%` | `51%` |
| RSI Diario > 65 | 296 | `52%` | `28%` | `45%` | `37%` | `19%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `138 min` | `105 min` | `210 min` |
| TP DOWN (desde entrada) | `126 min` | `90 min` | `210 min` |
| False Break UP → SL | `105 min` | - | - |
| False Break DOWN → SL | `101 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: WTI

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] NY Main (15m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `71.74%` (base: `55.58%`, +16%pp). N=88.

- **[EDGE CONTEXT-BOOST UP] London Initial (45m) | ATR Decreciente (<-10%)**: Extension 1.5x UP sube a `78.57%` (base: `66.67%`, +12%pp). N=41. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] NY Main (15m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `72.97%` (base: `55.51%`, +17%pp). N=88. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] NY Main (30m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `62.50%` (base: `45.11%`, +17%pp). N=90. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] London Initial (15m)**: Imantación cíclica brutal. El `78.57%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London Initial (30m)**: Imantación cíclica brutal. El `78.22%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London Initial (45m)**: Imantación cíclica brutal. El `77.53%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London Initial (60m)**: Imantación cíclica brutal. El `76.79%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] London Initial (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `63.66%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London Initial (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `64.48%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London Initial (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `64.23%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London Initial (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `63.55%` de los eventos evaluados.

- **[EDGE RSI-CONDITIONAL] London Initial (15m) | RSI 30-70 (Neutro)**: Shakeout UP post-fade al `61.37%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=849.

- **[EDGE RSI-CONDITIONAL] London Initial (15m) | RSI Diario < 35**: Shakeout UP post-fade al `62.69%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=84.

- **[EDGE SHAKEOUT-REVERSAL UP] London Initial (15m)**: Despues de un falso rompimiento alcista, el `60.21%` de las veces el precio retoma la direccion UP con extension >=1x OR. Media reversal: `2.28x OR` | Tiempo medio al re-breakout: 124 min. Sugerencia Algo: Orden limite de COMPRA en OR_Low tras primer rompimiento UP. El mercado barre stops y luego arranca.

- **[EDGE TENDENCIAL DOWN] London Initial (15m)**: Tasa de extensión polar bajista (1.5x) del `74.90%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London Initial (30m)**: Tasa de extensión polar bajista (1.5x) del `67.95%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London Initial (45m)**: Tasa de extensión polar bajista (1.5x) del `63.49%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London Initial (60m)**: Tasa de extensión polar bajista (1.5x) del `62.25%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London Initial (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `73.47%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London Initial (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `72.55%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London Initial (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `66.67%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London Initial (60m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `62.82%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London Initial 45m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=451 | UP: `49%` | Ext 1.5 UP: `76%` | Falsa Ruptura DW: `60%` | Reversión a PD_Close: `80%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=452 | UP: `51%` | Ext 1.5 UP: `52%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `75%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=192 | UP: `53%` | Ext 1.5 UP: `73%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `76%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1597 | UP: `49%` | Ext 1.5 UP: `66%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `78%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*