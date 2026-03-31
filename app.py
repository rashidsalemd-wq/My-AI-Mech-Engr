import streamlit as st
import google.generativeai as genai
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="مساعد SEC", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# 2. تفعيل المفتاح (تأكد إنه في Secrets باسم GEMINI_API_KEY)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# 3. وظيفة قراءة الملفات من قيت هب
def get_sec_data():
    all_text = ""
    # الملفات اللي نبي نقرأها (أي ملف غير ملفات النظام)
    ignore = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for file in os.listdir("."):
        if os.path.isfile(file) and file not in ignore:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    all_text += f"\n[مصدر: {file}]\n" + f.read()
            except:
                continue
    return all_text

# تحميل البيانات مرة واحدة
if "sec_data" not in st.session_state:
    st.session_state.sec_data = get_sec_data()

# 4. إعداد الموديل (استخدام الاسم المباشر لحل مشكلة 404)
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. واجهة الدردشة
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
        # دمج السؤال مع بيانات الملفات
        full_query = f"استخدم المعلومات التالية للإجابة بدقة: {st.session_state.sec_data[:30000]}\n\nالسؤال: {prompt}"
        try:
            response = model.generate_content(full_query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
