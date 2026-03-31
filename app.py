import streamlit as st
import google.generativeai as genai
import os

# إعداد الصفحة
st.set_page_config(page_title="مساعد SEC المطور", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# الربط مع الحساب
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("تأكد من وجود API Key في Secrets")
    st.stop()

# قراءة الملفات المرفوعة في GitHub
def get_knowledge_base():
    text = ""
    ignore = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for file in os.listdir("."):
        if os.path.isfile(file) and file not in ignore:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    text += f"\n--- مصدر: {file} ---\n{f.read()}\n"
            except: continue
    return text

if "kb" not in st.session_state:
    st.session_state.kb = get_knowledge_base()

# الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اسألني عن مواصفات SEC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # نرسل السؤال مع جزء من المعايير (أول 30 ألف حرف لضمان السرعة)
            context = st.session_state.kb[:30000]
            response = model.generate_content(f"المعايير:\n{context}\n\nالسؤال: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ: {e}")
