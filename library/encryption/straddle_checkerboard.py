import color

DESCRIPTION = "Straddle Checkerboard Variable-Length Numerical Cipher"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# Standard board setup with high-frequency letters (E, T) taking 1 digit
# Empty slots at '2' and '6' trigger two-digit coordinates
BOARD = {
    'E': '0', 'A': '1', 'I': '3', 'N': '4', 'O': '5', 'R': '7', 'S': '8', 'T': '9',
    'B': '20', 'C': '21', 'D': '22', 'F': '23', 'G': '24', 'H': '25', 'J': '26', 'K': '27', 'L': '28', 'M': '29',
    'P': '60', 'Q': '61', 'U': '62', 'V': '63', 'W': '64', 'X': '65', 'Y': '66', 'Z': '67', '.': '68', '/': '69'
}

REVERSE_BOARD = {v: k for k, v in BOARD.items()}

def straddle_encrypt(text: str) -> str:
    text_clean = [c.upper() for c in text if c.upper() in BOARD]
    result = []
    for char in text_clean:
        result.append(BOARD[char])
    return "".join(result)

def straddle_decrypt(cipher: str) -> str:
    cipher_clean = [c for c in cipher if c.isdigit()]
    result = []
    i = 0
    while i < len(cipher_clean):
        digit = cipher_clean[i]
        if digit in ['2', '6']:
            if i + 1 < len(cipher_clean):
                code = digit + cipher_clean[i+1]
                result.append(REVERSE_BOARD.get(code, '?'))
                i += 2
            else:
                break
        else:
            result.append(REVERSE_BOARD.get(digit, '?'))
            i += 1
    return "".join(result)

def run():
    print(color.color_text("--- Straddle Checkerboard Tool ---", COLOR))
    print(" [1] Encrypt text to numerical stream")
    print(" [2] Decrypt numerical stream to text")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        text = input("Enter text: ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return
        output = straddle_encrypt(text)
        print(color.color_text(f"\n[+] Encrypted Numbers:\n{output}", color.GREEN))

    elif choice == "2":
        cipher = input("Enter digits string: ").strip()
        if not cipher:
            print(color.color_text("[!] Input cannot be empty.", color.RED))
            return
        output = straddle_decrypt(cipher)
        print(color.color_text(f"\n[+] Decrypted Text:\n{output}", color.GREEN))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
