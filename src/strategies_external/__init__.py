"""External strategies research module — Plan 1 (infra + OOPS).

Backtest-only. Aislado del bot live (FADE/MATH).

Implementado en Plan 1:
- Infraestructura: data_loader, ExitManagers (doc/atr/indicator),
  backtester, metrics, walk_forward, monte_carlo, markdown report.
- Estrategia OOPS (Larry Williams) con runner ejecutable:
    python -m src.strategies_external.runners.run_oops

Pendiente (Plan 2):
- SMA-18, Doble Suelo, Perdices Fib, COT-1.
- COT downloader y estacionalidad.
- Reporte comparativo cross-estrategias.

Specs:
- docs/superpowers/specs/2026-05-06-strategies-external-design.md
"""
