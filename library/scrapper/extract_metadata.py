import urllib.request
import re
import color

DESCRIPTION = "Web Page Metadata Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_metadata(url: str):
    """Extract and display title, description, and meta tags from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract Title
            title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "N/A"
            
            print(color.color_text(f"\n[+] Page Title: {color.color_text(title, color.YELLOW)}", color.GREEN))
            
            # Extract Meta tags (description, keywords, author, etc.)
            meta_tags = re.findall(r'<meta\s+name=["\'](.*?)["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
            
            if meta_tags:
                print(color.color_text("\n[+] Meta Tags Found:", color.CYAN))
                for name, content in meta_tags:
                    print(f"  - {name}: {content}")
            else:
                print(color.color_text("\n[-] No standard meta name/content tags found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting metadata: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Metadata Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for metadata...\n", color.GREEN))
    extract_metadata(url)
