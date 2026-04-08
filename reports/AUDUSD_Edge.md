# 🌐 Matriz Probabilística Omnidireccional: AUDUSD

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
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `652`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `61.35%`
- **Rotura Bajista (DOWN):** `31.90%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `28.50%` | `25.00%` |
| 1.5x Rango OR | `13.75%` | `13.46%` |
| 2.0x Rango OR | `5.50%` | `10.58%` |
| 1.0x Volatilidad ATR Diaria | `0.00%` | `0.96%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `18.25%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `32.21%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `25.00%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `14.88%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `11.81%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `280`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `11.07%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `4.64%` |
| Shakeout & Re-breakout UP (>=2x OR) | `2.14%` |
| Continuacion Bajista (>=1x OR) | `23.57%` |
| Extension media reversal UP | `0.28x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.96x OR` | Mediana: `0.47x` |
| Tiempo medio al re-breakout | `40 min` | Mediana: `38 min` |

**False Breakouts DOWN analizados:** `466`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `4.08%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `1.93%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `1.50%` |
| Continuacion Alcista (>=1x OR) | `28.97%` |
| Extension media reversal DOWN | `0.15x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.74x OR` | Mediana: `0.59x` |
| Tiempo medio al re-breakout | `42 min` | Mediana: `38 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 27 | `44%` | `17%` | `17%` | `23%` | `12%` | `15%` |
| RSI 30-70 (Neutro) | 606 | `62%` ⭐ | `14%` | `18%` | `33%` | `11%` | `26%` |
| OR ABOVE_PD_HIGH | 128 | `62%` ⭐ | `12%` | `14%` | `26%` | `14%` | `5%` |
| OR BELOW_PD_LOW | 137 | `67%` ⭐ | `16%` | `26%` | `28%` | `12%` | `7%` |
| OR BETWEEN_CLOSE_AND_HIGH | 190 | `54%` | `14%` | `15%` | `33%` | `11%` | `31%` |
| OR BETWEEN_LOW_AND_CLOSE | 197 | `64%` ⭐ | `13%` | `18%` | `39%` | `8%` | `45%` |
| ATR Creciente (>10%) | 26 | `69%` ⭐ | `6%` | `33%` | `43%` | `27%` | `15%` |
| ATR Decreciente (<-10%) | 23 | `70%` ⭐ | `25%` | `25%` | `40%` | `11%` | `17%` |
| ATR Q1 (Baja Vol Historica) | 198 | `56%` | `15%` | `21%` | `31%` | `15%` | `28%` |
| ATR Q4 (Alta Vol Historica) | 139 | `61%` ⭐ | `13%` | `12%` | `18%` | `9%` | `17%` |
| RSI Diario < 35 | 87 | `60%` | `25%` | `10%` | `37%` | `24%` | `28%` |
| RSI Diario > 65 | 75 | `65%` ⭐ | `8%` | `22%` | `52%` | `10%` | `31%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `61 min` | `75 min` | `75 min` |
| TP DOWN (desde entrada) | `39 min` | `30 min` | `75 min` |
| False Break UP → SL | `44 min` | - | - |
| False Break DOWN → SL | `46 min` | - | - |

---

## Permutación #2: Sydney 30m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `926`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `59.18%`
- **Rotura Bajista (DOWN):** `31.21%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `20.26%` | `20.42%` |
| 1.5x Rango OR | `7.48%` | `10.38%` |
| 2.0x Rango OR | `2.19%` | `7.96%` |
| 1.0x Volatilidad ATR Diaria | `0.00%` | `0.35%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `14.60%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `24.57%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `21.27%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `13.17%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `10.91%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `350`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `5.14%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `2.57%` |
| Shakeout & Re-breakout UP (>=2x OR) | `0.86%` |
| Continuacion Bajista (>=1x OR) | `20.00%` |
| Extension media reversal UP | `0.17x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.70x OR` | Mediana: `0.45x` |
| Tiempo medio al re-breakout | `36 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `598`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `2.34%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `1.34%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `1.00%` |
| Continuacion Alcista (>=1x OR) | `20.57%` |
| Extension media reversal DOWN | `0.11x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.62x OR` | Mediana: `0.50x` |
| Tiempo medio al re-breakout | `37 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 22 | `32%` | `14%` | `14%` | `33%` | `7%` | `14%` |
| RSI > 70 (Overbought) | 21 | `67%` ⭐ | `7%` | `21%` | `33%` | `11%` | `5%` |
| RSI 30-70 (Neutro) | 883 | `60%` | `7%` | `14%` | `24%` | `5%` | `22%` |
| OR ABOVE_PD_HIGH | 189 | `57%` | `7%` | `17%` | `25%` | `7%` | `4%` |
| OR BELOW_PD_LOW | 209 | `60%` | `5%` | `18%` | `23%` | `3%` | `6%` |
| OR BETWEEN_CLOSE_AND_HIGH | 264 | `57%` | `12%` | `10%` | `24%` | `7%` | `25%` |
| OR BETWEEN_LOW_AND_CLOSE | 264 | `62%` ⭐ | `5%` | `15%` | `26%` | `4%` | `42%` |
| ATR Creciente (>10%) | 40 | `57%` | `4%` | `22%` | `17%` | `18%` | `12%` |
| ATR Decreciente (<-10%) | 28 | `54%` | `13%` | `0%` | `27%` | `9%` | `18%` |
| ATR Q1 (Baja Vol Historica) | 254 | `54%` | `10%` | `14%` | `26%` | `9%` | `24%` |
| ATR Q4 (Alta Vol Historica) | 215 | `56%` | `5%` | `12%` | `18%` | `0%` | `15%` |
| RSI Diario < 35 | 118 | `59%` | `13%` | `10%` | `33%` | `11%` | `22%` |
| RSI Diario > 65 | 106 | `59%` | `3%` | `19%` | `46%` | `5%` | `27%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `49 min` | `45 min` | `75 min` |
| TP DOWN (desde entrada) | `35 min` | `30 min` | `60 min` |
| False Break UP → SL | `40 min` | - | - |
| False Break DOWN → SL | `39 min` | - | - |

---

## Permutación #3: Sydney 45m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1186`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `56.16%`
- **Rotura Bajista (DOWN):** `32.72%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `14.56%` | `17.27%` |
| 1.5x Rango OR | `4.50%` | `7.22%` |
| 2.0x Rango OR | `1.65%` | `4.38%` |
| 1.0x Volatilidad ATR Diaria | `0.00%` | `0.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `10.96%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `20.10%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `18.97%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `11.64%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `9.57%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `413`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `3.87%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `1.94%` |
| Shakeout & Re-breakout UP (>=2x OR) | `0.97%` |
| Continuacion Bajista (>=1x OR) | `17.68%` |
| Extension media reversal UP | `0.14x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.61x OR` | Mediana: `0.40x` |
| Tiempo medio al re-breakout | `34 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `695`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `1.73%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `1.01%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `0.43%` |
| Continuacion Alcista (>=1x OR) | `15.68%` |
| Extension media reversal DOWN | `0.07x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.54x OR` | Mediana: `0.41x` |
| Tiempo medio al re-breakout | `36 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 25 | `12%` | `0%` | `33%` | `16%` | `0%` | `8%` |
| RSI > 70 (Overbought) | 21 | `71%` ⭐ | `7%` | `13%` | `25%` | `0%` | `10%` |
| RSI 30-70 (Neutro) | 1140 | `57%` | `4%` | `11%` | `20%` | `4%` | `19%` |
| OR ABOVE_PD_HIGH | 246 | `54%` | `7%` | `12%` | `22%` | `5%` | `2%` |
| OR BELOW_PD_LOW | 274 | `55%` | `2%` | `13%` | `15%` | `2%` | `5%` |
| OR BETWEEN_CLOSE_AND_HIGH | 323 | `54%` | `6%` | `6%` | `21%` | `4%` | `26%` |
| OR BETWEEN_LOW_AND_CLOSE | 343 | `60%` ⭐ | `4%` | `13%` | `23%` | `4%` | `36%` |
| ATR Creciente (>10%) | 51 | `51%` | `4%` | `15%` | `42%` | `13%` | `16%` |
| ATR Decreciente (<-10%) | 39 | `51%` | `10%` | `0%` | `29%` | `14%` | `15%` |
| ATR Q1 (Baja Vol Historica) | 323 | `53%` | `6%` | `13%` | `24%` | `5%` | `22%` |
| ATR Q4 (Alta Vol Historica) | 282 | `56%` | `4%` | `9%` | `12%` | `3%` | `13%` |
| RSI Diario < 35 | 148 | `60%` ⭐ | `9%` | `9%` | `30%` | `10%` | `20%` |
| RSI Diario > 65 | 131 | `53%` | `7%` | `9%` | `44%` | `12%` | `22%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `30 min` | `30 min` | `45 min` |
| TP DOWN (desde entrada) | `27 min` | `22 min` | `45 min` |
| False Break UP → SL | `39 min` | - | - |
| False Break DOWN → SL | `36 min` | - | - |

---

## Permutación #4: Sydney 60m
**Configuración:** Inicia a las `22:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1454`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.79%`
- **Rotura Bajista (DOWN):** `32.05%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `10.09%` | `12.88%` |
| 1.5x Rango OR | `3.19%` | `5.36%` |
| 2.0x Rango OR | `1.20%` | `3.22%` |
| 1.0x Volatilidad ATR Diaria | `0.00%` | `0.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `5.18%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `12.02%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `16.85%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `10.11%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `9.08%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `442`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `1.81%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `1.13%` |
| Shakeout & Re-breakout UP (>=2x OR) | `0.45%` |
| Continuacion Bajista (>=1x OR) | `14.71%` |
| Extension media reversal UP | `0.08x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `0.52x OR` | Mediana: `0.31x` |
| Tiempo medio al re-breakout | `30 min` | Mediana: `30 min` |

**False Breakouts DOWN analizados:** `727`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `0.83%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `0.28%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `0.14%` |
| Continuacion Alcista (>=1x OR) | `11.00%` |
| Extension media reversal DOWN | `0.03x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `0.47x OR` | Mediana: `0.35x` |
| Tiempo medio al re-breakout | `32 min` | Mediana: `30 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 39 | `26%` | `0%` | `10%` | `17%` | `5%` | `10%` |
| RSI > 70 (Overbought) | 21 | `57%` | `0%` | `8%` | `0%` | `0%` | `5%` |
| RSI 30-70 (Neutro) | 1394 | `52%` | `3%` | `5%` | `12%` | `2%` | `17%` |
| OR ABOVE_PD_HIGH | 313 | `50%` | `5%` | `6%` | `17%` | `1%` | `2%` |
| OR BELOW_PD_LOW | 341 | `47%` | `0%` | `8%` | `9%` | `2%` | `4%` |
| OR BETWEEN_CLOSE_AND_HIGH | 388 | `54%` | `5%` | `3%` | `13%` | `3%` | `23%` |
| OR BETWEEN_LOW_AND_CLOSE | 412 | `55%` | `2%` | `4%` | `10%` | `1%` | `33%` |
| ATR Creciente (>10%) | 61 | `54%` | `9%` | `0%` | `25%` | `0%` | `11%` |
| ATR Decreciente (<-10%) | 49 | `53%` | `4%` | `0%` | `8%` | `8%` | `12%` |
| ATR Q1 (Baja Vol Historica) | 402 | `48%` | `3%` | `6%` | `16%` | `3%` | `20%` |
| ATR Q4 (Alta Vol Historica) | 344 | `53%` | `4%` | `3%` | `11%` | `1%` | `14%` |
| RSI Diario < 35 | 171 | `54%` | `4%` | `4%` | `22%` | `4%` | `19%` |
| RSI Diario > 65 | 154 | `55%` | `5%` | `7%` | `18%` | `8%` | `18%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `27 min` | `30 min` | `45 min` |
| TP DOWN (desde entrada) | `27 min` | `30 min` | `45 min` |
| False Break UP → SL | `33 min` | - | - |
| False Break DOWN → SL | `32 min` | - | - |

---

## Permutación #5: London 15m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1540`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.70%`
- **Rotura Bajista (DOWN):** `46.82%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `79.87%` | `79.89%` |
| 1.5x Rango OR | `68.00%` | `70.46%` |
| 2.0x Rango OR | `57.87%` | `60.61%` |
| 1.0x Volatilidad ATR Diaria | `10.40%` | `12.07%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.53%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.87%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.82%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `53.51%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `43.18%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1225`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `47.92%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `37.63%` |
| Shakeout & Re-breakout UP (>=2x OR) | `29.71%` |
| Continuacion Bajista (>=1x OR) | `72.57%` |
| Extension media reversal UP | `1.61x OR` | Mediana: `0.90x` |
| Extension media continuacion DOWN | `2.63x OR` | Mediana: `2.00x` |
| Tiempo medio al re-breakout | `120 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1223`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `51.51%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `42.35%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `34.59%` |
| Continuacion Alcista (>=1x OR) | `71.55%` |
| Extension media reversal DOWN | `1.79x OR` | Mediana: `1.07x` |
| Extension media continuacion UP | `2.47x OR` | Mediana: `1.86x` |
| Tiempo medio al re-breakout | `122 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 95 | `23%` | `77%` ⭐ | `50%` | `62%` ⭐ | `43%` | `25%` |
| RSI > 70 (Overbought) | 83 | `76%` ⭐ | `59%` | `59%` | `50%` | `42%` | `33%` |
| RSI 30-70 (Neutro) | 1362 | `49%` | `69%` ⭐ | `59%` | `57%` | `49%` | `66%` ⭐ |
| OR ABOVE_PD_HIGH | 296 | `49%` | `68%` ⭐ | `60%` ⭐ | `53%` | `47%` | `52%` |
| OR BELOW_PD_LOW | 297 | `47%` | `68%` ⭐ | `53%` | `60%` ⭐ | `44%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 466 | `50%` | `72%` ⭐ | `57%` | `56%` | `50%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 481 | `49%` | `64%` ⭐ | `63%` ⭐ | `58%` | `49%` | `71%` ⭐ |
| ATR Creciente (>10%) | 74 | `47%` | `83%` ⭐ | `46%` | `57%` | `56%` | `61%` ⭐ |
| ATR Decreciente (<-10%) | 35 | `46%` | `69%` ⭐ | `75%` ⭐ | `75%` ⭐ | `58%` | `54%` |
| ATR Q1 (Baja Vol Historica) | 386 | `46%` | `66%` ⭐ | `59%` | `55%` | `45%` | `60%` |
| ATR Q4 (Alta Vol Historica) | 359 | `49%` | `65%` ⭐ | `56%` | `56%` | `50%` | `66%` ⭐ |
| RSI Diario < 35 | 185 | `45%` | `73%` ⭐ | `52%` | `59%` | `51%` | `69%` ⭐ |
| RSI Diario > 65 | 146 | `50%` | `66%` ⭐ | `67%` ⭐ | `54%` | `48%` | `63%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `221 min` | `150 min` | `375 min` |
| TP DOWN (desde entrada) | `219 min` | `150 min` | `390 min` |
| False Break UP → SL | `95 min` | - | - |
| False Break DOWN → SL | `92 min` | - | - |

---

## Permutación #6: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1973`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.23%`
- **Rotura Bajista (DOWN):** `47.69%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `73.16%` | `76.20%` |
| 1.5x Rango OR | `61.15%` | `62.91%` |
| 2.0x Rango OR | `50.66%` | `52.50%` |
| 1.0x Volatilidad ATR Diaria | `8.58%` | `10.10%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.94%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.22%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.94%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `53.83%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.27%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1558`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `37.03%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `27.92%` |
| Shakeout & Re-breakout UP (>=2x OR) | `20.92%` |
| Continuacion Bajista (>=1x OR) | `66.50%` |
| Extension media reversal UP | `1.17x OR` | Mediana: `0.43x` |
| Extension media continuacion DOWN | `2.05x OR` | Mediana: `1.59x` |
| Tiempo medio al re-breakout | `137 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1543`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `41.93%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `32.53%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `24.24%` |
| Continuacion Alcista (>=1x OR) | `63.97%` |
| Extension media reversal DOWN | `1.25x OR` | Mediana: `0.61x` |
| Extension media continuacion UP | `2.02x OR` | Mediana: `1.47x` |
| Tiempo medio al re-breakout | `135 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 118 | `21%` | `44%` | `72%` ⭐ | `48%` | `23%` | `31%` |
| RSI > 70 (Overbought) | 110 | `68%` ⭐ | `59%` | `55%` | `48%` | `32%` | `34%` |
| RSI 30-70 (Neutro) | 1745 | `51%` | `62%` ⭐ | `60%` ⭐ | `57%` | `38%` | `66%` ⭐ |
| OR ABOVE_PD_HIGH | 393 | `48%` | `61%` ⭐ | `62%` ⭐ | `53%` | `37%` | `50%` |
| OR BELOW_PD_LOW | 363 | `53%` | `55%` | `61%` ⭐ | `52%` | `32%` | `44%` |
| OR BETWEEN_CLOSE_AND_HIGH | 625 | `48%` | `65%` ⭐ | `58%` | `59%` | `40%` | `71%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 592 | `52%` | `61%` ⭐ | `60%` ⭐ | `58%` | `38%` | `71%` ⭐ |
| ATR Creciente (>10%) | 86 | `50%` | `79%` ⭐ | `47%` | `67%` ⭐ | `45%` | `60%` ⭐ |
| ATR Decreciente (<-10%) | 51 | `49%` | `68%` ⭐ | `56%` | `64%` ⭐ | `51%` | `51%` |
| ATR Q1 (Baja Vol Historica) | 502 | `47%` | `58%` | `59%` | `52%` | `37%` | `60%` |
| ATR Q4 (Alta Vol Historica) | 474 | `49%` | `64%` ⭐ | `61%` ⭐ | `58%` | `39%` | `66%` ⭐ |
| RSI Diario < 35 | 221 | `44%` | `64%` ⭐ | `55%` | `55%` | `37%` | `70%` ⭐ |
| RSI Diario > 65 | 180 | `49%` | `55%` | `70%` ⭐ | `60%` | `38%` | `66%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `268 min` | `255 min` | `420 min` |
| TP DOWN (desde entrada) | `248 min` | `225 min` | `390 min` |
| False Break UP → SL | `132 min` | - | - |
| False Break DOWN → SL | `135 min` | - | - |

---

## Permutación #7: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2072`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.71%`
- **Rotura Bajista (DOWN):** `49.08%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.06%` | `71.09%` |
| 1.5x Rango OR | `54.47%` | `56.64%` |
| 2.0x Rango OR | `43.11%` | `47.39%` |
| 1.0x Volatilidad ATR Diaria | `8.83%` | `10.42%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.54%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.10%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.25%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `54.05%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.67%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1609`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `29.65%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `20.57%` |
| Shakeout & Re-breakout UP (>=2x OR) | `14.92%` |
| Continuacion Bajista (>=1x OR) | `60.78%` |
| Extension media reversal UP | `0.88x OR` | Mediana: `0.21x` |
| Extension media continuacion DOWN | `1.77x OR` | Mediana: `1.33x` |
| Tiempo medio al re-breakout | `148 min` | Mediana: `112 min` |

**False Breakouts DOWN analizados:** `1557`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `34.04%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `24.08%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `17.66%` |
| Continuacion Alcista (>=1x OR) | `58.32%` |
| Extension media reversal DOWN | `0.97x OR` | Mediana: `0.33x` |
| Extension media continuacion UP | `1.72x OR` | Mediana: `1.28x` |
| Tiempo medio al re-breakout | `150 min` | Mediana: `120 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 115 | `14%` | `31%` | `88%` ⭐ | `52%` | `18%` | `25%` |
| RSI > 70 (Overbought) | 114 | `69%` ⭐ | `38%` | `57%` | `43%` | `25%` | `37%` |
| RSI 30-70 (Neutro) | 1843 | `51%` | `56%` | `58%` | `54%` | `31%` | `65%` ⭐ |
| OR ABOVE_PD_HIGH | 419 | `46%` | `56%` | `59%` | `50%` | `27%` | `51%` |
| OR BELOW_PD_LOW | 370 | `48%` | `45%` | `60%` ⭐ | `54%` | `25%` | `43%` |
| OR BETWEEN_CLOSE_AND_HIGH | 653 | `50%` | `58%` | `57%` | `54%` | `33%` | `70%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 630 | `53%` | `55%` | `59%` | `54%` | `31%` | `70%` ⭐ |
| ATR Creciente (>10%) | 87 | `52%` | `64%` ⭐ | `42%` | `62%` ⭐ | `36%` | `59%` |
| ATR Decreciente (<-10%) | 56 | `54%` | `57%` | `57%` | `62%` ⭐ | `38%` | `52%` |
| ATR Q1 (Baja Vol Historica) | 522 | `47%` | `56%` | `56%` | `50%` | `30%` | `59%` |
| ATR Q4 (Alta Vol Historica) | 510 | `50%` | `56%` | `61%` ⭐ | `54%` | `32%` | `65%` ⭐ |
| RSI Diario < 35 | 225 | `44%` | `62%` ⭐ | `52%` | `56%` | `31%` | `68%` ⭐ |
| RSI Diario > 65 | 189 | `46%` | `48%` | `68%` ⭐ | `56%` | `30%` | `66%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `283 min` | `270 min` | `420 min` |
| TP DOWN (desde entrada) | `267 min` | `255 min` | `420 min` |
| False Break UP → SL | `159 min` | - | - |
| False Break DOWN → SL | `167 min` | - | - |

---

## Permutación #8: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2101`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.98%`
- **Rotura Bajista (DOWN):** `49.88%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `64.63%` | `67.56%` |
| 1.5x Rango OR | `50.05%` | `52.19%` |
| 2.0x Rango OR | `35.76%` | `41.32%` |
| 1.0x Volatilidad ATR Diaria | `8.75%` | `9.54%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `56.37%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `51.62%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `60.26%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `53.21%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.15%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1603`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `24.70%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `16.41%` |
| Shakeout & Re-breakout UP (>=2x OR) | `11.17%` |
| Continuacion Bajista (>=1x OR) | `56.14%` |
| Extension media reversal UP | `0.71x OR` | Mediana: `0.05x` |
| Extension media continuacion DOWN | `1.54x OR` | Mediana: `1.14x` |
| Tiempo medio al re-breakout | `157 min` | Mediana: `135 min` |

**False Breakouts DOWN analizados:** `1536`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `27.34%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `18.42%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.11%` |
| Continuacion Alcista (>=1x OR) | `53.58%` |
| Extension media reversal DOWN | `0.74x OR` | Mediana: `0.13x` |
| Extension media continuacion UP | `1.48x OR` | Mediana: `1.08x` |
| Tiempo medio al re-breakout | `160 min` | Mediana: `135 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 103 | `16%` | `38%` | `62%` ⭐ | `53%` | `21%` | `31%` |
| RSI > 70 (Overbought) | 113 | `81%` ⭐ | `32%` | `56%` | `55%` | `14%` | `34%` |
| RSI 30-70 (Neutro) | 1885 | `49%` | `52%` | `56%` | `51%` | `25%` | `63%` ⭐ |
| OR ABOVE_PD_HIGH | 425 | `45%` | `51%` | `56%` | `50%` | `23%` | `50%` |
| OR BELOW_PD_LOW | 374 | `49%` | `41%` | `60%` ⭐ | `54%` | `18%` | `42%` |
| OR BETWEEN_CLOSE_AND_HIGH | 663 | `48%` | `54%` | `55%` | `54%` | `28%` | `68%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 639 | `52%` | `51%` | `56%` | `49%` | `27%` | `69%` ⭐ |
| ATR Creciente (>10%) | 87 | `56%` | `57%` | `45%` | `54%` | `28%` | `57%` |
| ATR Decreciente (<-10%) | 57 | `51%` | `41%` | `62%` ⭐ | `59%` | `34%` | `51%` |
| ATR Q1 (Baja Vol Historica) | 529 | `47%` | `51%` | `56%` | `49%` | `26%` | `57%` |
| ATR Q4 (Alta Vol Historica) | 518 | `48%` | `52%` | `56%` | `52%` | `25%` | `64%` ⭐ |
| RSI Diario < 35 | 228 | `48%` | `58%` | `51%` | `53%` | `27%` | `67%` ⭐ |
| RSI Diario > 65 | 189 | `48%` | `40%` | `67%` ⭐ | `53%` | `24%` | `64%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `297 min` | `285 min` | `435 min` |
| TP DOWN (desde entrada) | `285 min` | `270 min` | `420 min` |
| False Break UP → SL | `181 min` | - | - |
| False Break DOWN → SL | `195 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: AUDUSD

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] London (15m) | RSI Diario > 65**: Extension 1.5x DOWN sube a `80.60%` (base: `70.46%`, +10%pp). N=146.

- **[EDGE CONTEXT-BOOST DOWN] London (30m) | RSI > 70 (Overbought)**: Extension 1.5x DOWN sube a `74.19%` (base: `62.91%`, +11%pp). N=110.

- **[EDGE CONTEXT-BOOST UP] London (15m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `82.86%` (base: `68.00%`, +15%pp). N=74. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (30m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `79.07%` (base: `61.15%`, +18%pp). N=86. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `61.82%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `61.94%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `61.25%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `60.26%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `70.46%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `62.91%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `68.00%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `61.15%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 30m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=500 | UP: `47%` | Ext 1.5 UP: `69%` | Falsa Ruptura DW: `58%` | Reversión a PD_Close: `63%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=496 | UP: `50%` | Ext 1.5 UP: `55%` | Falsa Ruptura DW: `51%` | Reversión a PD_Close: `60%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=216 | UP: `51%` | Ext 1.5 UP: `57%` | Falsa Ruptura DW: `55%` | Reversión a PD_Close: `70%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1757 | UP: `50%` | Ext 1.5 UP: `62%` | Falsa Ruptura DW: `56%` | Reversión a PD_Close: `61%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*