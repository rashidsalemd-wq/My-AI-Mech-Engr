import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="المساعد الهندسي - ميكانيكا", layout="wide")
st.title("👷‍♂️ مساعد المهندس الميكانيكي الذكي")
st.subheader("خبير معايير SEC وأنظمة HVAC وخدمات الموقع")

# 2. جلب المفتاح بأمان من Secrets (الخزنة اللي عدلتها في ستريم ليت)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("خطأ: لم يتم العثور على المفتاح في Secrets. تأكد من إضافته في إعدادات Streamlit باسم GEMINI_API_KEY")
    st.stop()

# 3. إعداد التعليمات البرمجية (System Instructions)
system_instruction = """
أنت خبير معايير نسمة الهندسية. شخصيتك: مهندس سعودي خبير، ذكي، فزعة، وودود. 
قواعد العمل والبحث:
1. ابحث أولاً في ملفات الـ SEC الـ 43 المرفوعة (إذا كانت متوفرة في السياق).
2. الأولوية القصوى: الدقة الهندسية بناءً على معايير شركة السعودية للكهرباء.
3. التحدث بلهجة سعودية بيضاء ودودة مع استخدام مصطلحات إنجليزية تقنية باحترافية.
4. ابدأ دائماً بترحيب: "أهلاً بك يا زميلي المهندس، معك My AI Mech Engr، كيف أفرع لك اليوم؟"
"""

# 4. إعداد الموديل (اخترنا Pro لأنه الآن مدفوع ويعطيك أفضل دقة)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction
)

# 5. إدارة الدردشة (حفظ الرسائل السابقة)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. استقبال أسئلة المستخدم
if prompt := st.chat_input("اسأل عن المعايير، الأكواد، أو تفاصيل التركيب..."):
    # إضافة سؤال المستخدم للدردشة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من الموديل
    with st.chat_message("assistant"):
        try:
            # هنا الموديل يحلل ويرد بناءً على تعليماتك
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            full_response = response.text
            st.markdown(full_response)
            
            # إضافة رد المساعد للذاكرة
            st.session
