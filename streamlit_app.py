import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st import pandas as pd import plotly.express as px import plotly.graph_objects as go import numpy as np from datetime import datetime

————————————————

إعدادات الصفحة

————————————————

st.set_page_config( page_title="لوحة التحكم الاحترافية", page_icon="📊", layout="wide", initial_sidebar_state="expanded", )

————————————————

تنسيقات CSS مخصصة (يدعم RTL)

————————————————

st.markdown( """

<style>
    html, body, [data-testid="stAppViewContainer"], .main { direction: rtl; text-align: right; }
    [data-testid="stSidebar"] * { direction: rtl; text-align: right; }
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); }
    h1, h2, h3 { color: #1f77b4; }
    .stButton>button { background-color: #1f77b4; color: #fff; border-radius: 8px; padding: 0.5rem 1rem; border: none; }
    .stButton>button:hover { background-color: #155a8a; }
</style>""",
unsafe_allow_html=True,

)

————————————————

تهيئة حالة الجلسة

————————————————

if "data" not in st.session_state: st.session_state.data = pd.DataFrame()

if "manual_data" not in st.session_state: st.session_state.manual_data = []

————————————————

الشريط الجانبي

————————————————

with st.sidebar: st.title("📊 لوحة التحكم") st.markdown("---")

page = st.radio(
    "اختر القسم:",
    ["الرئيسية", "إدخال البيانات", "رفع الملفات", "التحليلات", "الرسوم البيانية"],
    index=0,
)

st.markdown("---")
st.info("💡 نصيحة: ابدأ بإدخال البيانات أو رفع ملف لعرض التحليلات")

————————————————

الصفحة الرئيسية

————————————————

if page == "الرئيسية": st.title("🏠 الصفحة الرئيسية") st.markdown("### مرحباً بك في لوحة التحكم الاحترافية")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="إجمالي السجلات",
        value=len(st.session_state.data) if not st.session_state.data.empty else 0,
        delta="جاهز للتحليل",
    )

with col2:
    st.metric(
        label="الأعمدة",
        value=len(st.session_state.data.columns) if not st.session_state.data.empty else 0,
        delta="متغيرات البيانات",
    )

with col3:
    st.metric(
        label="حالة البيانات",
        value="✓ جاهز" if not st.session_state.data.empty else "فارغ",
        delta="نظام تشغيلي",
    )

with col4:
    st.metric(
        label="آخر تحديث",
        value=datetime.now().strftime("%H:%M"),
        delta="الوقت الحالي",
    )

st.markdown("---")

st.subheader("📈 نظرة عامة على البيانات")

if not st.session_state.data.empty:
    st.dataframe(st.session_state.data, use_container_width=True)

    st.subheader("📊 إحصائيات سريعة")
    st.write(st.session_state.data.describe(include="all"))
else:
    st.info("لا توجد بيانات حالياً. يرجى إدخال البيانات من القسم المخصص.")

    st.markdown("### 🎯 مثال توضيحي")
    example_data = pd.DataFrame(
        {
            "التاريخ": pd.date_range(start="2024-01-01", periods=5),
            "المبيعات": [1200, 1500, 1800, 1300, 1600],
            "العملاء": [45, 52, 61, 48, 55],
            "الإيرادات": [50000, 62000, 75000, 54000, 66000],
        }
    )
    st.dataframe(example_data, use_container_width=True)

————————————————

إدخال البيانات

————————————————

elif page == "إدخال البيانات": st.title("✍️ إدخال البيانات يدوياً")

st.markdown("### أدخل بياناتك هنا")

with st.form("data_entry_form"):
    col1, col2 = st.columns(2)

    with col1:
        field1 = st.text_input("الحقل 1 (مثال: الاسم)")
        field3 = st.number_input("الحقل 3 (مثال: القيمة)", min_value=0.0)

    with col2:
        field2 = st.text_input("الحقل 2 (مثال: الفئة)")
        field4 = st.date_input("الحقل 4 (مثال: التاريخ)")

    submitted = st.form_submit_button("➕ إضافة السجل")

    if submitted:
        new_record = {
            "الحقل 1": field1,
            "الحقل 2": field2,
            "الحقل 3": field3,
            "الحقل 4": field4,
        }
        st.session_state.manual_data.append(new_record)
        st.success("✅ تم إضافة السجل بنجاح!")

if st.session_state.manual_data:
    st.markdown("### 📋 البيانات المدخلة")
    df_manual = pd.DataFrame(st.session_state.manual_data)
    st.dataframe(df_manual, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 حفظ البيانات"):
            st.session_state.data = df_manual
            st.success("✅ تم حفظ البيانات!")

    with col2:
        if st.button("🗑️ مسح الكل"):
            st.session_state.manual_data = []
            st.rerun()

    with col3:
        csv = df_manual.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 تحميل CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv",
        )

————————————————

رفع الملفات

————————————————

elif page == "رفع الملفات": st.title("📤 رفع الملفات")

st.markdown("### قم برفع ملف CSV أو Excel")

uploaded_file = st.file_uploader(
    "اختر ملف",
    type=["csv", "xlsx", "xls"],
    help="يدعم ملفات CSV و Excel",
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ تم رفع الملف بنجاح! عدد السجلات: {len(df)}")

        st.markdown("### 👁️ معاينة البيانات")
        st.dataframe(df.head(10), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("عدد الصفوف", len(df))
        with col2:
            st.metric("عدد الأعمدة", len(df.columns))

        if st.button("💾 حفظ البيانات للتحليل"):
            st.session_state.data = df
            st.success("✅ تم حفظ البيانات! يمكنك الآن الانتقال إلى قسم التحليلات")

    except Exception as e:
        st.error(f"❌ خطأ في قراءة الملف: {str(e)}")

————————————————

التحليلات

————————————————

elif page == "التحليلات": st.title("📊 التحليلات المتقدمة")

if st.session_state.data.empty:
    st.warning("⚠️ لا توجد بيانات للتحليل. يرجى إدخال البيانات أولاً.")
else:
    df = st.session_state.data

    st.markdown("### 📈 الإحصائيات الوصفية")
    st.dataframe(df.describe(include="all"), use_container_width=True)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        st.markdown("### 🔢 تحليل الأعمدة الرقمية")

        selected_col = st.selectbox("اختر عمود للتحليل:", numeric_cols)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("المتوسط", f"{df[selected_col].mean():.2f}")
        with col2:
            st.metric("الوسيط", f"{df[selected_col].median():.2f}")
        with col3:
            st.metric("الحد الأدنى", f"{df[selected_col].min():.2f}")
        with col4:
            st.metric("الحد الأقصى", f"{df[selected_col].max():.2f}")

    st.markdown("### ℹ️ معلومات البيانات")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**أنواع البيانات:**")
        st.write(df.dtypes)
    with col2:
        st.write("**القيم المفقودة:**")
        st.write(df.isnull().sum())

————————————————

الرسوم البيانية

————————————————

elif page == "الرسوم البيانية": st.title("📉 الرسوم البيانية التفاعلية")

if st.session_state.data.empty:
    st.warning("⚠️ لا توجد بيانات لعرضها. يرجى إدخال البيانات أولاً.")

    st.markdown("### 🎨 أمثلة على الرسوم البيانية")
    dates = pd.date_range(start="2024-01-01", periods=30)
    values = np.random.randint(100, 500, 30)
    fig1 = px.line(x=dates, y=values, title="مثال: الاتجاه الزمني", labels={"x": "التاريخ", "y": "القيمة"})
    st.plotly_chart(fig1, use_container_width=True)

    categories = ["فئة أ", "فئة ب", "فئة ج", "فئة د"]
    values2 = [30, 25, 20, 25]
    fig2 = px.pie(values=values2, names=categories, title="مثال: التوزيع")
    st.plotly_chart(fig2, use_container_width=True)

else:
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    all_cols = df.columns.tolist()

    chart_type = st.selectbox(
        "اختر نوع الرسم البياني:",
        ["رسم خطي", "رسم أعمدة", "رسم دائري", "رسم مبعثر", "رسم صندوقي"],
    )

    if chart_type == "رسم خطي" and len(numeric_cols) >= 1:
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("المحور X:", all_cols)
        with col2:
            y_col = st.selectbox("المحور Y:", numeric_cols)
        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} عبر {x_col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "رسم أعمدة" and len(numeric_cols) >= 1:
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("المحور X:", all_cols)
        with col2:
            y_col = st.selectbox("المحور Y:", numeric_cols)
        fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} حسب {x_col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "رسم دائري" and len(all_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            names_col = st.selectbox("الفئات:", all_cols)
        with col2:
            values_col = st.selectbox("القيم:", numeric_cols if numeric_cols else all_cols)
        fig = px.pie(df, names=names_col, values=values_col, title="التوزيع")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "رسم مبعثر" and len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("المحور X:", numeric_cols)
        with col2:
            y_col = st.selectbox("المحور Y:", numeric_cols)
        fig = px.scatter(df, x=x_col, y=y_col, title=f"العلاقة بين {x_col} و {y_col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "رسم صندوقي" and len(numeric_cols) >= 1:
        y_col = st.selectbox("اختر العمود:", numeric_cols)
        fig = px.box(df, y=y_col, title=f"توزيع {y_col}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("يرجى التأكد من وجود أعمدة رقمية كافية في البيانات لعرض هذا النوع من الرسوم.")

————————————————

التذييل

————————————————

st.markdown("---") st.markdown( "<div style='text-align: center; color: #666;'>لوحة التحكم الاحترافية © 2024</div>", unsafe_allow_html=True, )
