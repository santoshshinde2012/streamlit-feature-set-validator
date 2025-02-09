import streamlit as st
import pandas as pd

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