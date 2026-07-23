import secrets
import color

DESCRIPTION = "Synthetic International Phone Number Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

PHONE_CONFIGS = {
    "Egypt": {"code": "+20", "prefixes": ["10", "11", "12", "15"], "length": 8},
    "Saudi Arabia": {"code": "+966", "prefixes": ["50", "53", "55", "56", "58", "59"], "length": 7},
    "UAE": {"code": "+971", "prefixes": ["50", "52", "54", "55", "56"], "length": 7},
    "USA": {"code": "+1", "prefixes": ["201", "202", "305", "415", "212"], "length": 7}
}

def generate_phone_number(country: str = "Egypt") -> str:
    """Generate a realistic synthetic phone number for the given country."""
    if country not in PHONE_CONFIGS:
        country = "Egypt"
        
    config = PHONE_CONFIGS[country]
    code = config["code"]
    prefix = secrets.choice(config["prefixes"])
    remaining_len = config["length"] - len(prefix)
    
    subscriber_num = "".join([str(secrets.randbelow(10)) for _ in range(remaining_len)])
    number_body = f"{prefix}{subscriber_num}"
    
    # Format nicely
    if country == "USA":
        formatted = f"{code} ({number_body[:3]}) {number_body[3:6]}-{number_body[6:]}"
    else:
        formatted = f"{code} {number_body[:3]} {number_body[3:]}"
        
    return formatted

def run():
    print(color.color_text("--- Synthetic Phone Number Generator ---", COLOR))
    print(" [1] Egypt (+20)")
    print(" [2] Saudi Arabia (+966)")
    print(" [3] UAE (+971)")
    print(" [4] USA (+1)")

    choice = input("\nSelect country (default 1 - Egypt): ").strip() or "1"
    mapping = {"1": "Egypt", "2": "Saudi Arabia", "3": "UAE", "4": "USA"}
    country = mapping.get(choice, "Egypt")

    try:
        count = int(input("How many phone numbers to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated {country} Phone Number(s):\n", color.GREEN))
    for idx in range(1, count + 1):
        phone = generate_phone_number(country)
        print(f"  [{idx}] {phone}")
