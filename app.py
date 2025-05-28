import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="メルカリ利益計算＆検索ツール")

# タイトル
st.title("🔍 商品検索＋💰利益計算ツール")

st.write("商品名を入力して、画像検索と利益計算をしましょう。")

# =====================
# 🔍 商品検索リンク生成
# =====================
st.subheader("🔍 商品名で検索リンクを作成")

keyword = st.text_input("検索する商品名を入力してください")

if keyword:
    encoded = urllib.parse.quote(keyword)
    st.markdown("---")
    st.markdown(f"🛍️ [メルカリで検索](https://www.mercari.com/jp/search/?keyword={encoded})")
    st.markdown(f"🛒 [楽天で検索](https://search.rakuten.co.jp/search/mall/{encoded}/)")
    st.markdown(f"📷 [Google画像検索](https://www.google.com/search?tbm=isch&q={encoded})")
    st.markdown(f"🛍️ [Yahoo!ショッピングで検索](https://shopping.yahoo.co.jp/search?p={encoded})")
    st.markdown("---")

# =====================
# 💰 メルカリ利益計算
# =====================
st.subheader("💰 メルカリ利益計算")

price = st.number_input("販売価格（円）", value=1000)
shipping = st.number_input("送料（円）", value=200)
purchase_cost = st.number_input("仕入れ値（円）", value=500)

mercari_fee = price * 0.1
profit = price - mercari_fee - shipping - purchase_cost

st.write(f"🧾 メルカリ手数料: {mercari_fee:.0f} 円")
st.write(f"💡 利益: {profit:.0f} 円")

# =====================
# 💾 保存ボタン（CSV出力）
# =====================
if st.button("結果を保存する"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "日時": now,
        "商品名": keyword,
        "販売価格": price,
        "送料": shipping,
        "仕入れ値": purchase_cost,
        "手数料": mercari_fee,
        "利益": profit
    }])
    df.to_csv("profit_history.csv", mode='a', index=False, header=False)
    st.success("📁 保存しました！")
