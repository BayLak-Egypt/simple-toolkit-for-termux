import math
import color

DESCRIPTION = "Scytale Ancient Greek Transposition Cipher Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def scytale_encrypt(text: str, diameter: int) -> str:
    """Encrypt text using Scytale transposition with given rod diameter (columns)."""
    text_clean = "".join([c.upper() for c in text if c.isalnum()])
    if not text_clean or diameter <= 0:
        return ""

    num_rows = math.ceil(len(text_clean) / diameter)
    # Pad text to fill the full grid matrix
    padded_text = text_clean.ljust(num_rows * diameter, 'X')

    # Read column by column (around the cylinder rod)
    encrypted = []
    for col in range(diameter):
        for row in range(num_rows):
            idx = row * diameter + col
            encrypted.append(padded_text[idx])

    return "".join(encrypted)

def scytale_decrypt(cipher: str, diameter: int) -> str:
    """Decrypt text using Scytale transposition with given rod diameter (columns)."""
    cipher_clean = "".join([c.upper() for c in cipher if c.isalnum()])
    if not cipher_clean or diameter <= 0:
        return ""

    num_rows = len(cipher_clean) // diameter
    if num_rows == 0:
        return cipher_clean

    decrypted = [''] * len(cipher_clean)
    idx = 0
    for col in range(diameter):
        for row in range(num_rows):
            target_pos = row * diameter + col
            if idx < len(cipher_clean):
                decrypted[target_pos] = cipher_clean[idx]
                idx += 1

    return "".join(decrypted)

def run():
    print(color.color_text("--- Scytale Transposition Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        try:
            diameter = int(input("Enter rod diameter (number of columns/turns, e.g. 4): ").strip())
        except ValueError:
            print(color.color_text("[!] Diameter must be an integer.", color.RED))
            return

        if diameter <= 0:
            print(color.color_text("[!] Diameter must be greater than 0.", color.RED))
            return

        if choice == "1":
            output = scytale_encrypt(text, diameter)
        else:
            output = scytale_decrypt(text, diameter)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
