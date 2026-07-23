import itertools
import color

DESCRIPTION = "Custom Wordlist & Pattern Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

SPECIAL_CHARS = ["!", "@", "#", "$", "123", "2024", "2025", "2026"]

def generate_wordlist(keywords: list, append_specials: bool = True) -> set:
    """Generate combinations of base keywords with casing and special suffixes."""
    results = set()

    for word in keywords:
        word = word.strip()
        if not word:
            continue

        # Variations of casing
        variations = {word, word.lower(), word.upper(), word.capitalize()}
        results.update(variations)

        if append_specials:
            for var in variations:
                for spec in SPECIAL_CHARS:
                    results.add(f"{var}{spec}")
                    results.add(f"{spec}{var}")

    return results

def run():
    print(color.color_text("--- Custom Wordlist Generator ---", COLOR))

    raw_input = input("Enter base keywords (separated by commas, e.g. admin, company, test): ").strip()
    if not raw_input:
        print(color.color_text("[!] Keywords cannot be empty.", color.RED))
        return

    keywords = [k.strip() for k in raw_input.split(",") if k.strip()]
    
    spec_choice = input("Append common numbers and symbols (!, @, #, 2026, etc.)? (Y/n): ").strip().lower()
    include_specials = False if spec_choice == 'n' else True

    words = generate_wordlist(keywords, include_specials)

    filename = input("Enter output filename to save (e.g. custom_wordlist.txt) or leave empty to display: ").strip()

    if filename:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for w in sorted(words):
                    f.write(w + "\n")
            print(color.color_text(f"\n[+] Saved {len(words)} unique words to '{filename}' successfully.", color.GREEN))
        except Exception as e:
            print(color.color_text(f"\n[!] Error saving file: {e}", color.RED))
    else:
        print(color.color_text(f"\n[+] Generated {len(words)} Words:", color.GREEN))
        for w in sorted(words):
            print(w)
