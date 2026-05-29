import streamlit as st


def show_header():
    st.markdown(
        """
        <div class="main-header">
            <h1>🔐 Secure Message Encryption & Decryption</h1>
            <p>Protect your messages with AES-256 or RSA-2048 encryption</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>🔐 Secure Encryption Tool | AES-256 & RSA-2048 | Built with Streamlit</p>
            <p style='font-size: 12px;'>⚠️ Always keep your encryption keys secure and never share them publicly!</p>
        </div>
        """,
        unsafe_allow_html=True
    )