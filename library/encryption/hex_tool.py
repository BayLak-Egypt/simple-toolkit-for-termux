import color

DESCRIPTION = "Hexadecimal Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- Hexadecimal Tool ---", COLOR))
    print(" [1] Encode text to Hex")
    print(" [2] Decode Hex to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        encoded = text.encode('utf-8').hex()
        print(color.color_text(f"\n[+] Encoded Hex:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        hex_text = input("Enter Hex text to decode: ").strip().replace(" ", "")
        try:
            decoded = bytes.fromhex(hex_text).decode('utf-8')
            print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Invalid Hexadecimal string.", color.RED))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
