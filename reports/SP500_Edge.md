# 🌐 Matriz Probabilística Omnidireccional: SP500

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
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `729`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `50.48%`
- **Rotura Bajista (DOWN):** `44.86%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `83.42%` | `83.49%` |
| 1.5x Rango OR | `73.37%` | `74.01%` |
| 2.0x Rango OR | `65.49%` | `65.44%` |
| 1.0x Volatilidad ATR Diaria | `16.03%` | `21.10%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `61.68%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.43%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `224.55%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `172.98%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `127.37%`

---

## Permutación #2: Pre-Market 30m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1272`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.62%`
- **Rotura Bajista (DOWN):** `45.99%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `80.27%` | `78.97%` |
| 1.5x Rango OR | `71.50%` | `69.23%` |
| 2.0x Rango OR | `63.58%` | `61.20%` |
| 1.0x Volatilidad ATR Diaria | `12.65%` | `17.44%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.65%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `54.19%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `127.36%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `98.74%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `72.52%`

---

## Permutación #3: Pre-Market 45m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1685`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.91%`
- **Rotura Bajista (DOWN):** `47.30%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `71.34%` | `72.27%` |
| 1.5x Rango OR | `60.29%` | `58.47%` |
| 2.0x Rango OR | `50.18%` | `49.31%` |
| 1.0x Volatilidad ATR Diaria | `10.46%` | `14.68%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `55.65%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `59.60%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `94.30%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `73.12%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `53.44%`

---

## Permutación #4: Pre-Market 60m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1809`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.81%`
- **Rotura Bajista (DOWN):** `46.32%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.15%` | `70.17%` |
| 1.5x Rango OR | `57.71%` | `56.32%` |
| 2.0x Rango OR | `48.06%` | `48.33%` |
| 1.0x Volatilidad ATR Diaria | `9.77%` | `15.04%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `52.94%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.64%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `86.79%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `67.61%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `49.64%`

---

## Permutación #5: NY Cash 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `1733`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `46.97%`
- **Rotura Bajista (DOWN):** `46.39%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `68.18%` | `68.78%` |
| 1.5x Rango OR | `54.79%` | `54.10%` |
| 2.0x Rango OR | `42.87%` | `44.15%` |
| 1.0x Volatilidad ATR Diaria | `9.58%` | `15.55%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `48.77%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `53.98%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `86.32%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `66.65%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `50.03%`

---

## Permutación #6: NY Cash 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `1874`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `49.15%`
- **Rotura Bajista (DOWN):** `47.44%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `56.35%` | `59.51%` |
| 1.5x Rango OR | `42.35%` | `44.99%` |
| 2.0x Rango OR | `29.10%` | `34.87%` |
| 1.0x Volatilidad ATR Diaria | `7.38%` | `14.29%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `46.36%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `50.84%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `78.01%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `60.03%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `45.12%`

---

## Permutación #7: NY Cash 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `1911`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.70%`
- **Rotura Bajista (DOWN):** `45.53%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `48.58%` | `53.22%` |
| 1.5x Rango OR | `31.48%` | `37.93%` |
| 2.0x Rango OR | `20.45%` | `28.97%` |
| 1.0x Volatilidad ATR Diaria | `6.48%` | `13.56%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `43.22%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `46.44%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `74.46%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `56.72%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.88%`

---

## Permutación #8: NY Cash 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `1902`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `51.10%`
- **Rotura Bajista (DOWN):** `42.64%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `44.14%` | `50.43%` |
| 1.5x Rango OR | `27.06%` | `33.66%` |
| 2.0x Rango OR | `17.80%` | `25.77%` |
| 1.0x Volatilidad ATR Diaria | `6.38%` | `13.81%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `37.55%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `40.07%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `72.66%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `55.21%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `42.11%`

---

## 🎯 🧠 Master Quant Team Debate: SP500

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE FADE-BREAKOUT] Pre-Market (15m)**: Trampa de Liquidez Alcista del `61.68%`. Cada vez que rompe al alza, termina invalidándose devorando el OR Low. Sugerencia Algo: Stop-Limit en contra de falsos quiebres (Atrapar inversores manuales).

- **[EDGE MAGNET PD_CLOSE] NY Cash (15m)**: Imantación cíclica brutal. El `86.32%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] NY Cash (30m)**: Imantación cíclica brutal. El `78.01%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] NY Cash (45m)**: Imantación cíclica brutal. El `74.46%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] NY Cash (60m)**: Imantación cíclica brutal. El `72.66%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (15m)**: Imantación cíclica brutal. El `224.55%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (30m)**: Imantación cíclica brutal. El `127.36%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (45m)**: Imantación cíclica brutal. El `94.30%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (60m)**: Imantación cíclica brutal. El `86.79%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_MID] NY Cash (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `66.65%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] NY Cash (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `60.03%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Pre-Market (15m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `172.98%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Pre-Market (30m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `98.74%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Pre-Market (45m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `73.12%` de los eventos evaluados.

- **[EDGE MAGNET PD_MID] Pre-Market (60m)**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `67.61%` de los eventos evaluados.

- **[EDGE TENDENCIAL DOWN] Pre-Market (15m)**: Tasa de extensión polar bajista (1.5x) del `74.01%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Pre-Market (30m)**: Tasa de extensión polar bajista (1.5x) del `69.23%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] Pre-Market (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `73.37%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `71.50%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `60.29%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Pre-Market 15m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=183 | UP: `52%` | Ext 1.5 UP: `77%` | Falsa Ruptura DW: `52%` | Reversión a PD_Close: `66%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=183 | UP: `43%` | Ext 1.5 UP: `65%` | Falsa Ruptura DW: `48%` | Reversión a PD_Close: `64%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=32 | UP: `59%` | Ext 1.5 UP: `79%` | Falsa Ruptura DW: `15%` | Reversión a PD_Close: `50%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=697 | UP: `50%` | Ext 1.5 UP: `73%` | Falsa Ruptura DW: `56%` | Reversión a PD_Close: `68%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*