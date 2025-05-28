import streamlit as st
import pandas as pd
from datetime import datetime

# アプリタイトルと説明
st.title("🧮 メルカリ利益計算ツール")
st.write("こんにちは！これはメルカリ転売向けの利益計算アプリです。")

# =====================
# 📷 画像アップロード機能
# =====================
st.subheader("🖼️ 商品画像のアップロード")
uploaded_image = st.file_uploader("画像ファイルを選択してください（JPG, PNG）", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    st.image(uploaded_image, caption="アップロードされた画像", use_column_width=True)
    st.success("画像をアップロードしました！")

# =====================
# 💰 利益計算フォーム
# =====================
st.subheader("💸 利益計算フォーム")
price = st.number_input("販売価格（円）", value=1000)
shipping = st.number_input("送料（円）", value=200)
purchase_cost = st.number_input("仕入れ値（円）", value=500)

# =====================
# 🔍 計算処理
# =====================
mercari_fee = price * 0.1
profit = price - mercari_fee - shipping - purchase_cost

# =====================
# 📊 結果表示
# =====================
st.write(f"メルカリ手数料: {mercari_fee:.0f} 円")
st.write(f"利益: {profit:.0f} 円")

# =====================
# 💾 保存ボタン（CSV形式）
# =====================
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
