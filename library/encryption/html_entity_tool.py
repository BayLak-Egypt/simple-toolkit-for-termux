import html
import color

DESCRIPTION = "HTML Entity Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- HTML Entity Tool ---", COLOR))
    print(" [1] Encode text to HTML Entities")
    print(" [2] Decode HTML Entities to text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        encoded = html.escape(text)
        print(color.color_text(f"\n[+] Encoded HTML Entities:\n{encoded}", color.GREEN))
        
    elif choice == "2":
        html_text = input("Enter HTML Entities to decode: ").strip()
        decoded = html.unescape(html_text)
        print(color.color_text(f"\n[+] Decoded text:\n{decoded}", color.GREEN))
        
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
