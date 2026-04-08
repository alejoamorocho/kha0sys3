# Strategy Selection & Validation Pipeline

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** For each of 13 assets, identify max 3 strategies (archetype + session + duration + context filter) with WR >= 65%, backtest them individually and as a group, and generate per-strategy reports.

**Architecture:** A new strategy pipeline module scans all permutations of (session x duration x archetype x direction x context_filter) per asset, evaluates WR from historical data, selects top 3 via quant team logic, then runs full backtests with equity curves. Reports are generated per-strategy in Markdown.

**Tech Stack:** Python 3.12, Polars (vectorized), existing DataEnricher/TrackerEngine/StatisticalEngine pipeline.

---

### Task 1: Create Strategy Data Models

**Files:**
- Create: `src/domain/strategy_models.py`

- [ ] **Step 1: Create the strategy definition and result dataclasses**

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class StrategyDef:
    symbol: str
    session_name: str
    time_start: str
    duration: int
    archetype: str          # MOMENTUM_UP, MOMENTUM_DOWN, FADE_UP, FADE_DOWN, SHAKEOUT_UP, SHAKEOUT_DOWN
    direction: str          # UP or DOWN
    context_filter: Optional[Dict[str, str]] = None  # e.g. {"rsi_at_or_close": "<30"}
    tp_multiplier: float = 1.5
    label: str = ""

    def __post_init__(self):
        if not self.label:
            ctx = ""
            if self.context_filter:
                ctx = " | " + ", ".join(f"{k}{v}" for k, v in self.context_filter.items())
            self.label = f"{self.symbol} {self.session_name} {self.duration}m {self.archetype}{ctx}"

    @property
    def strategy_id(self) -> str:
        parts = [self.symbol, self.session_name, str(self.duration), self.archetype]
        if self.context_filter:
            for k, v in sorted(self.context_filter.items()):
                parts.append(f"{k}{v}")
        return "_".join(parts).replace(" ", "")


@dataclass
class StrategyResult:
    strategy: StrategyDef
    total_trades: int = 0
    trades_per_year: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    net_r: float = 0.0
    max_drawdown: float = 0.0
    sharpe: float = 0.0
    avg_r_per_trade: float = 0.0
    best_year: str = ""
    worst_year: str = ""
    yearly_stats: Dict = field(default_factory=dict)
    passes_filter: bool = False  # True if WR>=65%, 100+trades/yr, PF>1.0
```

- [ ] **Step 2: Commit**

```bash
git add src/domain/strategy_models.py
git commit -m "feat: add StrategyDef and StrategyResult data models"
```

---

### Task 2: Create the Strategy Scanner

Scans all permutations per asset and computes win rate for each archetype.

**Files:**
- Create: `src/engine/strategy_scanner.py`

- [ ] **Step 1: Create the scanner module**

```python
import polars as pl
from typing import List, Dict, Optional
from src.domain.strategy_models import StrategyDef


class StrategyScanner:
    """
    Scans all permutations of (session x duration x archetype x direction x context_filter)
    for a given asset and evaluates win rate from enriched historical data.
    """

    ARCHETYPES = ["MOMENTUM", "FADE", "SHAKEOUT"]
    DIRECTIONS = ["UP", "DOWN"]

    CONTEXT_FILTERS = {
        "rsi_oversold": {"col": "rsi_at_or_close", "op": "<", "val": 30, "label": "RSI<30"},
        "rsi_overbought": {"col": "rsi_at_or_close", "op": ">", "val": 70, "label": "RSI>70"},
        "atr_growing": {"col": "atr_change", "op": ">", "val": 0.1, "label": "ATR+10%"},
        "atr_shrinking": {"col": "atr_change", "op": "<", "val": -0.1, "label": "ATR-10%"},
        "above_pd_high": {"col": "or_position_vs_pd", "op": "==", "val": "ABOVE_PD_HIGH", "label": "AbovePD"},
        "below_pd_low": {"col": "or_position_vs_pd", "op": "==", "val": "BELOW_PD_LOW", "label": "BelowPD"},
        "between_close_high": {"col": "or_position_vs_pd", "op": "==", "val": "BETWEEN_CLOSE_AND_HIGH", "label": "BtwCloseHigh"},
        "between_low_close": {"col": "or_position_vs_pd", "op": "==", "val": "BETWEEN_LOW_AND_CLOSE", "label": "BtwLowClose"},
        "rsi_daily_low": {"col": "rsi_daily_14", "op": "<", "val": 35, "label": "RSI_D<35"},
        "rsi_daily_high": {"col": "rsi_daily_14", "op": ">", "val": 65, "label": "RSI_D>65"},
    }

    MIN_DAYS = 20  # Minimum events for statistical significance

    @staticmethod
    def apply_context_filter(df: pl.DataFrame, filt: Optional[Dict]) -> pl.DataFrame:
        """Apply a context filter dict to the dataframe."""
        if not filt:
            return df
        col = filt["col"]
        op = filt["op"]
        val = filt["val"]
        if col not in df.columns:
            return df.head(0)  # Empty if column missing
        if op == "<":
            return df.filter(pl.col(col) < val)
        elif op == ">":
            return df.filter(pl.col(col) > val)
        elif op == "==":
            return df.filter(pl.col(col) == val)
        return df

    @classmethod
    def evaluate_archetype(cls, stats_df: pl.DataFrame, archetype: str,
                           direction: str, context_filter: Optional[Dict] = None) -> Dict:
        """
        Evaluate win rate for a specific archetype + direction + optional context filter.
        Returns dict with win_rate, n_trades, wins, losses, r_per_trade.
        """
        valid_df = stats_df.filter(
            pl.col("first_break_dir").is_not_null() &
            pl.col("or_atr_ratio").is_between(0.1, 0.8)
        )

        # Apply context filter
        if context_filter:
            valid_df = cls.apply_context_filter(valid_df, context_filter)

        if valid_df.height < cls.MIN_DAYS:
            return {"win_rate": 0, "n_trades": 0, "viable": False}

        if archetype == "MOMENTUM":
            return cls._eval_momentum(valid_df, direction)
        elif archetype == "FADE":
            return cls._eval_fade(valid_df, direction)
        elif archetype == "SHAKEOUT":
            return cls._eval_shakeout(valid_df, direction)

        return {"win_rate": 0, "n_trades": 0, "viable": False}

    @staticmethod
    def _eval_momentum(df: pl.DataFrame, direction: str) -> Dict:
        """Standard ORB: enter on break, TP at tp_mult * OR_WIDTH."""
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_tp_up").is_not_null() &
                (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") < pl.col("time_sl_up")))
            ).height
            losses = trades.filter(
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") <= pl.col("time_tp_up")))
            ).height
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_tp_down").is_not_null() &
                (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") < pl.col("time_sl_down")))
            ).height
            losses = trades.filter(
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") <= pl.col("time_tp_down")))
            ).height

        n = wins + losses
        if n == 0:
            return {"win_rate": 0, "n_trades": 0, "viable": False}
        wr = wins / n
        return {"win_rate": wr, "n_trades": n, "wins": wins, "losses": losses, "viable": True}

    @staticmethod
    def _eval_fade(df: pl.DataFrame, direction: str) -> Dict:
        """
        Fade: go AGAINST the breakout. Win when original breakout fails (hits SL).
        R:R = 1:1 (both TP and SL are 1x OR_WIDTH from entry).
        """
        if direction == "UP":
            # Fade UP = SHORT when price breaks UP. Win if price returns to OR_LOW.
            trades = df.filter(pl.col("first_break_dir") == "UP")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            # Win = original breakout hit SL (false breakout)
            wins = trades.filter(
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
            ).height
            losses = trades.filter(
                pl.col("time_tp_up").is_not_null() &
                (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") <= pl.col("time_sl_up")))
            ).height
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            if trades.height == 0:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = trades.filter(
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
            ).height
            losses = trades.filter(
                pl.col("time_tp_down").is_not_null() &
                (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_sl_down")))
            ).height

        n = wins + losses
        if n == 0:
            return {"win_rate": 0, "n_trades": 0, "viable": False}
        wr = wins / n
        return {"win_rate": wr, "n_trades": n, "wins": wins, "losses": losses,
                "r_per_win": 1.0, "r_per_loss": -1.0, "viable": True}

    @staticmethod
    def _eval_shakeout(df: pl.DataFrame, direction: str) -> Dict:
        """
        Shakeout: after false breakout, re-enter in original direction.
        Entry after SL hit. Win if price re-breaks with >= 1x OR extension.
        R:R = 1:1 (entry at OR edge after SL, TP at 1x OR extension, SL at opposite OR edge).
        """
        if direction == "UP":
            # False breakout UP days (broke UP, hit SL at OR_LOW)
            false_days = df.filter(
                (pl.col("first_break_dir") == "UP") &
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
            )
            if false_days.height == 0 or "pf_up_rebreak_1x" not in df.columns:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            # Filter to days with post-fade data
            pf_days = false_days.filter(pl.col("pf_up_max_reversal_up").is_not_null())
            if pf_days.height < 10:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = pf_days.filter(pl.col("pf_up_rebreak_1x") == True).height
            losses = pf_days.height - wins
        else:
            false_days = df.filter(
                (pl.col("first_break_dir") == "DOWN") &
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
            )
            if false_days.height == 0 or "pf_down_rebreak_1x" not in df.columns:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            pf_days = false_days.filter(pl.col("pf_down_max_reversal_down").is_not_null())
            if pf_days.height < 10:
                return {"win_rate": 0, "n_trades": 0, "viable": False}
            wins = pf_days.filter(pl.col("pf_down_rebreak_1x") == True).height
            losses = pf_days.height - wins

        n = wins + losses
        wr = wins / n if n > 0 else 0
        return {"win_rate": wr, "n_trades": n, "wins": wins, "losses": losses,
                "r_per_win": 1.0, "r_per_loss": -1.0, "viable": True}

    @classmethod
    def scan_asset(cls, symbol: str, stats_by_combo: Dict[str, pl.DataFrame],
                   combo_meta: List[Dict]) -> List[Dict]:
        """
        Scan all strategy permutations for one asset.
        stats_by_combo: {combo_key: stats_df} where combo_key = "session_dur"
        combo_meta: list of {session_name, time_start, duration}
        Returns list of dicts with strategy definition + evaluation metrics, sorted by win_rate desc.
        """
        all_strategies = []

        for meta in combo_meta:
            key = f"{meta['session_name']}_{meta['duration']}"
            stats_df = stats_by_combo.get(key)
            if stats_df is None:
                continue

            for arch in cls.ARCHETYPES:
                for direction in cls.DIRECTIONS:
                    # Base strategy (no context filter)
                    result = cls.evaluate_archetype(stats_df, arch, direction)
                    if result.get("viable") and result["n_trades"] >= cls.MIN_DAYS:
                        all_strategies.append({
                            "symbol": symbol,
                            "session_name": meta["session_name"],
                            "time_start": meta["time_start"],
                            "duration": meta["duration"],
                            "archetype": f"{arch}_{direction}",
                            "direction": direction,
                            "context_filter": None,
                            "context_label": "BASE",
                            "win_rate": result["win_rate"],
                            "n_trades": result["n_trades"],
                            "wins": result.get("wins", 0),
                            "losses": result.get("losses", 0),
                        })

                    # With each context filter
                    for filt_key, filt_def in cls.CONTEXT_FILTERS.items():
                        result = cls.evaluate_archetype(stats_df, arch, direction, filt_def)
                        if result.get("viable") and result["n_trades"] >= cls.MIN_DAYS:
                            all_strategies.append({
                                "symbol": symbol,
                                "session_name": meta["session_name"],
                                "time_start": meta["time_start"],
                                "duration": meta["duration"],
                                "archetype": f"{arch}_{direction}",
                                "direction": direction,
                                "context_filter": filt_def,
                                "context_label": filt_def["label"],
                                "win_rate": result["win_rate"],
                                "n_trades": result["n_trades"],
                                "wins": result.get("wins", 0),
                                "losses": result.get("losses", 0),
                            })

        # Sort by win_rate descending
        all_strategies.sort(key=lambda x: x["win_rate"], reverse=True)
        return all_strategies
```

- [ ] **Step 2: Commit**

```bash
git add src/engine/strategy_scanner.py
git commit -m "feat: add StrategyScanner for exhaustive permutation evaluation"
```

---

### Task 3: Create the Quant Team Strategy Selector

Selects top 3 strategies per asset using quant team logic: WR priority, complementarity, diversification.

**Files:**
- Create: `src/engine/strategy_selector.py`

- [ ] **Step 1: Create the selector module**

```python
from typing import List, Dict


class StrategySelector:
    """
    Quant team logic: select max 3 strategies per asset.
    Priorities:
    1. WR >= 65% (hard prefer, but take best available if none meet threshold)
    2. Diversification: prefer different archetypes or sessions
    3. Complementarity: strategies that cover different market conditions
    4. Statistical significance: prefer more trades
    """

    TARGET_WR = 0.65
    MAX_STRATEGIES = 3
    MIN_TRADES_FOR_SELECTION = 30

    @classmethod
    def select_top_strategies(cls, candidates: List[Dict]) -> List[Dict]:
        """
        From a sorted (by WR desc) list of strategy candidates, select max 3
        that are diverse and complementary.
        """
        if not candidates:
            return []

        # Filter to minimum trade count
        viable = [c for c in candidates if c["n_trades"] >= cls.MIN_TRADES_FOR_SELECTION]
        if not viable:
            return []

        # Separate above and below target WR
        above_target = [c for c in viable if c["win_rate"] >= cls.TARGET_WR]
        below_target = [c for c in viable if c["win_rate"] < cls.TARGET_WR]

        selected = []
        used_archetypes = set()
        used_sessions = set()
        used_directions = set()

        def _diversity_score(candidate: Dict) -> float:
            """Higher score = more diverse from already selected strategies."""
            score = candidate["win_rate"] * 100  # Base: WR
            arch = candidate["archetype"]
            sess = candidate["session_name"]
            dirn = candidate["direction"]

            # Bonus for new archetype
            if arch not in used_archetypes:
                score += 10
            # Bonus for new session
            if sess not in used_sessions:
                score += 5
            # Bonus for new direction (UP vs DOWN coverage)
            if dirn not in used_directions:
                score += 5
            # Bonus for statistical significance
            score += min(candidate["n_trades"] / 100, 5)
            # Penalty for same archetype+session+direction (near-duplicate)
            key = f"{arch}_{sess}_{dirn}"
            for s in selected:
                if f"{s['archetype']}_{s['session_name']}_{s['direction']}" == key:
                    score -= 20
            return score

        # First pass: select from above-target candidates with diversity
        pool = above_target if above_target else below_target
        while len(selected) < cls.MAX_STRATEGIES and pool:
            # Score each remaining candidate
            scored = [(c, _diversity_score(c)) for c in pool]
            scored.sort(key=lambda x: x[1], reverse=True)
            best = scored[0][0]

            selected.append(best)
            used_archetypes.add(best["archetype"])
            used_sessions.add(best["session_name"])
            used_directions.add(best["direction"])
            pool.remove(best)

        # If we still have room and there were above-target candidates,
        # also look at below-target ones that complement
        if len(selected) < cls.MAX_STRATEGIES and above_target and below_target:
            for candidate in below_target:
                if len(selected) >= cls.MAX_STRATEGIES:
                    break
                # Only add if it brings something new
                arch = candidate["archetype"]
                sess = candidate["session_name"]
                if arch not in used_archetypes or sess not in used_sessions:
                    if candidate["win_rate"] >= 0.55:  # At least 55%
                        selected.append(candidate)
                        used_archetypes.add(arch)
                        used_sessions.add(sess)

        return selected

    @classmethod
    def explain_selection(cls, selected: List[Dict], all_candidates: List[Dict]) -> str:
        """Generate a quant team explanation of the selection rationale."""
        md = ""
        total_scanned = len(all_candidates)
        above_65 = sum(1 for c in all_candidates if c["win_rate"] >= cls.TARGET_WR)

        md += f"**Estrategias escaneadas:** {total_scanned}\n"
        md += f"**Con WR >= 65%:** {above_65}\n"
        md += f"**Seleccionadas:** {len(selected)}\n\n"

        if not selected:
            md += "> No se encontraron estrategias viables para este activo.\n"
            return md

        for i, s in enumerate(selected, 1):
            ctx = s.get("context_label", "BASE")
            md += f"**Estrategia #{i}:** {s['archetype']} | {s['session_name']} {s['duration']}m | {ctx}\n"
            md += f"- WR: `{s['win_rate']:.2%}` | Trades: `{s['n_trades']}` | W/L: `{s['wins']}/{s['losses']}`\n"

            # Explain why selected
            reasons = []
            if s["win_rate"] >= cls.TARGET_WR:
                reasons.append("WR supera umbral 65%")
            if i == 1:
                reasons.append("Mejor WR del activo")
            if s["n_trades"] >= 200:
                reasons.append(f"Alta significancia estadistica (N={s['n_trades']})")
            if s.get("context_label") != "BASE":
                reasons.append(f"Filtro contextual activo: {ctx}")
            md += f"- Razon: {', '.join(reasons)}\n\n"

        return md
```

- [ ] **Step 2: Commit**

```bash
git add src/engine/strategy_selector.py
git commit -m "feat: add StrategySelector with quant team diversity logic"
```

---

### Task 4: Create the Strategy Backtester

Full per-day backtest simulation for each archetype, producing equity curves, PF, max DD, yearly stats.

**Files:**
- Create: `src/engine/strategy_backtester.py`

- [ ] **Step 1: Create the backtester module**

```python
import polars as pl
import numpy as np
from typing import Dict, List, Optional
from src.domain.strategy_models import StrategyDef, StrategyResult
from src.engine.strategy_scanner import StrategyScanner


class StrategyBacktester:
    """
    Runs full backtest simulation for a given strategy definition.
    Produces equity curve, yearly breakdown, and all standard metrics.
    """

    @classmethod
    def backtest(cls, strategy: StrategyDef, stats_df: pl.DataFrame,
                 context_filter: Optional[Dict] = None) -> StrategyResult:
        """
        Run a day-by-day backtest for the strategy on the given stats_df.
        """
        valid_df = stats_df.filter(
            pl.col("first_break_dir").is_not_null() &
            pl.col("or_atr_ratio").is_between(0.1, 0.8)
        ).sort("trade_date")

        # Apply context filter
        if context_filter:
            valid_df = StrategyScanner.apply_context_filter(valid_df, context_filter)

        # Compute r_multiple for each day based on archetype
        base_arch = strategy.archetype.replace("_UP", "").replace("_DOWN", "")
        direction = strategy.direction

        trade_log = cls._compute_trades(valid_df, base_arch, direction, strategy.tp_multiplier)

        if trade_log.height == 0:
            return StrategyResult(strategy=strategy)

        # Calculate all metrics
        result = cls._compute_metrics(strategy, trade_log)
        return result

    @classmethod
    def _compute_trades(cls, df: pl.DataFrame, archetype: str,
                        direction: str, tp_mult: float) -> pl.DataFrame:
        """Compute per-day r_multiple based on archetype."""

        if archetype == "MOMENTUM":
            return cls._trades_momentum(df, direction, tp_mult)
        elif archetype == "FADE":
            return cls._trades_fade(df, direction)
        elif archetype == "SHAKEOUT":
            return cls._trades_shakeout(df, direction)
        return pl.DataFrame()

    @staticmethod
    def _trades_momentum(df: pl.DataFrame, direction: str, tp_mult: float) -> pl.DataFrame:
        """Standard ORB momentum trades."""
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_tp_up").is_not_null() &
                    (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") < pl.col("time_sl_up")))
                ).then(tp_mult)
                .when(
                    pl.col("time_sl_up").is_not_null() &
                    (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") <= pl.col("time_tp_up")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_tp_down").is_not_null() &
                    (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") < pl.col("time_sl_down")))
                ).then(tp_mult)
                .when(
                    pl.col("time_sl_down").is_not_null() &
                    (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") <= pl.col("time_tp_down")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        return trades.filter(pl.col("r_multiple") != 0.0).select(["trade_date", "r_multiple"])

    @staticmethod
    def _trades_fade(df: pl.DataFrame, direction: str) -> pl.DataFrame:
        """Fade trades: go against the breakout. R:R = 1:1."""
        if direction == "UP":
            trades = df.filter(pl.col("first_break_dir") == "UP")
            # Win when original breakout fails (SL hit = our TP)
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_sl_up").is_not_null() &
                    (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up")))
                ).then(1.0)
                .when(
                    pl.col("time_tp_up").is_not_null() &
                    (pl.col("time_sl_up").is_null() | (pl.col("time_tp_up") <= pl.col("time_sl_up")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        else:
            trades = df.filter(pl.col("first_break_dir") == "DOWN")
            trades = trades.with_columns(
                pl.when(
                    pl.col("time_sl_down").is_not_null() &
                    (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down")))
                ).then(1.0)
                .when(
                    pl.col("time_tp_down").is_not_null() &
                    (pl.col("time_sl_down").is_null() | (pl.col("time_tp_down") <= pl.col("time_sl_down")))
                ).then(-1.0)
                .otherwise(0.0)
                .alias("r_multiple")
            )
        return trades.filter(pl.col("r_multiple") != 0.0).select(["trade_date", "r_multiple"])

    @staticmethod
    def _trades_shakeout(df: pl.DataFrame, direction: str) -> pl.DataFrame:
        """Shakeout: re-enter after false breakout. R:R = 1:1."""
        if direction == "UP":
            # Only false breakout UP days with post-fade data
            if "pf_up_rebreak_1x" not in df.columns:
                return pl.DataFrame()
            trades = df.filter(
                (pl.col("first_break_dir") == "UP") &
                pl.col("time_sl_up").is_not_null() &
                (pl.col("time_tp_up").is_null() | (pl.col("time_sl_up") < pl.col("time_tp_up"))) &
                pl.col("pf_up_max_reversal_up").is_not_null()
            )
            trades = trades.with_columns(
                pl.when(pl.col("pf_up_rebreak_1x") == True)
                .then(1.0)
                .otherwise(-1.0)
                .alias("r_multiple")
            )
        else:
            if "pf_down_rebreak_1x" not in df.columns:
                return pl.DataFrame()
            trades = df.filter(
                (pl.col("first_break_dir") == "DOWN") &
                pl.col("time_sl_down").is_not_null() &
                (pl.col("time_tp_down").is_null() | (pl.col("time_sl_down") < pl.col("time_tp_down"))) &
                pl.col("pf_down_max_reversal_down").is_not_null()
            )
            trades = trades.with_columns(
                pl.when(pl.col("pf_down_rebreak_1x") == True)
                .then(1.0)
                .otherwise(-1.0)
                .alias("r_multiple")
            )
        return trades.filter(pl.col("r_multiple") != 0.0).select(["trade_date", "r_multiple"])

    @classmethod
    def _compute_metrics(cls, strategy: StrategyDef, trade_log: pl.DataFrame) -> StrategyResult:
        """Compute all metrics from a trade log."""
        trades = trade_log.sort("trade_date")
        r_vals = trades["r_multiple"].to_list()
        dates = trades["trade_date"].to_list()

        total = len(r_vals)
        wins = sum(1 for r in r_vals if r > 0)
        losses = sum(1 for r in r_vals if r < 0)
        wr = wins / total if total > 0 else 0

        gross_profit = sum(r for r in r_vals if r > 0)
        gross_loss = abs(sum(r for r in r_vals if r < 0))
        pf = gross_profit / gross_loss if gross_loss > 0 else float("inf")

        net_r = sum(r_vals)
        avg_r = net_r / total if total > 0 else 0

        # Max Drawdown
        cumulative = np.cumsum(r_vals)
        peak = np.maximum.accumulate(cumulative)
        dd = cumulative - peak
        max_dd = float(np.min(dd)) if len(dd) > 0 else 0

        # Sharpe (annualized, assuming ~252 trading days/year)
        if len(r_vals) > 1:
            mean_r = np.mean(r_vals)
            std_r = np.std(r_vals, ddof=1)
            sharpe = (mean_r / std_r) * np.sqrt(252) if std_r > 0 else 0
        else:
            sharpe = 0

        # Trades per year
        if dates:
            first_date = min(dates)
            last_date = max(dates)
            days_span = (last_date - first_date).days if hasattr(last_date - first_date, 'days') else 1
            years = max(days_span / 365.25, 0.1)
            tpy = total / years
        else:
            tpy = 0
            years = 0

        # Yearly breakdown
        trades_pd = trades.with_columns(
            pl.col("trade_date").cast(pl.Date).dt.year().alias("year")
        )
        yearly_stats = {}
        for year_row in trades_pd.group_by("year").agg([
            pl.col("r_multiple").count().alias("n"),
            pl.col("r_multiple").filter(pl.col("r_multiple") > 0).count().alias("w"),
            pl.col("r_multiple").sum().alias("net"),
        ]).sort("year").iter_rows(named=True):
            yr = year_row["year"]
            n = year_row["n"]
            w = year_row["w"]
            yearly_stats[str(yr)] = {
                "trades": n,
                "wins": w,
                "wr": w / n if n > 0 else 0,
                "net_r": year_row["net"],
            }

        best_yr = max(yearly_stats, key=lambda y: yearly_stats[y]["net_r"]) if yearly_stats else ""
        worst_yr = min(yearly_stats, key=lambda y: yearly_stats[y]["net_r"]) if yearly_stats else ""

        passes = wr >= 0.65 and tpy >= 100 and pf > 1.0

        return StrategyResult(
            strategy=strategy,
            total_trades=total,
            trades_per_year=tpy,
            win_rate=wr,
            profit_factor=pf,
            net_r=net_r,
            max_drawdown=max_dd,
            sharpe=sharpe,
            avg_r_per_trade=avg_r,
            best_year=best_yr,
            worst_year=worst_yr,
            yearly_stats=yearly_stats,
            passes_filter=passes,
        )

    @classmethod
    def backtest_group(cls, strategies: List[StrategyDef],
                       stats_dfs: Dict[str, pl.DataFrame],
                       context_filters: List[Optional[Dict]]) -> StrategyResult:
        """
        Run a combined backtest of multiple strategies (group per asset).
        Merges all trade logs by date and computes combined metrics.
        """
        all_trades = []
        for strat, ctx in zip(strategies, context_filters):
            key = f"{strat.session_name}_{strat.duration}"
            stats_df = stats_dfs.get(key)
            if stats_df is None:
                continue
            result = cls.backtest(strat, stats_df, ctx)
            if result.total_trades > 0:
                # Re-run to get the trade log
                valid_df = stats_df.filter(
                    pl.col("first_break_dir").is_not_null() &
                    pl.col("or_atr_ratio").is_between(0.1, 0.8)
                ).sort("trade_date")
                if ctx:
                    valid_df = StrategyScanner.apply_context_filter(valid_df, ctx)
                base_arch = strat.archetype.replace("_UP", "").replace("_DOWN", "")
                log = cls._compute_trades(valid_df, base_arch, strat.direction, strat.tp_multiplier)
                if log.height > 0:
                    all_trades.append(log)

        if not all_trades:
            group_strat = StrategyDef(
                symbol=strategies[0].symbol if strategies else "UNKNOWN",
                session_name="GROUP", time_start="", duration=0,
                archetype="GROUP", direction="ALL"
            )
            return StrategyResult(strategy=group_strat)

        combined = pl.concat(all_trades).sort("trade_date")
        # Deduplicate: if same date has multiple trades, keep all (they're different strategies)
        group_strat = StrategyDef(
            symbol=strategies[0].symbol,
            session_name="GROUP", time_start="", duration=0,
            archetype="GROUP", direction="ALL",
            label=f"{strategies[0].symbol} GRUPO ({len(strategies)} estrategias)"
        )
        return cls._compute_metrics(group_strat, combined)
```

- [ ] **Step 2: Commit**

```bash
git add src/engine/strategy_backtester.py
git commit -m "feat: add StrategyBacktester with archetype-aware trade simulation"
```

---

### Task 5: Create the Strategy Report Generator

Generates per-strategy markdown reports with all metrics, yearly breakdown, and quant team commentary.

**Files:**
- Create: `src/engine/strategy_reporter.py`

- [ ] **Step 1: Create the reporter module**

```python
import os
from typing import List, Dict
from src.domain.strategy_models import StrategyDef, StrategyResult
from src.engine.strategy_selector import StrategySelector


class StrategyReporter:
    """Generates markdown reports per strategy and per asset group."""

    def __init__(self, reports_dir: str):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)

    def write_strategy_report(self, result: StrategyResult) -> str:
        """Write a full markdown report for a single strategy. Returns file path."""
        s = result.strategy
        filename = f"{s.symbol}_{s.archetype}_{s.session_name}_{s.duration}m"
        if s.context_filter:
            ctx_label = s.context_filter.get("label", "filtered")
            filename += f"_{ctx_label}"
        filename = filename.replace(" ", "_").replace("/", "_") + "_Strategy.md"
        filepath = os.path.join(self.reports_dir, filename)

        md = self._build_strategy_md(result)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        return filepath

    def write_asset_summary(self, symbol: str, individual_results: List[StrategyResult],
                            group_result: StrategyResult,
                            selection_explanation: str,
                            all_candidates: List[Dict]) -> str:
        """Write a summary report for all strategies of one asset."""
        filepath = os.path.join(self.reports_dir, f"{symbol}_Strategy_Summary.md")
        md = self._build_asset_summary_md(symbol, individual_results, group_result,
                                           selection_explanation, all_candidates)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        return filepath

    def _build_strategy_md(self, result: StrategyResult) -> str:
        s = result.strategy
        status = "APROBADA" if result.passes_filter else "NO APROBADA"
        status_icon = "+" if result.passes_filter else "-"

        md = f"# Reporte de Estrategia: {s.label}\n\n"
        md += f"**Status:** `[{status}]`\n\n"

        # Strategy definition
        md += "## Definicion de la Estrategia\n\n"
        md += f"| Parametro | Valor |\n"
        md += f"| --- | --- |\n"
        md += f"| Activo | {s.symbol} |\n"
        md += f"| Sesion | {s.session_name} ({s.time_start} UTC) |\n"
        md += f"| Duracion OR | {s.duration} minutos |\n"
        md += f"| Arquetipo | {s.archetype} |\n"
        md += f"| Direccion | {s.direction} |\n"
        md += f"| TP Multiplier | {s.tp_multiplier}x OR |\n"
        if s.context_filter:
            md += f"| Filtro Contextual | `{s.context_filter.get('label', str(s.context_filter))}` |\n"
        md += "\n"

        # Logic explanation
        md += "### Logica de Ejecucion\n\n"
        base_arch = s.archetype.replace("_UP", "").replace("_DOWN", "")
        if base_arch == "MOMENTUM":
            md += f"Entrada en la rotura {'alcista' if s.direction == 'UP' else 'bajista'} del Opening Range. "
            md += f"TP fijo a {s.tp_multiplier}x OR width. SL en el extremo opuesto del OR (1R riesgo).\n\n"
        elif base_arch == "FADE":
            md += f"Entrada CONTRA la rotura {'alcista' if s.direction == 'UP' else 'bajista'}. "
            md += "Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. "
            md += "TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.\n\n"
        elif base_arch == "SHAKEOUT":
            md += f"Re-entrada {'LARGA' if s.direction == 'UP' else 'CORTA'} despues de un falso rompimiento. "
            md += "Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout "
            md += "apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.\n\n"

        if s.context_filter:
            md += f"**Filtro activo:** Solo opera cuando `{s.context_filter.get('col', '')} {s.context_filter.get('op', '')} {s.context_filter.get('val', '')}`\n\n"

        # Performance metrics
        md += "## Resultados del Backtest\n\n"
        md += "### Metricas Principales\n\n"
        md += f"| Metrica | Valor | Umbral |\n"
        md += f"| --- | --- | --- |\n"

        wr_icon = "pass" if result.win_rate >= 0.65 else "FAIL"
        tpy_icon = "pass" if result.trades_per_year >= 100 else "FAIL"
        pf_icon = "pass" if result.profit_factor > 1.0 else "FAIL"

        md += f"| Win Rate | `{result.win_rate:.2%}` | >= 65% [{wr_icon}] |\n"
        md += f"| Trades/Ano | `{result.trades_per_year:.1f}` | >= 100 [{tpy_icon}] |\n"
        md += f"| Profit Factor | `{result.profit_factor:.2f}` | > 1.0 [{pf_icon}] |\n"
        md += f"| Total Trades | `{result.total_trades}` | - |\n"
        md += f"| Net R | `{result.net_r:.2f}R` | - |\n"
        md += f"| R Promedio/Trade | `{result.avg_r_per_trade:.3f}R` | - |\n"
        md += f"| Max Drawdown | `{result.max_drawdown:.2f}R` | - |\n"
        md += f"| Sharpe (anualizado) | `{result.sharpe:.3f}` | - |\n"
        md += "\n"

        # Yearly breakdown
        if result.yearly_stats:
            md += "### Desglose Anual\n\n"
            md += "| Ano | Trades | Wins | WR | Net R |\n"
            md += "| --- | --- | --- | --- | --- |\n"
            for yr in sorted(result.yearly_stats.keys()):
                ys = result.yearly_stats[yr]
                yr_wr = ys["wr"]
                yr_icon = "+" if yr_wr >= 0.65 else ""
                md += f"| {yr} | {ys['trades']} | {ys['wins']} | `{yr_wr:.1%}`{yr_icon} | `{ys['net_r']:.1f}R` |\n"
            md += "\n"
            md += f"**Mejor ano:** {result.best_year} | **Peor ano:** {result.worst_year}\n\n"

        # Verdict
        md += "## Veredicto del Equipo Quant\n\n"
        if result.passes_filter:
            md += f"> **ESTRATEGIA APROBADA.** WR={result.win_rate:.1%}, PF={result.profit_factor:.2f}, "
            md += f"{result.trades_per_year:.0f} trades/ano. Edge consistente y explotable.\n"
        else:
            fails = []
            if result.win_rate < 0.65:
                fails.append(f"WR={result.win_rate:.1%} < 65%")
            if result.trades_per_year < 100:
                fails.append(f"Trades/ano={result.trades_per_year:.0f} < 100")
            if result.profit_factor <= 1.0:
                fails.append(f"PF={result.profit_factor:.2f} <= 1.0")
            md += f"> **ESTRATEGIA NO APROBADA.** Falla en: {', '.join(fails)}. "
            md += "Se documenta para referencia pero no se recomienda para operacion.\n"

        md += "\n---\n*Generado por KHA0SYS3 Strategy Pipeline*\n"
        return md

    def _build_asset_summary_md(self, symbol: str, results: List[StrategyResult],
                                 group_result: StrategyResult,
                                 selection_explanation: str,
                                 all_candidates: List[Dict]) -> str:
        md = f"# Resumen de Estrategias: {symbol}\n\n"

        # Selection rationale
        md += "## Seleccion del Equipo Quant\n\n"
        md += selection_explanation + "\n"

        # Individual results summary
        md += "## Resultados Individuales\n\n"
        md += "| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |\n"
        md += "| --- | --- | --- | --- | --- | --- | --- |\n"
        for i, r in enumerate(results, 1):
            status = "APROBADA" if r.passes_filter else "NO APROBADA"
            md += f"| {i} | {r.strategy.archetype} {r.strategy.session_name} {r.strategy.duration}m | "
            md += f"`{r.win_rate:.1%}` | `{r.profit_factor:.2f}` | `{r.trades_per_year:.0f}` | "
            md += f"`{r.net_r:.1f}R` | {status} |\n"
        md += "\n"

        # Group result
        md += "## Resultado Grupal (todas las estrategias combinadas)\n\n"
        if group_result.total_trades > 0:
            md += f"| Metrica | Valor |\n"
            md += f"| --- | --- |\n"
            md += f"| Total Trades | `{group_result.total_trades}` |\n"
            md += f"| Trades/Ano | `{group_result.trades_per_year:.1f}` |\n"
            md += f"| Win Rate | `{group_result.win_rate:.2%}` |\n"
            md += f"| Profit Factor | `{group_result.profit_factor:.2f}` |\n"
            md += f"| Net R | `{group_result.net_r:.2f}R` |\n"
            md += f"| Max Drawdown | `{group_result.max_drawdown:.2f}R` |\n"
            md += f"| Sharpe | `{group_result.sharpe:.3f}` |\n"
        else:
            md += "> No se pudieron combinar las estrategias (sin trades validos).\n"

        md += "\n"

        # Top 10 candidates that didn't make the cut
        md += "## Top 10 Candidatos Descartados\n\n"
        selected_archs = set()
        for r in results:
            selected_archs.add(f"{r.strategy.archetype}_{r.strategy.session_name}_{r.strategy.duration}")

        discarded = [c for c in all_candidates
                     if f"{c['archetype']}_{c['session_name']}_{c['duration']}" not in selected_archs][:10]
        if discarded:
            md += "| Estrategia | WR | Trades | Razon |\n"
            md += "| --- | --- | --- | --- |\n"
            for c in discarded:
                reason = "Menor WR" if c["win_rate"] < 0.65 else "Duplicado/No complementaria"
                md += f"| {c['archetype']} {c['session_name']} {c['duration']}m {c.get('context_label', '')} | "
                md += f"`{c['win_rate']:.1%}` | {c['n_trades']} | {reason} |\n"
        else:
            md += "> No hay candidatos adicionales.\n"

        md += "\n---\n*Generado por KHA0SYS3 Strategy Pipeline*\n"
        return md
```

- [ ] **Step 2: Commit**

```bash
git add src/engine/strategy_reporter.py
git commit -m "feat: add StrategyReporter for per-strategy and asset summary reports"
```

---

### Task 6: Create the Main Pipeline Runner

Orchestrates the full flow: load data, scan, select, backtest, report.

**Files:**
- Create: `src/engine/run_strategy_pipeline.py`

- [ ] **Step 1: Create the pipeline runner**

```python
import json
import os
from pathlib import Path
from typing import Dict, List

import polars as pl

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.domain.strategy_models import StrategyDef
from src.engine.strategy_scanner import StrategyScanner
from src.engine.strategy_selector import StrategySelector
from src.engine.strategy_backtester import StrategyBacktester
from src.engine.strategy_reporter import StrategyReporter


class StrategyPipeline:
    """
    Full pipeline: for each asset, scan strategies, select top 3,
    backtest individually and as group, generate reports.
    """

    DURATIONS = [15, 30, 45, 60]

    def __init__(self, data_dir: str, config_path: str, reports_dir: str):
        self.data_dir = data_dir
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
        self.reporter = StrategyReporter(reports_dir)

    def run_all(self):
        """Run the full pipeline for all assets."""
        master_summary = []

        for symbol in self.config:
            print(f"\n{'='*60}")
            print(f"  Processing: {symbol}")
            print(f"{'='*60}")

            try:
                asset_result = self.run_asset(symbol)
                master_summary.append(asset_result)
            except Exception as e:
                print(f"  ERROR processing {symbol}: {e}")
                import traceback
                traceback.print_exc()

        # Write master summary
        self._write_master_summary(master_summary)
        print(f"\nPipeline complete. Reports in: {self.reports_dir}")

    def run_asset(self, symbol: str) -> Dict:
        """Run the full pipeline for one asset."""
        cfg = self.config[symbol]

        # Step 1: Load and enrich data
        print(f"  [1/5] Loading and enriching data...")
        df_raw = self.loader.load_data(symbol, "M15")
        df_raw = DataEnricher.enrich_with_rsi(df_raw)
        df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])

        sessions = cfg.get("sessions", [])

        # Step 2: Build stats_df for each session x duration combo
        print(f"  [2/5] Building stats for {len(sessions)} sessions x {len(self.DURATIONS)} durations...")
        stats_by_combo = {}
        combo_meta = []

        for sess in sessions:
            for dur in self.DURATIONS:
                key = f"{sess['name']}_{dur}"
                try:
                    stats_df = self._build_stats(df_enriched, sess["time_start"], dur)
                    if stats_df is not None and stats_df.height > 0:
                        stats_by_combo[key] = stats_df
                        combo_meta.append({
                            "session_name": sess["name"],
                            "time_start": sess["time_start"],
                            "duration": dur,
                        })
                except Exception:
                    pass

        if not stats_by_combo:
            print(f"  No valid combos for {symbol}. Skipping.")
            return {"symbol": symbol, "strategies": [], "status": "NO_DATA"}

        # Step 3: Scan all strategy permutations
        print(f"  [3/5] Scanning strategy permutations...")
        all_candidates = StrategyScanner.scan_asset(symbol, stats_by_combo, combo_meta)
        print(f"  Found {len(all_candidates)} viable candidates. Top 5 WR:")
        for c in all_candidates[:5]:
            print(f"    {c['archetype']} {c['session_name']} {c['duration']}m "
                  f"{c.get('context_label', 'BASE')} -> WR={c['win_rate']:.2%} N={c['n_trades']}")

        # Step 4: Select top 3
        print(f"  [4/5] Quant team selecting top strategies...")
        selected = StrategySelector.select_top_strategies(all_candidates)
        selection_explanation = StrategySelector.explain_selection(selected, all_candidates)
        print(f"  Selected {len(selected)} strategies.")

        # Step 5: Backtest each selected strategy
        print(f"  [5/5] Running backtests...")
        individual_results = []
        strategy_defs = []
        context_filters = []

        for sel in selected:
            strat = StrategyDef(
                symbol=symbol,
                session_name=sel["session_name"],
                time_start=sel["time_start"],
                duration=sel["duration"],
                archetype=sel["archetype"],
                direction=sel["direction"],
                context_filter=sel.get("context_filter"),
                tp_multiplier=1.5 if "MOMENTUM" in sel["archetype"] else 1.0,
            )
            strategy_defs.append(strat)
            context_filters.append(sel.get("context_filter"))

            key = f"{sel['session_name']}_{sel['duration']}"
            stats_df = stats_by_combo[key]
            result = StrategyBacktester.backtest(strat, stats_df, sel.get("context_filter"))
            individual_results.append(result)

            status = "PASS" if result.passes_filter else "FAIL"
            print(f"    [{status}] {strat.label} -> WR={result.win_rate:.2%} "
                  f"PF={result.profit_factor:.2f} T/Y={result.trades_per_year:.0f} "
                  f"NetR={result.net_r:.1f}")

            # Write individual report
            filepath = self.reporter.write_strategy_report(result)
            print(f"    Report: {filepath}")

        # Group backtest
        group_result = StrategyBacktester.backtest_group(
            strategy_defs, stats_by_combo, context_filters
        )
        if group_result.total_trades > 0:
            gs = "PASS" if group_result.passes_filter else "FAIL"
            print(f"  [GROUP {gs}] WR={group_result.win_rate:.2%} "
                  f"PF={group_result.profit_factor:.2f} NetR={group_result.net_r:.1f}")

        # Write asset summary
        summary_path = self.reporter.write_asset_summary(
            symbol, individual_results, group_result,
            selection_explanation, all_candidates
        )
        print(f"  Summary: {summary_path}")

        return {
            "symbol": symbol,
            "strategies": selected,
            "individual_results": individual_results,
            "group_result": group_result,
            "status": "OK",
        }

    def _build_stats(self, df_enriched: pl.DataFrame, time_start: str, duration: int) -> pl.DataFrame:
        """Build the enriched stats DataFrame for one session/duration combo."""
        df_or = DataEnricher.enrich_with_opening_range(df_enriched, time_start, duration)
        stats_df = TrackerEngine.track_events(df_or, tp_multiplier=1.5)

        # Collect feature columns
        agg_cols = [pl.col("or_open").first(), pl.col("pd_or_high").first(), pl.col("pd_or_low").first()]
        for col_name in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                          "atr_percentile", "or_position_vs_pd"]:
            if col_name in df_or.columns:
                agg_cols.append(pl.col(col_name).first())

        daily_base = df_or.group_by("trade_date").agg(agg_cols)
        expanded_stats = daily_base.join(stats_df, on="trade_date", how="left")

        # Post-fade tracking
        expanded_stats = TrackerEngine.track_post_fade_events(df_or, expanded_stats)

        return expanded_stats

    def _write_master_summary(self, all_results: List[Dict]):
        """Write a master summary across all assets."""
        filepath = os.path.join(self.reports_dir, "MASTER_Strategy_Summary.md")
        md = "# KHA0SYS3 - Master Strategy Selection Report\n\n"
        md += f"**Activos procesados:** {len(all_results)}\n\n"

        # Summary table
        md += "## Resumen Global\n\n"
        md += "| Activo | # Estrategias | Mejor WR | Mejor PF | Grupo WR | Grupo PF | Status |\n"
        md += "| --- | --- | --- | --- | --- | --- | --- |\n"

        total_approved = 0
        for r in all_results:
            sym = r["symbol"]
            strats = r.get("individual_results", [])
            group = r.get("group_result")
            n = len(strats)

            if strats:
                best_wr = max(s.win_rate for s in strats)
                best_pf = max(s.profit_factor for s in strats)
                approved = sum(1 for s in strats if s.passes_filter)
                total_approved += approved
            else:
                best_wr = 0
                best_pf = 0
                approved = 0

            g_wr = group.win_rate if group and group.total_trades > 0 else 0
            g_pf = group.profit_factor if group and group.total_trades > 0 else 0

            status = f"{approved}/{n} aprobadas" if n > 0 else "Sin estrategias"
            md += f"| {sym} | {n} | `{best_wr:.1%}` | `{best_pf:.2f}` | "
            md += f"`{g_wr:.1%}` | `{g_pf:.2f}` | {status} |\n"

        md += f"\n**Total estrategias aprobadas:** {total_approved}\n"
        md += "\n---\n*Generado por KHA0SYS3 Strategy Pipeline*\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"\nMaster summary: {filepath}")


if __name__ == "__main__":
    pipeline = StrategyPipeline(
        data_dir="c:/Proyectos/kha0sys3/data",
        config_path="c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json",
        reports_dir="c:/Proyectos/kha0sys3/reports/strategies",
    )
    pipeline.run_all()
```

- [ ] **Step 2: Commit**

```bash
git add src/engine/run_strategy_pipeline.py
git commit -m "feat: add StrategyPipeline runner - full scan/select/backtest/report flow"
```

---

### Task 7: Run the Pipeline for All 13 Assets

**Files:**
- No new files

- [ ] **Step 1: Run the pipeline**

```bash
cd c:/Proyectos/kha0sys3
python -m src.engine.run_strategy_pipeline
```

Expected output: Progress for each of 13 assets, followed by report file paths.

- [ ] **Step 2: Verify reports generated**

```bash
ls -la reports/strategies/
```

Expected: One `*_Strategy.md` per selected strategy (up to 39 files for 13 assets x 3), plus 13 `*_Strategy_Summary.md` files, plus 1 `MASTER_Strategy_Summary.md`.

- [ ] **Step 3: Review and fix any runtime errors**

If any asset fails, check the error output and fix the issue in the relevant module.

- [ ] **Step 4: Commit generated reports**

```bash
git add reports/strategies/
git commit -m "feat: generate strategy selection reports for all 13 assets"
```
