# 🔐 Secure Message Encryption & Decryption Tool

A professional Streamlit-based web application that provides secure message and file encryption using **AES-256 symmetric encryption** and **RSA-2048 asymmetric encryption**.

The project demonstrates how modern encryption techniques work in a simple, interactive, and beginner-friendly way. It allows users to encrypt messages, generate required keys, download encrypted outputs, and decrypt messages using the correct keys.

---

## 🌐 Live Demo

🔗 **Application Link:**
https://cyber-security-message-encryption-dl3w8dsunub3quh4er25dy.streamlit.app/

---

## 📌 Project Overview

The **Secure Message Encryption & Decryption Tool** is designed to explain and demonstrate two important cryptographic techniques:

* **AES-256** for fast symmetric encryption
* **RSA-2048** for public/private key based asymmetric encryption

The application supports both direct text input and file upload. It also provides encrypted output, encryption keys, initialization vectors, public keys, and private keys based on the selected encryption method.

This project is useful for understanding:

* How messages are encrypted and decrypted
* How AES and RSA encryption differ
* Why AES is suitable for large data
* Why RSA is suitable for small messages and key exchange
* Why keys, IVs, padding, and Base64 encoding are required in real encryption workflows

---

## ✨ Features

### 🔐 Dual Encryption Methods

| Method   | Type                  | Best Used For                          |
| -------- | --------------------- | -------------------------------------- |
| AES-256  | Symmetric Encryption  | Large messages and files               |
| RSA-2048 | Asymmetric Encryption | Small messages and secure key exchange |

---

### 📥 Flexible Input Options

The application supports:

* Direct message typing
* File upload for encryption and decryption
* Text-based encrypted input
* File-based encrypted input

---

### 📤 Downloadable Outputs

The application allows users to download:

* Encrypted message
* AES encryption key
* AES initialization vector
* RSA public key
* RSA private key
* Decrypted message

---

### 🖥️ User-Friendly Interface

The interface is built using **Streamlit** and includes:

* Clean tab-based layout
* Separate encryption and decryption sections
* Clear warnings and instructions
* Download buttons for generated outputs
* Custom CSS styling

---

## 🧰 Technology Stack

| Technology              | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| Python                  | Main programming language                   |
| Streamlit               | Web application framework                   |
| PyCryptodome            | AES and RSA encryption library              |
| Base64                  | Converts encrypted bytes into readable text |
| HTML/CSS                | Custom UI styling                           |
| Streamlit Session State | Temporarily stores encryption results       |

---

## 📚 Core Concepts Used

| Concept     | Explanation                                         |
| ----------- | --------------------------------------------------- |
| AES-256     | Symmetric encryption using a 256-bit key            |
| RSA-2048    | Asymmetric encryption using public and private keys |
| AES-CBC     | AES encryption in Cipher Block Chaining mode        |
| IV          | Initialization Vector required for AES-CBC          |
| Padding     | Makes AES input size compatible with block size     |
| Unpadding   | Removes padding after decryption                    |
| PKCS1_OAEP  | Secure padding scheme used with RSA encryption      |
| Base64      | Converts binary encrypted data into readable text   |
| Ciphertext  | Encrypted unreadable output                         |
| Public Key  | RSA key used for encryption                         |
| Private Key | RSA key used for decryption                         |

---

## 🗂️ Project Structure

```txt
Cyber-Security-Message-Encryption-main/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── style.css
│
└── src/
    ├── constants.py
    │
    ├── crypto/
    │   ├── aes_crypto.py
    │   ├── rsa_crypto.py
    │   └── crypto_service.py
    │
    ├── state/
    │   └── session_state.py
    │
    ├── ui/
    │   ├── layout.py
    │   ├── encrypt_tab.py
    │   ├── decrypt_tab.py
    │   └── result_components.py
    │
    └── utils/
        ├── css_loader.py
        └── encoding.py
```

---

## 📁 File Explanation

| File / Folder                  | Purpose                                         |
| ------------------------------ | ----------------------------------------------- |
| `app.py`                       | Main controller of the Streamlit application    |
| `requirements.txt`             | Contains required Python libraries              |
| `.streamlit/config.toml`       | Controls Streamlit theme and server settings    |
| `assets/style.css`             | Contains custom CSS styling                     |
| `src/constants.py`             | Stores fixed project constants                  |
| `src/crypto/aes_crypto.py`     | Handles AES-256 encryption and decryption       |
| `src/crypto/rsa_crypto.py`     | Handles RSA-2048 encryption and decryption      |
| `src/crypto/crypto_service.py` | Connects UI with AES/RSA logic                  |
| `src/state/session_state.py`   | Stores encryption results temporarily           |
| `src/ui/layout.py`             | Handles page header and footer                  |
| `src/ui/encrypt_tab.py`        | Builds encryption interface                     |
| `src/ui/decrypt_tab.py`        | Builds decryption interface                     |
| `src/ui/result_components.py`  | Displays encrypted results and download buttons |
| `src/utils/css_loader.py`      | Loads custom CSS into Streamlit                 |
| `src/utils/encoding.py`        | Converts bytes to Base64 and Base64 to bytes    |

---

## 🔐 AES-256 Encryption

AES stands for:

```txt
Advanced Encryption Standard
```

AES is a **symmetric encryption algorithm**.

This means the same secret key is used for both encryption and decryption.

```txt
Same AES key → Encrypts the message
Same AES key → Decrypts the message
```

In this project, AES uses a **32-byte key**.

```txt
1 byte = 8 bits
32 bytes = 256 bits
```

Therefore, the project uses:

```txt
AES-256
```

---

## 🔗 AES-CBC Mode

AES is used in CBC mode.

```txt
AES-CBC = Advanced Encryption Standard - Cipher Block Chaining
```

CBC mode connects encrypted blocks together. Each block depends on the previous encrypted block.

AES-CBC also requires an **Initialization Vector**.

---

## 🧩 Initialization Vector

IV stands for:

```txt
Initialization Vector
```

The IV is a random value used by AES-CBC for the first encryption block.

Important points:

```txt
IV is not a password.
IV is not the AES key.
IV is not secret.
IV is required for decryption.
IV must be saved with the encrypted message.
```

The IV helps ensure that encrypting the same message multiple times produces different ciphertext outputs.

---

## 📦 Padding and Unpadding

AES works on fixed-size blocks.

AES block size:

```txt
16 bytes
```

If the message size is not a multiple of 16 bytes, padding is added before encryption.

Example:

```txt
Original message = HELLO
Length = 5 bytes

AES needs = 16 bytes
Padding added = 11 bytes
```

After decryption, the extra padding is removed using unpadding.

```txt
Padding   → Added before encryption
Unpadding → Removed after decryption
```

---

## 🛡️ RSA-2048 Encryption

RSA is an **asymmetric encryption algorithm**.

This means it uses two keys:

| Key         | Purpose             |
| ----------- | ------------------- |
| Public Key  | Used for encryption |
| Private Key | Used for decryption |

Basic RSA process:

```txt
Message + Public Key
↓
Encryption
↓
Ciphertext

Ciphertext + Private Key
↓
Decryption
↓
Original Message
```

The project uses:

```txt
RSA-2048
```

This means RSA keys are generated with a 2048-bit key size.

---

## 🔑 Public Key and Private Key

### Public Key

The public key is used to encrypt the message.

It can be shared with others.

### Private Key

The private key is used to decrypt the message.

It must be kept secret.

If the private key is lost, the RSA encrypted message cannot be decrypted.

---

## 🔐 PKCS1_OAEP

Full form:

```txt
PKCS1 = Public-Key Cryptography Standards #1
OAEP  = Optimal Asymmetric Encryption Padding
```

So:

```txt
PKCS1_OAEP = Public-Key Cryptography Standards #1 - Optimal Asymmetric Encryption Padding
```

In this project, `PKCS1_OAEP` is used with RSA to make encryption more secure.

OAEP adds:

```txt
Randomness
Security padding
Protection against predictable raw RSA encryption
```

---

## 📏 Why RSA Supports Only Small Messages

RSA does not encrypt large data directly.

For RSA-2048:

```txt
2048 bits = 256 bytes
```

However, the complete 256 bytes cannot be used only for the message because OAEP padding also needs space.

So the actual message size must be smaller than the total RSA block size.

This project uses a safe limit:

```txt
RSA_MAX_BYTES = 190
```

That is why RSA is suitable for:

```txt
Small messages
Keys
Secure key exchange
```

For larger messages and files, AES is the better choice.

---

## 🔤 Base64 Encoding

Base64 is not encryption.

Base64 is encoding.

Encrypted data is usually generated as raw bytes. Raw bytes may contain unreadable characters, so they are difficult to copy, paste, display, or download as text.

Base64 converts bytes into readable text.

```txt
Encrypted bytes
↓
Base64 text
```

Base64 is used for:

```txt
Encrypted message
AES key
Initialization Vector
RSA ciphertext
```

Correct flow:

```txt
Message string
↓
UTF-8 bytes
↓
Encryption
↓
Ciphertext bytes
↓
Base64 text
```

The message is not converted to Base64 before encryption. Base64 is applied after encryption.

---

# 🔄 Encryption and Decryption Flow Diagrams

## AES-256 Encryption and Decryption Flow

```txt
┌──────────────────────────────────────────────────────────────────────┐
│                          AES-256 WORKFLOW                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ENCRYPTION FLOW                                                     │
│                                                                      │
│  ┌──────────────┐                                                    │
│  │ Plain Message│                                                    │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌────────────────────┐                                              │
│  │ Convert to Bytes   │                                              │
│  │ UTF-8 Encoding     │                                              │
│  └──────┬─────────────┘                                              │
│         │                                                            │
│         ▼                                                            │
│  ┌────────────────────┐                                              │
│  │ Add Padding        │                                              │
│  │ 16-byte Block Size │                                              │
│  └──────┬─────────────┘                                              │
│         │                                                            │
│         ▼                                                            │
│  ┌────────────────────┐       ┌────────────────────┐                 │
│  │ Generate AES Key   │       │ Generate Random IV │                 │
│  │ 32 Bytes / 256 bit │       │ 16 Bytes           │                 │
│  └──────┬─────────────┘       └─────────┬──────────┘                 │
│         │                               │                            │
│         └───────────────┬───────────────┘                            │
│                         ▼                                            │
│  ┌────────────────────────────────────────────┐                      │
│  │ AES-CBC Encryption                          │                      │
│  │ Uses: Message + AES Key + IV                │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Ciphertext Bytes                            │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Convert Ciphertext, Key, and IV to Base64  │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Output: Encrypted Message + AES Key + IV   │                      │
│  └────────────────────────────────────────────┘                      │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  DECRYPTION FLOW                                                     │
│                                                                      │
│  ┌────────────────────────────────────────────┐                      │
│  │ Input: Encrypted Message + AES Key + IV    │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Convert Base64 Data Back to Bytes          │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ AES-CBC Decryption                          │                      │
│  │ Uses Same AES Key and Same IV               │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Remove Padding                              │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Convert Bytes Back to Text                 │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Original Message Recovered                 │                      │
│  └────────────────────────────────────────────┘                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## RSA-2048 Encryption and Decryption Flow

```txt
┌──────────────────────────────────────────────────────────────────────┐
│                          RSA-2048 WORKFLOW                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  KEY GENERATION                                                      │
│                                                                      │
│  ┌────────────────────────────────────────────┐                      │
│  │ Generate RSA-2048 Key Pair                 │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│          ┌────────────┴────────────┐                                 │
│          ▼                         ▼                                 │
│  ┌──────────────────┐      ┌──────────────────┐                      │
│  │ Public Key       │      │ Private Key      │                      │
│  │ Used to Encrypt  │      │ Used to Decrypt  │                      │
│  └──────────────────┘      └──────────────────┘                      │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ENCRYPTION FLOW                                                     │
│                                                                      │
│  ┌──────────────┐                                                    │
│  │ Plain Message│                                                    │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌────────────────────┐                                              │
│  │ Convert to Bytes   │                                              │
│  │ UTF-8 Encoding     │                                              │
│  └──────┬─────────────┘                                              │
│         │                                                            │
│         ▼                                                            │
│  ┌────────────────────────────────────────────┐                      │
│  │ Check Message Size Limit                   │                      │
│  │ RSA is only for small messages             │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Import Public Key                           │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Apply PKCS1_OAEP Padding                   │                      │
│  │ Adds Security and Randomness               │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ RSA Encryption Using Public Key            │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Ciphertext Bytes                            │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Convert Ciphertext to Base64               │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Output: Encrypted Message + Private Key    │                      │
│  │ Public Key is also shown/downloadable      │                      │
│  └────────────────────────────────────────────┘                      │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  DECRYPTION FLOW                                                     │
│                                                                      │
│  ┌────────────────────────────────────────────┐                      │
│  │ Input: Encrypted Message + Private Key     │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Convert Base64 Ciphertext Back to Bytes    │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Import Private Key                          │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ RSA-OAEP Decryption Using Private Key      │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Decrypted Bytes                             │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Convert Bytes Back to Text                 │                      │
│  └────────────────────┬───────────────────────┘                      │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────┐                      │
│  │ Original Message Recovered                 │                      │
│  └────────────────────────────────────────────┘                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ How the Application Works

The application follows a modular workflow:

```txt
User Interface
↓
Encryption / Decryption Tab
↓
Crypto Service Layer
↓
AES or RSA Crypto Module
↓
Base64 Encoding / Decoding Utility
↓
Result Display and Download
```

---

## 🔐 AES Workflow in the Application

When AES encryption is selected:

```txt
1. User enters a message or uploads a file
2. Application generates a random 32-byte AES key
3. AES-CBC mode is initialized
4. A random 16-byte IV is generated
5. Message is converted into bytes
6. Padding is applied
7. Message is encrypted using AES-CBC
8. Ciphertext, AES key, and IV are converted to Base64
9. Encrypted message, key, and IV are displayed/downloaded
```

For AES decryption:

```txt
1. User provides encrypted message
2. User provides AES key
3. User provides IV
4. Base64 values are converted back to bytes
5. AES-CBC decryption is performed
6. Padding is removed
7. Original message is displayed
```

---

## 🛡️ RSA Workflow in the Application

When RSA encryption is selected:

```txt
1. User enters a small message
2. Application generates RSA-2048 public/private key pair
3. Public key is used for encryption
4. Message is converted into bytes
5. PKCS1_OAEP padding is applied
6. Message is encrypted using RSA public key
7. Ciphertext is converted to Base64
8. Encrypted message, public key, and private key are displayed/downloaded
```

For RSA decryption:

```txt
1. User provides encrypted message
2. User provides private key
3. Base64 ciphertext is converted back to bytes
4. Private key is imported
5. RSA-OAEP decryption is performed
6. Original message is displayed
```

---

## 🆚 AES vs RSA

| Feature            | AES-256              | RSA-2048                    |
| ------------------ | -------------------- | --------------------------- |
| Encryption Type    | Symmetric            | Asymmetric                  |
| Number of Keys     | One key              | Two keys                    |
| Encryption Key     | Secret AES key       | Public key                  |
| Decryption Key     | Same AES key         | Private key                 |
| Speed              | Fast                 | Slower                      |
| Best For           | Large messages/files | Small messages/key exchange |
| IV Required        | Yes                  | No                          |
| Padding Used       | `pad()` / `unpad()`  | `PKCS1_OAEP`                |
| Output Encoding    | Base64               | Base64                      |
| Large File Support | Suitable             | Not suitable                |

---

## 📦 Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Cyber-Security-Message-Encryption-main
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

---

## 📌 Requirements

The project mainly requires:

```txt
streamlit
pycryptodome
```

These are stored inside `requirements.txt`.

---

## 🧪 Usage Guide

### Encrypting with AES-256

```txt
1. Open the application
2. Go to the Encrypt tab
3. Select AES-256 encryption
4. Type a message or upload a file
5. Click Encrypt
6. Download:
   - Encrypted message
   - AES key
   - IV
```

To decrypt AES encrypted data, the following are required:

```txt
Encrypted message
AES key
IV
```

---

### Encrypting with RSA-2048

```txt
1. Open the application
2. Go to the Encrypt tab
3. Select RSA-2048 encryption
4. Type a small message
5. Click Encrypt
6. Download:
   - Encrypted message
   - Public key
   - Private key
```

To decrypt RSA encrypted data, the following are required:

```txt
Encrypted message
Private key
```

---

## ⚠️ Security Notes

This project is created for educational and demonstration purposes.

Important points:

```txt
1. Never share the AES key publicly.
2. Never share the RSA private key publicly.
3. Losing the AES key means the AES encrypted message cannot be recovered.
4. Losing the RSA private key means the RSA encrypted message cannot be recovered.
5. IV is required for AES-CBC decryption.
6. Base64 is not encryption; it only converts bytes into readable text.
7. RSA should not be used for large files or long messages.
8. AES is better for large data encryption.
```

AES-CBC provides confidentiality, but it does not automatically provide strong tamper detection. For production-level systems, authenticated encryption modes such as AES-GCM are commonly preferred.

---

## 🚀 Future Improvements

Possible future enhancements:

```txt
1. Add AES-GCM mode for authenticated encryption
2. Add hybrid encryption using RSA + AES together
3. Add password-based encryption
4. Add user authentication
5. Add encrypted file storage
6. Add better error handling for invalid keys
7. Add dark mode and advanced UI themes
8. Add encryption history section
9. Add QR code export for keys
10. Add automated tests for encryption and decryption modules
```

---

## 🎯 Learning Outcomes

This project helps understand:

```txt
AES symmetric encryption
RSA asymmetric encryption
Public/private key cryptography
AES-CBC mode
Initialization Vector
Padding and unpadding
PKCS1_OAEP padding
Base64 encoding
Streamlit web app development
Modular Python project structure
```

---

## 📌 Final Summary

The **Secure Message Encryption & Decryption Tool** is a Python and Streamlit-based web application that demonstrates AES-256 and RSA-2048 encryption.

AES-256 is used for fast symmetric encryption and is suitable for large messages and files. It uses a 32-byte secret key, CBC mode, padding, and an initialization vector.

RSA-2048 is used for asymmetric encryption. It generates a public/private key pair where the public key encrypts the message and the private key decrypts it. RSA uses PKCS1_OAEP padding for improved security and is suitable only for small messages.

Base64 encoding is used to convert encrypted bytes, keys, and IV values into readable text format so they can be displayed, copied, and downloaded easily.

This project provides a practical and beginner-friendly demonstration of how secure message encryption and decryption works.

---

## 📄 License

This project is licensed under the terms included in the `LICENSE` file.

---

## 🔐 Project Status

```txt
STATUS: PROTECTED
AES-256: ACTIVE
RSA-2048: ACTIVE
STREAMLIT APP: DEPLOYED
```
