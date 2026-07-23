import subprocess
import platform
import color

DESCRIPTION = "Local ARP Table & Cache Viewer"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def get_arp_table():
    """Retrieve the local ARP cache table using system commands."""
    os_type = platform.system().lower()
    if os_type == "windows":
        command = ["arp", "-a"]
    else:
        command = ["arp", "-n"]
        
    try:
        output = subprocess.check_output(command, encoding="utf-8", errors="ignore")
        return output
    except Exception as e:
        return f"Error retrieving ARP table: {e}"

def run():
    print(color.color_text("--- Local ARP Table Viewer ---", COLOR))
    print(color.color_text("\n[+] Fetching local network ARP cache entries...\n", color.GREEN))

    result = get_arp_table()
    print(color.color_text(result, color.YELLOW))
