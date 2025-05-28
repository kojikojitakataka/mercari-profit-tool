import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.title("メルカリ利益計算・画像検索ツール")

st.header("🧮 利益計算")
price = st.number_input("販売価格（円）", value=1000)
shipping = st.number_input("送料（円）", value=200)
purchase_cost = st.number_input("仕入れ値（円）", value=500)

mercari_fee = price * 0.1
profit = price - mercari_fee - shipping - purchase_cost

st.write(f"メルカリ手数料: {mercari_fee:.0f} 円")
st.write(f"利益: {profit:.0f} 円")

if st.button("結果を保存する"):
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

st.header("🔍 商品検索リンク作成")
query = st.text_input("検索キーワードを入力してください")
if query:
    encoded_query = urllib.parse.quote(query)
    mercari_url = f"https://www.mercari.com/jp/search/?keyword={encoded_query}"
    st.markdown(f"[メルカリで検索する]({mercari_url})")

    # 🔍 画像検索リンク（Google）
    google_img_url = f"https://www.google.com/search?tbm=isch&q={encoded_query}"
    st.markdown(f"[Google画像検索で調べる]({google_img_url})")
