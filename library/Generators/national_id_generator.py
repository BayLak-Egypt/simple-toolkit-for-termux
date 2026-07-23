import secrets
import color

DESCRIPTION = "Synthetic National ID & Personal Identifier Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_mock_national_id() -> str:
    """Generate a structured synthetic 14-digit national ID (e.g. Century + YYMMDD + Governorate + Serial + Check)."""
    # Century code (e.g., '2' for 1900-1999, '3' for 2000-2099)
    century = secrets.choice(["2", "3"])
    
    # Year, Month, Day (e.g. 950512)
    yy = f"{secrets.randbelow(100):02d}"
    mm = f"{secrets.randbelow(12) + 1:02d}"
    dd = f"{secrets.randbelow(28) + 1:02d}"
    
    # Governorate code (2 digits)
    gov = f"{secrets.randbelow(88) + 1:02d}"
    
    # Serial number (3 digits)
    serial = f"{secrets.randbelow(900) + 100:03d}"
    
    # Gender digit (1 digit, odd for male, even for female)
    gender = str(secrets.randbelow(5) * 2 + 1)
    
    # Check digit (1 digit)
    check = str(secrets.randbelow(10))
    
    national_id = f"{century}{yy}{mm}{dd}{gov}{serial}{gender}{check}"
    return national_id

def run():
    print(color.color_text("--- Synthetic National ID Generator ---", COLOR))
    
    try:
        count = int(input("How many National IDs to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated Synthetic National ID(s):\n", color.GREEN))
    for idx in range(1, count + 1):
        nid = generate_mock_national_id()
        print(f"  [{idx}] {nid}")
