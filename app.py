import yagmail

# 利益通知機能（メール送信）※本運用にはセキュリティ設定が必要です
st.subheader("📧 利益が出たらメール通知")

notify_email = st.text_input("通知先メールアドレス", placeholder="example@gmail.com")
if notify_email and profit > 0:
    if st.button("メールで通知する"):
        try:
            yag = yagmail.SMTP("あなたのGmailアドレス", "アプリパスワード")
            subject = "利益商品通知【リサーチナビ】"
            contents = [
                f"商品名: {product_name}",
                f"利益: ¥{profit:,} 円",
                f"販売価格: ¥{sell_price:,}",
                f"仕入れ値: ¥{cost_price:,}",
                f"送料: ¥{shipping_fee:,}"
            ]
            yag.send(notify_email, subject, contents)
            st.success(f"通知を送信しました！⇒ {notify_email}")
        except Exception as e:
            st.error(f"通知失敗: {str(e)}")
