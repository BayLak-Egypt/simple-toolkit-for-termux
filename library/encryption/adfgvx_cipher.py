import color

DESCRIPTION = "ADFGVX Military Cipher Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

ADFGVX = ['A', 'D', 'F', 'G', 'V', 'X']

# Default 6x6 grid containing A-Z and 0-9
DEFAULT_GRID = [
    ['N', 'A', '1', 'C', '3', 'D'],
    ['8', 'Z', 'C', 'H', '0', 'O'],
    ['F', 'I', '2', 'W', 'P', '1'],
    ['E', 'S', '4', 'U', 'Y', '9'],
    ['5', 'R', '7', 'V', 'K', 'L'],
    ['M', '6', 'B', 'G', 'T', 'X']
]

def get_coordinates(char):
    char = char.upper()
    for r in range(6):
        for c in range(6):
            if DEFAULT_GRID[r][c] == char:
                return ADFGVX[r] + ADFGVX[c]
    return ""

def substitute_text(text):
    result = []
    for char in text.upper():
        if char.isalnum():
            coords = get_coordinates(char)
            if coords:
                result.append(coords)
    return "".join(result)

def transpose_encrypt(substituted_str, key):
    key = key.upper()
    cols = len(key)
    grid = {i: [] for i in range(cols)}

    for idx, char in enumerate(substituted_str):
        grid[idx % cols].append(char)

    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    
    cipher_text = []
    for idx in sorted_key_indices:
        cipher_text.append("".join(grid[idx]))

    return " ".join(cipher_text)

def run():
    print(color.color_text("--- ADFGVX Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text (Letters & Numbers): ").strip()
        key = input("Enter secret key word: ").strip()
        
        if not text or not key:
            print(color.color_text("[!] Text and key cannot be empty.", color.RED))
            return
            
        sub_text = substitute_text(text)
        encrypted = transpose_encrypt(sub_text, key)
        
        print(color.color_text(f"\n[+] Encrypted ADFGVX Text:\n{encrypted}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
