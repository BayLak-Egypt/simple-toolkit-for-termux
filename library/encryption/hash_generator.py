import hashlib
import color

DESCRIPTION = "Multi-Hash Generator (MD5, SHA1, SHA256, SHA512)"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- Hash Generator Tool ---", COLOR))
    text = input("Enter text to generate hashes: ").strip()
    
    if not text:
        print(color.color_text("[!] No text entered.", color.RED))
        return

    text_bytes = text.encode('utf-8')
    
    md5_hash = hashlib.md5(text_bytes).hexdigest()
    sha1_hash = hashlib.sha1(text_bytes).hexdigest()
    sha256_hash = hashlib.sha256(text_bytes).hexdigest()
    sha512_hash = hashlib.sha512(text_bytes).hexdigest()

    print(color.color_text("\n[+] Generated Hashes:\n", color.WHITE))
    print(f"  {color.YELLOW}MD5    :{color.RESET} {md5_hash}")
    print(f"  {color.YELLOW}SHA-1  :{color.RESET} {sha1_hash}")
    print(f"  {color.YELLOW}SHA-256:{color.RESET} {sha256_hash}")
    print(f"  {color.YELLOW}SHA-512:{color.RESET} {sha512_hash}\n")
