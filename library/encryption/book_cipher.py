import color

DESCRIPTION = "Book Cipher (Ottendorf / Beale Style) Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def book_encrypt(secret_text: str, book_text: str) -> str:
    words = book_text.split()
    word_map = {}
    
    # Map first letter of each word to its 1-based index
    for idx, word in enumerate(words, 1):
        clean_word = "".join(c for c in word if c.isalpha()).upper()
        if clean_word:
            first_char = clean_word[0]
            if first_char not in word_map:
                word_map[first_char] = []
            word_map[first_char].append(idx)

    encrypted_indices = []
    for char in secret_text.upper():
        if char.isalpha():
            if char in word_map and word_map[char]:
                # Pick the first available index
                idx = word_map[char].pop(0)
                encrypted_indices.append(str(idx))
            else:
                encrypted_indices.append("?")
        elif char == " ":
            encrypted_indices.append("/")

    return " ".join(encrypted_indices)

def book_decrypt(cipher_indices: str, book_text: str) -> str:
    words = book_text.split()
    tokens = cipher_indices.split()
    decrypted = []

    for token in tokens:
        if token == "/":
            decrypted.append(" ")
        elif token.isdigit():
            idx = int(token) - 1
            if 0 <= idx < len(words):
                word = words[idx]
                clean_word = "".join(c for c in word if c.isalpha()).upper()
                decrypted.append(clean_word[0] if clean_word else "?")
            else:
                decrypted.append("?")
        else:
            decrypted.append(token)

    return "".join(decrypted)

def run():
    print(color.color_text("--- Book Cipher Tool ---", COLOR))
    print(" [1] Encrypt text using reference book text")
    print(" [2] Decrypt text using reference book text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        book_text = input("Enter Reference Book Text (Key Source): ").strip()
        if not book_text:
            print(color.color_text("[!] Reference text cannot be empty.", color.RED))
            return

        if choice == "1":
            secret = input("Enter secret message to encrypt: ").strip()
            output = book_encrypt(secret, book_text)
            print(color.color_text(f"\n[+] Encrypted Indices:\n{output}", color.GREEN))
        else:
            cipher = input("Enter space-separated indices (e.g., 12 5 / 8): ").strip()
            output = book_decrypt(cipher, book_text)
            print(color.color_text(f"\n[+] Decrypted Text:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
