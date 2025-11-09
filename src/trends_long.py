from pytrends.request import TrendReq
import pandas as pd
import time

# --- 設定 ---
pytrends = TrendReq(hl='ja-JP', tz=540)
keywords = ["Kyoto travel", "Tokyo travel"]
interval = 5  # 年単位での分割取得（例: 2005-2009, 2010-2014, ...）

# --- データ取得 ---
dfs = []

for start in range(2005, 2026, interval):
    end = min(start + interval - 1, 2025)
    timeframe = f"{start}-01-01 {end}-12-31"
    print(f"📦 Fetching {timeframe} ...")
    
    try:
        pytrends.build_payload(keywords, timeframe=timeframe, geo='JP')
        df_part = pytrends.interest_over_time().reset_index()
        df_part["period"] = f"{start}-{end}"  # どの区間かを記録
        dfs.append(df_part)
        print(f"✅ Done: {timeframe} ({len(df_part)} rows)")
    except Exception as e:
        print(f"⚠️ Error on {timeframe}: {e}")
    
    time.sleep(5)  # Googleに優しく待つ

# --- 結合と保存 ---
df = pd.concat(dfs, ignore_index=True)
df = df.rename(columns={"index": "date"})  # 念のため列名補正
df.to_csv("data/trends_long.csv", index=False)

print("🎉 全期間（2005〜2025）データ取得完了！")
print(df.head())
print(f"🧾 Total rows: {len(df)}")