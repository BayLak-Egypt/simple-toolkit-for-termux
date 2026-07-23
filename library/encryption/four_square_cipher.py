import color

DESCRIPTION = "Four-Square Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 25 letters (J is mapped to I)

def generate_square(key: str) -> list:
    """Generate a 5x5 grid from a key word."""
    key_clean = "".join([c.upper().replace('J', 'I') for c in key if c.isalpha()])
    seen = set()
    square = []

    for char in key_clean:
        if char not in seen:
            seen.add(char)
            square.append(char)

    for char in ALPHABET:
        if char not in seen:
            seen.add(char)
            square.append(char)

    return [square[i:i+5] for i in range(0, 25, 5)]

def find_pos(square: list, char: str):
    for r in range(5):
        for c in range(5):
            if square[r][c] == char:
                return r, c
    return None

def prepare_pairs(text: str) -> list:
    clean = [c.upper().replace('J', 'I') for c in text if c.isalpha()]
    if len(clean) % 2 != 0:
        clean.append('X')
    return [(clean[i], clean[i+1]) for i in range(0, len(clean), 2)]

def four_square_encrypt(text: str, key1: str, key2: str) -> str:
    plain_square = generate_square("")
    q2_square = generate_square(key1)  # Top Right
    q3_square = generate_square(key2)  # Bottom Left

    pairs = prepare_pairs(text)
    result = []

    for char1, char2 in pairs:
        r1, c1 = find_pos(plain_square, char1)
        r2, c2 = find_pos(plain_square, char2)

        enc_char1 = q2_square[r1][c2]
        enc_char2 = q3_square[r2][c1]

        result.append(enc_char1 + enc_char2)

    return "".join(result)

def four_square_decrypt(cipher: str, key1: str, key2: str) -> str:
    plain_square = generate_square("")
    q2_square = generate_square(key1)
    q3_square = generate_square(key2)

    pairs = prepare_pairs(cipher)
    result = []

    for char1, char2 in pairs:
        r1, c2 = find_pos(q2_square, char1)
        r2, c1 = find_pos(q3_square, char2)

        plain_char1 = plain_square[r1][c1]
        plain_char2 = plain_square[r2][c2]

        result.append(plain_char1 + plain_char2)

    return "".join(result)

def run():
    print(color.color_text("--- Four-Square Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        key1 = input("Enter First Key Word: ").strip()
        key2 = input("Enter Second Key Word: ").strip()

        if not text or not key1 or not key2:
            print(color.color_text("[!] Text and both keys are required.", color.RED))
            return

        if choice == "1":
            output = four_square_encrypt(text, key1, key2)
        else:
            output = four_square_decrypt(text, key1, key2)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
