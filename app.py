import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="المساعد الهندسي", layout="wide")

# جلب المفتاح
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# مصفوفة الموديلات المتاحة (للتجربة التلقائية)
model_to_use = "gemini-1.5-flash" # هذا الأكثر ضماناً حالياً

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال السؤال
if prompt := st.chat_input("اسألني أي شيء هندسي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تشغيل الموديل
            model = genai.GenerativeModel(model_name=model_to_use)
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ في النظام: {e}")
