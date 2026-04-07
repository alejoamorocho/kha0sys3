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
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `2545`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `38.39%`
- **Rotura Bajista (DOWN):** `35.17%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `88.02%` | `87.60%` |
| 1.5x Rango OR | `79.63%` | `80.34%` |
| 2.0x Rango OR | `74.31%` | `74.64%` |
| 1.0x Volatilidad ATR Diaria | `10.03%` | `15.42%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.66%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `50.84%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `64.32%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `49.55%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `36.48%`

---

## Permutación #2: Pre-Market 30m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2545`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `38.11%`
- **Rotura Bajista (DOWN):** `37.72%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `82.89%` | `82.60%` |
| 1.5x Rango OR | `75.46%` | `74.90%` |
| 2.0x Rango OR | `68.56%` | `67.40%` |
| 1.0x Volatilidad ATR Diaria | `9.90%` | `15.94%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `53.09%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `52.19%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `63.65%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `49.35%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `36.25%`

---

## Permutación #3: Pre-Market 45m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2545`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `41.49%`
- **Rotura Bajista (DOWN):** `39.33%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `74.05%` | `74.33%` |
| 1.5x Rango OR | `64.39%` | `61.84%` |
| 2.0x Rango OR | `55.02%` | `53.15%` |
| 1.0x Volatilidad ATR Diaria | `8.90%` | `13.79%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `54.45%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `57.94%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `62.44%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `48.41%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `35.38%`

---

## Permutación #4: Pre-Market 60m
**Configuración:** Inicia a las `12:00 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2545`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `41.49%`
- **Rotura Bajista (DOWN):** `38.27%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `69.70%` | `72.28%` |
| 1.5x Rango OR | `59.85%` | `58.62%` |
| 2.0x Rango OR | `50.47%` | `50.41%` |
| 1.0x Volatilidad ATR Diaria | `8.81%` | `14.07%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `51.42%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `56.26%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `61.69%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `48.06%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `35.28%`

---

## Permutación #5: NY Cash 15m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `15 minutos`. Días procesados válidos: `2543`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `38.58%`
- **Rotura Bajista (DOWN):** `38.10%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `70.85%` | `70.79%` |
| 1.5x Rango OR | `58.82%` | `57.59%` |
| 2.0x Rango OR | `48.01%` | `47.78%` |
| 1.0x Volatilidad ATR Diaria | `8.26%` | `14.65%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `48.52%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `52.53%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `58.83%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `45.42%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `34.09%`

---

## Permutación #6: NY Cash 30m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `30 minutos`. Días procesados válidos: `2543`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `40.66%`
- **Rotura Bajista (DOWN):** `39.28%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `58.80%` | `60.76%` |
| 1.5x Rango OR | `44.87%` | `46.95%` |
| 2.0x Rango OR | `32.30%` | `37.44%` |
| 1.0x Volatilidad ATR Diaria | `7.06%` | `14.21%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `46.03%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `51.45%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `57.49%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `44.24%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `33.25%`

---

## Permutación #7: NY Cash 45m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `45 minutos`. Días procesados válidos: `2543`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `42.39%`
- **Rotura Bajista (DOWN):** `38.46%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `49.81%` | `53.27%` |
| 1.5x Rango OR | `32.84%` | `38.55%` |
| 2.0x Rango OR | `22.36%` | `30.27%` |
| 1.0x Volatilidad ATR Diaria | `6.59%` | `13.70%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `42.39%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `46.83%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `55.96%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `42.63%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `32.23%`

---

## Permutación #8: NY Cash 60m
**Configuración:** Inicia a las `13:30 UTC`. Tamaño de caja evaluativa: `60 minutos`. Días procesados válidos: `2543`.

### 🧭 Momentum Base Básico
- **Rotura Alcista (UP):** `42.27%`
- **Rotura Bajista (DOWN):** `35.39%`

### 🎯 Extensiones Geométricas (Target Limits)
| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |
| --- | --- | --- |
| 1.0x Rango OR | `44.28%` | `48.44%` |
| 1.5x Rango OR | `27.91%` | `32.44%` |
| 2.0x Rango OR | `19.07%` | `24.78%` |
| 1.0x Volatilidad ATR Diaria | `6.42%` | `13.78%` |

### ⚠️ Vulnerabilidad a Trampas (False Breakouts)
- Falsa Ruptura Alcista atrapada en SL contra-caja: `36.65%`
- Falsa Ruptura Bajista atrapada en SL contra-caja: `38.89%`

### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión
- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `54.35%`
- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `41.29%`
- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `31.50%`

---

## 🎯 🧠 Master Quant Team Debate: SP500

Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.

### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)
> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:

- **[EDGE MAGNET PD_CLOSE] Pre-Market (15m)**: Imantación cíclica brutal. El `64.32%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (30m)**: Imantación cíclica brutal. El `63.65%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (45m)**: Imantación cíclica brutal. El `62.44%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE MAGNET PD_CLOSE] Pre-Market (60m)**: Imantación cíclica brutal. El `61.69%` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.

- **[EDGE TENDENCIAL DOWN] Pre-Market (15m)**: Tasa de extensión polar bajista (1.5x) del `80.34%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Pre-Market (30m)**: Tasa de extensión polar bajista (1.5x) del `74.90%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL DOWN] Pre-Market (45m)**: Tasa de extensión polar bajista (1.5x) del `61.84%`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.

- **[EDGE TENDENCIAL UP] Pre-Market (15m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `79.63%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (30m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `75.46%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

- **[EDGE TENDENCIAL UP] Pre-Market (45m)**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `64.39%`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.

### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural
Hemos sometido la mejor matriz base (`Pre-Market 45m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:

#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)
- **Rango Ultras Estrecho (Q1)**: Eventos=530 | UP: `48%` | Ext 1.5 UP: `78%` | Falsa Ruptura DW: `59%` | Reversión a PD_Close: `68%`
- **Rango Masivo Hiper-Volátil (Q4)**: Eventos=530 | UP: `49%` | Ext 1.5 UP: `50%` | Falsa Ruptura DW: `57%` | Reversión a PD_Close: `63%`

#### 2. Relación de Apertura (Memoria de Día Anterior)
- **Apertura Interna (Consolidación atrapada en el OR de ayer)**: Eventos=208 | UP: `50%` | Ext 1.5 UP: `60%` | Falsa Ruptura DW: `66%` | Reversión a PD_Close: `63%`
- **Apertura en Gap Bidireccional (Desconexión de ayer)**: Eventos=1908 | UP: `50%` | Ext 1.5 UP: `65%` | Falsa Ruptura DW: `57%` | Reversión a PD_Close: `66%`

> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.

---
*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*