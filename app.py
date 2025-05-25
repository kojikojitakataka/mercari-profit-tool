import streamlit as st
import pandas as pd

st.set_page_config(page_title="メルカリ利益計算ツール", layout="wide")

st.title("📦 メルカリ利益計算ツール")

uploaded_file = st.file_uploader("📂 Excelファイルをアップロードしてください", type=["xlsx", "xlsm"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # 利益を自動計算
        if {"販売価格", "送料", "手数料（％）", "仕入れ値"}.issubset(df.columns):
            df["手数料"] = df["販売価格"] * df["手数料（％）"] / 100
            df["利益"] = df["販売価格"] - df["送料"] - df["手数料"] - df["仕入れ値"]
        else:
            st.warning("「販売価格」「送料」「手数料（％）」「仕入れ値」列が必要です。")

        # 並び替え（③）
        st.sidebar.subheader("🔽 並び替えオプション")
        sort_column = st.sidebar.selectbox("並び替え対象列を選んでください", df.columns, index=0)
        sort_order = st.sidebar.radio("並び順", ["降順（多い順）", "昇順（少ない順）"])
        df = df.sort_values(by=sort_column, ascending=(sort_order == "昇順（少ない順）"))

        # フィルター（④）
        if "状態" in df.columns:
            st.sidebar.subheader("📦 状態でフィルター")
            状態フィルター = st.sidebar.multiselect("表示したい状態", df["状態"].unique(), default=df["状態"].unique())
            df = df[df["状態"].isin(状態フィルター)]

        # 出品文自動生成（②）
        if "商品名" in df.columns:
            st.subheader("📝 出品説明文（自動生成）")
            df["出品文"] = df["商品名"].apply(lambda x: f"{x}をご覧いただきありがとうございます！\n状態良好で、丁寧に梱包して発送します♪\n即購入OKです。よろしくお願いします。")
        else:
            st.warning("「商品名」列がないため出品文の自動生成ができません。")

        st.subheader("📊 データプレビュー")
        st.dataframe(df)

        # ダウンロードボタン
        @st.cache_data
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')

        st.download_button(
            label="📥 加工済みデータをダウンロード",
            data=convert_df(df),
            file_name="mercari_profit_processed.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ ファイルの読み込み中にエラーが発生しました: {e}")
else:
    st.info("左のサイドバーからExcelファイルをアップロードしてください。")

