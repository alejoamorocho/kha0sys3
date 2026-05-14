"""End-to-end ORB pipeline runner.

Usage:
  python scripts/run_orb_pipeline.py [--skip-phase A|B|C|D ...]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl

from src.application.orb_utils import REPORTS_DIR
from src.engine.orb_universe_m1_mgmt import run_phase_a
from src.engine.orb_management_grid import run_phase_b
from src.engine.orb_robustness import run_phase_c, write_markdown_report
from src.engine.orb_optuna_refine import run_phase_d


def main(skip: set[str]) -> None:
    base = Path(REPORTS_DIR)
    if "A" not in skip:
        print("[Phase A] pattern discovery + edge scoring ...")
        run_phase_a()
    if "B" not in skip:
        print("[Phase B] management grid ...")
        run_phase_b()
    if "C" not in skip:
        print("[Phase C] robustness ...")
        run_phase_c()
    if "D" not in skip:
        print("[Phase D] Optuna refinement ...")
        run_phase_d()

    print("[Report] writing ORB_Pipeline_Report.md ...")
    rob_path = base / "orb_robustness.parquet"
    opt_path = base / "orb_optuna_results.parquet"
    rob = pl.read_parquet(rob_path) if rob_path.exists() else pl.DataFrame()
    opt = pl.read_parquet(opt_path) if opt_path.exists() else None
    write_markdown_report(rob, opt, base / "ORB_Pipeline_Report.md")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--skip-phase", action="append", choices=["A", "B", "C", "D"], default=[])
    args = p.parse_args()
    main(skip=set(args.skip_phase))
