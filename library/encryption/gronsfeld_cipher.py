import color

DESCRIPTION = "Gronsfeld Numeric Shift Cipher Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def gronsfeld_process(text: str, key_num: str, decrypt: bool = False) -> str:
    if not key_num.isdigit():
        raise ValueError("Key must contain digits only.")

    key_digits = [int(d) for d in key_num]
    result = []
    key_idx = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_digits[key_idx % len(key_digits)]
            if decrypt:
                shift = -shift
            
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(new_char)
            key_idx += 1
        else:
            result.append(char)

    return "".join(result)

def run():
    print(color.color_text("--- Gronsfeld Cipher Tool ---", COLOR))
    print(" [1] Encrypt text using numeric key")
    print(" [2] Decrypt text using numeric key")

    choice = input("\nSelect an option: ").strip()

    if choice in ["1", "2"]:
        text = input("Enter text: ").strip()
        key = input("Enter numeric key (e.g. 31415): ").strip()

        if not text or not key:
            print(color.color_text("[!] Text and key cannot be empty.", color.RED))
            return

        try:
            is_decrypt = (choice == "2")
            output = gronsfeld_process(text, key, decrypt=is_decrypt)
            print(color.color_text(f"\n[+] Result:\n{output}", color.GREEN))
        except ValueError as e:
            print(color.color_text(f"\n[!] Error: {e}", color.RED))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
