import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة المستخدم (تظهر للمهندسين في الموقع)
st.set_page_config(page_title="My AI Mech Engr", layout="centered", page_icon="👷‍♂️")

# التنسيق الجمالي للواجهة
st.title("👷‍♂️ My AI Mech Engr")
# التنسيق الجمالي المحسن (حل مشكلة ترتيب النص)
st.markdown("""
<div style="direction: rtl; text-align: right;">
    <h3>👷 My AI Mech Engr</h3>
    <p><b>مساعد المهندس الشخصي:</b> خبير تقني متخصص في أنظمة التكييف (HVAC)، مكافحة الحريق (Firefighting)، كاميرات المراقبة (CCTV)، وشبكات الصرف الصحي (Plumbing) وفق معايير SEC.</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# 2. إعداد الـ API Key الخاص بك (تم التحديث)
API_KEY = "AIzaSyAHw--SskwlsoBGd5CDT8gA368esIwvcbQ"

genai.configure(api_key=API_KEY)

# 3. توجيهات النظام (الخلفية الهندسية للمساعد)
system_instruction = """
أنت 'My AI Mech Engr'. شخصيتك: مهندس سعودي خبير، ذكي، فزعة، وودود.

قواعد العمل والبحث:
1. ابحث أولاً في ملفات SEC المرفوعة في المستودع (تفكيك الكود: TESP108، الجزء 10، مراجعة 0).
2. المراجع التكميلية: NFPA و HCIS (أحدث الإصدارات).
3. السياق المهني: محطات تحويل كهرباء (GIS Substations)، متخصص في (HVAC, Fire Protection, CCTV, Plumbing).
4. اللهجة: سعودية بيضاء ودودة مع استخدام مصطلحات إنجليزية تقنية باحترافية.
5. ابدأ دائماً بترحيب: "أهلاً بك يا زميلي المهندس، معك My AI Mech Engr، كيف أقدر أفزع لك اليوم؟"
"""

# إعداد النموذج
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 4. إدارة الدردشة (حفظ الرسائل السابقة)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال المهندس
if prompt := st.chat_input("اسأل عن المعايير، الأكواد، أو تفاصيل التركيب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الإجابة
    with st.chat_message("assistant"):
        try:
            # هنا المساعد سيستخدم ذكاء Gemini مع التعليمات المذكورة
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حصل خطأ فني يا هندسة: {e}")
