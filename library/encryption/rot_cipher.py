import color

DESCRIPTION = "ROT13 & ROT47 Substitution Ciphers"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def rot13(text: str) -> str:
    """Apply ROT13 transformation (Letters only)."""
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(char)
    return "".join(result)

def rot47(text: str) -> str:
    """Apply ROT47 transformation (ASCII printable chars from ! to ~)."""
    result = []
    for char in text:
        code = ord(char)
        if 33 <= code <= 126:
            result.append(chr(33 + ((code - 33 + 47) % 94)))
        else:
            result.append(char)
    return "".join(result)

def run():
    print(color.color_text("--- ROT Cipher Tool ---", COLOR))
    print(" [1] ROT13 (Letters A-Z)")
    print(" [2] ROT47 (ASCII Printable Characters)")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return

        # ROT ciphers are symmetric (applying same rotation toggles back)
        output = rot13(text) if choice == "1" else rot47(text)
        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
