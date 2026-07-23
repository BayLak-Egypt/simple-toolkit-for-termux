import urllib.request
import re
import color

DESCRIPTION = "Web Page IFrames Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_iframes(url: str):
    """Extract and display iframe source URLs and embedded frames from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract iframe src attributes
            iframe_srcs = re.findall(r'<iframe[^>]+src=["\'](.*?)["\']', html_content, re.IGNORECASE)
            unique_iframes = sorted(set(iframe_srcs))
            
            print(color.color_text(f"\n[+] Found {len(unique_iframes)} unique iframe(s) on {url}:\n", color.GREEN))
            
            if unique_iframes:
                for iframe in unique_iframes:
                    print(f"  - {color.color_text(iframe, color.YELLOW)}")
            else:
                print(color.color_text("[-] No iframe elements found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting iframes: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page IFrames Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for iframes...\n", color.GREEN))
    extract_iframes(url)
