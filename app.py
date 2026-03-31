import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مساعد SEC المطور", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# 1. إعداد المفتاح
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# 2. قراءة ملفات المعايير (الـ 43 ملف)
def load_sec_kb():
    content = ""
    exclude = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for f in os.listdir("."):
        if os.path.isfile(f) and f not in exclude:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    content += f"\n--- {f} ---\n{file.read()}\n"
            except: continue
    return content

if "kb" not in st.session_state:
    st.session_state.kb = load_sec_kb()

# 3. تعريف الموديل (بدون تعقيدات لإصلاح خطأ v1beta)
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
            # إرسال السياق مع السؤال مباشرة
            full_prompt = f"استخدم المعايير التالية للرد: {st.session_state.kb[:30000]}\n\nالسؤال: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # إذا استمر خطأ 404، سنعرف السبب هنا
            st.error(f"خطأ في الاتصال: {e}")
