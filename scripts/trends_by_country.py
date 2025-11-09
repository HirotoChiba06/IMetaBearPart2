import argparse
from pytrends.request import TrendReq
import pandas as pd
import time
from pathlib import Path

# ===== 引数処理 =====
parser = argparse.ArgumentParser()
parser.add_argument("--country", required=True, help="2-letter country code (e.g. KR, CN, US)")
parser.add_argument("--name", required=True, help="Country name (e.g. South Korea)")
args = parser.parse_args()

KEYWORD = "Japan travel"
COUNTRY_NAME = args.name
COUNTRY_CODE = args.country

START_DATE = "2005-01-01"
END_DATE = "2025-01-01"

output_dir = Path("data/trends")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"trends_japan_travel_{COUNTRY_CODE}.csv"

# ===== Google Trends 接続 =====
pytrends = TrendReq(hl="en-US", tz=540, timeout=(10,25), retries=2, backoff_factor=4)

print(f"📈 Fetching: {COUNTRY_NAME} ({COUNTRY_CODE}) ...")

try:
    pytrends.build_payload([KEYWORD], timeframe=f"{START_DATE} {END_DATE}", geo=COUNTRY_CODE)
    df = pytrends.interest_over_time()
    df = df.reset_index()[["date", KEYWORD]]
    df["country"] = COUNTRY_NAME
    df = df.rename(columns={KEYWORD: "trend_interest"})
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Saved: {output_file} ({len(df)} rows)")
except Exception as e:
    print(f"❌ Failed for {COUNTRY_NAME}: {e}")

time.sleep(15)