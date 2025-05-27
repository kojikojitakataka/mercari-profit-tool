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
