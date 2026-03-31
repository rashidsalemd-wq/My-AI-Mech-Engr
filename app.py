import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="المساعد الهندسي لشركة SEC", layout="wide")

# 1. إعداد المفتاح
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("تأكد من وضع المفتاح في Secrets")
    st.stop()

# 2. وظيفة قراءة جميع الملفات من المسار الرئيسي (Root)
def get_all_files_content():
    combined_content = ""
    # الملفات التي نريد تجاهلها (ملفات النظام)
    exclude = ['app.py', 'requirements.txt', 'packages.txt', '.gitignore', 'README.md']
    
    # يمر على كل الملفات في المستودع
    for file in os.listdir("."):
        if file not in exclude and os.path.isfile(file):
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    combined_content += f"\n--- محتوى ملف: {file} ---\n"
                    combined_content += f.read()
            except:
                continue
    return combined_content

# 3. تجهيز قاعدة البيانات والتعليمات
with st.spinner("جاري قراءة معايير SEC..."):
    sec_knowledge = get_all_files_content()

system_instructions = f"""
أنت المساعد التقني للمهندس راشد. خبير في معايير شركة السعودية للكهرباء (SEC).
مصدرك الأساسي هو الملفات المرفقة التي سأزودك بها. 
إذا سألك المهندس راشد عن معلومة، ابحث في النص أدناه:
{sec_knowledge[:15000]} # نأخذ أهم جزء لضمان السرعة

قواعد الرد:
1. إذا وجدت المعلومة في الملفات، اذكر اسم الملف إذا أمكن.
2. إذا لم تجدها، أجب من خبرتك الهندسية العامة وقل "بناءً على الممارسة الهندسية العامة".
3. الرد بلهجة سعودية بيضاء محترفة.
"""

# 4. تشغيل الموديل
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instructions
)

# 5. واجهة الدردشة
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
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
