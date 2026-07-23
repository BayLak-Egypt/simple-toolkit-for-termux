import urllib.request
import re
import color

DESCRIPTION = "Web Page JavaScript Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_scripts(url: str):
    """Extract and display external and inline JavaScript sources from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract script src attributes
            script_srcs = re.findall(r'<script[^>]+src=["\'](.*?)["\']', html_content, re.IGNORECASE)
            unique_srcs = sorted(set(script_srcs))
            
            print(color.color_text(f"\n[+] Found {len(unique_srcs)} external JavaScript file(s) on {url}:\n", color.GREEN))
            
            for src in unique_srcs:
                print(f"  - {color.color_text(src, color.YELLOW)}")

    except Exception as e:
        print(color.color_text(f"[!] Error extracting JavaScript sources: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page JavaScript Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for JavaScript links...\n", color.GREEN))
    extract_scripts(url)
