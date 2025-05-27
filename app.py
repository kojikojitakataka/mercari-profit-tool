import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.title("メルカリ利益計算ツール")

# 入力フォーム
price = st.number_input("販売価格（円）", value=1000)
shipping = st.number_input("送料（円）", value=200)
purchase_cost = st.number_input("仕入れ値（円）", value=500)

# 計算
mercari_fee = price * 0.1
profit = price - mercari_fee - shipping - purchase_cost

# 結果表示
st.write(f"メルカリ手数料: {mercari_fee:.0f} 円")
st.write(f"利益: {profit:.0f} 円")

# ダウンロードボタン（CSV形式）
df = pd.DataFrame([{
    "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "販売価格": price,
    "送料": shipping,
    "仕入れ値": purchase_cost,
    "手数料": mercari_fee,
    "利益": profit
}])

csv = df.to_csv(index=False)
st.download_button(
    label="結果をCSVでダウンロード",
    data=csv,
    file_name="profit_history.csv",
    mime="text/csv"
