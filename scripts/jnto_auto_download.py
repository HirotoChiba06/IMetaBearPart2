"""
JNTO データ自動ダウンロードスクリプト (requests版)
申請やSeleniumを使わず、Tableau Publicから直接CSVを取得。
"""

import time
import urllib.parse
from pathlib import Path
import pandas as pd
import requests
from io import StringIO

# ===== 設定 =====
BASE_URL = "https://public.tableau.com/views/3_1_Visitor_arrivals/CSV_3__2_3__1.csv"
OUTPUT_DIR = Path("data/jnto/monthly_auto")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===== 単一月のデータ取得 =====
def fetch_csv(year: int, month: int):
    params = {
        ":showVizHome": "no",
        "年 ": str(year),
        "月": str(month),
        "暫定値フラグ": "確定値,暫定値"
    }

    url = f"{BASE_URL}?{urllib.parse.urlencode(params, safe=',:')}"
    print(f"📥 Fetching {year}-{month:02d} ...")

    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()  # ステータスコードチェック

        # StringIOでテキストをCSV化
        df = pd.read_csv(StringIO(res.text), encoding="utf-8-sig")

        # 保存
        fname = OUTPUT_DIR / f"visitor_{year}_{month:02d}.csv"
        df.to_csv(fname, index=False, encoding="utf-8-sig")
        print(f"✅ {fname.name} saved ({len(df)} rows)")
        return True
    except Exception as e:
        print(f"❌ {year}-{month:02d} failed: {e}")
        return False


# ===== 範囲指定で自動DL =====
def fetch_range(start_year=2005, end_year=2025):
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            success = fetch_csv(year, month)
            time.sleep(1)  # サーバ対策
        print(f"--- {year} done ---")


if __name__ == "__main__":
    fetch_range(2005, 2025)