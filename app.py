import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="メルカリ利益計算ツール", layout="wide")
st.title('📦 メルカリ利益計算＆出品サポートツール')

uploaded_file = st.file_uploader('📂 Excelファイルをアップロードしてください', type=['xlsm', 'xlsx'])

@st.cache_data
def convert_df(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.success('✅ 読み込み成功！データを表示します')
        st.dataframe(df)

        # 利益計算
        if all(col in df.columns for col in ['販売価格', '送料', '手数料（％）', '仕入れ値']):
            df['手数料'] = df['販売価格'] * df['手数料（％）'] / 100
            df['利益'] = df['販売価格'] - df['送料'] - df['手数料'] - df['仕入れ値']
            st.subheader('💰 利益計算結果')
            st.dataframe(df[['商品名', '販売価格', '送料', '手数料', '仕入れ値', '利益']])

        # 出品文自動生成
        if '商品名' in df.columns:
            st.subheader('✏️ 出品説明文（自動生成）')
            def generate_description(name):
                return f"ご覧いただきありがとうございます！こちらは『{name}』です。\n状態は良好で、すぐにご使用いただけます。\n即購入OK・早い者勝ちです！ご検討よろしくお願いします。"
            df['出品説明文'] = df['商品名'].apply(generate_description)
            st.dataframe(df[['商品名', '出品説明文']])

        # 並び替え（いいね数・販売数）
        if 'いいね数' in df.columns or '販売数' in df.columns:
            st.subheader('📊 並び替え（売れ筋順）')
            sort_option = st.selectbox('並び替えの基準を選んでください', ['いいね数', '販売数'])
            df_sorted = df.sort_values(by=sort_option, ascending=False)
            st.dataframe(df_sorted)

        # 在庫管理
        st.subheader('📋 在庫・販売管理')
        if '状態' not in df.columns:
            df['状態'] = '出品中'
        status_options = ['出品中', '売切れ', '在庫']
        for i in range(len(df)):
            df.at[i, '状態'] = st.selectbox(f"{df.at[i, '商品名']} の状態", status_options, index=status_options.index(df.at[i, '状態']))
        st.dataframe(df[['商品名', '状態']])

        # 加工済みファイルのダウンロード
        st.download_button(
            label="📥 加工済みデータをダウンロード",
            data=convert_df(df),
            file_name="mercari_profit_processed.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f'❌ ファイルの読み込み中にエラーが発生しました: {e}')
import streamlit as st
from PIL import Image
import io
import requests
import pandas as pd
import matplotlib.pyplot as plt

# 画像アップロード
st.header("🖼️ 画像で商品を検索")
uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # 仮の類似商品検索ロジック（ここをAPIやスクレイピングに変更可能）
    st.info("🔍 類似商品を検索中...")
    # ↓ここではダミーデータ（実際は画像→商品名→メルカリ・PayPay検索）
    data = {
        "商品名": ["Tシャツ", "Tシャツ 白", "おしゃれTシャツ"],
        "価格": [1200, 1300, 1250]
    }
    df = pd.DataFrame(data)

    # 📊 グラフで価格分布を表示
    st.subheader("📈 類似商品の価格分布")
    st.bar_chart(df["価格"])

    # 💾 CSVダウンロード
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ CSVでダウンロード", csv, "similar_products.csv", "text/csv")

    # 中央値・最頻値表示
    st.write("🧮 **中央値：**", df["価格"].median())
    st.write("🔁 **最頻値：**", df["価格"].mode()[0])
from PIL import Image
import io

st.header("📷 画像から類似商品検索")

uploaded_image = st.file_uploader("画像をアップロードしてください（例：商品写真）", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="アップロードした画像", use_column_width=True)

    # 仮：画像から商品名を推定（ここは将来的にAIモデルに置き換え予定）
    st.markdown("🔍 **AIによる予測商品名（例）:**")
    predicted_name = "Tシャツ（白 無地）"  # 仮の例
    st.success(predicted_name)

    if st.button("🔎 メルカリ・PayPayフリマで検索する"):
        # 検索リンク表示
        mercari_url = f"https://www.mercari.com/jp/search/?keyword={predicted_name}"
        paypay_url = f"https://paypayfleamarket.yahoo.co.jp/search?query={predicted_name}"
        st.markdown(f"🟥 [メルカリで検索]({mercari_url})")
        st.markdown(f"🟦 [PayPayフリマで検索]({paypay_url})")
