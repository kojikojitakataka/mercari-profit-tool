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
