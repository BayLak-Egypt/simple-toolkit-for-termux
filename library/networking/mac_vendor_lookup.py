import urllib.request
import json
import color

DESCRIPTION = "MAC Address Vendor & Manufacturer Lookup"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def lookup_mac(mac_address: str) -> str:
    """Lookup MAC address vendor using public API."""
    url = f"https://api.macvendors.com/{urllib.parse.quote(mac_address)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "Vendor not found for this MAC address."
        return f"HTTP Error: {e.code}"
    except Exception as e:
        return f"Error: {str(e)}"

def run():
    print(color.color_text("--- MAC Address Vendor Lookup ---", COLOR))
    
    mac = input("Enter MAC address (e.g., 00:11:22:33:44:55): ").strip()
    if not mac:
        print(color.color_text("[!] MAC address cannot be empty.", color.RED))
        return

    print(color.color_text(f"\n[+] Looking up vendor for {mac}...\n", color.GREEN))
    vendor = lookup_mac(mac)
    
    print(color.color_text(f"  [+] Manufacturer: {vendor}", color.YELLOW))
