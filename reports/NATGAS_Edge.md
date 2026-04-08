# 🌐 Matriz Probabilística Omnidireccional: NATGAS

Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.

## Índice de Permutaciones

- [Permutación #1: **NY 15m**](#permutación-1-ny-15m)
- [Permutación #2: **NY 30m**](#permutación-2-ny-30m)
- [Permutación #3: **NY 45m**](#permutación-3-ny-45m)
- [Permutación #4: **NY 60m**](#permutación-4-ny-60m)

---
## Permutación #1: NY 15m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1937`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.52%`
- **Rotura Bajista (DOWN):** `47.96%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `66.70%` | `65.02%` |
| 1.5x Rango OR | `52.39%` | `53.07%` |
| 2.0x Rango OR | `40.62%` | `41.77%` |
| 1.0x Volatilidad ATR Diaria | `10.10%` | `7.00%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `47.84%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `48.12%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `53.48%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `46.15%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `37.51%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1458`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `31.96%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `24.69%` |
| Shakeout & Re-breakout UP (>=2x OR) | `18.66%` |
| Continuacion Bajista (>=1x OR) | `63.03%` |
| Extension media reversal UP | `1.01x OR` | Mediana: `0.20x` |
| Extension media continuacion DOWN | `1.98x OR` | Mediana: `1.52x` |
| Tiempo medio al re-breakout | `90 min` | Mediana: `60 min` |

**False Breakouts DOWN analizados:** `1449`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `35.75%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `28.09%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `21.05%` |
| Continuacion Alcista (>=1x OR) | `60.66%` |
| Extension media reversal DOWN | `1.09x OR` | Mediana: `0.30x` |
| Extension media continuacion UP | `1.94x OR` | Mediana: `1.40x` |
| Tiempo medio al re-breakout | `84 min` | Mediana: `45 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 203 | `28%` | `44%` | `49%` | `41%` | `23%` | `25%` |
| RSI > 70 (Overbought) | 234 | `63%` ⭐ | `48%` | `43%` | `49%` | `31%` | `28%` |
| RSI 30-70 (Neutro) | 1500 | `46%` | `54%` | `49%` | `49%` | `33%` | `61%` ⭐ |
| OR ABOVE_PD_HIGH | 427 | `47%` | `54%` | `44%` | `48%` | `29%` | `41%` |
| OR BELOW_PD_LOW | 403 | `50%` | `48%` | `48%` | `46%` | `31%` | `41%` |
| OR BETWEEN_CLOSE_AND_HIGH | 559 | `46%` | `50%` | `54%` | `48%` | `37%` | `65%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 548 | `44%` | `56%` | `44%` | `50%` | `29%` | `60%` ⭐ |
| ATR Creciente (>10%) | 64 | `50%` | `50%` | `38%` | `43%` | `25%` | `47%` |
| ATR Decreciente (<-10%) | 39 | `56%` | `59%` | `45%` | `59%` | `37%` | `59%` |
| ATR Q1 (Baja Vol Historica) | 509 | `47%` | `52%` | `44%` | `50%` | `31%` | `55%` |
| ATR Q4 (Alta Vol Historica) | 460 | `45%` | `59%` | `45%` | `50%` | `37%` | `53%` |
| RSI Diario < 35 | 189 | `49%` | `57%` | `46%` | `52%` | `39%` | `58%` |
| RSI Diario > 65 | 259 | `45%` | `48%` | `50%` | `48%` | `31%` | `54%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `108 min` | `75 min` | `180 min` |
| TP DOWN (desde entrada) | `122 min` | `75 min` | `225 min` |
| False Break UP → SL | `79 min` | - | - |
| False Break DOWN → SL | `81 min` | - | - |

---

## Permutación #2: NY 30m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2055`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.91%`
- **Rotura Bajista (DOWN):** `50.46%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `58.20%` | `57.86%` |
| 1.5x Rango OR | `41.08%` | `42.14%` |
| 2.0x Rango OR | `29.25%` | `29.80%` |
| 1.0x Volatilidad ATR Diaria | `7.78%` | `4.82%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `44.19%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `43.78%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `51.92%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `45.21%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `36.57%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1502`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `23.50%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `16.78%` |
| Shakeout & Re-breakout UP (>=2x OR) | `12.18%` |
| Continuacion Bajista (>=1x OR) | `54.66%` |
| Extension media reversal UP | `0.68x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.48x OR` | Mediana: `1.15x` |
| Tiempo medio al re-breakout | `103 min` | Mediana: `75 min` |

**False Breakouts DOWN analizados:** `1457`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `25.05%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `17.91%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `12.15%` |
| Continuacion Alcista (>=1x OR) | `52.71%` |
| Extension media reversal DOWN | `0.69x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.47x OR` | Mediana: `1.08x` |
| Tiempo medio al re-breakout | `98 min` | Mediana: `75 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 190 | `19%` | `35%` | `59%` | `38%` | `16%` | `16%` |
| RSI > 70 (Overbought) | 236 | `71%` ⭐ | `37%` | `40%` | `52%` | `18%` | `25%` |
| RSI 30-70 (Neutro) | 1629 | `47%` | `42%` | `44%` | `44%` | `25%` | `60%` ⭐ |
| OR ABOVE_PD_HIGH | 442 | `49%` | `42%` | `43%` | `43%` | `20%` | `40%` |
| OR BELOW_PD_LOW | 438 | `48%` | `40%` | `45%` | `41%` | `25%` | `40%` |
| OR BETWEEN_CLOSE_AND_HIGH | 595 | `45%` | `39%` | `47%` | `44%` | `28%` | `63%` ⭐ |
| OR BETWEEN_LOW_AND_CLOSE | 580 | `47%` | `43%` | `41%` | `47%` | `20%` | `58%` |
| ATR Creciente (>10%) | 64 | `52%` | `45%` | `27%` | `32%` | `15%` | `45%` |
| ATR Decreciente (<-10%) | 42 | `55%` | `57%` | `48%` | `58%` | `27%` | `55%` |
| ATR Q1 (Baja Vol Historica) | 515 | `48%` | `35%` | `39%` | `41%` | `20%` | `53%` |
| ATR Q4 (Alta Vol Historica) | 504 | `46%` | `48%` | `45%` | `47%` | `29%` | `53%` |
| RSI Diario < 35 | 209 | `49%` | `45%` | `43%` | `52%` | `31%` | `55%` |
| RSI Diario > 65 | 260 | `48%` | `44%` | `42%` | `39%` | `20%` | `53%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `134 min` | `105 min` | `225 min` |
| TP DOWN (desde entrada) | `138 min` | `105 min` | `240 min` |
| False Break UP → SL | `97 min` | - | - |
| False Break DOWN → SL | `104 min` | - | - |

---

## Permutación #3: NY 45m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2059`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.72%`
- **Rotura Bajista (DOWN):** `50.95%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `49.27%` | `46.43%` |
| 1.5x Rango OR | `31.70%` | `29.17%` |
| 2.0x Rango OR | `21.21%` | `18.88%` |
| 1.0x Volatilidad ATR Diaria | `6.44%` | `4.29%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `40.02%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `40.04%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `49.15%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `43.37%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `35.67%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1449`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `16.49%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `10.90%` |
| Shakeout & Re-breakout UP (>=2x OR) | `7.59%` |
| Continuacion Bajista (>=1x OR) | `45.00%` |
| Extension media reversal UP | `0.45x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.19x OR` | Mediana: `0.88x` |
| Tiempo medio al re-breakout | `114 min` | Mediana: `90 min` |

**False Breakouts DOWN analizados:** `1401`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `17.92%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `11.71%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `7.42%` |
| Continuacion Alcista (>=1x OR) | `44.61%` |
| Extension media reversal DOWN | `0.49x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.18x OR` | Mediana: `0.85x` |
| Tiempo medio al re-breakout | `107 min` | Mediana: `82 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 203 | `16%` | `24%` | `42%` | `33%` | `13%` | `17%` |
| RSI > 70 (Overbought) | 207 | `73%` ⭐ | `24%` | `34%` | `37%` | `14%` | `24%` |
| RSI 30-70 (Neutro) | 1649 | `47%` | `34%` | `41%` | `42%` | `17%` | `56%` |
| OR ABOVE_PD_HIGH | 439 | `50%` | `28%` | `45%` | `40%` | `15%` | `39%` |
| OR BELOW_PD_LOW | 447 | `44%` | `35%` | `35%` | `39%` | `17%` | `39%` |
| OR BETWEEN_CLOSE_AND_HIGH | 596 | `45%` | `31%` | `41%` | `40%` | `20%` | `59%` |
| OR BETWEEN_LOW_AND_CLOSE | 577 | `48%` | `33%` | `39%` | `41%` | `14%` | `55%` |
| ATR Creciente (>10%) | 62 | `52%` | `22%` | `41%` | `32%` | `10%` | `40%` |
| ATR Decreciente (<-10%) | 41 | `49%` | `40%` | `40%` | `60%` ⭐ | `24%` | `49%` |
| ATR Q1 (Baja Vol Historica) | 507 | `49%` | `25%` | `37%` | `35%` | `13%` | `50%` |
| ATR Q4 (Alta Vol Historica) | 511 | `45%` | `34%` | `39%` | `46%` | `21%` | `50%` |
| RSI Diario < 35 | 212 | `50%` | `31%` | `37%` | `51%` | `20%` | `49%` |
| RSI Diario > 65 | 256 | `47%` | `39%` | `35%` | `42%` | `12%` | `51%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `150 min` | `105 min` | `255 min` |
| TP DOWN (desde entrada) | `154 min` | `120 min` | `255 min` |
| False Break UP → SL | `114 min` | - | - |
| False Break DOWN → SL | `122 min` | - | - |

---

## Permutación #4: NY 60m
**Configuración:** Inicia a las `13:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2033`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.14%`
- **Rotura Bajista (DOWN):** `51.01%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `42.54%` | `39.83%` |
| 1.5x Rango OR | `24.95%` | `24.30%` |
| 2.0x Rango OR | `16.31%` | `14.95%` |
| 1.0x Volatilidad ATR Diaria | `5.44%` | `3.47%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `35.71%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `34.81%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `48.06%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `42.01%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `34.65%`

### 🔄 Anatomia Post-False Breakout
**False Breakouts UP analizados:** `1383`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout UP (>=1x OR) | `12.29%` |
| Shakeout & Re-breakout UP (>=1.5x OR) | `7.52%` |
| Shakeout & Re-breakout UP (>=2x OR) | `5.57%` |
| Continuacion Bajista (>=1x OR) | `38.90%` |
| Extension media reversal UP | `0.35x OR` | Mediana: `0.00x` |
| Extension media continuacion DOWN | `1.03x OR` | Mediana: `0.77x` |
| Tiempo medio al re-breakout | `122 min` | Mediana: `105 min` |

**False Breakouts DOWN analizados:** `1314`

| Metrica | Valor |
| --- | --- |
| Shakeout & Re-breakout DOWN (>=1x OR) | `13.85%` |
| Shakeout & Re-breakout DOWN (>=1.5x OR) | `8.22%` |
| Shakeout & Re-breakout DOWN (>=2x OR) | `4.49%` |
| Continuacion Alcista (>=1x OR) | `38.20%` |
| Extension media reversal DOWN | `0.37x OR` | Mediana: `0.00x` |
| Extension media continuacion UP | `1.01x OR` | Mediana: `0.71x` |
| Tiempo medio al re-breakout | `111 min` | Mediana: `90 min` |

### 🔬 Edge por Contexto de Features
| Contexto | N | Break UP | Ext 1.5x UP | False BK UP | False BK DW | Shakeout UP | Magnet PD_Close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RSI < 30 (Oversold) | 189 | `13%` | `25%` | `29%` | `28%` | `9%` | `16%` |
| RSI > 70 (Overbought) | 199 | `73%` ⭐ | `22%` | `29%` | `39%` | `12%` | `21%` |
| RSI 30-70 (Neutro) | 1645 | `47%` | `26%` | `37%` | `36%` | `13%` | `55%` |
| OR ABOVE_PD_HIGH | 428 | `48%` | `19%` | `43%` | `34%` | `10%` | `39%` |
| OR BELOW_PD_LOW | 442 | `42%` | `33%` | `30%` | `36%` | `13%` | `38%` |
| OR BETWEEN_CLOSE_AND_HIGH | 593 | `45%` | `23%` | `36%` | `34%` | `15%` | `58%` |
| OR BETWEEN_LOW_AND_CLOSE | 570 | `50%` | `26%` | `34%` | `35%` | `10%` | `53%` |
| ATR Creciente (>10%) | 60 | `50%` | `10%` | `37%` | `25%` | `5%` | `40%` |
| ATR Decreciente (<-10%) | 41 | `61%` ⭐ | `28%` | `32%` | `50%` | `21%` | `44%` |
| ATR Q1 (Baja Vol Historica) | 492 | `47%` | `19%` | `31%` | `30%` | `10%` | `48%` |
| ATR Q4 (Alta Vol Historica) | 511 | `47%` | `29%` | `36%` | `39%` | `15%` | `49%` |
| RSI Diario < 35 | 210 | `48%` | `25%` | `34%` | `49%` | `16%` | `48%` |
| RSI Diario > 65 | 249 | `49%` | `31%` | `33%` | `34%` | `10%` | `50%` |

### ⏱️ Velocidad de Ejecucion
| Metrica | Media | Mediana | P80 |
| --- | --- | --- | --- |
| TP UP (desde entrada) | `160 min` | `135 min` | `255 min` |
| TP DOWN (desde entrada) | `153 min` | `120 min` | `240 min` |
| False Break UP → SL | `123 min` | - | - |
| False Break DOWN → SL | `136 min` | - | - |

---

## 🎯 🧠 Master Quant Team Debate: NATGAS

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> ⚠️ **ALERTA DE SISTEMA (PÓLIZA DE RIESGO)**
> Tras compilar todas las permutaciones históricas de ventana y horario, la asimetría probabilística simple no logró consolidar un nivel de confianza base superior al **60%** en rangos operables o mitigaciones lógicas de reversión. 
> *Resolución:* **NO SE RECOMIENDA AUTOMATIZAR** modelos ciegos para este instrumento empleando estos features puros. Depende excesivamente de macroeconomía exógena (Aleatoriedad predominante intradía).

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`NY 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=489 | UP: `44%` | Ext 1.5 UP: `63%` | Falsa Ruptura DW: `55%` | Reversión a PD_Close: `56%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=485 | UP: `47%` | Ext 1.5 UP: `50%` | Falsa Ruptura DW: `48%` | Reversión a PD_Close: `50%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=268 | UP: `46%` | Ext 1.5 UP: `53%` | Falsa Ruptura DW: `45%` | Reversión a PD_Close: `60%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1669 | UP: `47%` | Ext 1.5 UP: `52%` | Falsa Ruptura DW: `49%` | Reversión a PD_Close: `52%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*