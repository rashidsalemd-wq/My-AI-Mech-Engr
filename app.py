import streamlit as st
import google.generativeai as genai
import os

# إعداد الصفحة
st.set_page_config(page_title="مساعد SEC المطور", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# جلب المفتاح
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # ملاحظة: السطر القادم هو الحل لخطأ 404
    genai.configure(api_key=api_key, transport='rest') 
except Exception as e:
    st.error(f"خطأ في المفتاح: {e}")
    st.stop()

# وظيفة قراءة الملفات
def load_sec_data():
    all_content = ""
    ignore = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    files = [f for f in os.listdir(".") if os.path.isfile(f) and f not in ignore]
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                all_content += f"\n--- {file} ---\n{f.read()}\n"
        except: continue
    return all_content

if "sec_kb" not in st.session_state:
    st.session_state.sec_kb = load_sec_data()

# اختيار الموديل بنسخته المستقرة
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اسألني عن أي تفصيلة في معايير SEC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # دمج المعايير مع السؤال
            context = st.session_state.sec_kb[:30000]
            full_prompt = f"استخدم المعايير التالية للرد: {context}\n\nسؤال المهندس راشد: {prompt}"
            
            # الطلب باستخدام النسخة المستقرة
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
