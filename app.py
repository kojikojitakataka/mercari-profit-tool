import streamlit as st
import pandas as pd

st.title("メルカリ利益計算＆ランキング＆在庫管理ツール")

uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 利益を計算
    df["手数料"] = df["販売価格"] * df["手数料（％）"] / 100
    df["利益"] = df["販売価格"] - df["仕入れ値"] - df["送料"] - df["手数料"]

    # ステータス判定
    def judge_status(stock):
        if stock <= 0:
            return "売り切れ（在庫なし）"
        else:
            return "出品中"

    df["ステータス"] = df["在庫数"].apply(judge_status)

    # 並び替え方法を選択
    sort_key = st.selectbox("並び替え方法を選んでください", ["利益", "いいね数", "販売数"])
    df_sorted = df.sort_values(by=sort_key, ascending=False)

    st.subheader("📊 ランキング表")
    st.dataframe(df_sorted[["商品名", "利益", "いいね数", "販売数", "在庫数", "ステータス"]])
else:
    st.info("Excel または CSV ファイルをアップロードしてください。")
# 状態でフィルターをかける（オプション）
if '状態' in df.columns:
    st.subheader("📦 状態でフィルター")
    状態フィルタ = st.multiselect("表示したい状態を選んでください", df['状態'].unique(), default=df['状態'].unique())
    df = df[df['状態'].isin(状態フィルタ)]

st.subheader("📋 在庫・販売管理一覧")
st.dataframe(df)
