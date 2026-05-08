import io
import zipfile
from pathlib import Path
from unittest.mock import patch

import polars as pl
import pytest

from src.strategies_external.data_sources.cot_downloader import (
    download_cot, parse_cot_text, cot_index,
)


def test_parse_cot_text_extracts_commercials():
    sample = (
        "Market_and_Exchange_Names,Report_Date_as_YYYY-MM-DD,Producer_Merchant_Long_All,Producer_Merchant_Short_All\n"
        "GOLD - COMMODITY EXCHANGE INC.,2024-01-09,100000,80000\n"
        "GOLD - COMMODITY EXCHANGE INC.,2024-01-16,110000,90000\n"
    )
    df = parse_cot_text(sample, market_keyword="GOLD")
    assert df.shape[0] == 2
    assert df["net"].to_list() == [20000, 20000]


def test_cot_index_normalizes_to_0_100():
    series = pl.Series("net", [10, 20, 30, 40, 50])
    idx = cot_index(series, window=5)
    # Last value: (50 - 10) / (50 - 10) * 100 = 100
    assert idx.to_list()[-1] == pytest.approx(100.0)


def test_download_cot_writes_parquet(tmp_path: Path):
    """Mock the urllib download to avoid live HTTP."""
    fake_csv = (
        "Market_and_Exchange_Names,Report_Date_as_YYYY-MM-DD,Producer_Merchant_Long_All,Producer_Merchant_Short_All\n"
        "GOLD - COMMODITY EXCHANGE INC.,2024-01-09,100,80\n"
    )
    fake_zip = io.BytesIO()
    with zipfile.ZipFile(fake_zip, "w") as zf:
        zf.writestr("c_year.csv", fake_csv)
    fake_zip.seek(0)
    with patch("src.strategies_external.data_sources.cot_downloader.urlopen") as mock_urlopen:
        mock_urlopen.return_value = fake_zip
        out = download_cot(year=2024, market_keyword="GOLD",
                           output_dir=str(tmp_path))
    assert out.exists()
    df = pl.read_parquet(out)
    assert df.shape[0] == 1
