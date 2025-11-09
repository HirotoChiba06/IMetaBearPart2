import pandas as pd
from pathlib import Path

# ===== ファイルパス =====
jnto_path = Path("data/jnto/visitor_all_2005_2025.csv")
trends_path = Path("data/trends/trends_japan_travel_6countries.csv")
output_path = Path("data/merged/merged_trends_visitors.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

# ===== JNTOデータ =====
df_jnto = pd.read_csv(jnto_path)
df_jnto["Visitor_Arrivals"] = (
    df_jnto["Visitor_Arrivals"].astype(str).str.replace(",", "").astype(float)
)
df_jnto["Month"] = df_jnto["Month_abbr"].str.replace(".", "", regex=False)
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
df_jnto["Month"] = df_jnto["Month"].map(month_map)
df_jnto["date"] = pd.to_datetime(df_jnto["Year"].astype(str) + "-" + df_jnto["Month"].astype(str) + "-01")
df_jnto = df_jnto[["date", "Country", "Visitor_Arrivals"]]

# ===== トレンドデータ =====
df_trends = pd.read_csv(trends_path)
df_trends["date"] = pd.to_datetime(df_trends["date"])
df_trends = df_trends.rename(columns={"country": "Country"})

# ===== 結合 =====
merged = pd.merge(df_trends, df_jnto, on=["date", "Country"], how="inner")
merged.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ Merged data saved → {output_path}")
print(merged.head())