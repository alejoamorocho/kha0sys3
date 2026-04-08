# 🌐 Matriz Probabilística Omnidireccional: BRENT

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
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `841`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.09%`
- **Rotura Bajista (DOWN):** `50.18%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `81.82%` | `81.28%` |
| 1.5x Rango OR | `72.22%` | `72.27%` |
| 2.0x Rango OR | `63.64%` | `66.35%` |
| 1.0x Volatilidad ATR Diaria | `10.61%` | `13.51%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.84%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `58.06%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `71.82%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.19%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.51%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `677`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `54.95%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `45.05%` |
| Shakeout & Re-breakout UP (>=2x OR) | `37.22%` |
| Continuacion Bajista (>=1x OR) | `74.00%` |
| Extension media reversal UP | `1.97x OR` | Mediana: `1.24x` |
| Extension media continuacion DOWN | `2.89x OR` | Mediana: `2.24x` |
| Tiempo medio al re-breakout | `120 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `663`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `51.43%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `44.80%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `37.25%` |
| Continuacion Alcista (>=1x OR) | `77.22%` |
| Extension media reversal DOWN | `1.93x OR` | Mediana: `1.14x` |
| Extension media continuacion UP | `2.82x OR` | Mediana: `2.20x` |
| Tiempo medio al re-breakout | `123 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 44 | `18%` | `88%` ⭐ | `50%` | `44%` | `55%` | `57%` |
| RSI > 70 (Overbought) | 49 | `73%` ⭐ | `75%` ⭐ | `58%` | `77%` ⭐ | `48%` | `51%` |
| RSI 30-70 (Neutro) | 748 | `47%` | `72%` ⭐ | `59%` | `59%` | `55%` | `74%` ⭐ |
| OR ABOVE_PD_HIGH | 121 | `40%` | `65%` ⭐ | `67%` ⭐ | `69%` ⭐ | `46%` | `60%` ⭐ |
| OR BELOW_PD_LOW | 115 | `49%` | `77%` ⭐ | `54%` | `55%` | `60%` | `54%` |
| OR BETWEEN_CLOSE_AND_HIGH | 300 | `48%` | `72%` ⭐ | `64%` ⭐ | `55%` | `54%` | `75%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 305 | `48%` | `73%` ⭐ | `53%` | `56%` | `58%` | `80%` ⭐ |
| ATR Creciente (>10%) | 39 | `49%` | `84%` ⭐ | `32%` | `47%` | `42%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 245 | `48%` | `73%` ⭐ | `58%` | `64%` ⭐ | `58%` | `73%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 180 | `49%` | `72%` ⭐ | `52%` | `60%` ⭐ | `51%` | `67%` ⭐ |
| RSI Diario < 35 | 74 | `49%` | `67%` ⭐ | `67%` ⭐ | `55%` | `55%` | `58%` |
| RSI Diario > 65 | 151 | `40%` | `70%` ⭐ | `65%` ⭐ | `59%` | `55%` | `72%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `201 min` | `135 min` | `360 min` |
| TP DOWN (desde entrada) | `191 min` | `105 min` | `360 min` |
| False Break UP → SL | `91 min` | - | - |
| False Break DOWN → SL | `82 min` | - | - |

---

## Permutación #2: London 30m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1382`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.06%`
- **Rotura Bajista (DOWN):** `49.20%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.09%` | `79.56%` |
| 1.5x Rango OR | `67.55%` | `65.74%` |
| 2.0x Rango OR | `59.73%` | `57.06%` |
| 1.0x Volatilidad ATR Diaria | `8.85%` | `12.06%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `58.55%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `61.03%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `73.73%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.89%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `44.36%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1093`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `49.86%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `37.97%` |
| Shakeout & Re-breakout UP (>=2x OR) | `30.19%` |
| Continuacion Bajista (>=1x OR) | `72.28%` |
| Extension media reversal UP | `1.54x OR` | Mediana: `0.99x` |
| Extension media continuacion DOWN | `2.54x OR` | Mediana: `1.87x` |
| Tiempo medio al re-breakout | `126 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1107`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `47.06%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `37.49%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `30.53%` |
| Continuacion Alcista (>=1x OR) | `73.53%` |
| Extension media reversal DOWN | `1.65x OR` | Mediana: `0.84x` |
| Extension media continuacion UP | `2.34x OR` | Mediana: `1.84x` |
| Tiempo medio al re-breakout | `124 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 67 | `19%` | `62%` ⭐ | `62%` ⭐ | `57%` | `49%` | `63%` ⭐ |
| RSI > 70 (Overbought) | 81 | `83%` ⭐ | `66%` ⭐ | `60%` | `77%` ⭐ | `45%` | `46%` |
| RSI 30-70 (Neutro) | 1234 | `48%` | `68%` ⭐ | `58%` | `61%` ⭐ | `50%` | `76%` ⭐ |
| OR ABOVE_PD_HIGH | 197 | `46%` | `64%` ⭐ | `66%` ⭐ | `63%` ⭐ | `46%` | `61%` ⭐ |
| OR BELOW_PD_LOW | 157 | `56%` | `66%` ⭐ | `60%` ⭐ | `51%` | `48%` | `55%` |
| OR BETWEEN_CLOSE_AND_HIGH | 521 | `46%` | `69%` ⭐ | `61%` ⭐ | `60%` ⭐ | `52%` | `77%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 507 | `51%` | `68%` ⭐ | `53%` | `63%` ⭐ | `50%` | `81%` ⭐ |
| ATR Creciente (>10%) | 44 | `55%` | `46%` | `67%` ⭐ | `58%` | `25%` | `64%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 373 | `49%` | `71%` ⭐ | `55%` | `64%` ⭐ | `55%` | `73%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 311 | `53%` | `64%` ⭐ | `58%` | `58%` | `43%` | `70%` ⭐ |
| RSI Diario < 35 | 110 | `48%` | `58%` | `68%` ⭐ | `67%` ⭐ | `47%` | `59%` |
| RSI Diario > 65 | 229 | `50%` | `65%` ⭐ | `64%` ⭐ | `62%` ⭐ | `46%` | `76%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `222 min` | `165 min` | `375 min` |
| TP DOWN (desde entrada) | `219 min` | `150 min` | `390 min` |
| False Break UP → SL | `106 min` | - | - |
| False Break DOWN → SL | `112 min` | - | - |

---

## Permutación #3: London 45m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1716`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.88%`
- **Rotura Bajista (DOWN):** `49.07%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `73.95%` | `72.33%` |
| 1.5x Rango OR | `60.63%` | `59.86%` |
| 2.0x Rango OR | `51.29%` | `51.07%` |
| 1.0x Volatilidad ATR Diaria | `7.24%` | `11.28%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `59.70%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `61.76%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `73.08%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `58.04%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.19%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1350`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `42.81%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `31.11%` |
| Shakeout & Re-breakout UP (>=2x OR) | `24.22%` |
| Continuacion Bajista (>=1x OR) | `65.85%` |
| Extension media reversal UP | `1.26x OR` | Mediana: `0.62x` |
| Extension media continuacion DOWN | `2.24x OR` | Mediana: `1.57x` |
| Tiempo medio al re-breakout | `135 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1374`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `40.61%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `31.80%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `25.11%` |
| Continuacion Alcista (>=1x OR) | `66.08%` |
| Extension media reversal DOWN | `1.37x OR` | Mediana: `0.52x` |
| Extension media continuacion UP | `2.00x OR` | Mediana: `1.52x` |
| Tiempo medio al re-breakout | `127 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 95 | `14%` | `77%` ⭐ | `38%` | `56%` | `43%` | `56%` |
| RSI > 70 (Overbought) | 109 | `85%` ⭐ | `54%` | `55%` | `67%` ⭐ | `38%` | `49%` |
| RSI 30-70 (Neutro) | 1512 | `50%` | `61%` ⭐ | `61%` ⭐ | `62%` ⭐ | `43%` | `76%` ⭐ |
| OR ABOVE_PD_HIGH | 236 | `47%` | `51%` | `67%` ⭐ | `63%` ⭐ | `46%` | `61%` ⭐ |
| OR BELOW_PD_LOW | 182 | `52%` | `62%` ⭐ | `62%` ⭐ | `53%` | `42%` | `56%` |
| OR BETWEEN_CLOSE_AND_HIGH | 672 | `49%` | `62%` ⭐ | `62%` ⭐ | `61%` ⭐ | `44%` | `77%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 626 | `51%` | `63%` ⭐ | `55%` | `65%` ⭐ | `41%` | `79%` ⭐ |
| ATR Creciente (>10%) | 46 | `52%` | `46%` | `54%` | `50%` | `20%` | `61%` ⭐ |
| ATR Decreciente (<-10%) | 20 | `35%` | `29%` | `71%` ⭐ | `62%` ⭐ | `33%` | `80%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 445 | `51%` | `66%` ⭐ | `57%` | `63%` ⭐ | `47%` | `72%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 408 | `51%` | `53%` | `59%` | `58%` | `37%` | `70%` ⭐ |
| RSI Diario < 35 | 135 | `47%` | `60%` ⭐ | `57%` | `56%` | `40%` | `59%` |
| RSI Diario > 65 | 270 | `52%` | `59%` | `65%` ⭐ | `65%` ⭐ | `39%` | `75%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `237 min` | `210 min` | `390 min` |
| TP DOWN (desde entrada) | `221 min` | `165 min` | `375 min` |
| False Break UP → SL | `123 min` | - | - |
| False Break DOWN → SL | `127 min` | - | - |

---

## Permutación #4: London 60m
**Configuración:** Inicia a las `07:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1900`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `48.79%`
- **Rotura Bajista (DOWN):** `48.89%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `72.06%` | `69.11%` |
| 1.5x Rango OR | `57.82%` | `57.70%` |
| 2.0x Rango OR | `47.36%` | `49.09%` |
| 1.0x Volatilidad ATR Diaria | `7.01%` | `11.73%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `56.31%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.20%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `72.84%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `57.68%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.08%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1456`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `36.81%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `26.72%` |
| Shakeout & Re-breakout UP (>=2x OR) | `19.71%` |
| Continuacion Bajista (>=1x OR) | `61.40%` |
| Extension media reversal UP | `1.02x OR` | Mediana: `0.42x` |
| Extension media continuacion DOWN | `2.01x OR` | Mediana: `1.40x` |
| Tiempo medio al re-breakout | `142 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1488`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `34.81%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `26.34%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `20.36%` |
| Continuacion Alcista (>=1x OR) | `61.76%` |
| Extension media reversal DOWN | `1.10x OR` | Mediana: `0.33x` |
| Extension media continuacion UP | `1.78x OR` | Mediana: `1.38x` |
| Tiempo medio al re-breakout | `137 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 101 | `14%` | `64%` ⭐ | `50%` | `53%` | `24%` | `54%` |
| RSI > 70 (Overbought) | 117 | `85%` ⭐ | `52%` | `52%` | `65%` ⭐ | `26%` | `49%` |
| RSI 30-70 (Neutro) | 1682 | `48%` | `58%` | `57%` | `60%` | `38%` | `76%` ⭐ |
| OR ABOVE_PD_HIGH | 258 | `47%` | `52%` | `62%` ⭐ | `55%` | `37%` | `60%` ⭐ |
| OR BELOW_PD_LOW | 194 | `51%` | `59%` | `54%` | `49%` | `36%` | `55%` |
| OR BETWEEN_CLOSE_AND_HIGH | 763 | `47%` | `57%` | `58%` | `61%` ⭐ | `38%` | `77%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 685 | `51%` | `60%` | `53%` | `61%` ⭐ | `36%` | `79%` ⭐ |
| ATR Creciente (>10%) | 45 | `53%` | `46%` | `50%` | `40%` | `16%` | `60%` ⭐ |
| ATR Decreciente (<-10%) | 24 | `38%` | `44%` | `56%` | `67%` ⭐ | `30%` | `75%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 481 | `52%` | `61%` ⭐ | `53%` | `63%` ⭐ | `40%` | `72%` ⭐ |
| ATR Q4 (Alta Vol Historica) | 463 | `48%` | `53%` | `58%` | `55%` | `32%` | `71%` ⭐ |
| RSI Diario < 35 | 151 | `43%` | `58%` | `57%` | `51%` | `38%` | `63%` ⭐ |
| RSI Diario > 65 | 287 | `49%` | `56%` | `59%` | `61%` ⭐ | `34%` | `75%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `243 min` | `218 min` | `390 min` |
| TP DOWN (desde entrada) | `227 min` | `180 min` | `390 min` |
| False Break UP → SL | `148 min` | - | - |
| False Break DOWN → SL | `147 min` | - | - |

---

## Permutación #5: NY 15m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1688`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `47.22%`
- **Rotura Bajista (DOWN):** `48.46%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.38%` | `69.32%` |
| 1.5x Rango OR | `53.83%` | `55.50%` |
| 2.0x Rango OR | `41.28%` | `43.28%` |
| 1.0x Volatilidad ATR Diaria | `4.27%` | `6.97%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.08%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.23%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `52.31%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `44.25%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `38.48%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1327`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `40.69%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `32.25%` |
| Shakeout & Re-breakout UP (>=2x OR) | `24.94%` |
| Continuacion Bajista (>=1x OR) | `67.22%` |
| Extension media reversal UP | `1.30x OR` | Mediana: `0.62x` |
| Extension media continuacion DOWN | `2.29x OR` | Mediana: `1.63x` |
| Tiempo medio al re-breakout | `76 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1326`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `41.48%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `32.58%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `25.34%` |
| Continuacion Alcista (>=1x OR) | `65.61%` |
| Extension media reversal DOWN | `1.37x OR` | Mediana: `0.54x` |
| Extension media continuacion UP | `2.08x OR` | Mediana: `1.58x` |
| Tiempo medio al re-breakout | `80 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 128 | `25%` | `53%` | `44%` | `44%` | `34%` | `27%` |
| RSI > 70 (Overbought) | 115 | `70%` ⭐ | `46%` | `60%` ⭐ | `53%` | `30%` | `17%` |
| RSI 30-70 (Neutro) | 1445 | `47%` | `55%` | `55%` | `58%` | `42%` | `57%` |
| OR ABOVE_PD_HIGH | 369 | `45%` | `54%` | `57%` | `56%` | `36%` | `40%` |
| OR BELOW_PD_LOW | 292 | `48%` | `55%` | `50%` | `59%` | `43%` | `35%` |
| OR BETWEEN_CLOSE_AND_HIGH | 526 | `47%` | `56%` | `57%` | `60%` ⭐ | `44%` | `63%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 501 | `49%` | `51%` | `55%` | `51%` | `39%` | `60%` ⭐ |
| ATR Creciente (>10%) | 42 | `33%` | `43%` | `57%` | `52%` | `39%` | `55%` |
| ATR Q1 (Baja Vol Historica) | 429 | `48%` | `60%` ⭐ | `53%` | `54%` | `44%` | `51%` |
| ATR Q4 (Alta Vol Historica) | 382 | `45%` | `49%` | `57%` | `52%` | `36%` | `49%` |
| RSI Diario < 35 | 128 | `50%` | `50%` | `56%` | `59%` | `47%` | `48%` |
| RSI Diario > 65 | 250 | `48%` | `64%` ⭐ | `53%` | `50%` | `43%` | `59%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `113 min` | `75 min` | `180 min` |
| TP DOWN (desde entrada) | `103 min` | `75 min` | `165 min` |
| False Break UP → SL | `64 min` | - | - |
| False Break DOWN → SL | `64 min` | - | - |

---

## Permutación #6: NY 30m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1953`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.00%`
- **Rotura Bajista (DOWN):** `47.00%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `61.13%` | `62.64%` |
| 1.5x Rango OR | `45.77%` | `48.58%` |
| 2.0x Rango OR | `34.80%` | `38.24%` |
| 1.0x Volatilidad ATR Diaria | `3.34%` | `7.19%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `51.20%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `51.42%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `51.82%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `43.78%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `38.33%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1482`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `30.30%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `22.67%` |
| Shakeout & Re-breakout UP (>=2x OR) | `16.60%` |
| Continuacion Bajista (>=1x OR) | `59.45%` |
| Extension media reversal UP | `0.92x OR` | Mediana: `0.26x` |
| Extension media continuacion DOWN | `1.91x OR` | Mediana: `1.33x` |
| Tiempo medio al re-breakout | `81 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `1504`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `32.65%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `24.14%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `18.62%` |
| Continuacion Alcista (>=1x OR) | `57.71%` |
| Extension media reversal DOWN | `1.04x OR` | Mediana: `0.27x` |
| Extension media continuacion UP | `1.72x OR` | Mediana: `1.26x` |
| Tiempo medio al re-breakout | `85 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 115 | `23%` | `54%` | `35%` | `42%` | `22%` | `30%` |
| RSI > 70 (Overbought) | 125 | `77%` ⭐ | `34%` | `55%` | `50%` | `22%` | `23%` |
| RSI 30-70 (Neutro) | 1713 | `49%` | `47%` | `51%` | `52%` | `31%` | `55%` |
| OR ABOVE_PD_HIGH | 425 | `49%` | `43%` | `57%` | `51%` | `29%` | `39%` |
| OR BELOW_PD_LOW | 318 | `51%` | `47%` | `46%` | `50%` | `31%` | `36%` |
| OR BETWEEN_CLOSE_AND_HIGH | 614 | `49%` | `45%` | `54%` | `55%` | `32%` | `61%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 596 | `48%` | `48%` | `47%` | `49%` | `30%` | `60%` ⭐ |
| ATR Creciente (>10%) | 46 | `39%` | `28%` | `72%` ⭐ | `43%` | `22%` | `50%` |
| ATR Decreciente (<-10%) | 22 | `59%` | `38%` | `46%` | `33%` | `7%` | `59%` |
| ATR Q1 (Baja Vol Historica) | 497 | `49%` | `51%` | `51%` | `49%` | `34%` | `52%` |
| ATR Q4 (Alta Vol Historica) | 462 | `48%` | `44%` | `54%` | `47%` | `27%` | `49%` |
| RSI Diario < 35 | 154 | `50%` | `44%` | `53%` | `54%` | `35%` | `47%` |
| RSI Diario > 65 | 282 | `50%` | `53%` | `49%` | `57%` | `30%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `112 min` | `90 min` | `180 min` |
| TP DOWN (desde entrada) | `103 min` | `75 min` | `165 min` |
| False Break UP → SL | `79 min` | - | - |
| False Break DOWN → SL | `76 min` | - | - |

---

## Permutación #7: NY 45m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2052`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.19%`
- **Rotura Bajista (DOWN):** `46.93%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `51.46%` | `54.41%` |
| 1.5x Rango OR | `34.85%` | `37.38%` |
| 2.0x Rango OR | `25.05%` | `27.41%` |
| 1.0x Volatilidad ATR Diaria | `3.20%` | `5.82%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `47.28%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `45.38%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `50.34%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `42.15%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `36.72%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1501`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `22.72%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `14.99%` |
| Shakeout & Re-breakout UP (>=2x OR) | `10.13%` |
| Continuacion Bajista (>=1x OR) | `52.56%` |
| Extension media reversal UP | `0.64x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.53x OR` | Mediana: `1.07x` |
| Tiempo medio al re-breakout | `92 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1518`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `25.36%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `16.80%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `11.99%` |
| Continuacion Alcista (>=1x OR) | `49.14%` |
| Extension media reversal DOWN | `0.74x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.36x OR` | Mediana: `0.97x` |
| Tiempo medio al re-breakout | `94 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 132 | `19%` | `28%` | `24%` | `31%` | `7%` | `25%` |
| RSI > 70 (Overbought) | 143 | `77%` ⭐ | `21%` | `46%` | `27%` | `16%` | `26%` |
| RSI 30-70 (Neutro) | 1777 | `50%` | `37%` | `48%` | `48%` | `24%` | `54%` |
| OR ABOVE_PD_HIGH | 451 | `49%` | `30%` | `54%` | `46%` | `22%` | `38%` |
| OR BELOW_PD_LOW | 327 | `52%` | `34%` | `47%` | `47%` | `21%` | `35%` |
| OR BETWEEN_CLOSE_AND_HIGH | 642 | `51%` | `36%` | `46%` | `45%` | `24%` | `57%` |
| OR BETWEEN_LOW_AND_CLOSE | 632 | `50%` | `37%` | `43%` | `45%` | `23%` | `60%` |
| ATR Creciente (>10%) | 44 | `45%` | `20%` | `70%` ⭐ | `52%` | `13%` | `48%` |
| ATR Decreciente (<-10%) | 25 | `40%` | `30%` | `30%` | `36%` | `6%` | `60%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 515 | `50%` | `38%` | `49%` | `43%` | `27%` | `50%` |
| ATR Q4 (Alta Vol Historica) | 502 | `48%` | `32%` | `52%` | `43%` | `22%` | `49%` |
| RSI Diario < 35 | 164 | `51%` | `31%` | `55%` | `49%` | `26%` | `48%` |
| RSI Diario > 65 | 294 | `51%` | `37%` | `46%` | `51%` | `21%` | `56%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `121 min` | `90 min` | `195 min` |
| TP DOWN (desde entrada) | `106 min` | `75 min` | `165 min` |
| False Break UP → SL | `90 min` | - | - |
| False Break DOWN → SL | `87 min` | - | - |

---

## Permutación #8: NY 60m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2065`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.20%`
- **Rotura Bajista (DOWN):** `47.02%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `44.00%` | `46.24%` |
| 1.5x Rango OR | `28.74%` | `31.31%` |
| 2.0x Rango OR | `18.50%` | `21.63%` |
| 1.0x Volatilidad ATR Diaria | `2.66%` | `5.15%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `40.94%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `40.47%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `49.30%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `41.40%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `35.91%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1448`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `18.37%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `11.40%` |
| Shakeout & Re-breakout UP (>=2x OR) | `7.80%` |
| Continuacion Bajista (>=1x OR) | `45.93%` |
| Extension media reversal UP | `0.49x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.29x OR` | Mediana: `0.91x` |
| Tiempo medio al re-breakout | `97 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1470`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `19.80%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `12.18%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `8.03%` |
| Continuacion Alcista (>=1x OR) | `42.65%` |
| Extension media reversal DOWN | `0.54x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.15x OR` | Mediana: `0.81x` |
| Tiempo medio al re-breakout | `97 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 132 | `12%` | `12%` | `19%` | `28%` | `7%` | `25%` |
| RSI > 70 (Overbought) | 132 | `81%` ⭐ | `15%` | `36%` | `36%` | `11%` | `17%` |
| RSI 30-70 (Neutro) | 1801 | `50%` | `31%` | `42%` | `42%` | `20%` | `53%` |
| OR ABOVE_PD_HIGH | 453 | `49%` | `22%` | `49%` | `38%` | `18%` | `38%` |
| OR BELOW_PD_LOW | 329 | `51%` | `32%` | `41%` | `41%` | `16%` | `35%` |
| OR BETWEEN_CLOSE_AND_HIGH | 650 | `48%` | `32%` | `38%` | `43%` | `20%` | `56%` |
| OR BETWEEN_LOW_AND_CLOSE | 633 | `49%` | `29%` | `38%` | `40%` | `19%` | `58%` |
| ATR Creciente (>10%) | 43 | `47%` | `20%` | `55%` | `43%` | `9%` | `49%` |
| ATR Decreciente (<-10%) | 25 | `44%` | `27%` | `36%` | `31%` | `0%` | `60%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 517 | `49%` | `31%` | `41%` | `39%` | `24%` | `49%` |
| ATR Q4 (Alta Vol Historica) | 510 | `44%` | `28%` | `40%` | `39%` | `16%` | `48%` |
| RSI Diario < 35 | 168 | `43%` | `28%` | `42%` | `48%` | `23%` | `46%` |
| RSI Diario > 65 | 294 | `49%` | `31%` | `44%` | `45%` | `19%` | `55%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `128 min` | `105 min` | `210 min` |
| TP DOWN (desde entrada) | `112 min` | `90 min` | `165 min` |
| False Break UP → SL | `95 min` | - | - |
| False Break DOWN → SL | `97 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: BRENT

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] London (30m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `78.95%` (base: `65.74%`, +13%pp). N=44.

- **[EDGE CONTEXT-BOOST DOWN] London (30m) | RSI > 70 (Overbought)**: Extension 1.5x DOWN sube a `84.62%` (base: `65.74%`, +19%pp). N=81.

- **[EDGE CONTEXT-BOOST DOWN] London (45m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `80.00%` (base: `59.86%`, +20%pp). N=46.

- **[EDGE CONTEXT-BOOST DOWN] NY (15m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `70.37%` (base: `55.50%`, +15%pp). N=42.

- **[EDGE CONTEXT-BOOST DOWN] NY (30m) | ATR Decreciente (<-10%)**: Extension 1.5x DOWN sube a `66.67%` (base: `48.58%`, +18%pp). N=22.

- **[EDGE CONTEXT-BOOST UP] London (15m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `84.21%` (base: `72.22%`, +12%pp). N=39. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (15m) | RSI < 30 (Oversold)**: Extension 1.5x UP sube a `87.50%` (base: `72.22%`, +15%pp). N=44. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] London (45m) | RSI < 30 (Oversold)**: Extension 1.5x UP sube a `76.92%` (base: `60.63%`, +16%pp). N=95. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE FADE-BREAKOUT] London (30m)**: Trampa de Liquidez Bajista del `61.03%`. Sugerencia Algo: Colocar orden de compra ciega si el activo cruza brevemente el piso y titubea.

- **[EDGE FADE-BREAKOUT] London (45m)**: Trampa de Liquidez Bajista del `61.76%`. Sugerencia Algo: Colocar orden de compra ciega si el activo cruza brevemente el piso y titubea.

- **[EDGE MAGNET PD_CLOSE] London (15m)**: Imantación cíclica brutal. El `71.82%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (30m)**: Imantación cíclica brutal. El `73.73%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (45m)**: Imantación cíclica brutal. El `73.08%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] London (60m)**: Imantación cíclica brutal. El `72.84%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE TENDENCIAL DOWN] London (15m)**: Tasa de extensión polar bajista (1.5x) del `72.27%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] London (30m)**: Tasa de extensión polar bajista (1.5x) del `65.74%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] London (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `72.22%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `67.55%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] London (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.63%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`London 45m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=431 | UP: `48%` | Ext 1.5 UP: `72%` | Falsa Ruptura DW: `63%` | Reversión a PD_Close: `71%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=431 | UP: `52%` | Ext 1.5 UP: `44%` | Falsa Ruptura DW: `60%` | Reversión a PD_Close: `70%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=174 | UP: `49%` | Ext 1.5 UP: `71%` | Falsa Ruptura DW: `63%` | Reversión a PD_Close: `72%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1542 | UP: `50%` | Ext 1.5 UP: `59%` | Falsa Ruptura DW: `62%` | Reversión a PD_Close: `73%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*