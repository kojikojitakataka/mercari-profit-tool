import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
from PIL import Image
import torch
import clip
import io

# 初期設定
st.set_page_config(page_title="リサーチナビ", layout="wide")
st.title("🔎 リサーチナビ（ResearchNavi）")
st.caption("📦 商品画像から商品名推定 → EC価格検索 → 利益計算まで対応")

# モード選択
mode = st.radio("📌 モードを選んでください", ["画像から検索", "利益計算"], horizontal=True)

# 画像検索モード
if mode == "画像から検索":
    st.subheader("🖼️ 商品画像のアップロード")
    uploaded_image = st.file_uploader("画像ファイルを選択（jpg, png）", type=["jpg", "jpeg", "png"])

    # 商品名入力 or 自動推定
    item_name = ""
    if uploaded_image:
        st.image(uploaded_image, caption="アップロードされた画像", use_container_width=True)
        st.info("🔍 商品名をAIで推定中...")

        image = Image.open(uploaded_image).convert("RGB")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)
        image_input = preprocess(image).unsqueeze(0).to(device)

        # 仮の候補リスト（実際はより多様なカテゴリで改善可能）
        candidate_names = [
            "AirPods Pro", "iPhone", "PlayStation 5", "Nintendo Switch", "炊飯器", "美容家電", "リュック", "Nike スニーカー"
        ]

        text_tokens = clip.tokenize(candidate_names).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            text_features = model.encode_text(text_tokens)
            similarity = (image_features @ text_features.T).softmax(dim=-1)

        best_idx = similarity[0].argmax().item()
        item_name = candidate_names[best_idx]
        st.success(f"✅ 推定商品名: **{item_name}**")

    # 商品名入力欄（上書きも可能）
    item_name = st.text_input("🔤 商品名を確認・修正", value=item_name or "例：AirPods Pro")

    # ECサイトリンク表示
    if item_name:
        st.subheader("🌐 ECサイト価格チェックリンク")
        keyword_encoded = urllib.parse.quote(item_name)
        ec_links = {
            "🛍️ Amazon": f"https://www.amazon.co.jp/s?k={keyword_encoded}",
            "🛒 楽天市場": f"https://search.rakuten.co.jp/search/mall/{keyword_encoded}/",
            "🛍️ Yahoo!ショッピング": f"https://shopping.yahoo.co.jp/search?p={keyword_encoded}",
            "📦 メルカリ（売り切れ）": f"https://www.mercari.com/jp/search/?keyword={keyword_encoded}&status=sold_out",
            "💰 PayPayフリマ": f"https://paypayfleamarket.yahoo.co.jp/search?query={keyword_encoded}",
            "🇨🇳 1688.com": f"https://s.1688.com/selloffer/offer_search.htm?keywords={keyword_encoded}",
            "🏬 Costco": f"https://www.costco.co.jp/CatalogSearch?keyword={keyword_encoded}",
            "🎯 ドン・キホーテ": f"https://www.google.com/search?q={keyword_encoded}+site:donki.com"
        }

        for site, url in ec_links.items():
            st.markdown(f"- [{site}]({url}) 🔗", unsafe_allow_html=True)

# 利益計算モード
elif mode == "利益計算":
    st.subheader("💰 メルカリ利益計算")
    price = st.number_input("販売価格（円）", value=1000)
    shipping = st.number_input("送料（円）", value=200)
    purchase_cost = st.number_input("仕入れ値（円）", value=500)

    fee = price * 0.1
    profit = price - fee - shipping - purchase_cost

    st.metric("🧾 手数料", f"{fee:.0f} 円")
    st.metric("📈 利益", f"{profit:.0f} 円")

    if st.button("💾 結果を保存（CSV）"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.DataFrame([{
            "日時": now,
            "販売価格": price,
            "送料": shipping,
            "仕入れ値": purchase_cost,
            "手数料": fee,
            "利益": profit
        }])
        df.to_csv("profit_history.csv", mode="a", index=False, header=False)
        st.success("保存しました！")
