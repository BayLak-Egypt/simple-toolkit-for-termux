import urllib.request
import re
import color

DESCRIPTION = "Web Page Social Media Links Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_social_links(url: str):
    """Extract and display social media profile links (Facebook, Twitter, LinkedIn, Instagram, etc.) from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Find all href links
            links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html_content, re.IGNORECASE)
            
            # Common social media domains filter
            social_domains = [
                'facebook.com', 'twitter.com', 'x.com', 'linkedin.com', 
                'instagram.com', 'youtube.com', 'github.com', 't.me', 
                'telegram.me', 'tiktok.com', 'pinterest.com', 'wa.me'
            ]
            
            found_socials = set()
            for link in links:
                for domain in social_domains:
                    if domain in link.lower():
                        found_socials.add(link)
                        
            unique_socials = sorted(found_socials)
            
            print(color.color_text(f"\n[+] Found {len(unique_socials)} unique social media link(s) on {url}:\n", color.GREEN))
            
            if unique_socials:
                for social in unique_socials:
                    print(f"  - {color.color_text(social, color.YELLOW)}")
            else:
                print(color.color_text("[-] No social media links found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting social links: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Social Media Links Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for social media profiles...\n", color.GREEN))
    extract_social_links(url)
