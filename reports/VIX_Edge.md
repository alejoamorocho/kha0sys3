# 🌐 Matriz Probabilística Omnidireccional: VIX

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **NY Cash 15m**](#permutación-1-ny-cash-15m)
- [Permutación #2: **NY Cash 30m**](#permutación-2-ny-cash-30m)
- [Permutación #3: **NY Cash 45m**](#permutación-3-ny-cash-45m)
- [Permutación #4: **NY Cash 60m**](#permutación-4-ny-cash-60m)

---
## Permutación #1: NY Cash 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `532`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `44.74%`
- **Rotura Bajista (DOWN):** `41.73%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `71.85%` | `63.96%` |
| 1.5x Rango OR | `59.24%` | `48.65%` |
| 2.0x Rango OR | `48.74%` | `38.29%` |
| 1.0x Volatilidad ATR Diaria | `21.85%` | `6.76%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.20%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `51.35%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `59.59%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `50.38%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.73%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `420`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `39.05%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `30.00%` |
| Shakeout & Re-breakout UP (>=2x OR) | `24.52%` |
| Continuacion Bajista (>=1x OR) | `61.19%` |
| Extension media reversal UP | `1.71x OR` | Mediana: `0.33x` |
| Extension media continuacion DOWN | `1.98x OR` | Mediana: `1.43x` |
| Tiempo medio al re-breakout | `84 min` | Mediana: `45 min` |

**False Breakouts DOWN analizados:** `419`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `41.53%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `31.26%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `24.34%` |
| Continuacion Alcista (>=1x OR) | `63.48%` |
| Extension media reversal DOWN | `1.33x OR` | Mediana: `0.79x` |
| Extension media continuacion UP | `2.80x OR` | Mediana: `1.56x` |
| Tiempo medio al re-breakout | `91 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 54 | `20%` | `64%` ⭐ | `55%` | `49%` | `35%` | `41%` |
| RSI > 70 (Overbought) | 34 | `74%` ⭐ | `68%` ⭐ | `36%` | `67%` ⭐ | `29%` | `29%` |
| RSI 30-70 (Neutro) | 444 | `45%` | `58%` | `56%` | `51%` | `40%` | `64%` ⭐ |
| OR ABOVE_PD_HIGH | 82 | `49%` | `75%` ⭐ | `48%` | `50%` | `40%` | `48%` |
| OR BELOW_PD_LOW | 114 | `45%` | `49%` | `59%` | `51%` | `37%` | `54%` |
| OR BETWEEN_CLOSE_AND_HIGH | 161 | `45%` | `54%` | `53%` | `46%` | `34%` | `64%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 175 | `43%` | `63%` ⭐ | `56%` | `57%` | `44%` | `65%` ⭐ |
| ATR Creciente (>10%) | 68 | `38%` | `77%` ⭐ | `42%` | `52%` | `51%` | `68%` ⭐ |
| ATR Decreciente (<-10%) | 37 | `35%` | `62%` ⭐ | `31%` | `50%` | `29%` | `70%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 107 | `48%` | `59%` | `43%` | `51%` | `38%` | `51%` |
| ATR Q4 (Alta Vol Historica) | 129 | `47%` | `53%` | `60%` ⭐ | `53%` | `38%` | `62%` ⭐ |
| RSI Diario < 35 | 37 | `32%` | `67%` ⭐ | `50%` | `50%` | `48%` | `59%` |
| RSI Diario > 65 | 39 | `36%` | `50%` | `71%` ⭐ | `54%` | `43%` | `62%` ⭐ |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `101 min` | `60 min` | `180 min` |
| TP DOWN (desde entrada) | `127 min` | `75 min` | `240 min` |
| False Break UP → SL | `64 min` | - | - |
| False Break DOWN → SL | `78 min` | - | - |

---

## Permutación #2: NY Cash 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `639`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `43.97%`
- **Rotura Bajista (DOWN):** `49.77%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `64.06%` | `55.66%` |
| 1.5x Rango OR | `50.89%` | `39.94%` |
| 2.0x Rango OR | `39.86%` | `27.99%` |
| 1.0x Volatilidad ATR Diaria | `20.64%` | `6.29%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.52%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `50.63%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `59.78%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `47.73%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `41.78%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `511`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `31.51%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `25.64%` |
| Shakeout & Re-breakout UP (>=2x OR) | `20.94%` |
| Continuacion Bajista (>=1x OR) | `51.08%` |
| Extension media reversal UP | `1.41x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.56x OR` | Mediana: `1.00x` |
| Tiempo medio al re-breakout | `94 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `473`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `30.23%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `21.78%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `16.07%` |
| Continuacion Alcista (>=1x OR) | `56.66%` |
| Extension media reversal DOWN | `0.95x OR` | Mediana: `0.44x` |
| Extension media continuacion UP | `2.32x OR` | Mediana: `1.29x` |
| Tiempo medio al re-breakout | `104 min` | Mediana: `60 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 58 | `14%` | `38%` | `62%` ⭐ | `46%` | `30%` | `31%` |
| RSI > 70 (Overbought) | 36 | `72%` ⭐ | `54%` | `54%` | `38%` | `30%` | `42%` |
| RSI 30-70 (Neutro) | 545 | `45%` | `51%` | `55%` | `52%` | `32%` | `64%` ⭐ |
| OR ABOVE_PD_HIGH | 90 | `49%` | `68%` ⭐ | `55%` | `45%` | `37%` | `52%` |
| OR BELOW_PD_LOW | 149 | `40%` | `40%` | `53%` | `53%` | `32%` | `52%` |
| OR BETWEEN_CLOSE_AND_HIGH | 187 | `44%` | `51%` | `54%` | `44%` | `22%` | `66%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 213 | `45%` | `49%` | `59%` | `58%` | `36%` | `63%` ⭐ |
| ATR Creciente (>10%) | 73 | `51%` | `62%` ⭐ | `59%` | `63%` ⭐ | `47%` | `63%` ⭐ |
| ATR Decreciente (<-10%) | 56 | `38%` | `57%` | `33%` | `55%` | `29%` | `71%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 144 | `44%` | `56%` | `48%` | `57%` | `37%` | `53%` |
| ATR Q4 (Alta Vol Historica) | 154 | `48%` | `45%` | `62%` ⭐ | `51%` | `26%` | `63%` ⭐ |
| RSI Diario < 35 | 54 | `35%` | `58%` | `63%` ⭐ | `54%` | `36%` | `63%` ⭐ |
| RSI Diario > 65 | 37 | `59%` | `59%` | `73%` ⭐ | `33%` | `39%` | `54%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `115 min` | `60 min` | `210 min` |
| TP DOWN (desde entrada) | `140 min` | `90 min` | `270 min` |
| False Break UP → SL | `89 min` | - | - |
| False Break DOWN → SL | `104 min` | - | - |

---

## Permutación #3: NY Cash 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `669`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `43.80%`
- **Rotura Bajista (DOWN):** `51.42%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `56.31%` | `43.90%` |
| 1.5x Rango OR | `43.69%` | `28.20%` |
| 2.0x Rango OR | `33.79%` | `18.90%` |
| 1.0x Volatilidad ATR Diaria | `21.16%` | `4.07%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `52.22%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `45.64%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `57.85%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `45.59%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `40.28%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `524`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `25.19%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `19.85%` |
| Shakeout & Re-breakout UP (>=2x OR) | `15.65%` |
| Continuacion Bajista (>=1x OR) | `41.03%` |
| Extension media reversal UP | `1.14x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.27x OR` | Mediana: `0.80x` |
| Tiempo medio al re-breakout | `103 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `467`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `23.98%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `15.85%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.21%` |
| Continuacion Alcista (>=1x OR) | `52.03%` |
| Extension media reversal DOWN | `0.77x OR` | Mediana: `0.17x` |
| Extension media continuacion UP | `2.07x OR` | Mediana: `1.13x` |
| Tiempo medio al re-breakout | `109 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 72 | `4%` | `33%` | `0%` | `43%` | `13%` | `25%` |
| RSI > 70 (Overbought) | 36 | `81%` ⭐ | `34%` | `45%` | `80%` ⭐ | `25%` | `36%` |
| RSI 30-70 (Neutro) | 561 | `47%` | `45%` | `54%` | `46%` | `27%` | `63%` ⭐ |
| OR ABOVE_PD_HIGH | 93 | `44%` | `51%` | `56%` | `43%` | `28%` | `51%` |
| OR BELOW_PD_LOW | 159 | `41%` | `42%` | `43%` | `43%` | `19%` | `48%` |
| OR BETWEEN_CLOSE_AND_HIGH | 193 | `45%` | `40%` | `57%` | `41%` | `25%` | `67%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 224 | `45%` | `46%` | `52%` | `53%` | `28%` | `60%` |
| ATR Creciente (>10%) | 73 | `55%` | `52%` | `57%` | `62%` ⭐ | `36%` | `63%` ⭐ |
| ATR Decreciente (<-10%) | 66 | `44%` | `38%` | `41%` | `41%` | `24%` | `67%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 157 | `45%` | `46%` | `46%` | `51%` | `28%` | `50%` |
| ATR Q4 (Alta Vol Historica) | 164 | `51%` | `39%` | `58%` | `48%` | `23%` | `62%` ⭐ |
| RSI Diario < 35 | 57 | `37%` | `48%` | `57%` | `34%` | `29%` | `58%` |
| RSI Diario > 65 | 36 | `58%` | `43%` | `71%` ⭐ | `29%` | `30%` | `53%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `120 min` | `60 min` | `225 min` |
| TP DOWN (desde entrada) | `144 min` | `90 min` | `285 min` |
| False Break UP → SL | `95 min` | - | - |
| False Break DOWN → SL | `121 min` | - | - |

---

## Permutación #4: NY Cash 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `698`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `40.69%`
- **Rotura Bajista (DOWN):** `51.00%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `56.69%` | `43.26%` |
| 1.5x Rango OR | `42.96%` | `28.37%` |
| 2.0x Rango OR | `34.51%` | `19.94%` |
| 1.0x Volatilidad ATR Diaria | `20.77%` | `4.78%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `44.37%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `37.64%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `57.59%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `45.27%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `39.61%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `528`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `22.92%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `16.48%` |
| Shakeout & Re-breakout UP (>=2x OR) | `12.88%` |
| Continuacion Bajista (>=1x OR) | `38.83%` |
| Extension media reversal UP | `0.93x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.20x OR` | Mediana: `0.74x` |
| Tiempo medio al re-breakout | `108 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `456`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `19.96%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `12.94%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `10.31%` |
| Continuacion Alcista (>=1x OR) | `50.00%` |
| Extension media reversal DOWN | `0.63x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.96x OR` | Mediana: `1.00x` |
| Tiempo medio al re-breakout | `113 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 79 | `15%` | `25%` | `33%` | `30%` | `11%` | `24%` |
| RSI > 70 (Overbought) | 34 | `68%` ⭐ | `43%` | `43%` | `67%` ⭐ | `50%` | `44%` |
| RSI 30-70 (Neutro) | 585 | `43%` | `44%` | `45%` | `39%` | `24%` | `63%` ⭐ |
| OR ABOVE_PD_HIGH | 94 | `37%` | `46%` | `49%` | `33%` | `23%` | `51%` |
| OR BELOW_PD_LOW | 170 | `43%` | `41%` | `33%` | `39%` | `13%` | `48%` |
| OR BETWEEN_CLOSE_AND_HIGH | 207 | `37%` | `46%` | `46%` | `35%` | `24%` | `67%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 227 | `44%` | `41%` | `50%` | `42%` | `28%` | `59%` |
| ATR Creciente (>10%) | 73 | `47%` | `53%` | `53%` | `53%` | `34%` | `66%` ⭐ |
| ATR Decreciente (<-10%) | 72 | `40%` | `45%` | `28%` | `30%` | `20%` | `68%` ⭐ |
| ATR Q1 (Baja Vol Historica) | 163 | `45%` | `43%` | `42%` | `43%` | `23%` | `50%` |
| ATR Q4 (Alta Vol Historica) | 177 | `42%` | `40%` | `45%` | `40%` | `22%` | `59%` |
| RSI Diario < 35 | 62 | `40%` | `40%` | `52%` | `25%` | `24%` | `58%` |
| RSI Diario > 65 | 35 | `51%` | `50%` | `72%` ⭐ | `29%` | `30%` | `51%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `129 min` | `90 min` | `240 min` |
| TP DOWN (desde entrada) | `152 min` | `120 min` | `300 min` |
| False Break UP → SL | `123 min` | - | - |
| False Break DOWN → SL | `141 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: VIX

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE CONTEXT-BOOST DOWN] NY Cash (15m) | ATR Creciente (>10%)**: Extension 1.5x DOWN sube a `62.96%` (base: `48.65%`, +14%pp). N=68.

- **[EDGE CONTEXT-BOOST DOWN] NY Cash (15m) | RSI Diario > 65**: Extension 1.5x DOWN sube a `69.23%` (base: `48.65%`, +21%pp). N=39.

- **[EDGE CONTEXT-BOOST UP] NY Cash (15m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `76.92%` (base: `59.24%`, +18%pp). N=68. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] NY Cash (15m) | OR ABOVE_PD_HIGH**: Extension 1.5x UP sube a `75.00%` (base: `59.24%`, +16%pp). N=82. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] NY Cash (30m) | ATR Creciente (>10%)**: Extension 1.5x UP sube a `62.16%` (base: `50.89%`, +11%pp). N=73. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

- **[EDGE CONTEXT-BOOST UP] NY Cash (30m) | OR ABOVE_PD_HIGH**: Extension 1.5x UP sube a `68.18%` (base: `50.89%`, +17%pp). N=90. Sugerencia: Filtrar entradas UP cuando se cumple esta condicion.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`NY Cash 30m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=168 | UP: `40%` | Ext 1.5 UP: `57%` | Falsa Ruptura DW: `60%` | Reversión a PD_Close: `65%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=179 | UP: `44%` | Ext 1.5 UP: `42%` | Falsa Ruptura DW: `43%` | Reversión a PD_Close: `55%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=106 | UP: `44%` | Ext 1.5 UP: `43%` | Falsa Ruptura DW: `31%` | Reversión a PD_Close: `53%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=533 | UP: `44%` | Ext 1.5 UP: `53%` | Falsa Ruptura DW: `54%` | Reversión a PD_Close: `61%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*