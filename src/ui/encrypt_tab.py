import streamlit as st

from src.constants import AES_TYPE, RSA_TYPE, ALLOWED_UPLOAD_TYPES
from src.crypto.crypto_service import encrypt_message
from src.ui.result_components import show_encryption_results


def show_encrypt_tab():
    st.header("Encrypt Your Message")

    input_method = st.radio(
        "Choose input method:",
        ["Type Message", "Upload File"],
        horizontal=True
    )

    message_to_encrypt = get_message_input(input_method)

    encryption_type = st.selectbox(
        "Select encryption type:",
        [AES_TYPE, RSA_TYPE],
        help="Symmetric: Same key for encryption/decryption. Asymmetric: Public key encrypts, private key decrypts."
    )

    show_encryption_info(encryption_type)

    if st.button("🔒 Encrypt Message", type="primary"):
        handle_encrypt_button(message_to_encrypt, encryption_type)

    show_encryption_results()


def get_message_input(input_method):
    if input_method == "Type Message":
        return st.text_area(
            "Enter your message:",
            height=150,
            placeholder="Type your secret message here..."
        )

    uploaded_file = st.file_uploader(
        "Upload a file:",
        type=ALLOWED_UPLOAD_TYPES
    )

    if uploaded_file is not None:
        message = uploaded_file.read()
        st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")
        st.info(f"File size: {len(message)} bytes")
        return message

    return ""


def show_encryption_info(encryption_type):
    if encryption_type == AES_TYPE:
        st.info("ℹ️ **AES-256**: Fast and efficient. Best for large messages.")
    else:
        st.info("ℹ️ **RSA-2048**: Best for small messages. Uses public/private key pair.")


def handle_encrypt_button(message_to_encrypt, encryption_type):
    if not message_to_encrypt:
        st.error("⚠️ Please enter a message or upload a file first!")
        st.session_state.show_results = False
        return

    try:
        with st.spinner("Encrypting your message..."):
            result = encrypt_message(message_to_encrypt, encryption_type)

            st.session_state.encrypted_message = result["encrypted_message"]
            st.session_state.encryption_key = result["encryption_key"]
            st.session_state.iv = result["iv"]
            st.session_state.public_key = result["public_key"]
            st.session_state.encryption_type_used = result["encryption_type_used"]
            st.session_state.show_results = True

            st.success("✅ Message encrypted successfully!")

    except Exception as e:
        st.error(f"❌ Encryption failed: {str(e)}")
        st.session_state.show_results = False