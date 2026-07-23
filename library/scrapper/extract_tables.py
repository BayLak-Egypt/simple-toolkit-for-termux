import urllib.request
import re
import color

DESCRIPTION = "Web Page HTML Tables Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_tables(url: str):
    """Extract and display HTML tables and their rows/columns from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Find all table tags
            tables = re.findall(r'<table.*?>(.*?)</table>', html_content, re.IGNORECASE | re.DOTALL)
            
            print(color.color_text(f"\n[+] Found {len(tables)} table(s) on {url}:\n", color.GREEN))
            
            for index, table_content in enumerate(tables, start=1):
                rows = re.findall(r'<tr.*?>(.*?)</tr>', table_content, re.IGNORECASE | re.DOTALL)
                print(color.color_text(f"  [Table #{index}] Contains {len(rows)} row(s)", color.CYAN))
                
                for r_idx, row in enumerate(rows[:5], start=1):  # Show first 5 rows as a preview
                    cells = re.findall(r'<(?:th|td).*?>(.*?)</(?:th|td)>', row, re.IGNORECASE | re.DOTALL)
                    # Clean simple HTML tags inside cells
                    clean_cells = [re.sub(r'<.*?>', '', c).strip() for c in cells]
                    print(f"      Row {r_idx}: {color.color_text(' | '.join(clean_cells), color.YELLOW)}")
                
                if len(rows) > 5:
                    print(f"      ... and {len(rows) - 5} more row(s).")
                print()

    except Exception as e:
        print(color.color_text(f"[!] Error extracting tables: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page HTML Tables Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for HTML tables...\n", color.GREEN))
    extract_tables(url)
