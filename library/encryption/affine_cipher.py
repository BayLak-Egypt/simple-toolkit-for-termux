import color

DESCRIPTION = "Affine Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# Valid 'a' keys must be coprime with 26
VALID_A_KEYS = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

def mod_inverse(a, m=26):
    """Find modular multiplicative inverse of a under modulo m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, a, b):
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            x = ord(char) - start
            enc_x = (a * x + b) % 26
            result.append(chr(enc_x + start))
        else:
            result.append(char)
    return "".join(result)

def affine_decrypt(text, a, b):
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None
    
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            y = ord(char) - start
            dec_x = (a_inv * (y - b)) % 26
            result.append(chr(dec_x + start))
        else:
            result.append(char)
    return "".join(result)

def run():
    print(color.color_text("--- Affine Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        
        print(f"\nValid 'a' key values (coprime to 26): {VALID_A_KEYS}")
        try:
            a = int(input("Enter key 'a': ").strip())
            b = int(input("Enter key 'b' (shift number): ").strip())
        except ValueError:
            print(color.color_text("[!] Keys must be integers.", color.RED))
            return

        if a not in VALID_A_KEYS:
            print(color.color_text("[!] Key 'a' must be coprime to 26.", color.RED))
            return

        if choice == "1":
            output = affine_encrypt(text, a, b)
        else:
            output = affine_decrypt(text, a, b)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
