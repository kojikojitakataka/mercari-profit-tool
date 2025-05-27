import streamlit as st
from PIL import Image
import pandas as pd
import urllib.parse

# ページ設定
st.set_page_config(page_title="画像で商品検索", layout="centered")
st.header("🖼️ 画像で商品検索ツール - フリマアシスト")

# ============================
# ① 画像アップロード
# ============================
uploaded_image = st.file_uploader("画像をアップロードしてください（例：商品写真）", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        image = Image.open(uploaded_image)
        st.image(image, caption="アップロードされた画像", use_container_width=True)

        # ============================
        # ② 仮の商品名予測（将来はCLIP AIで）
        # ============================
        predicted_name = "Tシャツ（白 無地）"  # 仮の商品名
        st.markdown("🔍 **AIによる予測商品名（仮）:**")
        st.success(predicted_name)

        # ============================
        # ③ 各種フリマ・ECサイト検索リンク
        # ============================
        st.subheader("🔎 関連サイトで検索")
        encoded_name = urllib.parse.quote(predicted_name)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.link_button("🟥 メルカリ", f"https://www.mercari.com/jp/search/?keyword={encoded_name}")
        with col2:
            st.link_button("🟦 PayPayフリマ", f"https://paypayfleamarket.yahoo.co.jp/search?query={encoded_name}")
        with col3:
            st.link_button("🟢 楽天市場", f"https://search.rakuten.co.jp/search/mall/{encoded_name}/")

        col4, col5 = st.columns(2)
        with col4:
            st.link_button("🟡 Yahooショッピング", f"https://shopping.yahoo.co.jp/search?p={encoded_name}")
        with col5:
            st.link_button("🟠 Amazon", f"https://www.amazon.co.jp/s?k={encoded_name}")

        # ============================
        # ④ ダミーの価格データで相場分析
        # ============================
        st.subheader("📊 類似商品の価格分布（例）")
        data = {
            "商品名": ["Tシャツ", "Tシャツ 白", "おしゃれTシャツ"],
            "価格": [1200, 1300, 1250]
        }
        df = pd.DataFrame(data)

        st.bar_chart(df["価格"])
        st.write("🧮 **中央値：**", df["価格"].median())
        st.write("🔁 **最頻値：**", df["価格"].mode()[0])

        # ============================
        # ⑤ データダウンロード
        # ============================
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ CSVでダウンロード", csv, "similar_products.csv", "text/csv")

    except Exception as e:
        st.error(f"画像の読み込みでエラーが発生しました: {e}")
