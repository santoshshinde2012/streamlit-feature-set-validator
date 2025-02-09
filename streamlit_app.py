import streamlit as st
from modules.layout import layout

def main() -> None:
    """Entry point of the Streamlit app."""
    st.set_page_config(layout="wide")
    st.title("Feature Set Validator")
    layout()

if __name__ == "__main__":
    main()
