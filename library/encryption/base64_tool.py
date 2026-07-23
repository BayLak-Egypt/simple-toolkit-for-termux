import base64
import color

DESCRIPTION = "Base64 Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- Base64 Tool ---", COLOR))
    print(" [1] Encode text to Base64")
    print(" [2] Decode Base64 to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        encoded = base64.b64encode(text.encode()).decode()
        print(color.color_text(f"\n[+] Encoded text:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        encoded_text = input("Enter Base64 text to decode: ").strip()
        try:
            decoded = base64.b64decode(encoded_text.encode()).decode()
            print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Invalid Base64 string.", color.RED))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
