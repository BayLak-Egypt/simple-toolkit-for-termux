import color

DESCRIPTION = "Atbash Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def apply_atbash(text):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(ord('Z') - (ord(char) - ord('A')))
            else:
                result += chr(ord('z') - (ord(char) - ord('a')))
        else:
            result += char
    return result

def run():
    print(color.color_text("--- Atbash Cipher Tool ---", COLOR))
    text = input("Enter text to apply Atbash Cipher: ").strip()
    
    if not text:
        print(color.color_text("[!] No text entered.", color.RED))
        return

    # Atbash is symmetric: applying it twice returns the original text
    result = apply_atbash(text)
    
    print(color.color_text(f"\n[+] Result:\n{result}", color.GREEN))
