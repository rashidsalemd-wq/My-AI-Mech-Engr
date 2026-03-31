import streamlit as st
import google.generativeai as genai
import os

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="مساعد SEC المطور", layout="wide")
st.title("👷‍♂️ مساعد المهندس راشد - خبير المعايير")

# 2. إعداد الاتصال بالحساب المدفوع (النسخة المستقرة)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # نحدد الإصدار v1 لضمان التوافق مع الحساب المدفوع وتجنب خطأ 404
    genai.configure(api_key=api_key, transport='rest') 
except Exception as e:
    st.error(f"تأكد من إعداد المفتاح في Secrets: {e}")
    st.stop()

# 3. وظيفة قراءة الملفات من المستودع
def load_all_sec_files():
    context = ""
    # استثناء ملفات النظام
    excluded = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    all_files = [f for f in os.listdir(".") if os.path.isfile(f) and f not in excluded]
    
    for file_name in all_files:
        try:
            with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                context += f"\n--- بداية ملف: {file_name} ---\n"
                context += f.read() + "\n"
        except:
            continue
    return context

# تخزين البيانات في الجلسة لسرعة الاستجابة
if "sec_knowledge" not in st.session_state:
    with st.spinner("جاري مسح ملفات المعايير..."):
        st.session_state.sec_knowledge = load_all_sec_files()

# 4. تعريف الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. إدارة سجل الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. معالجة سؤال المهندس
if prompt := st.chat_input("اسألني عن أي تفصيلة في معايير SEC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # دمج المعايير مع السؤال (Context Window)
            full_instruction = f"""
            أنت خبير هندسي سعودي. استخدم المعلومات المستخرجة من ملفات SEC المرفقة أدناه للإجابة بدقة:
            
            {st.session_state.sec_knowledge[:35000]}
            
            سؤال المهندس: {prompt}
            """
            response = model.generate_content(full_instruction)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالنظام: {e}")
