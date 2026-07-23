import base64
import color

DESCRIPTION = "Base32 Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- Base32 Tool ---", COLOR))
    print(" [1] Encode text to Base32")
    print(" [2] Decode Base32 to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        encoded = base64.b32encode(text.encode('utf-8')).decode('utf-8')
        print(color.color_text(f"\n[+] Encoded Base32:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        b32_text = input("Enter Base32 string to decode: ").strip()
        try:
            decoded = base64.b32decode(b32_text.encode('utf-8')).decode('utf-8')
            print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Invalid Base32 string.", color.RED))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
