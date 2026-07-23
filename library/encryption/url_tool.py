import urllib.parse
import color

DESCRIPTION = "URL Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- URL Encoder / Decoder ---", COLOR))
    print(" [1] Encode text to URL format")
    print(" [2] Decode URL format to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text/URL to encode: ").strip()
        encoded = urllib.parse.quote(text)
        print(color.color_text(f"\n[+] Encoded URL:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        encoded_text = input("Enter encoded URL to decode: ").strip()
        decoded = urllib.parse.unquote(encoded_text)
        print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
