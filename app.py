import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="المساعد الهندسي", layout="wide")

# 1. جلب المفتاح وتفعيله
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# 2. حل مشكلة 404 (اختيار الموديل المتاح تلقائياً)
try:
    # نبحث عن الموديلات المتاحة لحسابك المدفوع
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # نختار 1.5 flash إذا وجد، وإلا نختار أول موديل متاح
    selected_model = next((m for m in available_models if "gemini-1.5-flash" in m), available_models[0])
    model = genai.GenerativeModel(model_name=selected_model)
except Exception as e:
    st.error(f"خطأ في الوصول للموديلات: {e}")
    st.stop()

# 3. واجهة المستخدم
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
        try:
            # استخدام generate_content مباشرة للتبسيط وحل التعليق
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الرد: {e}")
