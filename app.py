import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import requests
from bs4 import BeautifulSoup

# アプリタイトル
st.set_page_config(page_title="リサーチナビ", layout="wide")
st.title("🛒 リサーチナビ - 利益計算 & 相場リサーチツール")
st.caption("制作者: 小島崇彦")

# 商品画像アップロード（任意）
st.subheader("🖼️ 商品画像のアップロード")
uploaded_image = st.file_uploader("画像を選択してください（任意）", type=["jpg", "jpeg", "png"])
if uploaded_image:
    st.image(uploaded_image, caption="アップロードされた画像", use_column_width=True)

# 商品名入力
st.subheader("🔍 商品名の入力")
product_name = st.text_input("検索する商品名を入力してください", placeholder="例: ナイキ エアフォース1")

# 価格取得（仮）
def get_mock_price(product_name, site_name):
    encoded = urllib.parse.quote(product_name)
    return f"https://www.{site_name}.com/search/?keyword={encoded}"

# サイト一覧
ec_sites = {
    "Amazon": "amazon.co.jp",
    "楽天": "rakuten.co.jp",
    "Yahoo!ショッピング": "shopping.yahoo.co.jp",
    "メルカリ": "mercari.com/jp",
    "PayPayフリマ": "paypayfleamarket.yahoo.co.jp",
    "1688.com": "1688.com",
    "ドン・キホーテ": "donki.com",
    "Costco": "costco.co.jp"
}

if product_name:
    st.subheader("🌐 ECサイト検索リンク")
    for site, domain in ec_sites.items():
        url = get_mock_price(product_name, domain)
        st.markdown(f"- [{site}で検索]({url})", unsafe_allow_html=True)

# 利益計算フォーム
st.subheader("💰 利益計算")
sell_price = st.number_input("販売価格（円）", value=1000)
shipping_fee = st.number_input("送料（円）", value=200)
cost_price = st.number_input("仕入れ値（円）", value=500)

mercari_fee = int(sell_price * 0.1)
profit = sell_price - mercari_fee - shipping_fee - cost_price

st.markdown(f"**🧾 メルカリ手数料：** ¥{mercari_fee:,}")
st.markdown(f"**📊 利益：** ¥{profit:,}")

# 保存ボタン
if st.button("CSVに保存する"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "日時": now,
        "商品名": product_name,
        "販売価格": sell_price,
        "送料": shipping_fee,
        "仕入れ値": cost_price,
        "手数料": mercari_fee,
        "利益": profit
    }])
    df.to_csv("profit_history.csv", mode="a", index=False, header=False)
    st.success("保存しました！")

# 注意：相場スクレイピング本実装は実行環境によって制限されます。
