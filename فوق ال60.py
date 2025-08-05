import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="تحليل الموظفين بين 52 و60 سنة", layout="wide")
st.title("تحليل الموظفين في بيانات الموارد البشرية")

st.markdown("<div class='section-header'>يرجى تحميل ملف بيانات الموظفين (Excel)</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("ارفع الملف", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, header=0)
    selected_sheet = st.selectbox("اختر الجهة", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    
    # تنظيف الأعمدة
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]

    # استثناء جهات محددة
    excluded_departments = ['HC.نادي عجمان للفروسية', 'PD.الشرطة المحلية لإمارة عجمان', 'RC.الديوان الأميري']
    if 'الدائرة' in df.columns:
        df = df[~df['الدائرة'].isin(excluded_departments)]

    # التأكد من وجود عمود العمر
    if 'العمر' in df.columns:
        # تحويل العمود إلى أرقام (لو كان فيه قيم نصية)
        df['العمر'] = pd.to_numeric(df['العمر'], errors='coerce')

        # تصفية الموظفين بين 52 و60 سنة
        age_filtered_df = df[(df['العمر'] >= 52) & (df['العمر'] <= 60)]

        total_employees = len(df)
        filtered_count = len(age_filtered_df)
        percentage = (filtered_count / total_employees) * 100 if total_employees > 0 else 0

        st.subheader("📊 إحصائيات عامة")
        st.markdown(f"- **عدد الموظفين بين 52 و60 سنة:** {filtered_count}")
        st.markdown(f"- **النسبة من إجمالي الموظفين:** {percentage:.2f}%")

        st.subheader("📋 تفاصيل الموظفين")
        st.dataframe(age_filtered_df)

        # دالة لتحويل DataFrame إلى Excel بداخل BytesIO
        @st.cache_data
        def convert_df_to_excel_bytes(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            processed_data = output.getvalue()
            return processed_data

        # تجهيز البيانات للتحميل
        excel_data = convert_df_to_excel_bytes(age_filtered_df)

        # زر التحميل
        st.download_button(
            label="📥 تحميل البيانات كـ Excel",
            data=excel_data,
            file_name="الموظفين_بين_52_و_60.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("⚠️ لا يوجد عمود باسم 'العمر' في الملف.")
