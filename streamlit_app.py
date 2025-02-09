import streamlit as st
import json
from PIL import Image
from modules.file_handler import load_file
from modules.schema_generator import generate_json_schema
from modules.validation import validate_data
from modules.ui_components import preview_data, show_no_records_screen


def layout() -> None:
    """Main layout of the Streamlit application."""
    st.set_page_config(layout="wide")
    st.title("Feature Set Validator")

    left_column, right_column = st.columns([35, 65])

    with left_column:
        df = load_file()

        if df is None or df.empty:
            show_no_records_screen()
        else:
            schema_json = generate_json_schema(df)
            schema_text = st.text_area(
                "Generated JSON Schema", json.dumps(schema_json, indent=4), height=300
            )

            try:
                updated_schema = json.loads(schema_text)
            except json.JSONDecodeError:
                st.error("Invalid JSON Schema format. Please correct it.")
                updated_schema = schema_json  

            with st.expander("Formatted JSON Schema"):
                st.json(updated_schema)

            json_schema_data = json.dumps(updated_schema, indent=4).encode("utf-8")
            st.download_button(
                label="Download JSON Schema",
                data=json_schema_data,
                file_name="json_schema.json",
                mime="application/json",
            )

    with right_column:
        if df is None or df.empty:
            placeholder = st.empty()
            image = Image.open("./assets/no_record.png")
            placeholder.image(image)
            return

        edited_df = preview_data(df)  

        if st.button("Validate", key="validate_button", use_container_width=True):
            validate_data(edited_df, updated_schema)


def main() -> None:
    """Entry point of the Streamlit app."""
    layout()


if __name__ == "__main__":
    main()
