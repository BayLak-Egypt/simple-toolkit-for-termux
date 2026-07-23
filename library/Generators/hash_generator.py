import hashlib
import color

DESCRIPTION = "Cryptographic Hash Generator (MD5, SHA-256, etc.)"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_hashes(text: str) -> dict:
    """Generate multiple standard cryptographic hashes for a given text."""
    data = text.encode('utf-8')
    return {
        "MD5": hashlib.md5(data).hexdigest(),
        "SHA-1": hashlib.sha1(data).hexdigest(),
        "SHA-256": hashlib.sha256(data).hexdigest(),
        "SHA-512": hashlib.sha512(data).hexdigest()
    }

def run():
    print(color.color_text("--- Cryptographic Hash Generator ---", COLOR))
    
    text = input("Enter text to hash: ").strip()
    if not text:
        print(color.color_text("[!] Input text cannot be empty.", color.RED))
        return

    hashes = generate_hashes(text)
    
    print(color.color_text(f"\n[+] Generated Hashes for '{text}':\n", color.GREEN))
    for algo, hval in hashes.items():
        print(f"  {algo:<8}: {hval}")
