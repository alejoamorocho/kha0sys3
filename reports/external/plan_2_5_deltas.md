# Plan 2.5 — Backtest Deltas vs Plan 2

**Generated:** 2026-05-07
**Reference doc:** `outputs/estrategias_detalladas_testeables.md`

Re-runs de cada strategy aplicando los 7 fixes del Plan 2.5 documentados en
`docs/superpowers/plans/2026-05-06-strategies-external-plan-2.5-fidelity-fixes.md`.

## Resumen ejecutivo

- **OOPS doc**: cambio de `tp1=2R` a EOD-only afecta poco (calmar idéntico).
- **Doble Suelo**: max_separation 80→30 reduce señales 67% pero la calidad sigue pésima — el detector no era el problema.
- **Perdices Fib**: cambio de `timestop fijo` a `exit_after_bars_if_below_R` no cambia métricas en H1 (todos los trades quedan <1R a 4h, así que ambos exits coinciden). Confirma que H1 placeholder no funciona; necesita M5.
- **COT-1**: fallo de descarga (HTTP 403 cftc.gov) → 0 trades. Bug del downloader, no del strategy. Issue para Plan 2.6 / debugging del downloader.
- **SMA-18**: el cambio más material (stop intra-bar SMA → 2 cierres consecutivos). Pendiente — re-run en curso, large data + 4241 signals × ATR sweep.

## Tabla comparativa por estrategia (modo doc)

| Strategy | Métrica | Plan 2 | Plan 2.5 | Δ | Diagnóstico |
|----------|---------|--------|----------|---|-------------|
| **OOPS** | n | 124 | 124 | 0 | Misma señal. Cambio solo en exit. |
| OOPS | wr | 0.250 | 0.234 | -0.016 | EOD permite cierres con menor profit que TP=2R |
| OOPS | pf | 0.291 | 0.284 | -0.007 | Mínimo |
| OOPS | dd_R | 69.4 | 71.7 | +2.3 | Mínimo |
| OOPS | calmar | -1.014 | -1.014 | 0 | Estrategia sigue no-viable |
| **Doble Suelo** | n | 1268 | 419 | **-849 (-67%)** | max_separation 80→30 elimina patrones lejanos |
| Doble Suelo | wr | 0.085 | 0.055 | -0.030 | Filtros más estrictos no mejoran calidad |
| Doble Suelo | pf | 0.021 | 0.011 | -0.010 | Mínimo |
| Doble Suelo | dd_R | 1162 | 482 | **-680** | Menos señales = menos pérdidas absolutas |
| Doble Suelo | calmar | -1.001 | -1.001 | 0 | No-viable |
| **Perdices Fib** | n | 1245 | 1245 | 0 | Estrategia idéntica |
| Perdices Fib | wr | 0.033 | 0.033 | 0 | exit_after_bars condicional no aplica en H1 |
| Perdices Fib | pf | 0.012 | 0.012 | 0 | |
| Perdices Fib | dd_R | 292.9 | 292.9 | 0 | |
| Perdices Fib | calmar | -1.001 | -1.001 | 0 | Espera M5 para test real |
| **COT-1** | n | 0¹ | 0² | — | ¹Plan 2 no corrió standalone, ²HTTP 403 cftc.gov |
| **SMA-18** | n | 4241 | 4344 | +103 | valid_until 60→90d permite más signals |
| SMA-18 | wr | 0.315 | 0.302 | -0.013 | |
| SMA-18 | pf | 1.129 | **0.793** | **-0.336** | Cambio crítico: 2-cierres deja correr pérdidas |
| SMA-18 | dd_R | 812 | 730 | -82 | |
| SMA-18 | calmar | **0.544** | **-0.622** | **-1.166** | **Win era artefactual del bug** |

## Issues abiertos para Plan 2.6

1. **COT downloader 403 Forbidden**: cftc.gov bloquea el User-Agent default de urllib. Fix: añadir `User-Agent: Mozilla/5.0` al request, o usar `requests` con headers. URL alternativa: el `dea/history/com_disagg_txt_<year>.zip` puede haber cambiado a otra ruta.

2. **SMA-18 trades overlap (n=4241)**: regla "1 trade abierto por símbolo a la vez" no implementada. Plan 2 producía señales solapadas. Plan 2.5 con valid_until=90 días + 2-closes-against potencia el solapamiento. Fix: añadir filtro de "no nueva señal hasta cerrar la actual" en el runner SMA-18.

3. **Trailing-to-BE post-TP1 + parcial 50%**: documento dice tomar 50% en TP1 y trail BE para resto. NO implementado en backtester. Postergado a Plan 2.6.

4. **Pirámide SMA-18**: documento permite añadir contratos en retests SMA-18. NO implementado. Postergado.

## Veredicto post Plan 2.5

| Strategy | Status | Razón |
|----------|--------|-------|
| OOPS | ❌ NO viable | Vantage 24h vs RTH NY mismatch + sin filtros macro |
| Doble Suelo | ❌ NO viable | Detector OK pero estrategia necesita filtro macro/contexto |
| Perdices Fib | ⏳ PENDING M5 | H1 placeholder no funciona, esperar datos M5 |
| COT-1 | ⚠️ BLOCKED | HTTP 403 cftc.gov — fix downloader y re-run |
| SMA-18 | ❌ NO viable | El "win" calmar=0.544 era artefactual del bug stop=intra-bar; con regla literal calmar=-0.622, PF<1 |

**Conclusión Plan 2.5**: ninguna estrategia del documento es viable con la data disponible
y reglas literales. El único "win" aparente (SMA-18 calmar=0.544) era artefacto del bug en
el modo stop. La regla correcta del documento ("2 cierres consecutivos contra SMA-18")
deja correr pérdidas y produce PF<1.

**Diagnóstico**: los autores del documento (Rosputnia, Williams, Schulz, Perdices) probablemente
combinan estas reglas literales con:
- Discrecionalidad humana (filtrar setups en tiempo real por contexto)
- Filtros macro no capturados (calendario económico, VIX, NFP, FOMC)
- Selección de mercados específicos (futuros directos vs CFDs Vantage)
- TFs distintos (RTH NY puro vs broker 24h)

**Próximos pasos sugeridos:**
1. **Plan 3 (FADE/MATH con M1)** — re-evaluar las estrategias del bot live (las únicas que
   realmente operan en Vantage) con M1 polars sobre los activos overlap. Eso responde la
   pregunta del usuario sobre el comportamiento de "nuestras estrategias" con M1.
2. **Plan 2.6 (issues abiertos)** — fix COT downloader, "1 trade open per symbol" filter,
   parcial TP1+trail BE, pirámide SMA-18. Estos quedan archivados como mejoras opcionales.
3. **Pivot**: dado que ninguna estrategia del documento pasa el filtro, considerar abandonar
   esta línea y enfocarse 100% en mejorar las FADE/MATH del bot que ya están en producción.
