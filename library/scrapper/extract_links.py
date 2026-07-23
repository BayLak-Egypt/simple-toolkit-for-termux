import urllib.request
import re
import color

DESCRIPTION = "Extract Links from Webpage"
GROUP_ID = 1  # Network & Data Extraction Tools
COLOR = color.MAGENTA

def run():
    print(color.color_text("--- Webpage Link Extractor ---", COLOR))
    url = input("Enter website URL: ").strip()
    
    if not url:
        print(color.color_text("[!] No URL entered.", color.RED))
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Android; Mobile)'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Find all links using Regular Expressions
            links = set(re.findall(r'href=["\'](https?://[^\s"\']+)["\']', html))
            
            print(color.color_text(f"\n[+] Found {len(links)} unique link(s):\n", color.GREEN))
            for i, link in enumerate(links, 1):
                print(f"  [{i}] {color.CYAN}{link}{color.RESET}")

    except Exception as e:
        print(color.color_text(f"\n[!] Failed to extract links: {e}", color.RED))
