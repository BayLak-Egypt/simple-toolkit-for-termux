import subprocess
import platform
import color

DESCRIPTION = "Wi-Fi Networks Scanner & Inspector"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def scan_wifi_windows():
    """Scan available Wi-Fi networks on Windows using netsh."""
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], encoding="utf-8", errors="ignore")
        return output
    except Exception as e:
        return f"Error scanning Wi-Fi: {e}"

def scan_wifi_linux():
    """Scan available Wi-Fi networks on Linux using nmcli or iwlist."""
    try:
        output = subprocess.check_output(["nmcli", "-f", "SSID,BSSID,SIGNAL,SECURITY", "device", "wifi"], encoding="utf-8", errors="ignore")
        return output
    except Exception as e:
        return f"Error scanning Wi-Fi (nmcli might not be installed): {e}"

def run():
    print(color.color_text("--- Wi-Fi Networks Scanner ---", COLOR))
    
    os_type = platform.system().lower()
    print(color.color_text(f"\n[+] Scanning nearby wireless networks for operating system: {os_type.capitalize()}...\n", color.GREEN))

    if os_type == "windows":
        result = scan_wifi_windows()
        print(color.color_text(result, color.YELLOW))
    elif os_type == "linux":
        result = scan_wifi_linux()
        print(color.color_text(result, color.YELLOW))
    else:
        print(color.color_text("[!] Wi-Fi scanning is not supported on this operating system by this tool.", color.RED))
