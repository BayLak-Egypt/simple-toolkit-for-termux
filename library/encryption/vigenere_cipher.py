import color

DESCRIPTION = "Vigenère Cipher Encoder / Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def vigenere_process(text, key, decrypt=False):
    result = []
    key = key.lower()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('a')
            
            if decrypt:
                shift = -shift
                
            processed_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(processed_char)
            key_index += 1
        else:
            result.append(char)
            
    return "".join(result)

def run():
    print(color.color_text("--- Vigenère Cipher Tool ---", COLOR))
    print(" [1] Encrypt text")
    print(" [2] Decrypt text")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        key = input("Enter secret key word (letters only): ").strip()
        
        if not text or not key or not key.isalpha():
            print(color.color_text("[!] Text and key must contain valid letters.", color.RED))
            return
            
        decrypt_flag = (choice == "2")
        output = vigenere_process(text, key, decrypt=decrypt_flag)
        
        print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
