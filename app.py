import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
from PIL import Image
import torch
import clip
import matplotlib.pyplot as plt
import base64

# ページ設定
st.set_page_config(page_title="リサーチナビ", layout="wide")
st.title("🔎 リサーチナビ（ResearchNavi）")
st.caption("📦 画像→商品名推定 → EC検索 → 利益計算＆履歴グラフ + 電脳せどり支援")

# ページ切り替え
page = st.sidebar.radio("🧭 ページ切替", ["画像検索", "利益計算＆履歴", "電脳せどり"])

# =================== 1. 画像検索 ===================
if page == "画像検索":
    st.subheader("🖼️ 商品画像アップロードとAI推定")
    uploaded_image = st.file_uploader("画像をアップロード（jpg, png）", type=["jpg", "jpeg", "png"])
    item_name = ""

    if uploaded_image:
        st.image(uploaded_image, caption="アップロード画像", use_container_width=True)
        st.info("🔍 AIが商品名を推定中...")

        image = Image.open(uploaded_image).convert("RGB")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)
        image_input = preprocess(image).unsqueeze(0).to(device)

        # 仮の候補（日本語CLIP未統合のため簡易）
        candidate_names = [
            "AirPods Pro", "iPhone", "PlayStation 5", "Nintendo Switch", "炊飯器", "美容家電", "リュック", "スニーカー"
        ]
        text_tokens = clip.tokenize(candidate_names).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            text_features = model.encode_text(text_tokens)
            similarity = (image_features @ text_features.T).softmax(dim=-1)
        best_idx = similarity[0].argmax().item()
        item_name = candidate_names[best_idx]
        st.success(f"✅ 推定商品名: **{item_name}**")

    item_name = st.text_input("📝 商品名を確認・修正", value=item_name or "")
    if item_name:
        st.subheader("🔗 ECサイト検索リンク")
        keyword = urllib.parse.quote(item_name)
        ec_links = {
            "Amazon": f"https://www.amazon.co.jp/s?k={keyword}",
            "楽天市場": f"https://search.rakuten.co.jp/search/mall/{keyword}/",
            "Yahooショッピング": f"https://shopping.yahoo.co.jp/search?p={keyword}",
            "メルカリ（売り切れ）": f"https://www.mercari.com/jp/search/?keyword={keyword}&status=sold_out",
            "PayPayフリマ": f"https://paypayfleamarket.yahoo.co.jp/search?query={keyword}",
            "1688.com": f"https://s.1688.com/selloffer/offer_search.htm?keywords={keyword}",
            "Costco": f"https://www.costco.co.jp/CatalogSearch?keyword={keyword}",
            "ドン・キホーテ": f"https://www.google.com/search?q={keyword}+site:donki.com"
        }
        for name, url in ec_links.items():
            st.markdown(f"- [{name}]({url}) 🔗", unsafe_allow_html=True)

# =================== 2. 利益計算＆履歴 ===================
elif page == "利益計算＆履歴":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 利益計算")
        price = st.number_input("販売価格（円）", value=1000)
        shipping = st.number_input("送料（円）", value=200)
        cost = st.number_input("仕入れ値（円）", value=500)

        fee = price * 0.1
        profit = price - fee - shipping - cost

        st.metric("🧾 手数料", f"{fee:.0f} 円")
        st.metric("📈 利益", f"{profit:.0f} 円")

        if st.button("💾 利益データを保存"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = pd.DataFrame([{
                "日時": now,
                "販売価格": price,
                "送料": shipping,
                "仕入れ値": cost,
                "手数料": fee,
                "利益": profit
            }])
            try:
                existing = pd.read_csv("profit_history.csv")
                df.to_csv("profit_history.csv", mode="a", index=False, header=False)
            except:
                df.to_csv("profit_history.csv", index=False)
            st.success("✅ 保存しました！")

    with col2:
        st.subheader("📊 利益履歴グラフ")
        try:
            data = pd.read_csv("profit_history.csv")
            st.dataframe(data.tail(10))

            st.markdown("#### 利益の推移（棒グラフ）")
            fig1, ax1 = plt.subplots()
            data["日時"] = pd.to_datetime(data["日時"])
            ax1.bar(data["日時"], data["利益"])
            ax1.set_ylabel("利益 (円)")
            ax1.tick_params(axis='x', rotation=45)
            st.pyplot(fig1)

            st.markdown("#### コスト内訳（円グラフ）")
            last = data.iloc[-1]
            labels = ['販売価格', '手数料', '送料', '仕入れ値', '利益']
            sizes = [last['販売価格'], last['手数料'], last['送料'], last['仕入れ値'], last['利益']]
            fig2, ax2 = plt.subplots()
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig2)

        except:
            st.warning("📭 まだ履歴がありません。")

# =================== 3. 電脳せどり ===================
elif page == "電脳せどり":
    st.subheader("🛍️ 電脳せどりショップ検索")
    keyword = st.text_input("🔍 商品名を入力", "")
    if keyword:
        keyword_encoded = urllib.parse.quote(keyword)
        shops = {
            "ヨドバシ": f"https://www.yodobashi.com/?word={keyword_encoded}",
            "ビックカメラ": f"https://www.biccamera.com/bc/category/?q={keyword_encoded}",
            "ノジマ": f"https://online.nojima.co.jp/search/?keyword={keyword_encoded}",
            "イオン": f"https://shops.aeonsquare.net/search?keyword={keyword_encoded}",
            "Joshin": f"https://joshinweb.jp/search/?KEYWORD={keyword_encoded}"
        }
        for name, url in shops.items():
            st.markdown(f"- [{name}]({url}) 🔗", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧮 電卓機能")
    calc_expr = st.text_input("数式を入力（例：1000-200-100）")
    if calc_expr:
        try:
            result = eval(calc_expr)
            st.success(f"✅ 結果: {result}")
        except:
            st.error("⚠️ 数式の形式が正しくありません。")
