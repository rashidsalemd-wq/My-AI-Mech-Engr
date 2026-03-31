import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="المساعد الهندسي", layout="wide")
st.title("👷‍♂️ مساعد المهندس الميكانيكي الذكي")

# 2. جلب المفتاح بأمان
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("تأكد من وضع المفتاح في Secrets في Streamlit")
    st.stop()

# 3. إعداد الموديل
system_instruction = "أنت مهندس ميكانيكي خبير بمواصفات شركة الكهرباء (SEC)."
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction
)

# 4. إدارة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استقبال الأسئلة
if prompt := st.chat_input("اسألني أي شيء هندسي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
