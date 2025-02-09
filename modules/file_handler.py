import streamlit as st
import pandas as pd
import json

def load_file() -> pd.DataFrame | None:
    """Handle file upload and return a DataFrame."""
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"], key="file_uploader")
    if uploaded_file is not None:
        try:
            file_extension = uploaded_file.name.split(".")[-1].lower()
            if file_extension == "csv":
                df = pd.read_csv(uploaded_file, chunksize=10000, na_values=["NIL"])
                df = pd.concat(df, ignore_index=True)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', na_values=["NIL"])
            return df
        except Exception as e:
            st.error(f"Error processing file: {e}")
    return None

def preview_data(df: pd.DataFrame) -> None:
    """Display uploaded data in table or JSON format."""
    data = df.to_dict(orient="records")
    json_data = json.dumps(data, default=str)

    with st.container(border=True):
        display_table = st.toggle("File Preview: Table = ON, JSON = OFF", value=True)
        st.subheader("File Preview:")
        if display_table:
            st.dataframe(df)
        else:
            st.json(json_data)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="data.json",
                mime="application/json",
            )
