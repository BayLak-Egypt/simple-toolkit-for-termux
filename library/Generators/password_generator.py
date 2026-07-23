import secrets
import string
import color

DESCRIPTION = "Secure Cryptographic Password Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_password(length: int = 16, use_symbols: bool = True, use_numbers: bool = True, use_uppercase: bool = True) -> str:
    """Generate a secure random password based on specified character sets."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ""
    numbers = string.digits if use_numbers else ""
    symbols = string.punctuation if use_symbols else ""
    
    all_chars = lowercase + uppercase + numbers + symbols
    if not all_chars:
        all_chars = lowercase  # Fallback
        
    # Ensure at least one character from each selected category is present for strength
    password_chars = []
    if use_uppercase:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if use_numbers:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice(string.punctuation))
        
    # Fill the rest of the length
    remaining_length = length - len(password_chars)
    for _ in range(max(0, remaining_length)):
        password_chars.append(secrets.choice(all_chars))
        
    # Shuffle the resulting characters securely
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

def run():
    print(color.color_text("--- Secure Password Generator ---", COLOR))
    
    try:
        length = int(input("Enter password length (default 16): ").strip() or "16")
        if length < 6:
            length = 6
    except ValueError:
        length = 16

    use_sym = input("Include symbols/special characters? [y/N] (default y): ").strip().lower() != "n"
    use_num = input("Include numbers? [y/N] (default y): ").strip().lower() != "n"
    use_upper = input("Include uppercase letters? [y/N] (default y): ").strip().lower() != "n"

    try:
        count = int(input("How many passwords to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated Secure Password(s):\n", color.GREEN))
    for idx in range(1, count + 1):
        pwd = generate_password(length, use_sym, use_num, use_upper)
        print(f"  [{idx}] {pwd}")
