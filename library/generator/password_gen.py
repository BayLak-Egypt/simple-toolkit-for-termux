import random
import string
import color

DESCRIPTION = "Random Password Generator"
GROUP_ID = 3  # أدوات متنوعة
COLOR = color.GREEN

def run():
    print(color.color_text("--- مولد كلمات السر العشوائية ---", COLOR))
    length_input = input("أدخل طول كلمة السر (الافتراضي 16): ").strip()
    
    length = int(length_input) if length_input.isdigit() and int(length_input) > 0 else 16

    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = ''.join(random.choice(chars) for _ in range(length))

    print(color.color_text(f"\n[+] كلمة السر المقترحة:\n", color.WHITE))
    print(f"  {color.YELLOW}{password}{color.RESET}\n")
