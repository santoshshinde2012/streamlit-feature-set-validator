import streamlit as st
from modules.schema_handler import load_schema
from modules.file_handler import load_file, preview_data
from modules.validation import validate_data

def layout() -> None:
    """Main layout of the Streamlit application."""
    left_column, right_column = st.columns([35, 65])

    with left_column:
        with st.container(border=True):
            schema_json = load_schema()

    with right_column:
        df = load_file()
        if df is not None and schema_json:
            preview_data(df)
            if st.button("Validate", key="validate_button", use_container_width=True):
                validate_data(df, schema_json)
