import urllib.request
import re
import color

DESCRIPTION = "Web Page Audio Stream Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_audio(url: str):
    """Extract and display audio file links and audio tags from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract audio src attributes and direct audio file links (mp3, wav, ogg, m4a, etc.)
            audio_tags = re.findall(r'<audio[^>]+src=["\'](.*?)["\']', html_content, re.IGNORECASE)
            source_tags = re.findall(r'<source[^>]+src=["\'](.*?\.(?:mp3|wav|ogg|m4a|aac))["\']', html_content, re.IGNORECASE)
            direct_links = re.findall(r'href=["\'](.*?\.(?:mp3|wav|ogg|m4a|aac))["\']', html_content, re.IGNORECASE)
            
            all_audio = sorted(set(list(audio_tags) + list(source_tags) + list(direct_links)))
            
            print(color.color_text(f"\n[+] Found {len(all_audio)} unique audio stream(s)/file(s) on {url}:\n", color.GREEN))
            
            if all_audio:
                for audio in all_audio:
                    print(f"  - {color.color_text(audio, color.YELLOW)}")
            else:
                print(color.color_text("[-] No direct audio files found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting audio links: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Audio Stream Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for audio streams...\n", color.GREEN))
    extract_audio(url)
