import secrets
import color

DESCRIPTION = "Diceware-style Passphrase Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

# Standard Wordlist Subset for Diceware Passphrases
WORDLIST = [
    "ability", "about", "above", "absent", "absorb", "abstract", "academic", "accent",
    "access", "account", "accuracy", "achieve", "action", "active", "actor", "actual",
    "adapt", "address", "adjust", "advance", "advice", "afford", "agency", "agent",
    "agree", "airport", "alarm", "album", "alert", "algebra", "alien", "allow",
    "alphabet", "always", "amber", "ambient", "anchor", "ancient", "angel", "angle",
    "animal", "answer", "antenna", "antique", "anvil", "apology", "apple", "archive",
    "arctic", "arena", "argon", "armor", "arrow", "artist", "aspect", "asset",
    "atlas", "atom", "atomic", "attic", "audio", "author", "auto", "autumn",
    "avalanche", "avatar", "avenue", "award", "axis", "bacon", "badge", "baker",
    "balance", "balloon", "bamboo", "banana", "banner", "baron", "barrel", "beacon",
    "beauty", "beetle", "behalf", "behavior", "belief", "bench", "berry", "beyond",
    "binary", "biology", "bird", "bishop", "bitter", "blanket", "blast", "blaze",
    "bless", "blind", "bllink", "blitz", "block", "blonde", "blood", "blossom",
    "blueprint", "board", "boat", "boiler", "bolt", "bonus", "border", "botany",
    "bounce", "boundary", "brave", "breeze", "bridge", "bronze", "bubble", "budget"
]

def generate_passphrase(word_count: int = 4, separator: str = "-", capitalize: bool = True) -> str:
    """Generate a secure multi-word passphrase using cryptographic randomness."""
    words = [secrets.choice(WORDLIST) for _ in range(word_count)]
    if capitalize:
        words = [w.capitalize() for w in words]
    return separator.join(words)

def run():
    print(color.color_text("--- Diceware Passphrase Generator ---", COLOR))
    
    try:
        count = int(input("Enter number of words (e.g. 4, 5, 6 - default 4): ").strip() or "4")
    except ValueError:
        count = 4

    sep = input("Enter separator character (e.g. -, _, . - default '-'): ").strip()
    if not sep:
        sep = "-"

    cap_input = input("Capitalize words? (Y/n): ").strip().lower()
    cap = False if cap_input == 'n' else True

    passphrase = generate_passphrase(word_count=count, separator=sep, capitalize=cap)
    print(color.color_text(f"\n[+] Generated Passphrase:\n{passphrase}", color.GREEN))
