# 🌐 Matriz Probabilística Omnidireccional: EURUSD

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
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1617`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.66%`
- **Rotura Bajista (DOWN):** `44.71%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `78.58%` | `80.50%` |
| 1.5x Rango OR | `67.87%` | `70.12%` |
| 2.0x Rango OR | `59.28%` | `60.44%` |
| 1.0x Volatilidad ATR Diaria | `15.57%` | `15.63%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.29%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.40%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `74.52%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `61.66%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.10%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1266`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `50.95%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `43.44%` |
| Shakeout & Re-breakout UP (>=2x OR) | `35.70%` |
| Continuacion Bajista (>=1x OR) | `75.99%` |
| Extension media reversal UP | `1.90x OR` | Mediana: `1.07x` |
| Extension media continuacion DOWN | `2.88x OR` | Mediana: `2.19x` |
| Tiempo medio al re-breakout | `111 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1304`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `54.52%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `46.55%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `38.57%` |
| Continuacion Alcista (>=1x OR) | `73.54%` |
| Extension media reversal DOWN | `2.00x OR` | Mediana: `1.27x` |
| Extension media continuacion UP | `2.82x OR` | Mediana: `2.15x` |
| Tiempo medio al re-breakout | `114 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 137 | `24%` | `67%` ⭐ | `55%` | `52%` | `45%` | `51%` |
| RSI > 70 (Overbought) | 113 | `69%` ⭐ | `60%` ⭐ | `51%` | `62%` ⭐ | `47%` | `53%` |
| RSI 30-70 (Neutro) | 1367 | `51%` | `69%` ⭐ | `58%` | `58%` | `52%` | `79%` ⭐ |
| OR ABOVE_PD_HIGH | 234 | `44%` | `64%` ⭐ | `57%` | `46%` | `48%` | `65%` ⭐ |
| OR BELOW_PD_LOW | 207 | `47%` | `64%` ⭐ | `53%` | `60%` ⭐ | `48%` | `64%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 554 | `51%` | `66%` ⭐ | `58%` | `60%` | `53%` | `79%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 622 | `51%` | `72%` ⭐ | `58%` | `59%` | `51%` | `78%` ⭐ |
| ATR Creciente (>10%) | 78 | `46%` | `72%` ⭐ | `69%` ⭐ | `67%` ⭐ | `57%` | `67%` ⭐ |
| ATR Decreciente (<-10%) | 62 | `50%` | `68%` ⭐ | `65%` ⭐ | `54%` | `57%` | `76%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 433 | `50%` | `73%` ⭐ | `50%` | `60%` ⭐ | `51%` | `76%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 368 | `52%` | `61%` ⭐ | `54%` | `51%` | `46%` | `73%` ⭐ |
| RSI Diario < 35 | 199 | `48%` | `75%` ⭐ | `48%` | `53%` | `53%` | `74%` ⭐ |
| RSI Diario > 65 | 159 | `45%` | `67%` ⭐ | `58%` | `45%` | `48%` | `80%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `184 min` | `120 min` | `330 min` |
| TP DOWN (desde entrada) | `192 min` | `120 min` | `345 min` |
| False Break UP → SL | `88 min` | - | - |
| False Break DOWN → SL | `87 min` | - | - |

---

## Permutación #2: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1997`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `52.38%`
- **Rotura Bajista (DOWN):** `45.22%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `72.66%` | `74.86%` |
| 1.5x Rango OR | `60.33%` | `63.23%` |
| 2.0x Rango OR | `50.48%` | `52.05%` |
| 1.0x Volatilidad ATR Diaria | `13.00%` | `14.84%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.93%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `55.04%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `74.06%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `61.64%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.89%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1534`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `40.55%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `31.68%` |
| Shakeout & Re-breakout UP (>=2x OR) | `24.45%` |
| Continuacion Bajista (>=1x OR) | `69.30%` |
| Extension media reversal UP | `1.34x OR` | Mediana: `0.51x` |
| Extension media continuacion DOWN | `2.35x OR` | Mediana: `1.73x` |
| Tiempo medio al re-breakout | `129 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1576`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `44.23%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `34.14%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `26.97%` |
| Continuacion Alcista (>=1x OR) | `67.39%` |
| Extension media reversal DOWN | `1.49x OR` | Mediana: `0.69x` |
| Extension media continuacion UP | `2.23x OR` | Mediana: `1.63x` |
| Tiempo medio al re-breakout | `131 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 146 | `23%` | `61%` ⭐ | `52%` | `43%` | `26%` | `45%` |
| RSI > 70 (Overbought) | 122 | `82%` ⭐ | `56%` | `46%` | `55%` | `27%` | `46%` |
| RSI 30-70 (Neutro) | 1729 | `53%` | `61%` ⭐ | `59%` | `57%` | `43%` | `79%` ⭐ |
| OR ABOVE_PD_HIGH | 301 | `44%` | `59%` | `60%` ⭐ | `47%` | `39%` | `65%` ⭐ |
| OR BELOW_PD_LOW | 243 | `55%` | `63%` ⭐ | `51%` | `59%` | `33%` | `65%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 693 | `54%` | `57%` | `60%` ⭐ | `55%` | `41%` | `78%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 760 | `54%` | `63%` ⭐ | `57%` | `58%` | `43%` | `77%` ⭐ |
| ATR Creciente (>10%) | 87 | `46%` | `68%` ⭐ | `55%` | `59%` | `48%` | `69%` ⭐ |
| ATR Decreciente (<-10%) | 79 | `53%` | `60%` | `71%` ⭐ | `50%` | `37%` | `75%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 515 | `53%` | `64%` ⭐ | `54%` | `58%` | `41%` | `76%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 486 | `54%` | `54%` | `59%` | `49%` | `36%` | `72%` ⭐ |
| RSI Diario < 35 | 227 | `55%` | `66%` ⭐ | `54%` | `51%` | `38%` | `73%` ⭐ |
| RSI Diario > 65 | 198 | `44%` | `57%` | `64%` ⭐ | `53%` | `41%` | `79%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `212 min` | `180 min` | `360 min` |
| TP DOWN (desde entrada) | `216 min` | `180 min` | `360 min` |
| False Break UP → SL | `124 min` | - | - |
| False Break DOWN → SL | `123 min` | - | - |

---

## Permutación #3: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2073`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.46%`
- **Rotura Bajista (DOWN):** `47.56%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `65.87%` | `71.30%` |
| 1.5x Rango OR | `51.63%` | `56.80%` |
| 2.0x Rango OR | `41.68%` | `46.35%` |
| 1.0x Volatilidad ATR Diaria | `11.95%` | `14.20%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `57.55%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.14%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `72.60%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `61.12%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.14%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1583`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `34.05%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `25.52%` |
| Shakeout & Re-breakout UP (>=2x OR) | `19.01%` |
| Continuacion Bajista (>=1x OR) | `63.11%` |
| Extension media reversal UP | `1.06x OR` | Mediana: `0.24x` |
| Extension media continuacion DOWN | `1.94x OR` | Mediana: `1.43x` |
| Tiempo medio al re-breakout | `138 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1579`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `35.72%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `26.22%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `19.95%` |
| Continuacion Alcista (>=1x OR) | `61.05%` |
| Extension media reversal DOWN | `1.10x OR` | Mediana: `0.37x` |
| Extension media continuacion UP | `1.87x OR` | Mediana: `1.36x` |
| Tiempo medio al re-breakout | `145 min` | Mediana: `105 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 153 | `17%` | `31%` | `58%` | `48%` | `24%` | `42%` |
| RSI > 70 (Overbought) | 141 | `82%` ⭐ | `47%` | `47%` | `61%` ⭐ | `22%` | `48%` |
| RSI 30-70 (Neutro) | 1779 | `51%` | `53%` | `59%` | `54%` | `36%` | `77%` ⭐ |
| OR ABOVE_PD_HIGH | 313 | `45%` | `54%` | `59%` | `46%` | `33%` | `63%` ⭐ |
| OR BELOW_PD_LOW | 248 | `57%` | `54%` | `57%` | `54%` | `29%` | `64%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 719 | `50%` | `48%` | `60%` ⭐ | `53%` | `33%` | `76%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 793 | `51%` | `53%` | `55%` | `56%` | `36%` | `76%` ⭐ |
| ATR Creciente (>10%) | 87 | `45%` | `56%` | `49%` | `61%` ⭐ | `35%` | `67%` ⭐ |
| ATR Decreciente (<-10%) | 81 | `48%` | `49%` | `67%` ⭐ | `56%` | `33%` | `70%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 531 | `51%` | `56%` | `57%` | `53%` | `37%` | `74%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 506 | `52%` | `47%` | `56%` | `50%` | `30%` | `72%` ⭐ |
| RSI Diario < 35 | 229 | `54%` | `55%` | `53%` | `49%` | `36%` | `72%` ⭐ |
| RSI Diario > 65 | 209 | `44%` | `48%` | `62%` ⭐ | `54%` | `32%` | `78%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `238 min` | `232 min` | `375 min` |
| TP DOWN (desde entrada) | `237 min` | `225 min` | `375 min` |
| False Break UP → SL | `156 min` | - | - |
| False Break DOWN → SL | `147 min` | - | - |

---

## Permutación #4: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2090`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.48%`
- **Rotura Bajista (DOWN):** `47.51%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `62.27%` | `66.47%` |
| 1.5x Rango OR | `46.54%` | `50.96%` |
| 2.0x Rango OR | `36.11%` | `38.67%` |
| 1.0x Volatilidad ATR Diaria | `11.56%` | `13.29%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `56.21%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `50.15%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `71.39%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `60.53%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.26%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1566`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `27.65%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `19.41%` |
| Shakeout & Re-breakout UP (>=2x OR) | `14.62%` |
| Continuacion Bajista (>=1x OR) | `57.54%` |
| Extension media reversal UP | `0.83x OR` | Mediana: `0.06x` |
| Extension media continuacion DOWN | `1.63x OR` | Mediana: `1.24x` |
| Tiempo medio al re-breakout | `149 min` | Mediana: `120 min` |

**False Breakouts DOWN analizados:** `1547`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `29.15%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `20.94%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `14.87%` |
| Continuacion Alcista (>=1x OR) | `55.46%` |
| Extension media reversal DOWN | `0.86x OR` | Mediana: `0.13x` |
| Extension media continuacion UP | `1.60x OR` | Mediana: `1.14x` |
| Tiempo medio al re-breakout | `157 min` | Mediana: `135 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 154 | `20%` | `35%` | `48%` | `38%` | `15%` | `40%` |
| RSI > 70 (Overbought) | 141 | `84%` ⭐ | `36%` | `50%` | `59%` | `13%` | `46%` |
| RSI 30-70 (Neutro) | 1795 | `50%` | `48%` | `57%` | `52%` | `30%` | `76%` ⭐ |
| OR ABOVE_PD_HIGH | 317 | `44%` | `49%` | `57%` | `44%` | `27%` | `62%` ⭐ |
| OR BELOW_PD_LOW | 249 | `59%` | `42%` | `60%` | `48%` | `23%` | `62%` ⭐ |
| OR BETWEEN_CLOSE_AND_HIGH | 724 | `50%` | `43%` | `59%` | `51%` | `27%` | `75%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 800 | `51%` | `50%` | `52%` | `53%` | `30%` | `75%` ⭐ |
| ATR Creciente (>10%) | 87 | `46%` | `50%` | `45%` | `52%` | `26%` | `66%` ⭐ |
| ATR Decreciente (<-10%) | 82 | `46%` | `39%` | `58%` | `52%` | `25%` | `71%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 533 | `50%` | `49%` | `55%` | `51%` | `30%` | `73%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 514 | `52%` | `41%` | `56%` | `48%` | `25%` | `71%` ⭐ |
| RSI Diario < 35 | 230 | `51%` | `47%` | `52%` | `47%` | `31%` | `72%` ⭐ |
| RSI Diario > 65 | 212 | `48%` | `45%` | `64%` ⭐ | `53%` | `26%` | `76%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `261 min` | `255 min` | `390 min` |
| TP DOWN (desde entrada) | `256 min` | `255 min` | `390 min` |
| False Break UP → SL | `183 min` | - | - |
| False Break DOWN → SL | `178 min` | - | - |

---

## Permutación #5: NY 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1785`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.11%`
- **Rotura Bajista (DOWN):** `45.71%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.17%` | `65.81%` |
| 1.5x Rango OR | `51.64%` | `51.96%` |
| 2.0x Rango OR | `40.83%` | `39.95%` |
| 1.0x Volatilidad ATR Diaria | `5.35%` | `5.02%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `49.45%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `48.90%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `42.75%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `38.60%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `34.57%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1364`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `33.87%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `25.07%` |
| Shakeout & Re-breakout UP (>=2x OR) | `19.13%` |
| Continuacion Bajista (>=1x OR) | `65.40%` |
| Extension media reversal UP | `1.07x OR` | Mediana: `0.28x` |
| Extension media continuacion DOWN | `2.07x OR` | Mediana: `1.56x` |
| Tiempo medio al re-breakout | `75 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1362`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `38.91%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `30.18%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `22.98%` |
| Continuacion Alcista (>=1x OR) | `61.82%` |
| Extension media reversal DOWN | `1.25x OR` | Mediana: `0.50x` |
| Extension media continuacion UP | `1.96x OR` | Mediana: `1.38x` |
| Tiempo medio al re-breakout | `71 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 141 | `28%` | `56%` | `46%` | `44%` | `32%` | `15%` |
| RSI > 70 (Overbought) | 132 | `60%` | `47%` | `42%` | `57%` | `34%` | `19%` |
| RSI 30-70 (Neutro) | 1512 | `47%` | `52%` | `50%` | `49%` | `34%` | `47%` |
| OR ABOVE_PD_HIGH | 428 | `49%` | `51%` | `52%` | `43%` | `33%` | `30%` |
| OR BELOW_PD_LOW | 416 | `49%` | `54%` | `47%` | `56%` | `34%` | `29%` |
| OR BETWEEN_CLOSE_AND_HIGH | 446 | `45%` | `47%` | `48%` | `50%` | `36%` | `55%` |
| OR BETWEEN_LOW_AND_CLOSE | 495 | `42%` | `54%` | `51%` | `47%` | `34%` | `54%` |
| ATR Creciente (>10%) | 83 | `46%` | `71%` ⭐ | `34%` | `38%` | `38%` | `36%` |
| ATR Decreciente (<-10%) | 59 | `58%` | `50%` | `32%` | `45%` | `28%` | `41%` |
| ATR Q1 (Baja Vol Historica) | 478 | `47%` | `54%` | `53%` | `49%` | `35%` | `45%` |
| ATR Q4 (Alta Vol Historica) | 400 | `45%` | `53%` | `47%` | `54%` | `33%` | `42%` |
| RSI Diario < 35 | 212 | `41%` | `50%` | `45%` | `57%` | `37%` | `41%` |
| RSI Diario > 65 | 175 | `47%` | `57%` | `49%` | `44%` | `27%` | `45%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `94 min` | `60 min` | `150 min` |
| TP DOWN (desde entrada) | `86 min` | `60 min` | `120 min` |
| False Break UP → SL | `62 min` | - | - |
| False Break DOWN → SL | `67 min` | - | - |

---

## Permutación #6: NY 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2018`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.22%`
- **Rotura Bajista (DOWN):** `47.13%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `56.94%` | `56.26%` |
| 1.5x Rango OR | `40.60%` | `39.96%` |
| 2.0x Rango OR | `28.06%` | `29.13%` |
| 1.0x Volatilidad ATR Diaria | `5.04%` | `4.42%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `44.30%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `41.54%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `41.67%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `36.77%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `33.05%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1456`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `21.29%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `14.90%` |
| Shakeout & Re-breakout UP (>=2x OR) | `10.92%` |
| Continuacion Bajista (>=1x OR) | `53.64%` |
| Extension media reversal UP | `0.64x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.53x OR` | Mediana: `1.10x` |
| Tiempo medio al re-breakout | `89 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1441`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `24.08%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `17.14%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.01%` |
| Continuacion Alcista (>=1x OR) | `50.59%` |
| Extension media reversal DOWN | `0.70x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.49x OR` | Mediana: `1.01x` |
| Tiempo medio al re-breakout | `87 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 139 | `18%` | `36%` | `48%` | `31%` | `10%` | `11%` |
| RSI > 70 (Overbought) | 139 | `69%` ⭐ | `33%` | `33%` | `41%` | `15%` | `18%` |
| RSI 30-70 (Neutro) | 1740 | `49%` | `42%` | `45%` | `43%` | `23%` | `46%` |
| OR ABOVE_PD_HIGH | 481 | `49%` | `42%` | `44%` | `38%` | `20%` | `28%` |
| OR BELOW_PD_LOW | 470 | `51%` | `41%` | `42%` | `43%` | `20%` | `28%` |
| OR BETWEEN_CLOSE_AND_HIGH | 500 | `46%` | `40%` | `47%` | `44%` | `25%` | `54%` |
| OR BETWEEN_LOW_AND_CLOSE | 567 | `47%` | `40%` | `43%` | `41%` | `20%` | `53%` |
| ATR Creciente (>10%) | 86 | `47%` | `45%` | `38%` | `42%` | `30%` | `37%` |
| ATR Decreciente (<-10%) | 78 | `49%` | `42%` | `39%` | `39%` | `19%` | `40%` |
| ATR Q1 (Baja Vol Historica) | 521 | `45%` | `42%` | `47%` | `46%` | `22%` | `44%` |
| ATR Q4 (Alta Vol Historica) | 485 | `52%` | `39%` | `47%` | `40%` | `23%` | `42%` |
| RSI Diario < 35 | 230 | `44%` | `34%` | `44%` | `49%` | `21%` | `40%` |
| RSI Diario > 65 | 201 | `49%` | `43%` | `51%` | `34%` | `21%` | `43%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `114 min` | `75 min` | `195 min` |
| TP DOWN (desde entrada) | `104 min` | `75 min` | `180 min` |
| False Break UP → SL | `87 min` | - | - |
| False Break DOWN → SL | `94 min` | - | - |

---

## Permutación #7: NY 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2034`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.16%`
- **Rotura Bajista (DOWN):** `49.07%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `42.20%` | `41.98%` |
| 1.5x Rango OR | `25.70%` | `26.45%` |
| 2.0x Rango OR | `17.00%` | `17.43%` |
| 1.0x Volatilidad ATR Diaria | `3.70%` | `3.31%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `38.50%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `34.47%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `38.69%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `35.00%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `31.24%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1390`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `13.67%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `8.49%` |
| Shakeout & Re-breakout UP (>=2x OR) | `5.97%` |
| Continuacion Bajista (>=1x OR) | `40.29%` |
| Extension media reversal UP | `0.39x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.13x OR` | Mediana: `0.81x` |
| Tiempo medio al re-breakout | `101 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1347`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `14.48%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `9.80%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `5.79%` |
| Continuacion Alcista (>=1x OR) | `39.35%` |
| Extension media reversal DOWN | `0.42x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.08x OR` | Mediana: `0.73x` |
| Tiempo medio al re-breakout | `101 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 154 | `15%` | `9%` | `35%` | `27%` | `5%` | `9%` |
| RSI > 70 (Overbought) | 133 | `78%` ⭐ | `17%` | `26%` | `44%` | `11%` | `10%` |
| RSI 30-70 (Neutro) | 1747 | `50%` | `27%` | `40%` | `35%` | `15%` | `44%` |
| OR ABOVE_PD_HIGH | 484 | `47%` | `26%` | `36%` | `32%` | `11%` | `27%` |
| OR BELOW_PD_LOW | 470 | `49%` | `25%` | `37%` | `38%` | `12%` | `25%` |
| OR BETWEEN_CLOSE_AND_HIGH | 509 | `48%` | `26%` | `43%` | `36%` | `18%` | `50%` |
| OR BETWEEN_LOW_AND_CLOSE | 571 | `52%` | `26%` | `38%` | `33%` | `13%` | `49%` |
| ATR Creciente (>10%) | 86 | `49%` | `36%` | `36%` | `42%` | `19%` | `36%` |
| ATR Decreciente (<-10%) | 80 | `46%` | `35%` | `27%` | `34%` | `12%` | `38%` |
| ATR Q1 (Baja Vol Historica) | 510 | `47%` | `29%` | `40%` | `36%` | `15%` | `41%` |
| ATR Q4 (Alta Vol Historica) | 502 | `53%` | `24%` | `40%` | `36%` | `15%` | `39%` |
| RSI Diario < 35 | 230 | `47%` | `25%` | `39%` | `37%` | `14%` | `37%` |
| RSI Diario > 65 | 201 | `48%` | `26%` | `41%` | `33%` | `13%` | `41%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `131 min` | `90 min` | `225 min` |
| TP DOWN (desde entrada) | `126 min` | `90 min` | `210 min` |
| False Break UP → SL | `106 min` | - | - |
| False Break DOWN → SL | `115 min` | - | - |

---

## Permutación #8: NY 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2016`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.27%`
- **Rotura Bajista (DOWN):** `49.60%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `36.73%` | `36.00%` |
| 1.5x Rango OR | `20.67%` | `19.90%` |
| 2.0x Rango OR | `11.54%` | `12.20%` |
| 1.0x Volatilidad ATR Diaria | `3.04%` | `2.60%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `32.21%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `30.20%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `37.30%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `33.83%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `30.23%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1309`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `10.16%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `6.42%` |
| Shakeout & Re-breakout UP (>=2x OR) | `4.20%` |
| Continuacion Bajista (>=1x OR) | `34.38%` |
| Extension media reversal UP | `0.30x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.96x OR` | Mediana: `0.69x` |
| Tiempo medio al re-breakout | `108 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1253`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `10.45%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `6.54%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `3.91%` |
| Continuacion Alcista (>=1x OR) | `34.64%` |
| Extension media reversal DOWN | `0.31x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.94x OR` | Mediana: `0.64x` |
| Tiempo medio al re-breakout | `104 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 137 | `19%` | `12%` | `23%` | `21%` | `3%` | `10%` |
| RSI > 70 (Overbought) | 126 | `75%` ⭐ | `16%` | `21%` | `29%` | `7%` | `9%` |
| RSI 30-70 (Neutro) | 1753 | `48%` | `21%` | `34%` | `31%` | `11%` | `41%` |
| OR ABOVE_PD_HIGH | 479 | `45%` | `21%` | `29%` | `27%` | `7%` | `27%` |
| OR BELOW_PD_LOW | 465 | `48%` | `20%` | `33%` | `35%` | `9%` | `24%` |
| OR BETWEEN_CLOSE_AND_HIGH | 506 | `46%` | `21%` | `37%` | `30%` | `13%` | `47%` |
| OR BETWEEN_LOW_AND_CLOSE | 566 | `49%` | `20%` | `30%` | `28%` | `11%` | `48%` |
| ATR Creciente (>10%) | 84 | `52%` | `20%` | `36%` | `41%` | `13%` | `33%` |
| ATR Decreciente (<-10%) | 81 | `42%` | `29%` | `26%` | `35%` | `10%` | `36%` |
| ATR Q1 (Baja Vol Historica) | 502 | `45%` | `21%` | `33%` | `32%` | `11%` | `39%` |
| ATR Q4 (Alta Vol Historica) | 502 | `50%` | `21%` | `34%` | `31%` | `12%` | `38%` |
| RSI Diario < 35 | 228 | `48%` | `22%` | `35%` | `31%` | `11%` | `34%` |
| RSI Diario > 65 | 200 | `46%` | `22%` | `30%` | `27%` | `10%` | `39%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `140 min` | `105 min` | `210 min` |
| TP DOWN (desde entrada) | `131 min` | `105 min` | `210 min` |
| False Break UP → SL | `112 min` | - | - |
| False Break DOWN → SL | `125 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: EURUSD

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] London (15m) | RSI Diario > 65**: Extension 1.5x DOWN sube a `81.71%` (base: `70.12%`, +12%pp). N=159.

- **[EDGE CONTEXT-BOOST UP] NY (15m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `71.05%` (base: `51.64%`, +19%pp). N=83. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `74.52%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `74.06%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `72.60%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `71.39%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] London (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `61.66%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `61.64%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `61.12%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] London (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `60.53%` de los eventos evaluados.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `70.12%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `63.23%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `67.87%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.33%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=416 | UP: `45%` | Ext 1.5 UP: `79%` | Falsa Ruptura DW: `56%` | Reversión a PD_Close: `76%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=412 | UP: `50%` | Ext 1.5 UP: `55%` | Falsa Ruptura DW: `57%` | Reversión a PD_Close: `71%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=139 | UP: `49%` | Ext 1.5 UP: `65%` | Falsa Ruptura DW: `53%` | Reversión a PD_Close: `71%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1478 | UP: `50%` | Ext 1.5 UP: `68%` | Falsa Ruptura DW: `58%` | Reversión a PD_Close: `75%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*