"""COT report downloader from cftc.gov."""

import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import polars as pl


_CFTC_URL_TEMPLATE = (
    "https://www.cftc.gov/files/dea/history/com_disagg_txt_{year}.zip"
)


def parse_cot_text(text: str, market_keyword: str) -> pl.DataFrame:
    """Parse COT CSV text; filter rows by market_keyword (case-insensitive)
    and return a polars DataFrame with columns: date, long, short, net."""
    df = pl.read_csv(io.StringIO(text))
    cols = df.columns
    name_col = next(c for c in cols if "market" in c.lower() and "name" in c.lower())
    date_col = next(c for c in cols if "report_date" in c.lower())
    long_col = next(c for c in cols if "producer" in c.lower() and "long" in c.lower())
    short_col = next(c for c in cols if "producer" in c.lower() and "short" in c.lower())
    df = (
        df.filter(pl.col(name_col).str.contains(market_keyword, literal=True))
        .with_columns(
            pl.col(date_col).str.strptime(pl.Date, "%Y-%m-%d", strict=False).alias("date"),
            pl.col(long_col).cast(pl.Int64).alias("long"),
            pl.col(short_col).cast(pl.Int64).alias("short"),
        )
        .with_columns((pl.col("long") - pl.col("short")).alias("net"))
        .select(["date", "long", "short", "net"])
        .sort("date")
    )
    return df


def cot_index(net_positions: pl.Series, window: int = 26) -> pl.Series:
    rolling_min = net_positions.rolling_min(window)
    rolling_max = net_positions.rolling_max(window)
    return 100.0 * (net_positions - rolling_min) / (rolling_max - rolling_min).replace(0, 1)


def download_cot(
    year: int, market_keyword: str, output_dir: str = "data/cot"
) -> Path:
    """Download Disaggregated COT report for a year and persist parsed parquet.

    Returns path to the saved parquet.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    url = _CFTC_URL_TEMPLATE.format(year=year)
    raw = urlopen(url)
    with zipfile.ZipFile(io.BytesIO(raw.read())) as zf:
        csv_name = next(n for n in zf.namelist() if n.endswith(".csv") or n.endswith(".txt"))
        with zf.open(csv_name) as f:
            text = f.read().decode("utf-8", errors="replace")
    df = parse_cot_text(text, market_keyword=market_keyword)
    safe = market_keyword.lower().replace(" ", "_").replace(",", "")
    path = Path(output_dir) / f"{safe}_{year}.parquet"
    df.write_parquet(path)
    return path
