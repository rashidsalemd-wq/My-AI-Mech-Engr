import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مساعد SEC الذكي", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - إصدار Gemini 2.0")

# 1. إعداد المفتاح
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

# 2. قراءة ملفات المعايير
@st.cache_data
def load_sec_files():
    all_text = ""
    ignore = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for file in os.listdir("."):
        if os.path.isfile(file) and file not in ignore:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    all_text += f"\n--- ملف: {file} ---\n{f.read()}\n"
            except: continue
    return all_text

sec_context = load_sec_files()

# 3. استخدام الموديل المتوفر في حسابك (Gemini 2.0 Flash)
# ملاحظة: هذا الموديل يدعم الحسابات الاحترافية Tier 1
model = genai.GenerativeModel('gemini-3.0-flash-preview') 

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اسألني عن أي معيار هندسي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # دمج الخبرة مع السؤال
            full_input = f"أنت خبير في معايير SEC. استعن بالنص التالي:\n{sec_context[:30000]}\n\nالسؤال: {prompt}"
            response = model.generate_content(full_input)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ في الاتصال بالموديل 2.0: {e}")
            st.info("نصيحة: إذا استمر الخطأ، جرب تغيير اسم الموديل إلى 'gemini-2.0-flash' فقط.")
