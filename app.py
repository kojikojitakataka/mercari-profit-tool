from PIL import Image
import io
import pandas as pd
import streamlit as st

st.header("📷 画像から類似商品検索")

# 画像アップロード
uploaded_image = st.file_uploader("画像をアップロードしてください（例：商品写真）", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="アップロードした画像", use_container_width=True)  # ✅ 警告対応済

    # 仮：AIで商品名を推定（将来はCLIPなど）
    predicted_name = "Tシャツ（白 無地）"
    st.markdown("🔍 **AIによる予測商品名（例）:**")
    st.success(predicted_name)

    # メルカリ・PayPay検索ボタン
    if st.button("🔎 メルカリ・PayPayフリマで検索する"):
        mercari_url = f"https://www.mercari.com/jp/search/?keyword={predicted_name}"
        paypay_url = f"https://paypayfleamarket.yahoo.co.jp/search?query={predicted_name}"
        st.markdown(f"🟥 [メルカリで検索]({mercari_url})")
        st.markdown(f"🟦 [PayPayフリマで検索]({paypay_url})")

    # 仮の類似商品価格データ（将来は実データに）
    data = {
        "商品名": ["Tシャツ", "Tシャツ 白", "おしゃれTシャツ"],
        "価格": [1200, 1300, 1250]
    }
    df = pd.DataFrame(data)

    # 📊 グラフで価格分布を表示
    st.subheader("📈 類似商品の価格分布")
    st.bar_chart(df["価格"])

    # 中央値・最頻値
    st.write("🧮 **中央値：**", df["価格"].median())
    st.write("🔁 **最頻値：**", df["価格"].mode()[0])

    # 💾 CSVダウンロード
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ CSVでダウンロード", csv, "similar_products.csv", "text/csv")
