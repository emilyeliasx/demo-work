import pandas as pd
import streamlit as st 
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

import os.path
import pathlib



st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="Customer Test Dashboard", page_icon=":bar_chart:", layout="wide")

# # ---- SIDE BAR ----
st.sidebar.header("Upload Your Data")

uploaded_file = st.sidebar.file_uploader("Choose a CSV file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = uploaded_file.getvalue().decode('utf-8').splitlines()         
    st.session_state["preview"] = ''
    for i in range(0, min(5, len(data))):
        st.session_state["preview"] += data[i]
preview = st.sidebar.text_area("CSV Preview", "", height=150, key="preview")


# # ---- MAINPAGE ----
st.title(":bar_chart: Customer Dashboard")
st.markdown("##")

@st.cache
def get_data(path:str)->pd.DataFrame:
    data_frame = pd.read_csv(
        path,
    )
    return data_frame

# customer_data = get_data("customer_data.csv") # path to the file

all_visuals = ['NA Info', 'Descriptive Analysis', 'Distribution of Numerical Columns', 'Count Plots of Categorical Columns', 'Box Plots']       
visuals = st.sidebar.multiselect("Choose which visualizations you want to see 👇", all_visuals)

if uploaded_file is not None:
    customer_data = pd.read_csv(uploaded_file)

    st.write(f"Rows: {customer_data.shape[0]}")
    st.write(f"Columns: {customer_data.shape[1]}")

    # if st.checkbox("Show description of dataset"):
    #     st.table(customer_data.describe())

    st.write(customer_data)

    if 'NA Info' in visuals:
        st.subheader('NA Value Information')
        if customer_data.isnull().sum().sum() == 0:
            st.write('There is not any NA value in your dataset.')
        else:
            nan_count = customer_data.isna().sum()
            st.write(nan_count)

    if 'Descriptive Analysis' in visuals:
        st.subheader('Descriptive Analysis:')
        st.dataframe(customer_data.describe())

    num_columns = customer_data.select_dtypes(exclude='object').columns
    cat_columns = customer_data.select_dtypes(include='object').columns

    if 'Distribution of Numerical Columns' in visuals:
        if len(num_columns) == 0:
            st.write("There are no numerical columns in the data.")
        else:
            selected_num_columns = st.sidebar.multiselect("Choose columns for distribution plots:" ,num_columns)
            st.subheader('Distribution of numerical columns')
            i = 0
            while (i < len(selected_num_columns)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_num_columns)):
                        break

                    fig = px.histogram(customer_data, x = selected_num_columns[i], color_discrete_sequence=px.colors.qualitative.Pastel2)
                    fig.update_xaxes(type='category')
                    j.plotly_chart(fig, use_container_width=True)
                    i += 1

    if 'Count Plots of Categorical Columns' in visuals:

        if len(cat_columns) == 0:
            st.write('There is no categorical columns in the data.')
        else:
            selected_cat_cols = st.sidebar.multiselect('Choose columns for Count plots:', cat_columns)
            st.subheader('Count plots of categorical columns')
            i = 0
            while (i < len(selected_cat_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_cat_cols)):
                        break

                    fig = px.histogram(customer_data, x = selected_cat_cols[i], color_discrete_sequence=px.colors.qualitative.Pastel2)
                    j.plotly_chart(fig, use_container_width=True)
                    i += 1

    if 'Box Plots' in visuals:
        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols = st.sidebar.multiselect('Choose columns for Box plots:', num_columns)
            st.subheader('Box plots')
            i = 0
            while (i < len(selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:
                    
                    if (i >= len(selected_num_cols)):
                        break
                    
                    fig = px.box(customer_data, y = selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width = True)
                    i += 1








# try:
#     education_options = st.sidebar.multiselect('Pick Education', customer_data['education'].unique())
# except Exception as e:
#     pass

# new_customer_data = customer_data[(customer_data['education'].isin(education_options))]
# st.write(new_customer_data)

# st.dataframe(customer_data)



#if st.checkbox("Show Dataset"):
# st.write("### Enter the number of rows to view")
# rows = st.number_input("", min_value=0, value=5)
# if rows > 0:
#     st.dataframe(customer_data.head(rows))



# st.sidebar.header("Filter Your Data")
# education = customer_data['education'].unique().tolist()
# education_selected = st.sidebar.multiselect('Education', education, education)
# mask_education = customer_data['education'].isin(education_selected)

# gender = customer_data['gender'].unique().tolist()
# gender_selected = st.sidebar.multiselect('Gender', gender, gender)
# mask_gender = customer_data['gender'].isin(gender_selected)

# df_filtered = customer_data[mask_education & mask_gender]
# st.write(df_filtered)


