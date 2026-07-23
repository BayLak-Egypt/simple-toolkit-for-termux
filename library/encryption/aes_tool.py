import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import color

DESCRIPTION = "AES-256 Symmetric Encryption Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from a user password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_aes(plain_text: str, password: str) -> str:
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    # Combine salt + iv + cipher_text and encode with base64 for portable output
    combined = salt + iv + cipher_text
    return base64.b64encode(combined).decode('utf-8')

def decrypt_aes(encrypted_base64: str, password: str) -> str:
    data = base64.b64decode(encrypted_base64.encode('utf-8'))
    salt = data[:16]
    iv = data[16:32]
    cipher_text = data[32:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain_text = unpadder.update(padded_data) + unpadder.finalize()
    return plain_text.decode('utf-8')

def run():
    print(color.color_text("--- AES-256 Encryption Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encrypt: ").strip()
        password = input("Enter secret passphrase: ").strip()
        
        if not text or not password:
            print(color.color_text("[!] Text and passphrase cannot be empty.", color.RED))
            return
            
        encrypted = encrypt_aes(text, password)
        print(color.color_text(f"\n[+] Encrypted (Base64 Payload):\n{encrypted}", color.GREEN))
        
    elif choice == "2":
        encrypted_text = input("Enter Encrypted Base64 Payload: ").strip()
        password = input("Enter secret passphrase: ").strip()
        
        try:
            decrypted = decrypt_aes(encrypted_text, password)
            print(color.color_text(f"\n[+] Decrypted text:\n{decrypted}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Decryption failed. Incorrect passphrase or corrupt payload.", color.RED))
            
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
