import streamlit as st
import base64
from encryption_utils import SymmetricEncryption, AsymmetricEncryption

# Page configuration
st.set_page_config(
    page_title="Secure Message Encryption/Decryption",
    page_icon="🔐",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .key-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for persistent storage
if 'encrypted_message' not in st.session_state:
    st.session_state.encrypted_message = ""
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = ""
if 'iv' not in st.session_state:
    st.session_state.iv = ""
if 'public_key' not in st.session_state:
    st.session_state.public_key = ""
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'encryption_type_used' not in st.session_state:
    st.session_state.encryption_type_used = ""

# Welcome Header
st.markdown('<div class="main-header"><h1>🔐 Secure Message Encryption & Decryption</h1><p>Protect your messages with AES-256 or RSA-2048 encryption</p></div>', unsafe_allow_html=True)

# Create tabs for Encryption and Decryption
tab1, tab2 = st.tabs(["🔒 Encrypt Message", "🔓 Decrypt Message"])

# ========== ENCRYPTION TAB ==========
with tab1:
    st.header("Encrypt Your Message")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["Type Message", "Upload File"], horizontal=True)
    
    message_to_encrypt = ""
    
    if input_method == "Type Message":
        message_to_encrypt = st.text_area(
            "Enter your message:",
            height=150,
            placeholder="Type your secret message here..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a file (text files work best):",
            type=['txt', 'pdf', 'docx', 'jpg', 'png']
        )
        if uploaded_file is not None:
            try:
                message_to_encrypt = uploaded_file.read()
                st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")
                st.info(f"File size: {len(message_to_encrypt)} bytes")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    # Encryption type selection
    encryption_type = st.selectbox(
        "Select encryption type:",
        ["Symmetric (AES-256)", "Asymmetric (RSA-2048)"],
        help="Symmetric: Same key for encryption/decryption. Asymmetric: Public key encrypts, private key decrypts."
    )
    
    # Information about selected encryption
    if encryption_type == "Symmetric (AES-256)":
        st.info("ℹ️ **AES-256**: Fast and efficient. Best for large messages. Uses the same key for encryption and decryption.")
    else:
        st.info("ℹ️ **RSA-2048**: More secure key exchange. Best for small messages (max 190 bytes). Uses public/private key pair.")
    
    # Encrypt button
    if st.button("🔒 Encrypt Message", type="primary"):
        if not message_to_encrypt:
            st.error("⚠️ Please enter a message or upload a file first!")
            st.session_state.show_results = False
        else:
            try:
                with st.spinner("Encrypting your message..."):
                    if encryption_type == "Symmetric (AES-256)":
                        # Generate key
                        key = SymmetricEncryption.generate_key()
                        
                        # Encrypt
                        encrypted_msg, iv = SymmetricEncryption.encrypt(message_to_encrypt, key)
                        
                        # Store in session state
                        st.session_state.encrypted_message = encrypted_msg
                        st.session_state.encryption_key = base64.b64encode(key).decode('utf-8')
                        st.session_state.iv = iv
                        st.session_state.public_key = ""
                        st.session_state.show_results = True
                        st.session_state.encryption_type_used = "Symmetric (AES-256)"
                        
                        st.success("✅ Message encrypted successfully!")
                    
                    else:  # Asymmetric RSA
                        # Check message size
                        msg_size = len(message_to_encrypt) if isinstance(message_to_encrypt, bytes) else len(message_to_encrypt.encode('utf-8'))
                        
                        if msg_size > 190:
                            st.error("⚠️ Message too large for RSA encryption! RSA can only encrypt up to 190 bytes. Please use Symmetric encryption for larger messages.")
                            st.session_state.show_results = False
                        else:
                            # Generate key pair
                            public_key, private_key = AsymmetricEncryption.generate_keys()
                            
                            # Encrypt
                            encrypted_msg = AsymmetricEncryption.encrypt(message_to_encrypt, public_key)
                            
                            # Store in session state
                            st.session_state.encrypted_message = encrypted_msg
                            st.session_state.encryption_key = private_key
                            st.session_state.public_key = public_key
                            st.session_state.iv = ""
                            st.session_state.show_results = True
                            st.session_state.encryption_type_used = "Asymmetric (RSA-2048)"
                            
                            st.success("✅ Message encrypted successfully!")
                
            except Exception as e:
                st.error(f"❌ Encryption failed: {str(e)}")
                st.session_state.show_results = False
    
    # Display results if encryption was successful
    if st.session_state.show_results and st.session_state.encrypted_message:
        st.markdown("---")
        st.subheader("🎉 Encryption Results")
        
        if st.session_state.encryption_type_used == "Symmetric (AES-256)":
            # Display results for AES
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
                
                st.markdown("### 🎲 IV (Initialization Vector)")
                st.code(st.session_state.iv, language=None)
                st.download_button(
                    "📥 Download IV",
                    st.session_state.iv,
                    file_name="iv.txt",
                    key="download_iv"
                )
            
            st.warning("⚠️ **IMPORTANT**: Save both the key and IV securely! You'll need them to decrypt the message.")
        
        else:  # RSA
            # Display results for RSA
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
                st.markdown("### 🔑 Private Key (for decryption)")
                st.code(st.session_state.encryption_key, language=None)
                st.download_button(
                    "📥 Download Private Key",
                    st.session_state.encryption_key,
                    file_name="private_key.pem",
                    key="download_private_key"
                )
                
                st.markdown("### 🔓 Public Key (used for encryption)")
                st.code(st.session_state.public_key, language=None)
                st.download_button(
                    "📥 Download Public Key",
                    st.session_state.public_key,
                    file_name="public_key.pem",
                    key="download_public_key"
                )
            
            st.warning("⚠️ **IMPORTANT**: Keep your private key secure! Anyone with it can decrypt your messages.")
        
        # Add a clear button to reset
        if st.button("🔄 Clear Results & Encrypt New Message"):
            st.session_state.show_results = False
            st.session_state.encrypted_message = ""
            st.session_state.encryption_key = ""
            st.session_state.iv = ""
            st.session_state.public_key = ""
            st.rerun()

# ========== DECRYPTION TAB ==========
with tab2:
    st.header("Decrypt Your Message")
    
    # Decryption type selection
    decryption_type = st.selectbox(
        "Select decryption type:",
        ["Symmetric (AES-256)", "Asymmetric (RSA-2048)"],
        key="decrypt_type"
    )
    
    # Input method selection for decryption
    decrypt_input_method = st.radio(
        "Choose input method:",
        ["Paste Text", "Upload Files"],
        horizontal=True,
        key="decrypt_input_method"
    )
    
    encrypted_input = ""
    key_input = ""
    iv_input = None
    
    if decrypt_input_method == "Paste Text":
        # Input fields for decryption - Manual Paste
        encrypted_input = st.text_area(
            "Paste your encrypted message:",
            height=150,
            placeholder="Paste the encrypted message here...",
            value=st.session_state.encrypted_message if st.session_state.encryption_type_used == decryption_type else "",
            key="encrypted_paste"
        )
        
        if decryption_type == "Symmetric (AES-256)":
            key_input = st.text_area(
                "Paste your encryption key:",
                height=100,
                placeholder="Paste your encryption key here...",
                value=st.session_state.encryption_key if st.session_state.encryption_type_used == decryption_type else "",
                key="key_paste"
            )
            
            iv_input = st.text_area(
                "Paste your IV (Initialization Vector):",
                height=100,
                placeholder="Paste your IV here...",
                value=st.session_state.iv if st.session_state.encryption_type_used == decryption_type else "",
                key="iv_paste"
            )
        else:
            key_input = st.text_area(
                "Paste your private key:",
                height=200,
                placeholder="Paste your RSA private key here...",
                value=st.session_state.encryption_key if st.session_state.encryption_type_used == decryption_type else "",
                key="private_key_paste"
            )
    
    else:  # Upload Files
        st.info("📁 Upload the files you downloaded earlier")
        
        # Upload encrypted message file
        encrypted_file = st.file_uploader(
            "Upload encrypted message file:",
            type=['txt'],
            key="encrypted_file_upload"
        )
        if encrypted_file is not None:
            try:
                encrypted_input = encrypted_file.read().decode('utf-8')
                st.success(f"✅ Encrypted message loaded from '{encrypted_file.name}'")
            except Exception as e:
                st.error(f"Error reading encrypted message: {str(e)}")
        
        if decryption_type == "Symmetric (AES-256)":
            # Upload key file
            key_file = st.file_uploader(
                "Upload encryption key file:",
                type=['txt'],
                key="key_file_upload"
            )
            if key_file is not None:
                try:
                    key_input = key_file.read().decode('utf-8')
                    st.success(f"✅ Key loaded from '{key_file.name}'")
                except Exception as e:
                    st.error(f"Error reading key: {str(e)}")
            
            # Upload IV file
            iv_file = st.file_uploader(
                "Upload IV (Initialization Vector) file:",
                type=['txt'],
                key="iv_file_upload"
            )
            if iv_file is not None:
                try:
                    iv_input = iv_file.read().decode('utf-8')
                    st.success(f"✅ IV loaded from '{iv_file.name}'")
                except Exception as e:
                    st.error(f"Error reading IV: {str(e)}")
        
        else:  # RSA
            # Upload private key file
            private_key_file = st.file_uploader(
                "Upload private key file:",
                type=['pem', 'txt'],
                key="private_key_file_upload"
            )
            if private_key_file is not None:
                try:
                    key_input = private_key_file.read().decode('utf-8')
                    st.success(f"✅ Private key loaded from '{private_key_file.name}'")
                except Exception as e:
                    st.error(f"Error reading private key: {str(e)}")
    
    # Decrypt button
    if st.button("🔓 Decrypt Message", type="primary", key="decrypt_btn"):
        if not encrypted_input or not key_input:
            st.error("⚠️ Please provide both the encrypted message and the key!")
        elif decryption_type == "Symmetric (AES-256)" and not iv_input:
            st.error("⚠️ Please provide the IV (Initialization Vector) for AES decryption!")
        else:
            try:
                with st.spinner("Decrypting your message..."):
                    if decryption_type == "Symmetric (AES-256)":
                        # Decode key
                        key = base64.b64decode(key_input.strip())
                        
                        # Decrypt
                        decrypted_msg = SymmetricEncryption.decrypt(
                            encrypted_input.strip(),
                            key,
                            iv_input.strip()
                        )
                    else:  # Asymmetric RSA
                        # Decrypt
                        decrypted_msg = AsymmetricEncryption.decrypt(
                            encrypted_input.strip(),
                            key_input.strip()
                        )
                    
                    st.success("✅ Message decrypted successfully!")
                    
                    # Display decrypted message
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
                st.info("💡 Make sure you're using the correct key, IV (for AES), and encryption type.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🔐 Secure Encryption Tool | AES-256 & RSA-2048 | Built with Streamlit</p>
        <p style='font-size: 12px;'>⚠️ Always keep your encryption keys secure and never share them publicly!</p>
    </div>
""", unsafe_allow_html=True)
