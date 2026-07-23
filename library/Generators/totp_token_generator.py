import hmac
import hashlib
import base64
import struct
import time
import color

DESCRIPTION = "TOTP (Time-based One-Time Password) Token Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_totp(secret_key: str, time_step: int = 30, digits: int = 6) -> str:
    """Generate a TOTP token for the current Unix time using a base32/secret string."""
    # Ensure secret is properly padded for base32 decoding if needed, or fallback to bytes
    try:
        # Normalize secret and add padding if missing
        missing_padding = len(secret_key) % 8
        if missing_padding:
            secret_key += '=' * (8 - missing_padding)
        key_bytes = base64.b32decode(secret_key.upper())
    except Exception:
        key_bytes = secret_key.encode('utf-8')

    # Current time step counter
    counter = int(time.time() // time_step)
    
    # Pack counter into 8 bytes big-endian
    msg = struct.pack(">Q", counter)
    
    # Calculate HMAC-SHA1
    hash_digest = hmac.new(key_bytes, msg, hashlib.sha1).digest()
    
    # Dynamic truncation
    offset = hash_digest[-1] & 0x0F
    binary_code = (
        ((hash_digest[offset] & 0x7F) << 24) |
        ((hash_digest[offset + 1] & 0xFF) << 16) |
        ((hash_digest[offset + 2] & 0xFF) << 8) |
        (hash_digest[offset + 3] & 0xFF)
    )
    
    otp = binary_code % (10 ** digits)
    return f"{otp:0{digits}d}"

def run():
    print(color.color_text("--- TOTP Token Generator ---", COLOR))
    
    default_secret = "JBSWY3DPEHPK3PXP" # Standard test secret base32 ("Hello! :)")
    secret_key = input(f"Enter Base32 Secret Key (default test secret): ").strip() or default_secret

    try:
        token = generate_totp(secret_key)
        remaining_seconds = 30 - (int(time.time()) % 30)
        
        print(color.color_text(f"\n[+] Generated TOTP Token:", color.GREEN))
        print(color.color_text(f"    Code: {token}", color.YELLOW))
        print(color.color_text(f"    Valid for next: {remaining_seconds} seconds", color.CYAN))
    except Exception as e:
        print(color.color_text(f"[!] Error generating TOTP: {e}", color.RED))
