import urllib.request
import re
import color

DESCRIPTION = "Web Page Phone Number Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_phones(url: str):
    """Extract and display all phone numbers from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Regex to find common phone number formats
            phone_pattern = r'\+?[0-9][0-9()\-\s\.]{7,}[0-9]'
            phones = re.findall(phone_pattern, html_content)
            
            # Clean up and filter results
            cleaned_phones = [p.strip() for p in phones if len(p.strip()) >= 8]
            unique_phones = sorted(set(cleaned_phones))
            
            print(color.color_text(f"\n[+] Found {len(unique_phones)} potential phone numbers on {url}:\n", color.GREEN))
            
            for phone in unique_phones:
                print(f"  - {color.color_text(phone, color.YELLOW)}")

    except Exception as e:
        print(color.color_text(f"[!] Error extracting phone numbers: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Phone Number Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for phone numbers...\n", color.GREEN))
    extract_phones(url)
