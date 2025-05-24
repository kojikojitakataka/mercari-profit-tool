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
st.markdown('---')
st.header("📝 出品説明文 自動生成ツール")

product_name = st.text_input("商品名を入力してください")

if st.button("出品文を生成する"):
    if product_name:
        description = f"""
【商品名】\n{product_name}

【商品の説明】
ご覧いただきありがとうございます。
こちらの商品は「{product_name}」です。
丁寧に保管しており、状態は良好です。
即購入OK、早い者勝ちです！

【発送について】
防水対策・緩衝材を使用し、迅速に発送いたします。
24時間以内の発送を心がけています！
【その他】

不明点があれば、お気軽にコメントください。
        """
        st.text_area("👇 コピペ用出品文", description, height=250)
    else:
        st.warning("商品名を入力してください。")
import streamlit as st
import pandas as pd

st.title("メルカリ利益計算＆ランキングツール")

uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 利益を計算
    df["手数料"] = df["販売価格"] * df["手数料（％）"] / 100
    df["利益"] = df["販売価格"] - df["仕入れ値"] - df["送料"] - df["手数料"]

    # 並び替え方法を選択
    sort_key = st.selectbox("並び替え方法を選んでください", ["利益", "いいね数", "販売数"])
    df_sorted = df.sort_values(by=sort_key, ascending=False)

    st.subheader("📊 ランキング表")
    st.dataframe(df_sorted[["商品名", "利益", "いいね数", "販売数"]])

else:
    st.info("Excel または CSV ファイルをアップロードしてください。")

