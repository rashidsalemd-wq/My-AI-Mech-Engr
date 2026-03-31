import streamlit as st
import google.generativeai as genai
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="المساعد الهندسي - SEC", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد (نسخة المعايير)")

# 2. جلب المفتاح وتفعيل الموديل
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # تعريف الموديل مباشرة لتجنب خطأ NotFound
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في إعدادات المفتاح: {e}")
    st.stop()

# 3. وظيفة قراءة ملفات المعايير من الـ Root
def load_sec_knowledge():
    context = ""
    # ملفات نتجاهلها عشان ما تخرب الذاكرة
    ignore_files = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    
    files = [f for f in os.listdir(".") if os.path.isfile(f) and f not in ignore_files]
    
    for file_name in files:
        try:
            with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                context += f"\n--- مصدر من ملف: {file_name} ---\n"
                context += f.read() + "\n"
        except:
            continue
    return context

# 4. تجهيز الذاكرة (تحدث مرة واحدة عند التشغيل)
if "knowledge_base" not in st.session_state:
    with st.spinner("جاري فحص ملفات المعايير..."):
        st.session_state.knowledge_base = load_sec_knowledge()

# 5. إدارة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. الرد على المستخدم
if prompt := st.chat_input("اسألني عن أي معيار في SEC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # دمج السؤال مع الملفات في طلب واحد (Context Injection)
            full_prompt = f"""
            أنت مهندس ميكانيكي خبير. استخدم المعلومات التالية للإجابة على سؤال المستخدم بدقة.
            المعلومات المستخرجة من ملفات المعايير:
            {st.session_state.knowledge_base[:20000]} 
            
            سؤال المستخدم: {prompt}
            """
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
