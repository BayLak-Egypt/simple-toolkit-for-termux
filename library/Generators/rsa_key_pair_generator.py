from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import color

DESCRIPTION = "RSA Public/Private Key Pair Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_rsa_keys(key_size: int = 2048) -> dict:
    """Generate an RSA private and public key pair in PEM format."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    
    return {
        "Private Key": private_pem,
        "Public Key": public_pem
    }

def run():
    print(color.color_text("--- RSA Key Pair Generator ---", COLOR))
    
    print(" [1] 2048-bit (Standard)")
    print(" [2] 4096-bit (High Security)")
    choice = input("\nSelect key size option (default 1 - 2048): ").strip() or "1"
    key_size = 4096 if choice == "2" else 2048

    print(color.color_text(f"\n[+] Generating {key_size}-bit RSA Key Pair...\n", color.GREEN))
    keys = generate_rsa_keys(key_size)
    
    print(color.color_text("--- Private Key (PEM) ---", color.YELLOW))
    print(keys["Private Key"])
    print(color.color_text("--- Public Key (PEM) ---", color.YELLOW))
    print(keys["Public Key"])
