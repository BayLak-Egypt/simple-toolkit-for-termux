import secrets
import hashlib
import color

DESCRIPTION = "Secure API Key Generator with Prefix & Checksum"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_api_key(prefix: str = "sk_live", secret_length: int = 24) -> str:
    """Generate a secure API key with prefix and trailing checksum byte."""
    # Generate random secret bytes
    random_bytes = secrets.token_bytes(secret_length)
    secret_hex = random_bytes.hex()
    
    # Calculate a 2-character checksum from the secret
    checksum = hashlib.sha256(random_bytes).hexdigest()[:2]
    
    # Format: prefix_secrethex_checksum
    return f"{prefix}_{secret_hex}{checksum}"

def verify_api_key_format(api_key: str, prefix: str = "sk_live") -> bool:
    """Fast integrity check on API key structure and checksum."""
    if not api_key.startswith(f"{prefix}_"):
        return False
    
    body = api_key[len(prefix) + 1:]
    if len(body) < 4:
        return False

    secret_hex = body[:-2]
    provided_checksum = body[-2:]
    
    try:
        raw_bytes = bytes.fromhex(secret_hex)
        calculated_checksum = hashlib.sha256(raw_bytes).hexdigest()[:2]
        return secrets.compare_digest(provided_checksum, calculated_checksum)
    except ValueError:
        return False

def run():
    print(color.color_text("--- API Key Generator ---", COLOR))
    
    prefix = input("Enter key prefix (e.g. sk_live, pk_test - default 'sk_live'): ").strip() or "sk_live"
    
    try:
        count = int(input("How many keys to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated API Key(s):\n", color.GREEN))
    for _ in range(count):
        key = generate_api_key(prefix=prefix)
        is_valid = verify_api_key_format(key, prefix=prefix)
        print(f"  Key    : {key}")
        print(f"  Valid  : {is_valid}\n")
