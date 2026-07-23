import urllib.request
import os
import color

DESCRIPTION = "Web Page Downloader Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def download_page(url: str, output_filename: str = "downloaded_page.html"):
    """Download a web page and save its HTML content to a local file."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        print(color.color_text(f"\n[+] Connecting to {url}...", color.CYAN))
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read()
            
            # Save to file
            with open(output_filename, 'wb') as f:
                f.write(html_content)
                
            file_size = os.path.getsize(output_filename)
            print(color.color_text(f"\n[+] Success! Page successfully downloaded.", color.GREEN))
            print(f"  - Saved as: {color.color_text(output_filename, color.YELLOW)}")
            print(f"  - File size: {color.color_text(f'{file_size} bytes', color.YELLOW)}")

    except Exception as e:
        print(color.color_text(f"[!] Error downloading page: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Downloader Tool ---", COLOR))
    
    url = input("Enter target URL to download (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    output_name = input("Enter output filename (default: downloaded_page.html): ").strip()
    if not output_name:
        output_name = "downloaded_page.html"
    elif not output_name.endswith(".html"):
        output_name += ".html"

    download_page(url, output_name)
