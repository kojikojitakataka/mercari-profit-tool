import streamlit as st
import urllib.parse
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="リサーチナビ Lite", layout="wide")
st.title("🔎 リサーチナビ Lite（軽量高速版）")

# 利益計算
st.header("💰 利益計算ツール")
sale = st.number_input("販売価格（円）", value=2000)
shipping = st.number_input("送料（円）", value=300)
cost = st.number_input("仕入れ値（円）", value=1000)

fee = sale * 0.1
profit = sale - fee - shipping - cost

st.metric("手数料", f"{fee:.0f} 円")
st.metric("利益", f"{profit:.0f} 円")

if st.button("📊 結果を保存"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "日時": now,
        "販売価格": sale,
        "送料": shipping,
        "仕入れ値": cost,
        "手数料": fee,
        "利益": profit
    }])
    try:
        old = pd.read_csv("profit_simple.csv")
        df.to_csv("profit_simple.csv", mode="a", index=False, header=False)
    except:
        df.to_csv("profit_simple.csv", index=False)
    st.success("保存しました！")

# 検索リンク
st.header("🔗 ECサイト検索リンク")
keyword = st.text_input("🔍 商品名を入力", "")
if keyword:
    enc = urllib.parse.quote(keyword)
    urls = {
        "Amazon": f"https://www.amazon.co.jp/s?k={enc}",
        "楽天": f"https://search.rakuten.co.jp/search/mall/{enc}/",
        "Yahooショッピング": f"https://shopping.yahoo.co.jp/search?p={enc}",
        "メルカリ": f"https://www.mercari.com/jp/search/?keyword={enc}",
        "PayPayフリマ": f"https://paypayfleamarket.yahoo.co.jp/search?query={enc}",
    }
    for name, link in urls.items():
        st.markdown(f"- [{name}]({link}) 🔗", unsafe_allow_html=True)
