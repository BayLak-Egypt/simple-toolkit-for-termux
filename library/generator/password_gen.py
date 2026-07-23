import random
import string
import color

DESCRIPTION = "Random Password Generator"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.GREEN

def run():
    print(color.color_text("--- Random Password Generator ---", COLOR))
    length_input = input("Enter password length (default 16): ").strip()
    
    length = int(length_input) if length_input.isdigit() and int(length_input) > 0 else 16

    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = ''.join(random.choice(chars) for _ in range(length))

    print(color.color_text(f"\n[+] Generated Password:\n", color.WHITE))
    print(f"  {color.YELLOW}{password}{color.RESET}\n")
