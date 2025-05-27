import streamlit as st
from PIL import Image
import pandas as pd
import urllib.parse
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="画像で商品検索 & 利益計算ツール", layout="centered")
st.header("🛍️ フリマアシスト - 万能せどり支援アプリ")

# --- 画像アップロード ---
uploaded_image = st.file_uploader("画像をアップロードしてください（jpg, png）", type=["jpg", "jpeg", "png"])

# --- 商品ジャンル選択（補助） ---
genre = st.selectbox("商品ジャンルを選択してください（任意）", ["衣類", "家電", "本・雑誌", "ホビー", "その他"])

if uploaded_image is not None:
    try:
        image = Image.open(uploaded_image)
        st.image(image, caption="アップロードされた画像", use_container_width=True)

        # --- 商品名予測（仮） ---
        predicted_name = "Tシャツ（白 無地）"  # 仮の名前（AI導入予定）
        st.markdown("🔍 **AIによる予測商品名（仮）:**")
        st.success(predicted_name)

        # --- EC/フリマ 検索リンク ---
        st.subheader("🔗 関連サイトで検索")
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

        # --- ダミー価格データで相場表示 ---
        st.subheader("📊 類似商品の価格相場（例）")
        df = pd.DataFrame({
            "商品名": ["Tシャツ", "Tシャツ 白", "おしゃれTシャツ"],
            "価格": [1200, 1300, 1250]
        })
        st.bar_chart(df["価格"])
        st.write("🧮 **中央値：**", df["価格"].median())
        st.write("🔁 **最頻値：**", df["価格"].mode()[0])
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ 類似商品のCSVダウンロード", csv, "similar_products.csv", "text/csv")

        # --- 利益計算フォーム ---
        st.subheader("💰 利益計算シミュレーター")
        col1, col2 = st.columns(2)
        with col1:
            cost_price = st.number_input("仕入れ価格（円）", min_value=0)
        with col2:
            sell_price = st.number_input("販売価格（円）", min_value=0)

        if sell_price > 0:
            fee = int(sell_price * 0.1)  # メルカリ10%手数料
            profit = sell_price - fee - cost_price
            st.info(f"🧾 手数料（10%）: {fee}円")
            st.success(f"💹 利益: {profit}円")

        # --- 入力記録の保存（CSV形式） ---
        st.subheader("📝 記録をCSVに保存")
        if st.button("記録を保存する"):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            record_df = pd.DataFrame([{
                "日時": now,
                "商品名": predicted_name,
                "ジャンル": genre,
                "仕入れ価格": cost_price,
                "販売価格": sell_price,
                "手数料": fee,
                "利益": profit
            }])
            record_csv = record_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ この記録をダウンロード", record_csv, "record.csv", "text/csv")

        # --- サポートリンク ---
        st.subheader("📚 お役立ちリンク")
        st.markdown("- [メルカリ出品ページ](https://www.mercari.com/jp/sell/)")
        st.markdown("- [メルカリ公式の送料一覧](https://www.mercari.com/jp/help_center/article/entry/516/)")
        st.markdown("- [メルカリガイド](https://help.jp.mercari.com/)")
        st.markdown("- [ヤフオク送料早見表](https://auctions.yahoo.co.jp/topic/promo/post/guide/price.html)")

    except Exception as e:
        st.error(f"エラー: {e}")
