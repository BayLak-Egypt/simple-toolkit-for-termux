import urllib.request
import re
import color

DESCRIPTION = "Web Page HTML Forms Extractor Tool"
GROUP_ID = 5  # Scraper Tools
COLOR = color.BLUE

def extract_forms(url: str):
    """Extract and display HTML forms and their input fields from a web page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            # Find all form tags
            forms = re.findall(r'<form.*?>.*?</form>', html_content, re.IGNORECASE | re.DOTALL)
            
            print(color.color_text(f"\n[+] Found {len(forms)} form(s) on {url}:\n", color.GREEN))
            
            for index, form in enumerate(forms, start=1):
                # Extract action and method
                action_match = re.search(r'action=["\'](.*?)["\']', form, re.IGNORECASE)
                method_match = re.search(r'method=["\'](.*?)["\']', form, re.IGNORECASE)
                
                action = action_match.group(1) if action_match else "N/A"
                method = method_match.group(1).upper() if method_match else "GET"
                
                print(color.color_text(f"  [Form #{index}] Method: {method} | Action: {action}", color.CYAN))
                
                # Extract input fields inside the form
                inputs = re.findall(r'<input.*?>', form, re.IGNORECASE)
                if inputs:
                    print("    Inputs:")
                    for inp in inputs:
                        name_match = re.search(r'name=["\'](.*?)["\']', inp, re.IGNORECASE)
                        type_match = re.search(r'type=["\'](.*?)["\']', inp, re.IGNORECASE)
                        
                        inp_name = name_match.group(1) if name_match else "N/A"
                        inp_type = type_match.group(1) if type_match else "text"
                        
                        print(f"      - Type: {inp_type}, Name: {color.color_text(inp_name, color.YELLOW)}")
                else:
                    print("    Inputs: None found")
                print()

    except Exception as e:
        print(color.color_text(f"[!] Error extracting forms: {e}", color.RED))

def run():
    print(color.color_text("--- Web Page HTML Forms Extractor Tool ---", COLOR))
    
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not url:
        print(color.color_text("[!] URL cannot be empty.", color.RED))
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(color.color_text(f"\n[+] Scanning {url} for HTML forms...\n", color.GREEN))
    extract_forms(url)
