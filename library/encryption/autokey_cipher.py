import color

DESCRIPTION = "Autokey Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def autokey_encrypt(text: str, key: str) -> str:
    text_clean = [c.upper() for c in text if c.isalpha()]
    key_clean = [c.upper() for c in key if c.isalpha()]
    
    if not key_clean:
        return ""
        
    # Extended key = initial key + plaintext
    full_key = key_clean + text_clean
    result = []
    
    for i, char in enumerate(text_clean):
        p = ord(char) - ord('A')
        k = ord(full_key[i]) - ord('A')
        c = (p + k) % 26
        result.append(chr(c + ord('A')))
        
    return "".join(result)

def autokey_decrypt(cipher: str, key: str) -> str:
    cipher_clean = [c.upper() for c in cipher if c.isalpha()]
    key_clean = [c.upper() for c in key if c.isalpha()]
    
    if not key_clean:
        return ""
        
    result = []
    current_key = list(key_clean)
    
    for i, char in enumerate(cipher_clean):
        c = ord(char) - ord('A')
        k = ord(current_key[i]) - ord('A')
        p = (c - k) % 26
        plain_char = chr(p + ord('A'))
        result.append(plain_char)
        # Append recovered plaintext char to extend key dynamically
        current_key.append(plain_char)
        
    return "".join(result)

def run():
    print(color.color_text("--- Autokey Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text (letters only): ").strip()
        key = input("Enter primer key word: ").strip()

        if not text or not key:
            print(color.color_text("[!] Text and key cannot be empty.", color.RED))
            return

        if choice == "1":
            output = autokey_encrypt(text, key)
        else:
            output = autokey_decrypt(text, key)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
