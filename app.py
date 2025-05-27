import streamlit as st
from PIL import Image
import pandas as pd
import urllib.parse
import datetime
import torch
import clip
import os

# --- ページ設定 ---
st.set_page_config(page_title="複合せどり売買ツール（セドファクトリー）", layout="centered")
st.title("🛍️ 複合せどり売買ツール（セドファクトリー）")
st.caption("制作者：小島 崇彦　制作日：2025年5月27日")

# --- 画像アップロード ---
uploaded_image = st.file_uploader("画像をアップロードしてください（jpg, png）", type=["jpg", "jpeg", "png"])

# --- 商品ジャンル選択 ---
genre = st.selectbox(
    "商品ジャンルを選択してください（任意）",
    [
        "衣類", "家電", "本・雑誌", "ホビー", "おもちゃ", "ゲーム", "スポーツ用品",
        "アウトドア", "美容・健康", "食品・飲料", "家具・インテリア", "ベビー・キッズ",
        "ペット用品", "車・バイク", "楽器", "チケット", "その他"
    ]
)

if uploaded_image is not None:
    try:
        image = Image.open(uploaded_image)
        st.image(image, caption="アップロードされた画像", use_container_width=True)

        # --- CLIPモデルによる商品名予測 ---
        st.markdown("🔍 **AIによる予測商品名:**")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)

        # 画像の前処理
        image_preprocessed = preprocess(image).unsqueeze(0).to(device)

        # 商品名の候補リスト
        candidate_labels = [
            "白いTシャツ", "黒いTシャツ", "青いジーンズ", "赤いスニーカー", "ノートパソコン",
            "スマートフォン", "腕時計", "バックパック", "ギター", "電子レンジ"
        ]

        # テキストの前処理
        text_tokens = clip.tokenize(candidate_labels).to(device)

        # 特徴量の取得
        with torch.no_grad():
            image_features = model.encode_image(image_preprocessed)
            text_features = model.encode_text(text_tokens)

        # 類似度の計算
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarities = (image_features @ text_features.T).squeeze(0)

        # 最も類似度の高いラベルを選択
        best_match_index = similarities.argmax().item()
        predicted_name = candidate_labels[best_match_index]
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
        st.markdown("- 🟥 [メルカリ 出品ページ](https://www.mercari.com/jp/sell/)")
        st.markdown("- 🟥 [メルカリ 送料早見表（最新）](https://help.jp.mercari.com/guide/articles/1080/)")
        st.markdown("- 🟦 [PayPayフリマ 出品ページ](https://paypayfleamarket.yahoo.co.jp/sell)")
        st.markdown("- 🟦 [PayPayフリマ 発送方法ガイド](https://paypayfleamarket.yahoo.co.jp/contents/shipping)")

    except Exception as e:
        st.error(f"エラー: {e}")
