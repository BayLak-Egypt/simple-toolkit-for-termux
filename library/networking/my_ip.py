import urllib.request
import json
import color

DESCRIPTION = "Check Public IP Address"
GROUP_ID = 1  # Network Tools Group
COLOR = color.CYAN

def run():
    print(color.color_text("--- Public IP Checker ---", COLOR))
    try:
        url = "https://api.ipify.org?format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(color.color_text(f"\n[+] Your Public IP Address is: {data['ip']}", color.GREEN))
    except Exception as e:
        print(color.color_text(f"\n[!] Error fetching IP address: {e}", color.RED))
