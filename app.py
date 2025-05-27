import streamlit as st
import urllib.parse

# タイトル
st.title("🔍 商品検索リンク生成ツール")

# 検索キーワード入力
keyword = st.text_input("検索キーワードを入力してください")

# 検索リンク生成関数
def generate_search_links(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    return {
        "Amazon": f"https://www.amazon.co.jp/s?k={encoded_keyword}",
        "楽天市場": f"https://search.rakuten.co.jp/search/mall/{encoded_keyword}/",
        "Yahoo!ショッピング": f"https://shopping.yahoo.co.jp/search?p={encoded_keyword}",
        "PayPayフリマ": f"https://paypayfleamarket.yahoo.co.jp/search?query={encoded_keyword}",
        "メルカリ": f"https://www.mercari.com/jp/search/?keyword={encoded_keyword}"
    }

# 入力された場合のみ表示
if keyword:
    st.markdown("### 🔗 各サイトの検索リンク")
    links = generate_search_links(keyword)
    for name, url in links.items():
        st.markdown(f"- [{name}]({url})", unsafe_allow_html=True)

# フッター
st.markdown("---")
st.caption("🛠️ 制作：小島崇彦")
import pandas as pd
from datetime import datetime

# ① タイトルと説明（ここは今あるコードにすでにあります）

# ② 入力フォーム
price = st.number_input("販売価格（円）", value=1000)
shipping = st.number_input("送料（円）", value=200)
purchase_cost = st.number_input("仕入れ値（円）", value=500)

# ③ 計算
mercari_fee = price * 0.1
profit = price - mercari_fee - shipping - purchase_cost

# ④ 結果表示
st.write(f"メルカリ手数料: {mercari_fee:.0f} 円")
st.write(f"利益: {profit:.0f} 円")

# ⑤ 保存ボタン（CSV形式）
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
