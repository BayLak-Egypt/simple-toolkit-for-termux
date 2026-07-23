import urllib.request
import color

DESCRIPTION = "HTTP Security Headers Analyzer"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def analyze_headers(url: str):
    """Fetch and check common security headers of a web server."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            resp_headers = response.headers
            
            print(color.color_text(f"\n[+] HTTP Status Code: {response.status} {response.reason}", color.CYAN))
            print(color.color_text("\n[+] Analyzing Security Headers:\n", color.GREEN))
            
            security_headers = [
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "X-XSS-Protection",
                "Referrer-Policy",
                "Permissions-Policy"
            ]
            
            for header in security_headers:
                val = resp_headers.get(header)
                if val:
                    print(f"  [FOUND]     {header}: {color.color_text(val, color.YELLOW)}")
                else:
                    print(f"  [MISSING]   {color.color_text(header, color.RED)}")
                    
            print(color.color_text("\n[+] General Headers:", color.CYAN))
            for gen_header in ["Server", "X-Powered-By", "Content-Type"]:
                val = resp_headers.get(gen_header)
                if val:
                    print(f"    - {gen_header}: {val}")

    except Exception as e:
        print(color.color_text(f"[!] Error analyzing headers: {e}", color.RED))

def run():
    print(color.color_text("--- HTTP Security Headers Analyzer ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Fetching headers from {url}...\n", color.GREEN))
    analyze_headers(url)
