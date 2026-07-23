import secrets
import color

DESCRIPTION = "Synthetic Mock Data Generator for Dev & Testing"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Cameron", "Jesse"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
DOMAINS = ["example.com", "test.org", "demo.net", "local.dev"]
STREETS = ["Main St", "High St", "Park Ave", "Oak Rd", "Cedar Ln", "Maple St"]
CITIES = ["Springfield", "Metropolis", "Gotham", "Rivendell", "Star City"]

def generate_profile() -> dict:
    """Generate a single fake user profile."""
    first = secrets.choice(FIRST_NAMES)
    last = secrets.choice(LAST_NAMES)
    domain = secrets.choice(DOMAINS)
    
    email = f"{first.lower()}.{last.lower()}{secrets.randbelow(99)}@{domain}"
    ip_addr = f"{secrets.randbelow(220)+1}.{secrets.randbelow(255)}.{secrets.randbelow(255)}.{secrets.randbelow(254)+1}"
    phone = f"+1-{secrets.randbelow(800)+200}-{secrets.randbelow(800)+200}-{secrets.randbelow(9000)+1000}"
    address = f"{secrets.randbelow(999)+1} {secrets.choice(STREETS)}, {secrets.choice(CITIES)}"
    
    return {
        "Name": f"{first} {last}",
        "Email": email,
        "Phone": phone,
        "Address": address,
        "IP Address": ip_addr
    }

def run():
    print(color.color_text("--- Synthetic Mock Data Generator ---", COLOR))
    
    try:
        count = int(input("How many records to generate? (default 3): ").strip() or "3")
    except ValueError:
        count = 3

    print(color.color_text(f"\n[+] Generated {count} Mock Profiles:\n", color.GREEN))

    for idx in range(1, count + 1):
        profile = generate_profile()
        print(color.color_text(f"--- Profile #{idx} ---", color.YELLOW))
        for key, value in profile.items():
            print(f"  {key:<12}: {value}")
        print()
