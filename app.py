import streamlit as st
import urllib.parse

# アプリ初期設定
st.set_page_config(page_title="リサーチナビ", layout="wide")
st.title("🔍 リサーチナビ（ResearchNavi）")
st.caption("画像から商品名を推定し、すべてのECサイトで価格チェック＆利益計算")

# モード選択
mode = st.radio("モードを選んでください", ["画像から検索", "利益計算"], horizontal=True)

# 画像アップロードモード
if mode == "画像から検索":
    st.subheader("🖼️ 商品画像のアップロード")
    uploaded_image = st.file_uploader("画像ファイルを選択（jpg, png）", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="アップロードされた画像", use_container_width=True)
        st.success("画像をアップロードしました！")

    # 商品名の入力欄（将来的にAI推定と連携）
    item_name = st.text_input("🔤 商品名を入力または推定", value="Apple AirPods Pro")

    if item_name:
        st.subheader("🌐 ECサイト検索リンク一覧")
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
    st.subheader("💰 メルカリ利益計算ツール")

    price = st.number_input("販売価格（円）", value=1000)
    shipping = st.number_input("送料（円）", value=200)
    purchase_cost = st.number_input("仕入れ値（円）", value=500)

    mercari_fee = price * 0.1
    profit = price - mercari_fee - shipping - purchase_cost

    st.write(f"🧾 メルカリ手数料: {mercari_fee:.0f} 円")
    st.write(f"📈 利益: {profit:.0f} 円")

    if st.button("💾 結果を保存（CSV）"):
        import pandas as pd
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.DataFrame([{
            "日時": now,
            "販売価格": price,
            "送料": shipping,
            "仕入れ値": purchase_cost,
            "手数料": mercari_fee,
            "利益": profit
        }])
        df.to_csv("profit_history.csv", mode='a', index=False, header=False)
        st.success("保存しました！")
