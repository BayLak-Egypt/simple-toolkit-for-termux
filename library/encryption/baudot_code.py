import color

DESCRIPTION = "Baudot Code (ITA2 5-bit Telegraph) Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# ITA2 Letters Shift Table
LETTERS_MAP = {
    'A': '11000', 'B': '10011', 'C': '01110', 'D': '10010', 'E': '10000',
    'F': '10110', 'G': '01011', 'H': '00101', 'I': '01100', 'J': '11010',
    'K': '11110', 'L': '01001', 'M': '00111', 'N': '00110', 'O': '00011',
    'P': '01101', 'Q': '11101', 'R': '01010', 'S': '10100', 'T': '00001',
    'U': '11100', 'V': '01111', 'W': '10001', 'X': '10111', 'Y': '10101',
    'Z': '10001', ' ': '00100'
}

REVERSE_LETTERS = {val: key for key, val in LETTERS_MAP.items()}

def baudot_encode(text: str) -> str:
    encoded = []
    for char in text.upper():
        if char in LETTERS_MAP:
            encoded.append(LETTERS_MAP[char])
        else:
            encoded.append("?????")
    return " ".join(encoded)

def baudot_decode(code_str: str) -> str:
    tokens = code_str.split()
    decoded = []
    for token in tokens:
        decoded.append(REVERSE_LETTERS.get(token, '?'))
    return "".join(decoded)

def run():
    print(color.color_text("--- Baudot Code (ITA2 Telegraph) Tool ---", COLOR))
    print(" [1] Encode text to 5-bit Baudot Code")
    print(" [2] Decode 5-bit Baudot Code to text")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        text = input("Enter text (A-Z and spaces): ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return
        output = baudot_encode(text)
        print(color.color_text(f"\n[+] Encoded 5-bit Baudot Code:\n{output}", color.GREEN))

    elif choice == "2":
        code_str = input("Enter 5-bit binary blocks (e.g., 11000 10000): ").strip()
        if not code_str:
            print(color.color_text("[!] Input cannot be empty.", color.RED))
            return
        output = baudot_decode(code_str)
        print(color.color_text(f"\n[+] Decoded Text:\n{output}", color.GREEN))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
