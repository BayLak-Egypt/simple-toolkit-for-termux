import color

DESCRIPTION = "Binary (01) Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- Binary Tool ---", COLOR))
    print(" [1] Encode text to Binary")
    print(" [2] Decode Binary to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        binary_str = ' '.join(format(ord(char), '08b') for char in text)
        print(color.color_text(f"\n[+] Encoded Binary:\n{binary_str}", color.GREEN))
        
    elif choice == "2":
        binary_text = input("Enter Binary string (space-separated bytes): ").strip()
        try:
            bytes_list = binary_text.split()
            decoded = ''.join(chr(int(b, 2)) for b in bytes_list)
            print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Invalid Binary string.", color.RED))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
