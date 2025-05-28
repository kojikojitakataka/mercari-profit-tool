import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime

# アプリの設定
st.set_page_config(page_title="リサーチナビ", layout="wide")

# ヘッダー
st.markdown("<h1 style='color:red;'>🔍 リサーチナビ</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:orange;'>画像から商品を検索して、価格比較＆利益計算！</h3>", unsafe_allow_html=True)

# -------------------------
# 📷 画像アップロード
# -------------------------
st.subheader("🖼️ 商品画像アップロード")
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_container_width=True)
    # ★ 仮の商品名（AIで推定予定の部分）
    product_name = "ナイキ エアマックス（仮）"
    st.success(f"画像から推定された商品名: {product_name}")

    # -------------------------
    # 🔗 ECサイトリンク
    # -------------------------
    st.subheader("🛒 各サイトで検索")
    query = product_name.replace(" ", "+")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f"[メルカリ](https://www.mercari.com/jp/search/?keyword={query})", unsafe_allow_html=True)
    with col2:
        st.markdown(f"[Amazon](https://www.amazon.co.jp/s?k={query})", unsafe_allow_html=True)
    with col3:
        st.markdown(f"[楽天](https://search.rakuten.co.jp/search/mall/{query}/)", unsafe_allow_html=True)
    with col4:
        st.markdown(f"[Yahoo!](https://shopping.yahoo.co.jp/search?p={query})", unsafe_allow_html=True)
    with col5:
        st.markdown(f"[PayPayフリマ](https://paypayfleamarket.yahoo.co.jp/search/{query})", unsafe_allow_html=True)
    with col6:
        st.markdown(f"[1688.com](https://s.1688.com/selloffer/offer_search.htm?keywords={query})", unsafe_allow_html=True)

# -------------------------
# 💰 利益計算
# -------------------------
st.subheader("💸 利益計算フォーム")

price = st.number_input("販売価格（円）", value=3000)
shipping = st.number_input("送料（円）", value=500)
cost = st.number_input("仕入れ値（円）", value=1500)

mercari_fee = price * 0.1
profit = price - shipping - cost - mercari_fee

st.write(f"🧾 メルカリ手数料：{mercari_fee:.0f}円")
st.write(f"💹 利益：{profit:.0f}円")

# -------------------------
# 💾 CSV保存
# -------------------------
if st.button("📥 計算結果を保存（CSV）"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "日時": now,
        "販売価格": price,
        "送料": shipping,
        "仕入れ値": cost,
        "手数料": mercari_fee,
        "利益": profit
    }])
    df.to_csv("profit_history.csv", mode='a', index=False, header=False)
    st.success("✅ 結果を保存しました！")
