import color

DESCRIPTION = "Polybius Square Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

# Standard 5x5 Polybius Square (I and J share the position '24')
SQUARE = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'],  # Note: J is mapped to I
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]

def polybius_encrypt(text: str) -> str:
    text = text.upper().replace('J', 'I')
    encoded = []
    
    for char in text:
        if char == ' ':
            encoded.append('/')
            continue
        
        found = False
        for row in range(5):
            for col in range(5):
                if SQUARE[row][col] == char:
                    # Row and Column starting from 1 to 5
                    encoded.append(f"{row + 1}{col + 1}")
                    found = True
                    break
            if found:
                break
        if not found and char.isalnum():
            encoded.append(char)
            
    return " ".join(encoded)

def polybius_decrypt(cipher: str) -> str:
    tokens = cipher.split()
    decoded = []
    
    for token in tokens:
        if token == '/':
            decoded.append(' ')
        elif len(token) == 2 and token.isdigit():
            r = int(token[0]) - 1
            c = int(token[1]) - 1
            if 0 <= r < 5 and 0 <= c < 5:
                decoded.append(SQUARE[r][c])
            else:
                decoded.append('?')
        else:
            decoded.append(token)
            
    return "".join(decoded)

def run():
    print(color.color_text("--- Polybius Square Tool ---", COLOR))
    print(" [1] Encode text to Polybius coordinates")
    print(" [2] Decode Polybius coordinates to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return
        output = polybius_encrypt(text)
        print(color.color_text(f"\n[+] Encoded Coordinates:\n{output}", color.GREEN))
        
    elif choice == "2":
        cipher = input("Enter coordinate pairs (e.g. 11 15 32 or / for space): ").strip()
        if not cipher:
            print(color.color_text("[!] Input cannot be empty.", color.RED))
            return
        output = polybius_decrypt(cipher)
        print(color.color_text(f"\n[+] Decoded text:\n{output}", color.GREEN))
        
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
