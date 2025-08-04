import streamlit as st
import pandas as pd

st.set_page_config(page_title="تحليل الموظفين فوق الـ 60", layout="wide")
st.title("تحليل الموظفين في بيانات الموارد البشرية")

st.markdown("<div class='section-header'>يرجى تحميل ملف بيانات الموظفين (Excel)</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("ارفع الملف", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None, header=0)
    selected_sheet = st.selectbox("اختر الجهة", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]

    # استبعاد جهات معينة
    excluded_departments = ['HC.نادي عجمان للفروسية', 'PD.الشرطة المحلية لإمارة عجمان', 'RC.الديوان الأميري']
    if 'الدائرة' in df.columns:
        df = df[~df['الدائرة'].isin(excluded_departments)]

    # التأكد من وجود عمود العمر
    if 'العمر' in df.columns:
        total_employees = len(df)

        tab1, tab2, tab3, tab4 = st.tabs(["الذين أعمارهم فوق 60 (حاليًا)", 
                                          "فوق 60 بعد 3 سنوات", 
                                          "فوق 60 بعد 6 سنوات", 
                                          "فوق 60 بعد 9 سنوات"])

        def display_tab(df, added_years, tab):
            df_temp = df.copy()
            df_temp['العمر بعد سنوات'] = df_temp['العمر'] + added_years
            df_filtered = df_temp[df_temp['العمر بعد سنوات'] > 60]
            count = len(df_filtered)
            percentage = round((count / total_employees) * 100, 2)

            with tab:
                st.subheader(f"عدد الموظفين: {count}")
                st.write(f"النسبة من إجمالي الموظفين: {percentage}%")
                st.dataframe(df_filtered)

        display_tab(df, 0, tab1)
        display_tab(df, 3, tab2)
        display_tab(df, 6, tab3)
        display_tab(df, 9, tab4)

    else:
        st.error("⚠️ لم يتم العثور على عمود 'العمر' في الجدول. تأكد أن العمود موجود باسم صحيح.")
