# 🌐 Matriz Probabilística Omnidireccional: XAUUSD

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
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1294`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.70%`
- **Rotura Bajista (DOWN):** `44.90%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.42%` | `79.17%` |
| 1.5x Rango OR | `71.00%` | `70.91%` |
| 2.0x Rango OR | `63.98%` | `61.45%` |
| 1.0x Volatilidad ATR Diaria | `14.80%` | `14.46%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.75%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.04%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.62%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `58.42%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.39%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `994`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `54.43%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `46.98%` |
| Shakeout & Re-breakout UP (>=2x OR) | `39.94%` |
| Continuacion Bajista (>=1x OR) | `74.75%` |
| Extension media reversal UP | `2.10x OR` | Mediana: `1.36x` |
| Extension media continuacion DOWN | `3.13x OR` | Mediana: `2.30x` |
| Tiempo medio al re-breakout | `130 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1025`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `52.88%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `44.68%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `36.98%` |
| Continuacion Alcista (>=1x OR) | `77.37%` |
| Extension media reversal DOWN | `2.07x OR` | Mediana: `1.16x` |
| Extension media continuacion UP | `3.09x OR` | Mediana: `2.49x` |
| Tiempo medio al re-breakout | `146 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 72 | `39%` | `54%` | `57%` | `49%` | `41%` | `36%` |
| RSI > 70 (Overbought) | 92 | `64%` ⭐ | `66%` ⭐ | `66%` ⭐ | `63%` ⭐ | `64%` ⭐ | `42%` |
| RSI 30-70 (Neutro) | 1130 | `52%` | `72%` ⭐ | `55%` | `54%` | `55%` | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 221 | `46%` | `78%` ⭐ | `51%` | `62%` ⭐ | `55%` | `47%` |
| OR BELOW_PD_LOW | 208 | `55%` | `66%` ⭐ | `57%` | `51%` | `52%` | `53%` |
| OR BETWEEN_CLOSE_AND_HIGH | 396 | `51%` | `69%` ⭐ | `59%` | `59%` | `57%` | `76%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 469 | `53%` | `72%` ⭐ | `54%` | `47%` | `53%` | `74%` ⭐ |
| ATR Creciente (>10%) | 89 | `49%` | `70%` ⭐ | `48%` | `48%` | `42%` | `79%` ⭐ |
| ATR Decreciente (<-10%) | 56 | `54%` | `70%` ⭐ | `60%` ⭐ | `60%` ⭐ | `61%` ⭐ | `59%` |
| ATR Q1 (Baja Vol Historica) | 370 | `56%` | `71%` ⭐ | `50%` | `51%` | `52%` | `71%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 251 | `54%` | `70%` ⭐ | `57%` | `50%` | `50%` | `57%` |
| RSI Diario < 35 | 104 | `54%` | `70%` ⭐ | `59%` | `54%` | `53%` | `77%` ⭐ |
| RSI Diario > 65 | 266 | `52%` | `70%` ⭐ | `55%` | `53%` | `53%` | `62%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `200 min` | `150 min` | `360 min` |
| TP DOWN (desde entrada) | `204 min` | `165 min` | `360 min` |
| False Break UP → SL | `107 min` | - | - |
| False Break DOWN → SL | `98 min` | - | - |

---

## Permutación #2: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1789`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.37%`
- **Rotura Bajista (DOWN):** `46.56%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `78.67%` | `77.79%` |
| 1.5x Rango OR | `66.81%` | `66.87%` |
| 2.0x Rango OR | `56.26%` | `58.22%` |
| 1.0x Volatilidad ATR Diaria | `13.17%` | `13.09%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.10%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.74%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `67.41%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `59.14%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.77%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1348`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `47.11%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `37.91%` |
| Shakeout & Re-breakout UP (>=2x OR) | `29.82%` |
| Continuacion Bajista (>=1x OR) | `70.99%` |
| Extension media reversal UP | `1.60x OR` | Mediana: `0.84x` |
| Extension media continuacion DOWN | `2.60x OR` | Mediana: `1.92x` |
| Tiempo medio al re-breakout | `146 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1404`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `44.59%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `35.26%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `28.70%` |
| Continuacion Alcista (>=1x OR) | `73.15%` |
| Extension media reversal DOWN | `1.58x OR` | Mediana: `0.73x` |
| Extension media continuacion UP | `2.50x OR` | Mediana: `1.97x` |
| Tiempo medio al re-breakout | `154 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 84 | `31%` | `73%` ⭐ | `42%` | `39%` | `33%` | `39%` |
| RSI > 70 (Overbought) | 105 | `72%` ⭐ | `67%` ⭐ | `47%` | `66%` ⭐ | `47%` | `41%` |
| RSI 30-70 (Neutro) | 1600 | `51%` | `67%` ⭐ | `54%` | `55%` | `48%` | `71%` ⭐ |
| OR ABOVE_PD_HIGH | 308 | `49%` | `69%` ⭐ | `52%` | `58%` | `48%` | `50%` |
| OR BELOW_PD_LOW | 262 | `52%` | `66%` ⭐ | `53%` | `45%` | `45%` | `58%` |
| OR BETWEEN_CLOSE_AND_HIGH | 568 | `49%` | `66%` ⭐ | `53%` | `58%` | `48%` | `74%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 651 | `54%` | `67%` ⭐ | `54%` | `54%` | `47%` | `74%` ⭐ |
| ATR Creciente (>10%) | 111 | `43%` | `69%` ⭐ | `48%` | `57%` | `41%` | `76%` ⭐ |
| ATR Decreciente (<-10%) | 80 | `46%` | `62%` ⭐ | `54%` | `49%` | `48%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 479 | `53%` | `63%` ⭐ | `51%` | `53%` | `43%` | `68%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 391 | `51%` | `67%` ⭐ | `52%` | `53%` | `43%` | `60%` ⭐ |
| RSI Diario < 35 | 137 | `57%` | `62%` ⭐ | `59%` | `48%` | `44%` | `77%` ⭐ |
| RSI Diario > 65 | 354 | `51%` | `73%` ⭐ | `48%` | `61%` ⭐ | `45%` | `64%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `237 min` | `232 min` | `360 min` |
| TP DOWN (desde entrada) | `230 min` | `210 min` | `360 min` |
| False Break UP → SL | `141 min` | - | - |
| False Break DOWN → SL | `137 min` | - | - |

---

## Permutación #3: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1996`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.60%`
- **Rotura Bajista (DOWN):** `48.30%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `72.38%` | `72.72%` |
| 1.5x Rango OR | `60.69%` | `61.83%` |
| 2.0x Rango OR | `47.92%` | `51.45%` |
| 1.0x Volatilidad ATR Diaria | `12.77%` | `14.21%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.37%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.19%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.98%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `59.17%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.54%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1501`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `39.77%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `31.11%` |
| Shakeout & Re-breakout UP (>=2x OR) | `23.18%` |
| Continuacion Bajista (>=1x OR) | `65.42%` |
| Extension media reversal UP | `1.26x OR` | Mediana: `0.52x` |
| Extension media continuacion DOWN | `2.23x OR` | Mediana: `1.59x` |
| Tiempo medio al re-breakout | `155 min` | Mediana: `135 min` |

**False Breakouts DOWN analizados:** `1544`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `37.76%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `28.43%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `21.57%` |
| Continuacion Alcista (>=1x OR) | `66.19%` |
| Extension media reversal DOWN | `1.22x OR` | Mediana: `0.46x` |
| Extension media continuacion UP | `2.09x OR` | Mediana: `1.61x` |
| Tiempo medio al re-breakout | `161 min` | Mediana: `135 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 102 | `19%` | `63%` ⭐ | `26%` | `45%` | `30%` | `43%` |
| RSI > 70 (Overbought) | 125 | `70%` ⭐ | `53%` | `56%` | `62%` ⭐ | `34%` | `43%` |
| RSI 30-70 (Neutro) | 1769 | `51%` | `61%` ⭐ | `54%` | `56%` | `41%` | `70%` ⭐ |
| OR ABOVE_PD_HIGH | 352 | `51%` | `61%` ⭐ | `55%` | `56%` | `39%` | `50%` |
| OR BELOW_PD_LOW | 281 | `51%` | `56%` | `53%` | `51%` | `38%` | `57%` |
| OR BETWEEN_CLOSE_AND_HIGH | 641 | `49%` | `63%` ⭐ | `53%` | `58%` | `41%` | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 722 | `52%` | `60%` ⭐ | `53%` | `54%` | `40%` | `73%` ⭐ |
| ATR Creciente (>10%) | 115 | `50%` | `60%` | `53%` | `52%` | `32%` | `75%` ⭐ |
| ATR Decreciente (<-10%) | 89 | `46%` | `46%` | `56%` | `48%` | `39%` | `65%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 519 | `52%` | `59%` | `51%` | `52%` | `35%` | `67%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 468 | `52%` | `58%` | `57%` | `55%` | `37%` | `60%` ⭐ |
| RSI Diario < 35 | 150 | `51%` | `56%` | `55%` | `49%` | `37%` | `76%` ⭐ |
| RSI Diario > 65 | 385 | `52%` | `65%` ⭐ | `51%` | `55%` | `36%` | `64%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `259 min` | `255 min` | `360 min` |
| TP DOWN (desde entrada) | `234 min` | `240 min` | `360 min` |
| False Break UP → SL | `175 min` | - | - |
| False Break DOWN → SL | `164 min` | - | - |

---

## Permutación #4: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2048`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.27%`
- **Rotura Bajista (DOWN):** `47.56%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `70.10%` | `71.46%` |
| 1.5x Rango OR | `56.95%` | `57.29%` |
| 2.0x Rango OR | `45.33%` | `47.95%` |
| 1.0x Volatilidad ATR Diaria | `13.43%` | `14.27%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.05%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.34%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `66.46%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `58.59%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.60%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1519`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `34.23%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `25.87%` |
| Shakeout & Re-breakout UP (>=2x OR) | `18.43%` |
| Continuacion Bajista (>=1x OR) | `62.08%` |
| Extension media reversal UP | `1.03x OR` | Mediana: `0.33x` |
| Extension media continuacion DOWN | `1.97x OR` | Mediana: `1.40x` |
| Tiempo medio al re-breakout | `158 min` | Mediana: `135 min` |

**False Breakouts DOWN analizados:** `1577`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `33.54%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `24.16%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `18.64%` |
| Continuacion Alcista (>=1x OR) | `62.02%` |
| Extension media reversal DOWN | `1.04x OR` | Mediana: `0.30x` |
| Extension media continuacion UP | `1.84x OR` | Mediana: `1.37x` |
| Tiempo medio al re-breakout | `164 min` | Mediana: `150 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 99 | `22%` | `64%` ⭐ | `36%` | `44%` | `25%` | `43%` |
| RSI > 70 (Overbought) | 123 | `78%` ⭐ | `49%` | `56%` | `62%` ⭐ | `30%` | `41%` |
| RSI 30-70 (Neutro) | 1826 | `51%` | `58%` | `53%` | `56%` | `35%` | `69%` ⭐ |
| OR ABOVE_PD_HIGH | 361 | `55%` | `57%` | `57%` | `54%` | `34%` | `50%` |
| OR BELOW_PD_LOW | 283 | `50%` | `53%` | `49%` | `53%` | `32%` | `57%` |
| OR BETWEEN_CLOSE_AND_HIGH | 663 | `48%` | `60%` | `54%` | `58%` | `35%` | `73%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 741 | `52%` | `56%` | `52%` | `54%` | `35%` | `73%` ⭐ |
| ATR Creciente (>10%) | 116 | `45%` | `54%` | `48%` | `52%` | `27%` | `75%` ⭐ |
| ATR Decreciente (<-10%) | 90 | `41%` | `41%` | `57%` | `49%` | `33%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 526 | `49%` | `53%` | `49%` | `55%` | `31%` | `67%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 489 | `54%` | `56%` | `54%` | `57%` | `32%` | `59%` |
| RSI Diario < 35 | 149 | `48%` | `52%` | `56%` | `53%` | `35%` | `76%` ⭐ |
| RSI Diario > 65 | 397 | `57%` | `58%` | `53%` | `54%` | `30%` | `64%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `273 min` | `270 min` | `375 min` |
| TP DOWN (desde entrada) | `239 min` | `240 min` | `360 min` |
| False Break UP → SL | `194 min` | - | - |
| False Break DOWN → SL | `189 min` | - | - |

---

## Permutación #5: NY 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1954`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.57%`
- **Rotura Bajista (DOWN):** `45.80%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `61.22%` | `59.78%` |
| 1.5x Rango OR | `44.57%` | `47.82%` |
| 2.0x Rango OR | `31.09%` | `37.21%` |
| 1.0x Volatilidad ATR Diaria | `6.32%` | `7.37%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `46.68%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `47.49%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `44.22%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `41.04%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `35.98%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1444`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `28.53%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `20.43%` |
| Shakeout & Re-breakout UP (>=2x OR) | `15.44%` |
| Continuacion Bajista (>=1x OR) | `56.93%` |
| Extension media reversal UP | `0.90x OR` | Mediana: `0.18x` |
| Extension media continuacion DOWN | `1.84x OR` | Mediana: `1.26x` |
| Tiempo medio al re-breakout | `75 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1469`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `29.20%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `21.78%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `16.13%` |
| Continuacion Alcista (>=1x OR) | `57.25%` |
| Extension media reversal DOWN | `0.95x OR` | Mediana: `0.13x` |
| Extension media continuacion UP | `1.76x OR` | Mediana: `1.22x` |
| Tiempo medio al re-breakout | `77 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 167 | `25%` | `39%` | `37%` | `38%` | `27%` | `25%` |
| RSI > 70 (Overbought) | 175 | `70%` ⭐ | `46%` | `38%` | `44%` | `26%` | `21%` |
| RSI 30-70 (Neutro) | 1612 | `49%` | `45%` | `49%` | `49%` | `29%` | `49%` |
| OR ABOVE_PD_HIGH | 494 | `52%` | `48%` | `47%` | `51%` | `31%` | `31%` |
| OR BELOW_PD_LOW | 370 | `44%` | `38%` | `43%` | `47%` | `26%` | `26%` |
| OR BETWEEN_CLOSE_AND_HIGH | 545 | `50%` | `48%` | `47%` | `47%` | `28%` | `58%` |
| OR BETWEEN_LOW_AND_CLOSE | 545 | `47%` | `41%` | `48%` | `46%` | `29%` | `54%` |
| ATR Creciente (>10%) | 109 | `45%` | `45%` | `55%` | `53%` | `30%` | `46%` |
| ATR Decreciente (<-10%) | 81 | `57%` | `54%` | `43%` | `35%` | `24%` | `42%` |
| ATR Q1 (Baja Vol Historica) | 490 | `48%` | `46%` | `52%` | `48%` | `34%` | `45%` |
| ATR Q4 (Alta Vol Historica) | 474 | `47%` | `44%` | `49%` | `50%` | `29%` | `41%` |
| RSI Diario < 35 | 146 | `51%` | `43%` | `53%` | `53%` | `34%` | `54%` |
| RSI Diario > 65 | 387 | `50%` | `52%` | `48%` | `49%` | `31%` | `44%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `101 min` | `60 min` | `165 min` |
| TP DOWN (desde entrada) | `95 min` | `60 min` | `165 min` |
| False Break UP → SL | `68 min` | - | - |
| False Break DOWN → SL | `79 min` | - | - |

---

## Permutación #6: NY 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2014`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.85%`
- **Rotura Bajista (DOWN):** `46.13%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `49.80%` | `48.33%` |
| 1.5x Rango OR | `33.76%` | `33.37%` |
| 2.0x Rango OR | `22.81%` | `24.65%` |
| 1.0x Volatilidad ATR Diaria | `5.88%` | `5.27%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `39.14%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `40.04%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `42.90%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `39.08%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `34.33%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1371`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `17.51%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `11.16%` |
| Shakeout & Re-breakout UP (>=2x OR) | `7.51%` |
| Continuacion Bajista (>=1x OR) | `47.78%` |
| Extension media reversal UP | `0.51x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.35x OR` | Mediana: `0.94x` |
| Tiempo medio al re-breakout | `96 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1418`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `19.39%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `13.68%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `9.38%` |
| Continuacion Alcista (>=1x OR) | `45.20%` |
| Extension media reversal DOWN | `0.58x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.28x OR` | Mediana: `0.86x` |
| Tiempo medio al re-breakout | `90 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 152 | `20%` | `32%` | `35%` | `34%` | `10%` | `16%` |
| RSI > 70 (Overbought) | 189 | `76%` ⭐ | `29%` | `30%` | `49%` | `12%` | `18%` |
| RSI 30-70 (Neutro) | 1673 | `50%` | `35%` | `41%` | `40%` | `19%` | `48%` |
| OR ABOVE_PD_HIGH | 514 | `52%` | `34%` | `38%` | `40%` | `19%` | `31%` |
| OR BELOW_PD_LOW | 373 | `49%` | `30%` | `36%` | `41%` | `11%` | `25%` |
| OR BETWEEN_CLOSE_AND_HIGH | 570 | `49%` | `36%` | `41%` | `40%` | `19%` | `56%` |
| OR BETWEEN_LOW_AND_CLOSE | 557 | `50%` | `35%` | `40%` | `40%` | `19%` | `52%` |
| ATR Creciente (>10%) | 114 | `49%` | `32%` | `45%` | `47%` | `19%` | `47%` |
| ATR Decreciente (<-10%) | 87 | `56%` | `43%` | `39%` | `27%` | `6%` | `40%` |
| ATR Q1 (Baja Vol Historica) | 513 | `48%` | `37%` | `47%` | `42%` | `24%` | `44%` |
| ATR Q4 (Alta Vol Historica) | 496 | `52%` | `38%` | `41%` | `38%` | `17%` | `41%` |
| RSI Diario < 35 | 149 | `53%` | `30%` | `38%` | `43%` | `17%` | `50%` |
| RSI Diario > 65 | 386 | `54%` | `42%` | `41%` | `41%` | `21%` | `42%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `132 min` | `75 min` | `225 min` |
| TP DOWN (desde entrada) | `111 min` | `60 min` | `195 min` |
| False Break UP → SL | `95 min` | - | - |
| False Break DOWN → SL | `110 min` | - | - |

---

## Permutación #7: NY 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2001`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.52%`
- **Rotura Bajista (DOWN):** `45.28%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `36.30%` | `38.85%` |
| 1.5x Rango OR | `23.44%` | `24.61%` |
| 2.0x Rango OR | `15.23%` | `16.56%` |
| 1.0x Volatilidad ATR Diaria | `4.55%` | `4.64%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `31.06%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `31.46%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `40.68%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `37.23%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `32.18%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1232`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `11.20%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `6.82%` |
| Shakeout & Re-breakout UP (>=2x OR) | `4.63%` |
| Continuacion Bajista (>=1x OR) | `37.82%` |
| Extension media reversal UP | `0.32x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.05x OR` | Mediana: `0.73x` |
| Tiempo medio al re-breakout | `105 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1305`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `12.87%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `8.20%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `4.90%` |
| Continuacion Alcista (>=1x OR) | `34.25%` |
| Extension media reversal DOWN | `0.37x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.99x OR` | Mediana: `0.64x` |
| Tiempo medio al re-breakout | `100 min` | Mediana: `68 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 142 | `22%` | `23%` | `26%` | `25%` | `6%` | `16%` |
| RSI > 70 (Overbought) | 178 | `81%` ⭐ | `19%` | `24%` | `31%` | `8%` | `19%` |
| RSI 30-70 (Neutro) | 1681 | `50%` | `24%` | `32%` | `32%` | `12%` | `45%` |
| OR ABOVE_PD_HIGH | 518 | `49%` | `25%` | `26%` | `31%` | `11%` | `30%` |
| OR BELOW_PD_LOW | 366 | `51%` | `19%` | `31%` | `34%` | `8%` | `25%` |
| OR BETWEEN_CLOSE_AND_HIGH | 574 | `50%` | `26%` | `36%` | `31%` | `14%` | `51%` |
| OR BETWEEN_LOW_AND_CLOSE | 543 | `52%` | `22%` | `31%` | `30%` | `11%` | `50%` |
| ATR Creciente (>10%) | 112 | `54%` | `26%` | `44%` | `38%` | `13%` | `46%` |
| ATR Decreciente (<-10%) | 92 | `58%` | `19%` | `42%` | `29%` | `4%` | `41%` |
| ATR Q1 (Baja Vol Historica) | 511 | `49%` | `26%` | `37%` | `35%` | `15%` | `42%` |
| ATR Q4 (Alta Vol Historica) | 502 | `52%` | `27%` | `32%` | `30%` | `13%` | `38%` |
| RSI Diario < 35 | 146 | `52%` | `18%` | `30%` | `33%` | `13%` | `47%` |
| RSI Diario > 65 | 378 | `56%` | `30%` | `34%` | `32%` | `12%` | `40%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `158 min` | `105 min` | `240 min` |
| TP DOWN (desde entrada) | `127 min` | `105 min` | `225 min` |
| False Break UP → SL | `112 min` | - | - |
| False Break DOWN → SL | `126 min` | - | - |

---

## Permutación #8: NY 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1974`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.44%`
- **Rotura Bajista (DOWN):** `44.68%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `31.25%` | `35.60%` |
| 1.5x Rango OR | `19.67%` | `20.18%` |
| 2.0x Rango OR | `11.68%` | `12.70%` |
| 1.0x Volatilidad ATR Diaria | `4.00%` | `4.42%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `24.59%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `25.85%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `39.41%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `35.82%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `31.28%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1126`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `7.99%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `4.35%` |
| Shakeout & Re-breakout UP (>=2x OR) | `2.93%` |
| Continuacion Bajista (>=1x OR) | `33.93%` |
| Extension media reversal UP | `0.23x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.93x OR` | Mediana: `0.63x` |
| Tiempo medio al re-breakout | `114 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1210`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `9.59%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `5.70%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `3.39%` |
| Continuacion Alcista (>=1x OR) | `29.17%` |
| Extension media reversal DOWN | `0.26x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.88x OR` | Mediana: `0.58x` |
| Tiempo medio al re-breakout | `107 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 116 | `20%` | `17%` | `22%` | `19%` | `3%` | `16%` |
| RSI > 70 (Overbought) | 155 | `85%` ⭐ | `17%` | `18%` | `24%` | `2%` | `12%` |
| RSI 30-70 (Neutro) | 1703 | `48%` | `20%` | `26%` | `27%` | `9%` | `43%` |
| OR ABOVE_PD_HIGH | 509 | `47%` | `21%` | `18%` | `27%` | `8%` | `29%` |
| OR BELOW_PD_LOW | 357 | `52%` | `14%` | `25%` | `25%` | `5%` | `25%` |
| OR BETWEEN_CLOSE_AND_HIGH | 572 | `50%` | `22%` | `29%` | `23%` | `10%` | `49%` |
| OR BETWEEN_LOW_AND_CLOSE | 536 | `50%` | `20%` | `26%` | `28%` | `8%` | `49%` |
| ATR Creciente (>10%) | 109 | `55%` | `17%` | `42%` | `34%` | `8%` | `43%` |
| ATR Decreciente (<-10%) | 90 | `53%` | `17%` | `31%` | `24%` | `2%` | `43%` |
| ATR Q1 (Baja Vol Historica) | 504 | `48%` | `23%` | `30%` | `28%` | `10%` | `41%` |
| ATR Q4 (Alta Vol Historica) | 498 | `52%` | `22%` | `26%` | `27%` | `9%` | `36%` |
| RSI Diario < 35 | 144 | `49%` | `11%` | `28%` | `28%` | `9%` | `46%` |
| RSI Diario > 65 | 363 | `55%` | `27%` | `29%` | `26%` | `10%` | `40%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `158 min` | `120 min` | `285 min` |
| TP DOWN (desde entrada) | `135 min` | `105 min` | `225 min` |
| False Break UP → SL | `127 min` | - | - |
| False Break DOWN → SL | `138 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: XAUUSD

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] NY (15m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `65.45%` (base: `47.82%`, +18%pp). N=109.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `66.62%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `67.41%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `66.98%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `66.46%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE RSI-CONDITIONAL] London (15m) | RSI > 70 (Overbought)**: Shakeout UP post-fade al `64.29%`. Cuando el RSI esta en esta zona, los false breakouts tienden a revertir con fuerza. N=92.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `70.91%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `66.87%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (45m)**: Tasa de extensión polar bajista (1.5x) del `61.83%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `71.00%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `66.81%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.69%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=324 | UP: `55%` | Ext 1.5 UP: `75%` | Falsa Ruptura DW: `52%` | Reversión a PD_Close: `70%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=324 | UP: `51%` | Ext 1.5 UP: `65%` | Falsa Ruptura DW: `54%` | Reversión a PD_Close: `57%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=96 | UP: `55%` | Ext 1.5 UP: `66%` | Falsa Ruptura DW: `63%` | Reversión a PD_Close: `81%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1198 | UP: `51%` | Ext 1.5 UP: `71%` | Falsa Ruptura DW: `53%` | Reversión a PD_Close: `65%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*