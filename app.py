import streamlit as st
import requests
import pandas as pd

# مشخصات اتصال به ایتا
TOKEN = "bot508914:1a90f8a2-e801-4e64-abdf-9fad6e5922d6"
CHANNEL_ID = 11209050

def send_message(text_to_send):
    url = f"https://eitaayar.ir/api/{TOKEN}/sendMessage"
    data_packet = {
        'chat_id': CHANNEL_ID,
        'text': text_to_send
    }
    response = requests.post(url, data=data_packet)
    return response.json()

# --- تنظیمات صفحه ---
st.set_page_config(page_title="پنل مدیریت پیشرفته قیمت‌ها", page_icon="🥩", layout="centered")

st.title("📢 پنل مدیریت و ارسال پویا قیمت‌ها")
st.write("در جدول زیر می‌توانید قیمت‌ها را تغییر دهید یا با دکمه Add row محصول جدید اضافه کنید.")

st.divider()

# ۱. ساخت لیست اولیه محصولات به عنوان نمونه برای کارفرما
if 'price_data' not in st.session_state:
    st.session_state.price_data = pd.DataFrame([
        {"نام محصول": "ران Gوسفندی", "قیمت (تومان)": "550,000"},
        {"نام محصول": "سینه مرغ", "قیمت (تومان)": "120,000"},
        {"نام محصول": "فیله گوساله", "قیمت (تومان)": "620,000"},
        {"نام محصول": "چرخ کرده مخلوط", "قیمت (تومان)": "480,000"}
    ])

# ۲. نمایش جدول با قابلیت ویرایش، حذف و اضافه کردن ردیف جدید
edited_df = st.data_editor(
    st.session_state.price_data,
    num_rows="dynamic", # این گزینه اجازه میده کارفرما ردیف جدید بسازه یا حذف کنه
    use_container_width=True
)

st.divider()

# ۳. دکمه شلیک پیام به کانال
if st.button("🚀 بروزرسانی و ارسال لیست جدید به کانال", type="primary"):
    
    # ساخت متن پست به صورت پویا از روی جدول
    post_text = "📢 لیست قیمت روز محصولات پروتئینی\n\n"
    
    for index, row in edited_df.iterrows():
        name = str(row["نام محصول"]).strip()
        price = str(row["قیمت (تومان)"]).strip()
        
        # اگر سطر خالی نبود، اضافه‌اش کن
        if name and price and name != "None" and price != "None":
            post_text += f"🔹 {name} : {price} تومان\n"
            
    post_text += "\n✨ خرید حضوری و آنلاین"
    
    # ارسال به ایتا
    with st.spinner("در حال ارسال لیست جدید..."):
        result = send_message(post_text)
        
    if result.get('ok'):
        st.success("✅ لیست قیمت‌های جدید با موفقیت ارسال شد!")
        # ذخیره آخرین وضعیت جدول در سیستم
        st.session_state.price_data = edited_df
    else:
        st.error(f"❌ خطا در ارسال: {result.get('description')}")