import streamlit as st
import pandas as pd
import json

def preview_data(df: pd.DataFrame) -> pd.DataFrame:
    """Display uploaded data in table or JSON format, allowing editing."""
    with st.container(border=True):
        if df.empty:
            st.warning("⚠️ No data available.")
            return df

        display_table = st.toggle("File Preview: Table = ON, JSON = OFF", value=True)
        st.subheader("File Preview:")

        if not display_table:
            json_data = json.dumps(df.to_dict(orient="records"), default=str)
            st.json(json_data)
            st.download_button("Download JSON", data=json_data, file_name="data.json", mime="application/json")
            return df 

        edited_df = st.data_editor(df, num_rows="dynamic")
        st.download_button("Download Modified CSV", data=edited_df.to_csv(index=False).encode("utf-8"),
                           file_name="modified_data.csv", mime="text/csv")
        return edited_df

def show_no_records_screen():
    """Display a message when no records are available."""
    st.warning("⚠️ No records found. Please upload a file to proceed.")
