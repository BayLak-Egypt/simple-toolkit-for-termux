import base64
import color

DESCRIPTION = "Base85 (ASCII85) Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- Base85 Tool ---", COLOR))
    print(" [1] Encode text to Base85")
    print(" [2] Decode Base85 to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        encoded = base64.b85encode(text.encode('utf-8')).decode('utf-8')
        print(color.color_text(f"\n[+] Encoded Base85:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        b85_text = input("Enter Base85 string to decode: ").strip()
        try:
            decoded = base64.b85decode(b85_text.encode('utf-8')).decode('utf-8')
            print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        except Exception:
            print(color.color_text("\n[!] Invalid Base85 string.", color.RED))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
