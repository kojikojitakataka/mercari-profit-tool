import streamlit as st
import pandas as pd

st.title('📦 メルカリ利益計算ツール')

uploaded_file = st.file_uploader('📂 Excelファイルをアップロードしてください', type=['xlsm', 'xlsx'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write('✅ 最初の5行を表示します：')
        st.dataframe(df.head())
    except Exception as e:
        st.error(f'❌ ファイルの読み込み中にエラーが発生しました: {e}')

