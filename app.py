import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions
import os

st.set_page_config(page_title="مساعد SEC", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# الإعداد الإجباري للنسخة المستقرة
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # استخدام الإعدادات الافتراضية المستقرة
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود")
    st.stop()

# قراءة ملفات المعايير
def load_sec_kb():
    text = ""
    ignore = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for f_name in os.listdir("."):
        if os.path.isfile(f_name) and f_name not in ignore:
            try:
                with open(f_name, 'r', encoding='utf-8', errors='ignore') as f:
                    text += f"\n--- {f_name} ---\n{f.read()}\n"
            except: continue
    return text

if "kb" not in st.session_state:
    st.session_state.kb = load_sec_kb()

# تعريف الموديل مع تحديد الإصدار المستقر يدوياً في الطلب
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
            # هنا التعديل الجوهري: نرسل الطلب للنسخة المستقرة v1
            full_content = f"المعايير:\n{st.session_state.kb[:30000]}\n\nالسؤال: {prompt}"
            
            # نحدد api_version='v1' في الخيارات لقتل خطأ v1beta
            response = model.generate_content(
                full_content,
                request_options=RequestOptions(api_version='v1')
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
