import urllib.request
import re
import color

DESCRIPTION = "Web Page Document Links Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_documents(url: str):
    """Extract and display document and archive file links from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract href links ending with common document and archive extensions
            doc_extensions = r'(?:pdf|doc|docx|xls|xlsx|ppt|pptx|txt|csv|zip|rar|tar|gz|7z)'
            doc_links = re.findall(rf'href=["\'](.*?\.{doc_extensions})["\']', html_content, re.IGNORECASE)
            
            unique_docs = sorted(set(doc_links))
            
            print(color.color_text(f"\n[+] Found {len(unique_docs)} unique document/archive link(s) on {url}:\n", color.GREEN))
            
            if unique_docs:
                for doc in unique_docs:
                    print(f"  - {color.color_text(doc, color.YELLOW)}")
            else:
                print(color.color_text("[-] No document or archive links found.", color.RED))

    except Exception as e:
        print(color.color_text(f"[!] Error extracting document links: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page Document Links Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for documents and archives...\n", color.GREEN))
    extract_documents(url)
