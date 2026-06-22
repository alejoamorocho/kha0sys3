# KHA0SYS3 — Setup LIVE actual + Roadmap de estrategias

**Fecha:** 2026-06-21 · **Estado:** EN VIVO con dinero real

---

## 1. Cuenta

| | |
|---|---|
| Broker / Servidor | Vantage · `VantageMarkets-Live 5` |
| Login | `30046745` |
| Tipo | **REAL** |
| Balance | **$1,100 USD** · apalancamiento 1:500 |
| AutoTrading | ON (con protección de fin de semana, `common.ini Account=0/Profile=0`) |
| Bot activo | `Kha0sysAmo8` (AMO8, magic 8338) — único motor operando |

**Riesgo:** **$50 fijo por trade** (`risk_fixed_usd=50`). ≈ 4.5% del balance por operación.
Máximo simultáneo (las 4 a la vez, peor caso) = $200 ≈ 18% del balance.
**Dedup:** 1 entrada por estrategia por día UTC (idéntico a backtest y demo — verificado).

---

## 2. Estrategias ACTIVAS (4) — AMO8 false-break ORB

Todas: entrada por **falso rompimiento** del rango de apertura, RR 1.5, salida OR_FIXED
(SL/TP derivados del ancho del rango). `n live` = trades en la ventana post-purga (~11d, muestra chica).

| # | ID | Activo | Tipo | Dir | Ventana OR (UTC) | exp.WR | exp.PF | live n | live WR | live PF(pips) |
|---|----|--------|------|-----|------------------|--------|--------|--------|---------|----------------|
| 1 | AMO8·018 | SP500 | False-break-down | LONG | 12:30 · 15min | 73% | 2.65 | 6 | 83% | **9.09** |
| 2 | AMO8·081 | NAS100 | False-break-down | LONG | 07:00 · 15min | 68% | 2.12 | 7 | 86% | **7.60** |
| 3 | AMO8·046 | XAUUSD | False-break-down | LONG | 12:30 · 15min | 68% | 2.31 | 5 | 60% | **5.27** |
| 4 | AMO8·066 | SP500 | False-break-up | SHORT | 12:30 · 30min | 69% | 2.19 | 7 | 57% | 1.67 |

**Por qué estas 4:** mejor edge confirmado del portafolio (PF en pips 5–9 en las 3 primeras),
sobre índices y oro (margen barato → sin rechazos en cuenta chica), y sobreviven a comisión.

**Horario de operación (UTC real):**
- **07:00** → NAS100 (rango 07:00–07:15)
- **12:30** → SP500 ×2 (15m y 30m) + XAUUSD (rango 12:30–12:45 / 12:30–13:00)
- La *entrada* ocurre después de que cierra el rango, cuando se da el falso rompimiento (no todos los días hay).

---

## 3. PRÓXIMAS candidatas a activar (4)

Ordenadas por facilidad/seguridad de activación. `exp.*` = backtest robusto; `live 30d` = muestra real reciente.

### Tier A — extensión directa de AMO8 (mismo bot, solo agregar a la config)

| ID | Activo | Tipo | Dir | Ventana OR (UTC) | exp.WR | exp.PF | live 30d (n/WR/PF) | Nota |
|----|--------|------|-----|------------------|--------|--------|---------------------|------|
| **AMO8·112** | XAUUSD | False-break-up | SHORT | **00:00** · 15min | 68% | 2.01 | 7 / 57% / 1.17 | Oro (margen barato). Era la 5ª AMO8; edge modesto pero positivo. Dispara a medianoche UTC. |

### Tier B — ORB (requiere reactivar `Kha0sysTradersBot`, magic 1340)

| ID | Activo | Dir | Ventana OR (UTC) | exp.WR | exp.PF (IS/OOS) | live 30d (n/WR/PF) | Nota |
|----|--------|-----|------------------|--------|------------------|---------------------|------|
| **TO_GBPJPY_07h_30m** | GBPJPY | LONG | 07:00 · 30min | 56% | 2.75 / **2.64** | 10 / **80%** / **3.64** | La más fuerte en vivo. FX (JPY). |
| **TO_GBPAUD_07h_30m** | GBPAUD | LONG | 07:00 · 30min | 57% | 2.38 / **2.67** | 11 / 64% / 1.66 | FX. Buen OOS. |
| **TO_NASDAQ100_13h_30m** | NAS100 | LONG | 13:00 · 30min | 54% | 2.33 / 2.05 | 19 / 47% / 1.08 | Índice (margen barato). Más trades/año. |

---

## 4. Recomendación de activación

1. **Primero AMO8·112** — es trivial (mismo bot, agregar 1 línea a `bot_config_amo8.json`), oro = margen barato, edge positivo. Bajo riesgo de implementación.
2. **Luego las 3 ORB** — son las de mejor track histórico (GBPJPY 80% WR en vivo), pero implican reactivar `Kha0sysTradersBot` (hoy detenido/deshabilitado) y su propio Telegram. GBPJPY y GBPAUD son FX; NASDAQ100 es índice (más fácil de margen).

**Antes de activar cualquiera, conviene:**
- Dejar correr las 4 actuales unas semanas en vivo para tener muestra real con dinero.
- Revisar el riesgo agregado: con $50 fijo, cada nueva estrategia suma ~4.5% de exposición por trade. Con balance de $1,100, 4 activas ya dan hasta 18% simultáneo; sumar más sin capitalizar la cuenta sube ese tope.

---

## 5. Infraestructura (servicios VPS)

**Activos (lo único necesario para live):**
- `Kha0sysAmo8` — bot AMO8 live
- `Kha0sysATWatchdog` — mantiene AutoTrading ON (protección fin de semana)
- 1 terminal MT5 (sesión 0)

**Retirados (Stopped + Disabled, inertes):** `Kha0sysMathBot` · `Kha0sysTradersBot` · `Kha0sysMathWatchdog` · `Kha0sysWatchdog3`.

> Para activar las ORB (Tier B) habría que re-habilitar `Kha0sysTradersBot` y poblar
> `bot_config_traders_orb.json` (hoy vacío) con las 3 estrategias + `risk_fixed_usd`.

**Monitoreo:** Telegram (bot interactivo en AmoBot: `/balance` `/pnl` `/positions` `/status`
`/stop` `/resume`, cuenta real) + app móvil MT5 con el login `30046745`.
