import streamlit as st


def load_css(file_path):
    with open(file_path, "r") as file:
        css = file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )