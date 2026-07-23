import urllib.request
import re
import color

DESCRIPTION = "Web Page Video Stream Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_videos(url: str):
    """Extract and display video file links and video tags from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract video src attributes, source tags, and direct video file links (mp4, webm, ogv, mov, etc.)
            video_tags = re.findall(r'<video[^>]+src=["\'](.*?)["\']', html_content, re.IGNORECASE)
            source_tags = re.findall(r'<source[^>]+src=["\'](.*?\.(?:mp4|webm|ogv|mov|m4v))["\']', html_content, re.IGNORECASE)
            direct_links = re.findall(r'href=["\'](.*?\.(?:mp4|webm|ogv|mov|m4v))["\']', html_content, re.IGNORECASE)
            
            all_videos = sorted(set(list(video_tags) + list(source_tags) + list(direct_links)))
            
            print(color.color_text(f"\n[+] Found {len(all_videos)} unique video stream(s)/file(s) on {url}:\n", color.GREEN))
            
            if all_videos:
                for video in all_videos:
                    print(f"  - {color.color_text(video, color.YELLOW)}")
            else:
                print(color.color_text("[-] No direct video files found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting video links: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Video Stream Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for video streams...\n", color.GREEN))
    extract_videos(url)
