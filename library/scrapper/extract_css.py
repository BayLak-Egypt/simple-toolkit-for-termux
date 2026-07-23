import urllib.request
import re
import color

DESCRIPTION = "Web Page CSS Stylesheets Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_css(url: str):
    """Extract and display external CSS stylesheet links and inline styles from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract link tags pointing to stylesheets
            css_links = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\'](.*?)["\']', html_content, re.IGNORECASE)
            alt_css_links = re.findall(r'<link[^>]+href=["\'](.*?)["\'][^>]+rel=["\']stylesheet["\']', html_content, re.IGNORECASE)
            
            all_css = sorted(set(list(css_links) + list(alt_css_links)))
            
            print(color.color_text(f"\n[+] Found {len(all_css)} unique CSS stylesheet(s) on {url}:\n", color.GREEN))
            
            if all_css:
                for css in all_css:
                    print(f"  - {color.color_text(css, color.YELLOW)}")
            else:
                print(color.color_text("[-] No external CSS stylesheets found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting CSS links: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page CSS Stylesheets Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for CSS stylesheets...\n", color.GREEN))
    extract_css(url)
