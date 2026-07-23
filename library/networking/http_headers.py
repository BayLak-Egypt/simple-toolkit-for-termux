import urllib.request
import color

DESCRIPTION = "HTTP Headers & Status Inspector"
GROUP_ID = 1  # Network Tools Group
COLOR = color.MAGENTA

def run():
    print(color.color_text("--- HTTP Headers & Status Inspector ---", COLOR))
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    
    if not url:
        print(color.color_text("[!] No URL entered.", color.RED))
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Termux Utility)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            print(color.color_text(f"\n[+] Status Code: {response.status}", color.GREEN))
            print(color.color_text("\n--- Headers ---", color.WHITE))
            for header, value in response.getheaders():
                print(f"  {color.CYAN}{header}{color.RESET}: {value}")

    except Exception as e:
        print(color.color_text(f"\n[!] Failed to connect to website: {e}", color.RED))
