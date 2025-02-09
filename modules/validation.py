import streamlit as st
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

def validate_data(df, schema_json):
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
    st.success("Validation successful! All records conform to the schema.")
