import streamlit as st

from src.constants import AES_TYPE
from src.state.session_state import clear_encryption_results


def show_encryption_results():
    if not st.session_state.show_results or not st.session_state.encrypted_message:
        return

    st.markdown("---")
    st.subheader("🎉 Encryption Results")

    if st.session_state.encryption_type_used == AES_TYPE:
        show_aes_results()
    else:
        show_rsa_results()

    if st.button("🔄 Clear Results & Encrypt New Message"):
        clear_encryption_results()
        st.rerun()


def show_aes_results():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔐 Encrypted Message")
        st.code(st.session_state.encrypted_message, language=None)
        st.download_button(
            "📥 Download Encrypted Message",
            st.session_state.encrypted_message,
            file_name="encrypted_message.txt",
            key="download_enc_msg"
        )

    with col2:
        st.markdown("### 🔑 Encryption Key")
        st.code(st.session_state.encryption_key, language=None)
        st.download_button(
            "📥 Download Key",
            st.session_state.encryption_key,
            file_name="encryption_key.txt",
            key="download_key"
        )

        st.markdown("### 🎲 IV")
        st.code(st.session_state.iv, language=None)
        st.download_button(
            "📥 Download IV",
            st.session_state.iv,
            file_name="iv.txt",
            key="download_iv"
        )

    st.warning("⚠️ Save both the key and IV securely. You need them to decrypt the message.")


def show_rsa_results():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔐 Encrypted Message")
        st.code(st.session_state.encrypted_message, language=None)
        st.download_button(
            "📥 Download Encrypted Message",
            st.session_state.encrypted_message,
            file_name="encrypted_message.txt",
            key="download_enc_msg_rsa"
        )

    with col2:
        st.markdown("### 🔑 Private Key")
        st.code(st.session_state.encryption_key, language=None)
        st.download_button(
            "📥 Download Private Key",
            st.session_state.encryption_key,
            file_name="private_key.pem",
            key="download_private_key"
        )

        st.markdown("### 🔓 Public Key")
        st.code(st.session_state.public_key, language=None)
        st.download_button(
            "📥 Download Public Key",
            st.session_state.public_key,
            file_name="public_key.pem",
            key="download_public_key"
        )

    st.warning("⚠️ Keep your private key secure. Anyone with it can decrypt your messages.")