import streamlit as st
import pandas as pd
import json
from jsonschema import validate, ValidationError
from concurrent.futures import ThreadPoolExecutor

def validate_record(record: dict, schema_json: dict) -> str | None:
    """Validate a single record against the given JSON schema."""
    try:
        validate(instance=record, schema=schema_json)
        return None
    except ValidationError as e:
        return f"Validation Error in record {record}: {e.message}"

def load_schema() -> dict | None:
    """Load and return the JSON schema entered by the user."""
    schema_input = st.text_area(
        "Enter JSON Schema",
        """
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "required": ["name"]
        }
        """,
        height=500,
    )
    try:
        schema_json = json.loads(schema_input)
        with st.expander("Formatted Schema"):
            st.json(schema_json)
        return schema_json
    except json.JSONDecodeError:
        st.error("Invalid JSON Schema. Please check the format.")
        return None

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

def validate_data(df: pd.DataFrame, schema_json: dict) -> None:
    """Validate records against the schema."""
    records = df.to_dict(orient="records")
    total_records = len(records)
    progress_bar = st.progress(5)
    
    with ThreadPoolExecutor() as executor:
        for i, result in enumerate(executor.map(lambda record: validate_record(record, schema_json), records)):
            progress_bar.progress(int((i + 1) / total_records * 100))
            if result is not None:
                st.error(f"Validation Failed: {result}")
                return
    
    progress_bar.progress(100)
    st.success("Validation successful! All records confirm to the schema.")

def layout() -> None:
    """Main layout of the Streamlit application."""
    st.set_page_config(layout="wide")
    st.title("Feature Set Validator")
    
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

def main() -> None:
    """Entry point of the Streamlit app."""
    layout()

if __name__ == "__main__":
    main()
