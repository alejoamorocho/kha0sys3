"""COT report downloader from cftc.gov."""

import io
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

import polars as pl


_CFTC_URL_TEMPLATE = (
    "https://www.cftc.gov/files/dea/history/com_disagg_txt_{year}.zip"
)
# cftc.gov rejects the default urllib User-Agent ("Python-urllib/X.Y") with
# HTTP 403 Forbidden. Spoof a real browser UA.
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def parse_cot_text(text: str, market_keyword: str) -> pl.DataFrame:
    """Parse COT CSV text; filter rows by market_keyword (case-insensitive)
    and return a polars DataFrame with columns: date, long, short, net.

    Tolerant parsing: read all columns as strings then cast long/short with
    `strict=False` so any non-numeric junk row becomes null and is dropped.
    """
    df = pl.read_csv(io.StringIO(text), infer_schema_length=0, ignore_errors=True)
    cols = df.columns
    name_col = next(c for c in cols if "market" in c.lower() and "name" in c.lower())
    date_col = next(c for c in cols if "report_date" in c.lower())
    # cftc.gov uses "Prod_Merc_Positions_Long_All" (Producer/Merchant abbreviated).
    # Pick the *_All variant to avoid the _Old/_Other futures-only splits.
    long_col = next(
        c for c in cols
        if "prod" in c.lower() and "long" in c.lower() and c.lower().endswith("_all")
    )
    short_col = next(
        c for c in cols
        if "prod" in c.lower() and "short" in c.lower() and c.lower().endswith("_all")
    )
    df = (
        df.filter(pl.col(name_col).str.contains(market_keyword, literal=True))
        .with_columns(
            pl.col(date_col).str.strip_chars().str.strptime(
                pl.Date, "%Y-%m-%d", strict=False
            ).alias("date"),
            pl.col(long_col).str.strip_chars().cast(pl.Int64, strict=False).alias("long"),
            pl.col(short_col).str.strip_chars().cast(pl.Int64, strict=False).alias("short"),
        )
        .drop_nulls(["date", "long", "short"])
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
    req = Request(url, headers={"User-Agent": _USER_AGENT})
    raw = urlopen(req)
    with zipfile.ZipFile(io.BytesIO(raw.read())) as zf:
        csv_name = next(n for n in zf.namelist() if n.endswith(".csv") or n.endswith(".txt"))
        with zf.open(csv_name) as f:
            text = f.read().decode("utf-8", errors="replace")
    df = parse_cot_text(text, market_keyword=market_keyword)
    safe = market_keyword.lower().replace(" ", "_").replace(",", "")
    path = Path(output_dir) / f"{safe}_{year}.parquet"
    df.write_parquet(path)
    return path
