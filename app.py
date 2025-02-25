import streamlit as st
import pandas as pd
import os
from io import BytesIO
#set up our app
st.set_page_config(page_title="Data sweeper", layout='wide')

st.title("Data sweeper")
st.write("Transform your file between CSV and Exel formats with built_in data cleaning and visualization!")
uploaded_files= st.file_uploader("uplod you files (CSV or Excel):", type=["csv", "xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv" :
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
             df = pd.read_excel(file)
        else:
            st.error(f"Unsupport file type: {file_ext}")
            continue
        #Display about info the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")
        
        #show 5 rows of our df
        st.write("Preiew The Head of The DataFrame")
        st.dataframe(df.head())
       


        #Option data cleaning
        st.subheader("Data Cleaning Option")
        if st.checkbox(f"Clean data for {file.name}"):
            col1 , col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicate form {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed successfully!")

            with col2:
                if st.button(f"File Missing Values for {file.name}"):
                    numeric_cols2 = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols2] = df[numeric_cols2].fillna(df[numeric_cols2].mean())
                    
                    st.write("✅ Missing values have been filled!")

    #Choose specsific Colums to keep over convert
    st.subheader("select Columns to Convert ")
    columns = st.multiselect(f"Chose Colams for {file.name}", df.columns, default=df.columns)
    df = df[columns]

    #Create Some Visualization
    st.subheader("Data Visualization ")
    if st.checkbox(f"show Visualizationfor {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        # Convwer a file  -> CSV to Excel
        st.subheader("Conversion Options")
        converstion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"convert {file.name}"):
            buffer = BytesIO()
            if converstion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif converstion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                #Download button
                st.download_button(
                    label=f"Download {file.name} as {converstion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                st.success("✅ File processed successfully!")




