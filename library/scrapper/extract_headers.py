import urllib.request
import color

DESCRIPTION = "Web Page HTTP Headers Inspector Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_headers(url: str):
    """Retrieve and display HTTP response headers from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            print(color.color_text(f"\n[+] HTTP Response Status: {response.status} {response.reason}\n", color.GREEN))
            print(color.color_text("  [+] Response Headers:", color.CYAN))
            
            for header, value in response.headers.items():
                print(f"      - {color.color_text(header, color.YELLOW)}: {value}")

    except Exception as e:
        print(color.color_text(f"[!] Error retrieving headers: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page HTTP Headers Inspector Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Fetching HTTP headers for {url}...\n", color.GREEN))
    extract_headers(url)
