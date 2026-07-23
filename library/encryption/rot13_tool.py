import codecs
import color

DESCRIPTION = "ROT13 Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def run():
    print(color.color_text("--- ROT13 Cipher Tool ---", COLOR))
    text = input("Enter text to apply ROT13: ").strip()
    
    if not text:
        print(color.color_text("[!] No text entered.", color.RED))
        return

    # ROT13 is symmetric: applying it twice returns the original text
    result = codecs.encode(text, 'rot_13')
    
    print(color.color_text(f"\n[+] Result:\n{result}", color.GREEN))
