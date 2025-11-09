import pandas as pd
from pathlib import Path

input_dir = Path("data/trends")
output_path = input_dir / "trends_japan_travel_6countries.csv"

files = sorted(input_dir.glob("trends_japan_travel_*.csv"))

all_data = []
for f in files:
    print(f"📂 Merging {f.name} ...")
    df = pd.read_csv(f)
    all_data.append(df)

if all_data:
    result = pd.concat(all_data, ignore_index=True)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Merged → {output_path} ({len(result)} rows)")
else:
    print("⚠️ No data found.")