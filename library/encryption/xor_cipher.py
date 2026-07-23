import color

DESCRIPTION = "XOR Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def xor_encrypt_decrypt(text, key):
    result = []
    key_length = len(key)
    for i, char in enumerate(text):
        # Apply XOR between char code and key character code
        key_char = key[i % key_length]
        result.append(chr(ord(char) ^ ord(key_char)))
    return "".join(result)

def run():
    print(color.color_text("--- XOR Cipher Tool ---", COLOR))
    text = input("Enter text: ").strip()
    key = input("Enter secret key: ").strip()

    if not text or not key:
        print(color.color_text("[!] Text and key cannot be empty.", color.RED))
        return

    # XOR is symmetric: applying the same operation with the same key decrypts the message
    output = xor_encrypt_decrypt(text, key)
    
    print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
