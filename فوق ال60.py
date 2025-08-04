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

    excluded_departments = ['HC.نادي عجمان للفروسية', 'PD.الشرطة المحلية لإمارة عجمان', 'RC.الديوان الأميري']
    if 'الدائرة' in df.columns:
        df = df[~df['الدائرة'].isin(excluded_departments)]

    if 'العمر' in df.columns:
        total_employees = len(df)
        df_filtered = df.copy()

        # تجهيز التابات
        tab1, tab2, tab3, tab4 = st.tabs([
            "الذين أعمارهم فوق 60 (حاليًا)",
            "فوق 60 بعد 3 سنوات",
            "فوق 60 بعد 6 سنوات",
            "فوق 60 بعد 9 سنوات"
        ])

        # دالة لاستخراج الموظفين الذين سيصلون لعمر > 60 بعد عدد سنوات، دون تكرار
        def extract_group(df_input, years, previously_selected_ids):
            df_temp = df_input.copy()
            df_temp['العمر بعد سنوات'] = df_temp['العمر'] + years
            df_temp = df_temp[df_temp['العمر بعد سنوات'] > 60]
            if 'رقم الموظف' in df_temp.columns:
                df_temp = df_temp[~df_temp['رقم الموظف'].isin(previously_selected_ids)]
                new_ids = df_temp['رقم الموظف'].tolist()
            else:
                df_temp = df_temp[~df_temp.index.isin(previously_selected_ids)]
                new_ids = df_temp.index.tolist()
            return df_temp, new_ids

        selected_ids = []

        def display(tab, df_group, title):
            count = len(df_group)
            percent = round((count / total_employees) * 100, 2)
            with tab:
                st.subheader(f"{title}")
                st.write(f"🔢 عدد الموظفين: {count}")
                st.write(f"📊 النسبة من إجمالي الموظفين: {percent}%")
                st.dataframe(df_group)

        # تاب 1: حاليًا
        group1, ids1 = extract_group(df_filtered, 0, [])
        display(tab1, group1, "أعمارهم فوق 60 الآن")
        selected_ids.extend(ids1)

        # تاب 2: بعد 3 سنوات
        group2, ids2 = extract_group(df_filtered, 3, selected_ids)
        display(tab2, group2, "أعمارهم فوق 60 بعد 3 سنوات")
        selected_ids.extend(ids2)

        # تاب 3: بعد 6 سنوات
        group3, ids3 = extract_group(df_filtered, 6, selected_ids)
        display(tab3, group3, "أعمارهم فوق 60 بعد 6 سنوات")
        selected_ids.extend(ids3)

        # تاب 4: بعد 9 سنوات
        group4, ids4 = extract_group(df_filtered, 9, selected_ids)
        display(tab4, group4, "أعمارهم فوق 60 بعد 9 سنوات")

    else:
        st.error("⚠️ لم يتم العثور على عمود 'العمر' في الجدول. تأكد من وجوده.")
