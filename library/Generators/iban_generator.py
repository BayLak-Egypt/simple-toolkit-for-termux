import secrets
import color

DESCRIPTION = "Synthetic International Bank Account Number (IBAN) Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

# Sample country structures (Country Code, Basic Bank Account Number length)
COUNTRY_CONFIGS = {
    "SA": {"name": "Saudi Arabia", "bban_len": 18, "bank_prefix": ["01", "05", "10", "15", "20", "45", "55"]},
    "AE": {"name": "United Arab Emirates", "bban_len": 19, "bank_prefix": ["03", "34", "02", "01"]},
    "EG": {"name": "Egypt", "bban_len": 25, "bank_prefix": ["001", "002", "003", "004"]},
    "GB": {"name": "United Kingdom", "bban_len": 18, "bank_prefix": ["NWBK", "BARC", "LOYD"]}
}

def calculate_iban_checksum(country_code: str, bban: str) -> str:
    """Calculate ISO 7064 Mod 97-10 check digits for IBAN."""
    # Move country code and '00' to the end
    rearranged = bban + country_code + "00"
    
    # Convert letters to numbers (A=10, B=11, ..., Z=35)
    numeric_str = ""
    for char in rearranged:
        if char.isdigit():
            numeric_str += char
        else:
            numeric_str += str(ord(char.upper()) - 55)
            
    # Calculate remainder mod 97
    remainder = int(numeric_str) % 97
    check_digits = 98 - remainder
    return f"{check_digits:02d}"

def generate_iban(country_code: str = "SA") -> str:
    """Generate a valid mock IBAN for the given country code."""
    if country_code not in COUNTRY_CONFIGS:
        country_code = "SA"
        
    config = COUNTRY_CONFIGS[country_code]
    bban_len = config["bban_len"]
    
    # Generate random BBAN (digits)
    bban = "".join([str(secrets.randbelow(10)) for _ in range(bban_len)])
    
    # Calculate checksum
    checksum = calculate_iban_checksum(country_code, bban)
    
    # Construct final IBAN: CC + Checksum + BBAN
    iban = f"{country_code}{checksum}{bban}"
    
    # Format with spaces every 4 characters for readability
    formatted_iban = " ".join([iban[i:i+4] for i in range(0, len(iban), 4)])
    return formatted_iban

def run():
    print(color.color_text("--- Synthetic IBAN Generator ---", COLOR))
    print(" [1] Saudi Arabia (SA)")
    print(" [2] United Arab Emirates (AE)")
    print(" [3] Egypt (EG)")
    print(" [4] United Kingdom (GB)")

    choice = input("\nSelect country (default 1 - SA): ").strip() or "1"
    
    mapping = {"1": "SA", "2": "AE", "3": "EG", "4": "GB"}
    country_code = mapping.get(choice, "SA")

    try:
        count = int(input("How many IBANs to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    print(color.color_text(f"\n[+] Generated {COUNTRY_CONFIGS[country_code]['name']} IBAN(s):\n", color.GREEN))
    for idx in range(1, count + 1):
        iban = generate_iban(country_code)
        print(f"  [{idx}] {iban}")
