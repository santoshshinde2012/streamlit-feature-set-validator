import streamlit as st
import pandas as pd
import json

def preview_data(df: pd.DataFrame) -> None:
    """Display uploaded data in table or JSON format."""
    data = df.to_dict(orient="records")
    json_data = json.dumps(data, default=str)
    
    with st.container(border=True):
        display_table = st.toggle("File Preview: Table = ON, JSON = OFF", value=True)
        st.subheader("File Preview:")
        if display_table:
            edited_df = st.data_editor(df, num_rows="dynamic")
            csv_data = edited_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Modified CSV", data=csv_data, file_name="modified_data.csv", mime="text/csv")
        else:
            st.json(json_data)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="data.json",
                mime="application/json",
            )

def show_no_records_screen():
    """Display a message when no records are available."""
    st.warning("⚠️ No records found. Please upload a file to proceed.")
