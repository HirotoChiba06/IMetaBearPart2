import pandas as pd
from pathlib import Path

# === 設定 ===
data_path = Path("data/jnto/visitor_all_2005_2025.csv")

# === データ読み込み ===
df = pd.read_csv(data_path)

# カラム名の標準化
df.columns = [c.strip().replace(" ", "_") for c in df.columns]
if "Visitor_Arrivals" not in df.columns:
    # JNTO形式（自動保存時の列名対応）
    df = df.rename(columns={"Visitor_Arrivals": "Visitor_Arrivals",
                            "Country/Area(23_Markets)": "Country"})

# 「Visitor_Arrivals」を数値化（カンマ除去）
df["Visitor_Arrivals"] = (
    df["Visitor_Arrivals"].astype(str).str.replace(",", "").astype(float)
)

# === 国別に合計 ===
top_countries = (
    df.groupby("Country")["Visitor_Arrivals"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# === 上位5件を抽出 ===
top5 = top_countries.head(7)

# === 結果出力 ===
output_path = Path("data/jnto/top5_countries.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
top5.to_csv(output_path, index=False, encoding="utf-8-sig")

print("✅ Top 7 countries saved →", output_path)
print(top5)