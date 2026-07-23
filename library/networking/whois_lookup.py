import urllib.request
import json
import color

DESCRIPTION = "WHOIS Domain Registration Lookup"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def query_whois(domain: str) -> str:
    """Query basic WHOIS/registration info using public RDAP/API service."""
    url = f"https://rdap.org/domain/{urllib.parse.quote(domain)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Extract common fields safely
            handle = data.get('handle', 'N/A')
            ldh_name = data.get('ldhName', domain)
            status = ", ".join(data.get('status', ['N/A']))
            
            events = data.get('events', [])
            dates = {}
            for event in events:
                dates[event.get('eventAction')] = event.get('eventDate')
                
            output = f"Domain Name: {ldh_name}\n"
            output += f"Handle: {handle}\n"
            output += f"Status: {status}\n"
            if 'registration' in dates:
                output += f"Registered On: {dates['registration']}\n"
            if 'expiration' in dates:
                output += f"Expires On: {dates['expiration']}\n"
            if 'last changed' in dates:
                output += f"Last Updated: {dates['last changed']}\n"
                
            return output
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "Domain registration info not found."
        return f"HTTP Error: {e.code}"
    except Exception as e:
        return f"Error: {str(e)}"

def run():
    print(color.color_text("--- WHOIS Domain Lookup ---", COLOR))
    
    domain = input("Enter domain name (e.g., example.com): ").strip()
    if not domain:
        print(color.color_text("[!] Domain name cannot be empty.", color.RED))
        return

    print(color.color_text(f"\n[+] Querying WHOIS data for {domain}...\n", color.GREEN))
    result = query_whois(domain)
    
    print(color.color_text(result, color.YELLOW))
