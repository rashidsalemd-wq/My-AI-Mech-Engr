import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="مساعد SEC - إصدار 2.5", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد (Gemini 2.5)")

# جلب المفتاح
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("المفتاح غير موجود")
    st.stop()

# قراءة الملفات الهندسية
@st.cache_data
def load_sec_files():
    all_text = ""
    ignore = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    for f in os.listdir("."):
        if os.path.isfile(f) and f not in ignore:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    all_text += f"\n--- ملف: {f} ---\n{file.read()}\n"
            except: continue
    return all_text

sec_data = load_sec_files()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("اسألني عن أي معيار هندسي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # استخدام موديل 2.5 اللي ظهر في قائمتك
        model_name = "gemini-2.5-flash-preview-tts"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{"text": f"أنت خبير في معايير SEC. استعن بالنص التالي للإجابة:\n{sec_data[:40000]}\n\nالسؤال: {prompt}"}]
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            if 'candidates' in result:
                answer = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("الموديل لم يستطع الرد، تأكد من صلاحية المفتاح لهذا الإصدار.")
                st.json(result) # لإظهار تفاصيل الخطأ إذا وُجد
        except Exception as e:
            st.error(f"فشل الاتصال بموديل 2.5: {e}")
