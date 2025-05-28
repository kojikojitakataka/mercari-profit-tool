from datetime import datetime
import streamlit as st
import pandas as pd
import urllib.parse

# アプリの基本設定
st.set_page_config(page_title="リサーチナビ", layout="wide")
st.title("🔎 リサーチナビ")
st.markdown("**画像から商品名を推定し、複数ECサイトで価格比較・利益計算ができる最強のせどりツールです。**")

# テーマカラー適用（赤と黄色）
st.markdown("""
    <style>
    .main { background-color: #fff8f0; }
    h1 { color: red; }
    .stButton>button {
        background-color: yellow;
        color: black;
        font-size: 18px;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 画像アップロードと商品名入力
st.header("1️⃣ 商品画像のアップロードと商品名入力")
uploaded_image = st.file_uploader("商品画像をアップロード（任意）", type=["jpg", "jpeg", "png"])
if uploaded_image:
    st.image(uploaded_image, caption="アップロードされた画像", use_container_width=True)

product_name = st.text_input("商品名を入力または推定（例：iPhone 14 Pro）", "")

# 各サイトへの検索リンク表示
if product_name:
    st.header("2️⃣ 各サイト検索リンク（新しいタブで開きます）")
    encoded_name = urllib.parse.quote(product_name)

    search_urls = {
        "Amazon": f"https://www.amazon.co.jp/s?k={encoded_name}",
        "楽天": f"https://search.rakuten.co.jp/search/mall/{encoded_name}/",
        "Yahooショッピング": f"https://shopping.yahoo.co.jp/search?p={encoded_name}",
        "メルカリ（売り切れ）": f"https://www.mercari.com/jp/search/?keyword={encoded_name}&status=sold_out",
        "PayPayフリマ": f"https://paypayfleamarket.yahoo.co.jp/search?query={encoded_name}",
        "1688.com": f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded_name}",
        "Costco": f"https://www.costco.co.jp/CatalogSearch?keyword={encoded_name}",
        "ドン・キホーテ": f"https://www.google.com/search?q={encoded_name}+site:donki.com",
    }

    for site, url in search_urls.items():
        st.markdown(f"[🔗 {site} で検索]({url})", unsafe_allow_html=True)

# 利益計算エリア
st.header("3️⃣ 利益計算ツール")
col1, col2, col3 = st.columns(3)
with col1:
    sell_price = st.number_input("販売価格（円）", value=1000)
with col2:
    shipping_cost = st.number_input("送料（円）", value=200)
with col3:
    purchase_price = st.number_input("仕入れ値（円）", value=500)

fee = round(sell_price * 0.1)
profit = sell_price - fee - shipping_cost - purchase_price

st.write(f"📦 メルカリ手数料: **{fee} 円**")
st.write(f"💹 利益: **{profit} 円**")

# CSV保存機能
if st.button("📥 利益結果をCSV保存"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "日時": now,
        "商品名": product_name,
        "販売価格": sell_price,
        "送料": shipping_cost,
        "仕入れ値": purchase_price,
        "手数料": fee,
        "利益": profit
    }])
    df.to_csv("profit_history.csv", mode='a', index=False, header=False)
    st.success("CSVに保存しました！")
