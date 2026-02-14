# Steganography (AES-256 + LSB) — Python GUI Application

A Python desktop steganography project that securely embeds confidential text into digital images using **Least Significant Bit (LSB)** encoding, with **AES-256 encryption** applied before embedding for layered privacy.

## Overview
This repository contains a sender/receiver workflow:
- **Encrypt GUI**: encrypts plaintext with a password and hides encrypted bytes inside an image.
- **Decrypt GUI**: extracts hidden bytes from a stego image and decrypts them with the same password.
- **Research notebooks**: iterative experiments and method exploration under `Models and Methods/`.

## Features
- Tkinter-based GUI for both embed and extract operations.
- AES-CBC encryption with a random IV per message.
- SHA-256 based key derivation utility (32-byte key => AES-256).
- LSB bit-level embedding into image channels.
- Input image support for `.png`, `.jpg`, `.jpeg`, `.bmp`.

## Repository Structure
```text
.
├── Encrypt_GUI.py
├── Decrypt_GUI.py
├── sample_input_image.jpg
└── Models and Methods/
    ├── AES_Based_Steganography.ipynb
    ├── LSB_Encryption_Based_Steganography.ipynb
    ├── Steganography_Basic_Model.ipynb
    └── Steganography_Final_(AES+LSB).ipynb
```

## Tech Stack
- **Language:** Python 3
- **GUI:** Tkinter
- **Image Processing:** OpenCV (`cv2`)
- **Cryptography:** PyCryptodome (`Crypto.Cipher.AES`, PKCS#7 padding)
- **Hashing:** `hashlib` (SHA-256)

## Installation
### 1) Clone
```bash
git clone https://github.com/prasunray477/Steganography.git
cd Steganography
```

### 2) Install dependencies
```bash
pip install opencv-python pycryptodome
```

> Note: Tkinter ships with most Python distributions. If missing on Linux, install `python3-tk` from your package manager.

## Usage
### A. Hide a message
```bash
python Encrypt_GUI.py
```
1. Click **Select Image**.
2. Enter the secret message.
3. Enter a password.
4. Click **Hide Message**.
5. Save the stego image (PNG recommended).

### B. Extract a message
```bash
python Decrypt_GUI.py
```
1. Click **Select Stego Image**.
2. Enter the same password.
3. Click **Extract Message**.
4. Read decrypted output in the result panel.

## Algorithm Summary
### Encryption + Embedding
1. Derive a 32-byte key from password (`SHA-256(password)`).
2. Encrypt plaintext with AES-CBC using a random 16-byte IV.
3. Prepend IV to ciphertext.
4. Embed bits of `IV || ciphertext` into LSBs of image channels.

### Extraction + Decryption
1. Sequentially read LSBs and reconstruct candidate bytes.
2. Split into IV (first 16 bytes) + ciphertext remainder.
3. Attempt AES-CBC decryption with the same password-derived key.
4. If valid plaintext is found, display it.

## Security Notes
- This project demonstrates cryptography + steganography for educational and practical experimentation.
- Use **PNG** as output to avoid lossy recompression artifacts that can destroy embedded bits.
- Current extraction logic is heuristic (tries block-aligned lengths) and does not include a cryptographic authenticity tag.

## Limitations
- No explicit payload length header in embedded data.
- No MAC/AEAD integrity protection in current message format.
- Decryption success is inferred; robust framing can improve reliability.

## Suggested Improvements
- Move from AES-CBC to AEAD mode (e.g., AES-GCM) for integrity + confidentiality.
- Embed payload length and versioned metadata format.
- Add automated tests and optional CLI interface.
- Add support for larger payload handling and compression.


