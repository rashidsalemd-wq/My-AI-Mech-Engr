import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مساعد SEC المطور", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد")

# 1. الإعداد الأساسي (الذي نجح معك سابقاً)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # نستخدم الموديل الأكثر استقراراً ومجرباً من قبلك
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error(f"خطأ في إعداد المفتاح: {e}")
    st.stop()

# 2. وظيفة قراءة الملفات "ببساطة" (السر هنا)
def get_sec_knowledge():
    combined_text = ""
    # تجاهل ملفات الكود والنظام
    ignored = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    # جلب كل ملفات المعايير من المجلد الرئيسي
    for filename in os.listdir("."):
        if os.path.isfile(filename) and filename not in ignored:
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    combined_text += f"\n--- محتوى ملف: {filename} ---\n"
                    combined_text += f.read() + "\n"
            except:
                continue
    return combined_text

# تحميل البيانات في ذاكرة الجلسة لمرة واحدة فقط
if "sec_kb" not in st.session_state:
    with st.spinner("جاري قراءة ملفات المعايير..."):
        st.session_state.sec_kb = get_sec_knowledge()

# 3. واجهة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني عن معايير SEC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # هنا نقوم بدمج محتوى ملفاتك مع سؤالك في طلب واحد
            # أخذنا أول 30 ألف حرف لضمان السرعة وعدم تجاوز الحدود
            context = st.session_state.sec_kb[:30000]
            
            full_prompt = f"""
            أنت خبير هندسي. استخدم المعايير التالية المأخوذة من ملفاتك للإجابة بدقة:
            
            {context}
            
            سؤال المهندس راشد: {prompt}
            """
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")
