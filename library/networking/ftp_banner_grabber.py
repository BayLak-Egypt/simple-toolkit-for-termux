import socket
import color

DESCRIPTION = "FTP Service Banner Grabbing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def grab_ftp_banner(target_ip: str, port: int = 21) -> str:
    """Connect to FTP service and retrieve banner/version string."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target_ip, port))
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        return banner
    except Exception as e:
        return f"Error connecting to FTP: {e}"

def run():
    print(color.color_text("--- FTP Banner Grabbing Tool ---", COLOR))
    
    target = input("Enter target IP address or domain: ").strip()
    if not target:
        print(color.color_text("[!] Target cannot be empty.", color.RED))
        return

    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        print(color.color_text(f"[!] Could not resolve target: {e}", color.RED))
        return

    try:
        port = int(input("Enter FTP port (default 21): ").strip() or "21")
    except ValueError:
        port = 21

    print(color.color_text(f"\n[+] Connecting to {target_ip}:{port} to grab FTP banner...\n", color.GREEN))
    banner = grab_ftp_banner(target_ip, port)
    
    print(color.color_text(f"  [+] Banner Response:\n{banner}", color.YELLOW))
