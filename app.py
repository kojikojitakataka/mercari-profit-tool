import streamlit as st
from PIL import Image, UnidentifiedImageError
import pandas as pd

st.set_page_config(page_title="画像で商品検索", layout="centered")

st.header("🖼️ 画像で商品を検索")

uploaded_image = st.file_uploader("画像をアップロードしてください（例：商品写真）", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        image = Image.open(uploaded_image)
        st.image(image, caption="アップロードされた画像", use_container_width=True)

        # 仮のAIによる商品名推測
        st.markdown("🔍 **AIによる予測商品名（例）:**")
        predicted_name = "Tシャツ（白 無地）"
        st.success(predicted_name)

        # 検索ボタンでリンク表示
        if st.button("🔎 メルカリ・PayPayフリマで検索する"):
            mercari_url = f"https://www.mercari.com/jp/search/?keyword={predicted_name}"
            paypay_url = f"https://paypayfleamarket.yahoo.co.jp/search?query={predicted_name}"
            st.markdown(f"🟥 [メルカリで検索]({mercari_url})")
            st.markdown(f"🟦 [PayPayフリマで検索]({paypay_url})")

        # 仮の価格データ
        st.subheader("📈 類似商品の価格分布")
        data = {
            "商品名": ["Tシャツ", "Tシャツ 白", "おしゃれTシャツ"],
            "価格": [1200, 1300, 1250]
        }
        df = pd.DataFrame(data)
        st.bar_chart(df["価格"])

        st.write("🧮 **中央値：**", df["価格"].median())
        st.write("🔁 **最頻値：**", df["価格"].mode()[0])

        # CSVダウンロード
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ CSVでダウンロード", csv, "similar_products.csv", "text/csv")

    except UnidentifiedImageError:
        st.error("❌ 画像の読み込みに失敗しました。JPGまたはPNG形式の画像を選んでください。")
    except Exception as e:
        st.error(f"❌ エラーが発生しました：{e}")
