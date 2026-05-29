import streamlit as st

from src.utils.css_loader import load_css
from src.state.session_state import init_session_state
from src.ui.layout import show_header, show_footer
from src.ui.encrypt_tab import show_encrypt_tab
from src.ui.decrypt_tab import show_decrypt_tab


st.set_page_config(
    page_title="Secure Message Encryption/Decryption",
    page_icon="🔐",
    layout="wide"
)

load_css("assets/style.css")
init_session_state()

show_header()

tab1, tab2 = st.tabs(["🔒 Encrypt Message", "🔓 Decrypt Message"])

with tab1:
    show_encrypt_tab()

with tab2:
    show_decrypt_tab()

show_footer()