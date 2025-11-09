"""
JNTO 自動ダウンロード済みCSVを統合（修正版）
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/jnto/monthly_auto")
OUTPUT_PATH = Path("data/jnto/visitor_all_2005_2025.csv")

all_files = sorted(DATA_DIR.glob("visitor_*.csv"))
merged = []

for file in all_files:
    try:
        df = pd.read_csv(file, encoding="utf-8-sig")
        if df.empty:
            print(f"⚠️ {file.name} skipped (empty)")
            continue

        # 年月をファイル名から抽出
        year, month = file.stem.split("_")[1:]
        df["Year"] = int(year)
        df["Month"] = int(month)

        # 列名の標準化
        df = df.rename(
            columns={
                "Area(23 Markets)": "Area",
                "Country/Area(23 Markets)": "Country",
                "Month (abbr)": "Month_abbr",
                "Rate(%)": "Rate",
                "Visitor Arrivals": "Visitor_Arrivals",
            }
        )

        # 数値整形
        if "Visitor_Arrivals" in df.columns:
            df["Visitor_Arrivals"] = (
                df["Visitor_Arrivals"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .astype(float)
            )

        merged.append(df)
        print(f"✅ Added: {file.name} ({len(df)} rows)")
    except Exception as e:
        print(f"❌ {file.name} failed: {e}")

# 結合と並び替え
if merged:
    result = pd.concat(merged, ignore_index=True)
    result = result.sort_values(["Year", "Month", "Country"])
    result.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\n🎉 Saved merged dataset → {OUTPUT_PATH} ({len(result)} rows)")
else:
    print("❌ No valid CSV files found.")