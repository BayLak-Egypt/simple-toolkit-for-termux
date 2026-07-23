import re
import unicodedata
import color

DESCRIPTION = "URL Slug & Clean Identifier Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_slug(text: str, separator: str = "-") -> str:
    """Convert any text/title into a clean, URL-friendly slug."""
    # Normalize unicode characters (remove accents/diacritics if possible)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and punctuation with separator
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', separator, text).strip(separator)
    
    return text

def run():
    print(color.color_text("--- URL Slug Generator ---", COLOR))
    
    text = input("Enter text or article title to slugify: ").strip()
    if not text:
        print(color.color_text("[!] Input text cannot be empty.", color.RED))
        return

    sep_choice = input("Select separator [1] Hyphen '-' (default) [2] Underscore '_': ").strip()
    separator = "_" if sep_choice == "2" else "-"

    slug = generate_slug(text, separator)

    print(color.color_text(f"\n[+] Generated Slug:\n", color.GREEN))
    print(f"  {slug}")
