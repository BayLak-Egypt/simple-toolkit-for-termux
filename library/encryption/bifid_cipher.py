import color

DESCRIPTION = "Bifid Cipher Tool (Polybius + Fractionation)"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

SQUARE = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'],  # Note: J is mapped to I
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]

def get_coords(char):
    char = char.upper().replace('J', 'I')
    for r in range(5):
        for c in range(5):
            if SQUARE[r][c] == char:
                return r, c
    return None

def bifid_encrypt(text: str) -> str:
    clean_text = [c.upper().replace('J', 'I') for c in text if c.isalpha()]
    rows = []
    cols = []
    
    for char in clean_text:
        coords = get_coords(char)
        if coords:
            rows.append(coords[0])
            cols.append(coords[1])
            
    combined = rows + cols
    result = []
    
    for i in range(0, len(combined), 2):
        r = combined[i]
        c = combined[i+1]
        result.append(SQUARE[r][c])
        
    return "".join(result)

def bifid_decrypt(cipher: str) -> str:
    clean_cipher = [c.upper().replace('J', 'I') for c in cipher if c.isalpha()]
    combined = []
    
    for char in clean_cipher:
        coords = get_coords(char)
        if coords:
            combined.append(coords[0])
            combined.append(coords[1])
            
    half = len(combined) // 2
    rows = combined[:half]
    cols = combined[half:]
    
    result = []
    for r, c in zip(rows, cols):
        result.append(SQUARE[r][c])
        
    return "".join(result)

def run():
    print(color.color_text("--- Bifid Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return

        if choice == "1":
            output = bifid_encrypt(text)
        else:
            output = bifid_decrypt(text)

        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
