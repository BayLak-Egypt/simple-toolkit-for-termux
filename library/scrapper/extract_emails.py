import urllib.request
import re
import color

DESCRIPTION = "Web Page Email Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_emails(url: str):
    """Extract and display all email addresses from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Regex to find email addresses
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, html_content)
            unique_emails = sorted(set(emails))
            
            print(color.color_text(f"\n[+] Found {len(unique_emails)} unique email addresses on {url}:\n", color.GREEN))
            
            for email in unique_emails:
                print(f"  - {color.color_text(email, color.YELLOW)}")

    except Exception as e:
        print(color.color_text(f"[!] Error extracting emails: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Email Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for emails...\n", color.GREEN))
    extract_emails(url)
