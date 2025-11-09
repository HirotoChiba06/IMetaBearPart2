from pytrends.request import TrendReq
import pandas as pd



# Google Trendsへ接続
pytrends = TrendReq(hl='ja-JP', tz=540)

# 検索キーワード設定
keywords = ["Kyoto travel", "Tokyo travel"]

# データ取得条件を構築（期間・地域など
#現時点の出力は月単位のものである。そのため133ヶ月分のデータが取得される。
pytrends.build_payload(
    kw_list=keywords,
    cat=0,
    timeframe='2005-01-01 2025-11-01',
    geo='JP',
    gprop=''
)

# 時系列データを取得
df = pytrends.interest_over_time()

# ✅ インデックス（date）を列に戻す
df = df.reset_index()

# CSVとして保存
df.to_csv("data/trends.csv", index=False)

# 実行確認
print("✅ Data saved to data/trends.csv")
print(df.head())