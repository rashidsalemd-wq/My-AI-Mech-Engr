import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="المساعد الهندسي", layout="wide")

# جلب المفتاح من Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# تعريف الموديل بالاسم الكامل (لحل مشكلة 404)
# جربنا Flash هنا لأنها الأسرع في الربط مع الحسابات الجديدة
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    # اختبار بسيط للموديل
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"خطأ في الاتصال بالموديل: {e}")

# واجهة المستخدم
st.title("👷‍♂️ مساعد المهندس راشد")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
