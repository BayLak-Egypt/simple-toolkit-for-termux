import urllib.request
import re
import color

DESCRIPTION = "Web Page Image Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_images(url: str):
    """Extract and display all image links from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Regex to find img src tags
            images = re.findall(r'<img[^>]+src=["\'](.*?)["\']', html_content, re.IGNORECASE)
            unique_images = sorted(set(images))
            
            print(color.color_text(f"\n[+] Found {len(unique_images)} unique images on {url}:\n", color.GREEN))
            
            for img in unique_images:
                print(f"  - {color.color_text(img, color.YELLOW)}")

    except Exception as e:
        print(color.color_text(f"[!] Error extracting images: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Image Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for images...\n", color.GREEN))
    extract_images(url)
