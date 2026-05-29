import streamlit as st

from src.constants import AES_TYPE, RSA_TYPE
from src.crypto.crypto_service import decrypt_message


def show_decrypt_tab():
    st.header("Decrypt Your Message")

    decryption_type = st.selectbox(
        "Select decryption type:",
        [AES_TYPE, RSA_TYPE],
        key="decrypt_type"
    )

    decrypt_input_method = st.radio(
        "Choose input method:",
        ["Paste Text", "Upload Files"],
        horizontal=True,
        key="decrypt_input_method"
    )

    if decrypt_input_method == "Paste Text":
        encrypted_input, key_input, iv_input = get_decryption_text_inputs(decryption_type)
    else:
        encrypted_input, key_input, iv_input = get_decryption_file_inputs(decryption_type)

    if st.button("🔓 Decrypt Message", type="primary", key="decrypt_btn"):
        handle_decrypt_button(encrypted_input, key_input, iv_input, decryption_type)


def get_decryption_text_inputs(decryption_type):
    encrypted_input = st.text_area(
        "Paste your encrypted message:",
        height=150,
        value=st.session_state.encrypted_message
        if st.session_state.encryption_type_used == decryption_type
        else "",
        key="encrypted_paste"
    )

    if decryption_type == AES_TYPE:
        key_input = st.text_area(
            "Paste your encryption key:",
            height=100,
            value=st.session_state.encryption_key
            if st.session_state.encryption_type_used == decryption_type
            else "",
            key="key_paste"
        )

        iv_input = st.text_area(
            "Paste your IV:",
            height=100,
            value=st.session_state.iv
            if st.session_state.encryption_type_used == decryption_type
            else "",
            key="iv_paste"
        )

    else:
        key_input = st.text_area(
            "Paste your private key:",
            height=200,
            value=st.session_state.encryption_key
            if st.session_state.encryption_type_used == decryption_type
            else "",
            key="private_key_paste"
        )
        iv_input = None

    return encrypted_input, key_input, iv_input


def get_decryption_file_inputs(decryption_type):
    st.info("📁 Upload the files you downloaded earlier")

    encrypted_input = ""
    key_input = ""
    iv_input = None

    encrypted_file = st.file_uploader(
        "Upload encrypted message file:",
        type=["txt"],
        key="encrypted_file_upload"
    )

    if encrypted_file is not None:
        encrypted_input = encrypted_file.read().decode("utf-8")
        st.success(f"✅ Encrypted message loaded from '{encrypted_file.name}'")

    if decryption_type == AES_TYPE:
        key_file = st.file_uploader(
            "Upload encryption key file:",
            type=["txt"],
            key="key_file_upload"
        )

        if key_file is not None:
            key_input = key_file.read().decode("utf-8")
            st.success(f"✅ Key loaded from '{key_file.name}'")

        iv_file = st.file_uploader(
            "Upload IV file:",
            type=["txt"],
            key="iv_file_upload"
        )

        if iv_file is not None:
            iv_input = iv_file.read().decode("utf-8")
            st.success(f"✅ IV loaded from '{iv_file.name}'")

    else:
        private_key_file = st.file_uploader(
            "Upload private key file:",
            type=["pem", "txt"],
            key="private_key_file_upload"
        )

        if private_key_file is not None:
            key_input = private_key_file.read().decode("utf-8")
            st.success(f"✅ Private key loaded from '{private_key_file.name}'")

    return encrypted_input, key_input, iv_input


def handle_decrypt_button(encrypted_input, key_input, iv_input, decryption_type):
    if not encrypted_input or not key_input:
        st.error("⚠️ Please provide both the encrypted message and the key!")
        return

    if decryption_type == AES_TYPE and not iv_input:
        st.error("⚠️ Please provide the IV for AES decryption!")
        return

    try:
        with st.spinner("Decrypting your message..."):
            decrypted_msg = decrypt_message(
                encrypted_input.strip(),
                key_input.strip(),
                decryption_type,
                iv_input.strip() if iv_input else None
            )

        st.success("✅ Message decrypted successfully!")

        st.subheader("📄 Decrypted Message")
        st.text_area(
            "Your original message:",
            value=decrypted_msg,
            height=200,
            disabled=True
        )

        st.download_button(
            "📥 Download Decrypted Message",
            decrypted_msg,
            file_name="decrypted_message.txt",
            key="download_decrypted"
        )

    except Exception as e:
        st.error(f"❌ Decryption failed: {str(e)}")
        st.info("💡 Make sure you're using the correct key, IV, and encryption type.")