import streamlit as st
import pandas as pd
from datetime import datetime

# サイドバーでページを選択
page = st.sidebar.selectbox("表示する機能を選んでください", ["🔍 商品検索リンク生成ツール", "📈 メルカリ利益計算ツール"])

# ① 検索ツール
if page == "🔍 商品検索リンク生成ツール":
    st.title("🔍 商品検索リンク生成ツール")
    keyword = st.text_input("検索キーワードを入力してください")

    if keyword:
        st.write("【リンク】")
        st.markdown(f"- [メルカリ](https://www.mercari.com/jp/search/?keyword={keyword})")
        st.markdown(f"- [楽天](https://search.rakuten.co.jp/search/mall/{keyword})")
        st.markdown(f"- [Amazon](https://www.amazon.co.jp/s?k={keyword})")
        st.markdown(f"- [Yahooショッピング](https://shopping.yahoo.co.jp/search?p={keyword})")

# ② 利益計算ツール
elif page == "📈 メルカリ利益計算ツール":
    st.title("📈 メルカリ利益計算ツール")

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
