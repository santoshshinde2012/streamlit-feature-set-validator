import streamlit as st
import json

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
