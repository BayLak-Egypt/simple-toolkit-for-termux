import base64
import json
import hmac
import hashlib
import time
import color

DESCRIPTION = "Developer JWT (JSON Web Token) Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def base64url_encode(data: bytes) -> str:
    """Encode bytes using Base64URL encoding without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def generate_jwt(payload_data: dict, secret_key: str) -> str:
    """Generate a signed JWT token using HS256 algorithm."""
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    # Encode Header and Payload
    encoded_header = base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    encoded_payload = base64url_encode(json.dumps(payload_data, separators=(',', ':')).encode('utf-8'))

    # Create Signature
    signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hmac.new(secret_key.encode('utf-8'), signing_input, hashlib.sha256).digest()
    encoded_signature = base64url_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def run():
    print(color.color_text("--- JWT Token Generator (HS256) ---", COLOR))
    
    sub = input("Enter Subject/User ID (e.g. user_123): ").strip() or "dev_user"
    role = input("Enter Role (e.g. admin, user): ").strip() or "user"
    
    try:
        exp_minutes = int(input("Enter expiration in minutes (default 60): ").strip() or "60")
    except ValueError:
        exp_minutes = 60

    secret = input("Enter Secret Key (for HMAC-SHA256 signature): ").strip()
    if not secret:
        print(color.color_text("[!] Secret key cannot be empty.", color.RED))
        return

    now = int(time.time())
    payload = {
        "sub": sub,
        "role": role,
        "iat": now,
        "exp": now + (exp_minutes * 60)
    }

    token = generate_jwt(payload, secret)

    print(color.color_text(f"\n[+] Generated JWT Payload:\n{json.dumps(payload, indent=2)}", color.GREEN))
    print(color.color_text(f"\n[+] Signed JWT Token:\n{token}", color.GREEN))
