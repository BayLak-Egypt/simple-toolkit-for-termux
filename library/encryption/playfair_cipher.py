import color

DESCRIPTION = "Playfair Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def generate_key_matrix(key: str):
    """Generate 5x5 key matrix for Playfair Cipher (combining I and J)."""
    key = key.upper().replace('J', 'I')
    matrix = []
    seen = set()

    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)

    for code in range(ord('A'), ord('Z') + 1):
        char = chr(code)
        if char == 'J':
            continue
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None

def prepare_text(text: str) -> str:
    text = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')
    prepared = []
    i = 0
    while i < len(text):
        char1 = text[i]
        char2 = text[i + 1] if i + 1 < len(text) else 'X'

        if char1 == char2:
            prepared.append(char1)
            prepared.append('X')
            i += 1
        else:
            prepared.append(char1)
            prepared.append(char2)
            i += 2

    if len(prepared) % 2 != 0:
        prepared.append('X')

    return "".join(prepared)

def playfair_process(text: str, key: str, decrypt: bool = False) -> str:
    matrix = generate_key_matrix(key)
    prepared_text = prepare_text(text) if not decrypt else text.upper().replace('J', 'I')
    shift = -1 if decrypt else 1
    result = []

    for i in range(0, len(prepared_text), 2):
        r1, c1 = find_position(matrix, prepared_text[i])
        r2, c2 = find_position(matrix, prepared_text[i + 1])

        if r1 == r2:
            # Same row
            result.append(matrix[r1][(c1 + shift) % 5])
            result.append(matrix[r2][(c2 + shift) % 5])
        elif c1 == c2:
            # Same column
            result.append(matrix[(r1 + shift) % 5][c1])
            result.append(matrix[(r2 + shift) % 5][c2])
        else:
            # Rectangle swap
            result.append(matrix[r1][c2])
            result.append(matrix[r2][c1])

    return "".join(result)

def run():
    print(color.color_text("--- Playfair Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        key = input("Enter secret key word: ").strip()

        if not text or not key:
            print(color.color_text("[!] Text and key cannot be empty.", color.RED))
            return

        decrypt_flag = (choice == "2")
        output = playfair_process(text, key, decrypt=decrypt_flag)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
