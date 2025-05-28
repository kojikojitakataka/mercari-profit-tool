import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# アプリの基本設定
st.set_page_config(page_title="リサーチナビ", layout="wide")
st.title("🔎 リサーチナビ（最強のせどりツール）")
st.markdown("商品画像をもとに、仕入れ・販売・利益を一括チェック！")

# サイトリンク生成関数
def generate_search_links(product_name):
    sites = {
        "メルカリ": f"https://www.mercari.com/jp/search/?keyword={product_name}",
        "Amazon": f"https://www.amazon.co.jp/s?k={product_name}",
        "楽天": f"https://search.rakuten.co.jp/search/mall/{product_name}/",
        "Yahoo!ショッピング": f"https://shopping.yahoo.co.jp/search?p={product_name}",
        "PayPayフリマ": f"https://paypayfleamarket.yahoo.co.jp/search/{product_name}",
        "ドン・キホーテ": f"https://www.donki.com/j-kakaku/?q={product_name}",
        "Costco": f"https://www.costco.co.jp/CatalogSearch?dept=All&keyword={product_name}",
        "1688.com": f"https://s.1688.com/selloffer/offer_search.htm?keywords={product_name}"
    }
    return sites

# 商品画像アップロード
st.subheader("🖼️ 商品画像アップロード")
uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

product_name = ""

# 仮の商品名推定（今後AI連携可能）
if uploaded_image is not None:
    st.image(uploaded_image, caption="アップロードされた画像", use_container_width=True)
    st.success("画像がアップロードされました！")
    product_name = st.text_input("📦 推定商品名（修正可）", "例：AirPods Pro 第2世代")

# 商品名があれば検索リンクを表示
if product_name:
    st.subheader("🔗 ECサイト検索リンク")
    links = generate_search_links(product_name)
    for name, url in links.items():
        st.markdown(f"- [{name}]({url})", unsafe_allow_html=True)

# 利益計算
st.subheader("💰 利益計算")
sell_price = st.number_input("販売価格（円）", value=1000)
shipping = st.number_input("送料（円）", value=200)
purchase_cost = st.number_input("仕入れ価格（円）", value=500)

mercari_fee = sell_price * 0.1
profit = sell_price - mercari_fee - shipping - purchase_cost

st.markdown(f"**メルカリ手数料**：{mercari_fee:.0f}円")
st.markdown(f"**利益**：{profit:.0f}円")

# 保存機能
if st.button("💾 結果を保存（CSV）"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "日時": now,
        "商品名": product_name,
        "販売価格": sell_price,
        "送料": shipping,
        "仕入れ価格": purchase_cost,
        "手数料": mercari_fee,
        "利益": profit
    }])
    df.to_csv("profit_history.csv", mode="a", index=False, header=False)
    st.success("CSVに保存しました！")
