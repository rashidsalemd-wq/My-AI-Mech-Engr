import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مساعد SEC المطور", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# 1. إعداد المفتاح للنسخة المستقرة
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# 2. قراءة ملفات المعايير الـ 43
@st.cache_data
def load_all_documents():
    full_text = ""
    excluded = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for file in os.listdir("."):
        if os.path.isfile(file) and file not in excluded:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    full_text += f"\n--- مصدر: {file} ---\n{f.read()}\n"
            except: continue
    return full_text

context_data = load_all_documents()

# 3. استخدام الموديل المستقر (v1)
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # إرسال السياق (المعايير) مع السؤال في طلب واحد
            # تم تحديد 30000 حرف لضمان عدم تجاوز حدود الذاكرة والسرعة
            refined_prompt = f"بناءً على ملفات SEC التالية:\n{context_data[:30000]}\n\nأجب على سؤال المهندس: {prompt}"
            
            response = model.generate_content(refined_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
