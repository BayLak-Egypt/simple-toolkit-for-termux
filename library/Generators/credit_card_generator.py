import secrets
import color

DESCRIPTION = "Synthetic Credit Card & Payment Info Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

# Card prefixes (BIN/IIN) for Luhn-compliant generation
CARD_TYPES = {
    "Visa": {"prefix": ["4"], "length": 16},
    "MasterCard": {"prefix": ["51", "52", "53", "54", "55"], "length": 16},
    "Amex": {"prefix": ["34", "37"], "length": 15},
    "Discover": {"prefix": ["6011"], "length": 16}
}

def luhn_checksum(card_num: str) -> int:
    """Calculate Luhn checksum digit for valid card number generation."""
    digits = [int(c) for c in card_num]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(divmod(2 * d, 10))
    return (10 - (total % 10)) % 10

def generate_credit_card(card_type: str = "Visa") -> dict:
    """Generate a mock payment card matching Luhn algorithm."""
    if card_type not in CARD_TYPES:
        card_type = "Visa"
        
    config = CARD_TYPES[card_type]
    prefix = secrets.choice(config["prefix"])
    length = config["length"]
    
    # Generate remaining random digits except the last checksum digit
    remaining_len = length - len(prefix) - 1
    body = prefix + "".join([str(secrets.randbelow(10)) for _ in range(remaining_len)])
    
    # Append Luhn check digit
    check_digit = luhn_checksum(body + "0")
    card_number = body + str(check_digit)
    
    # Format number with spaces for readability
    if length == 16:
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
    else:  # Amex 15 digits
        formatted_number = f"{card_number[:4]} {card_number[4:10]} {card_number[10:]}"

    cvv_len = 3 if card_type != "Amex" else 4
    cvv = "".join([str(secrets.randbelow(10)) for _ in range(cvv_len)])
    
    month = f"{secrets.randbelow(12) + 1:02d}"
    year = f"{secrets.randbelow(6) + 2026}"
    
    return {
        "Card Type": card_type,
        "Card Number": formatted_number,
        "Expiry Date": f"{month}/{year}",
        "CVV": cvv
    }

def run():
    print(color.color_text("--- Synthetic Credit Card Generator ---", COLOR))
    print(" [1] Visa")
    print(" [2] MasterCard")
    print(" [3] American Express (Amex)")
    print(" [4] Discover")

    choice = input("\nSelect card type (default 1 - Visa): ").strip() or "1"
    
    mapping = {"1": "Visa", "2": "MasterCard", "3": "Amex", "4": "Discover"}
    card_type = mapping.get(choice, "Visa")

    try:
        count = int(input("How many cards to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated {card_type} Card(s):\n", color.GREEN))
    for idx in range(1, count + 1):
        card = generate_credit_card(card_type)
        print(color.color_text(f"--- Card #{idx} ---", color.YELLOW))
        for key, value in card.items():
            print(f"  {key:<13}: {value}")
        print()
