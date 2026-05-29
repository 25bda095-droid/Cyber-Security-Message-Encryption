import streamlit as st


def init_session_state():
    default_values = {
        "encrypted_message": "",
        "encryption_key": "",
        "iv": "",
        "public_key": "",
        "show_results": False,
        "encryption_type_used": ""
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_encryption_results():
    st.session_state.encrypted_message = ""
    st.session_state.encryption_key = ""
    st.session_state.iv = ""
    st.session_state.public_key = ""
    st.session_state.show_results = False
    st.session_state.encryption_type_used = ""