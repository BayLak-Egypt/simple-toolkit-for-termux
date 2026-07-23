import color

DESCRIPTION = "Caesar Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def encrypt_caesar(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def run():
    print(color.color_text("--- Caesar Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        shift_input = input("Enter shift key (number, default 3): ").strip()
        shift = int(shift_input) if shift_input.isdigit() else 3
        
        if choice == "2":
            shift = -shift
            
        output = encrypt_caesar(text, shift)
        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
