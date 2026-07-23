import socket
import struct
import color

DESCRIPTION = "SMB Share Enumeration Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def check_smb_port(target_ip: str, port: int = 445) -> bool:
    """Check if SMB port (445 or 139) is open."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex((target_ip, port))
        s.close()
        return result == 0
    except Exception:
        return False

def run():
    print(color.color_text("--- SMB Share Enumeration Tool ---", COLOR))
    print(color.color_text("[!] Note: This tool checks SMB service availability and standard ports.\n", color.CYAN))
    
    target = input("Enter target IP address or domain: ").strip()
    if not target:
        print(color.color_text("[!] Target cannot be empty.", color.RED))
        return

    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        print(color.color_text(f"[!] Could not resolve target: {e}", color.RED))
        return

    print(color.color_text(f"\n[+] Checking SMB ports on {target_ip}...\n", color.GREEN))

    ports = [445, 139]
    open_ports = []

    for port in ports:
        if check_smb_port(target_ip, port):
            open_ports.append(port)
            print(color.color_text(f"  [+] Port {port} (SMB): OPEN", color.YELLOW))
        else:
            print(f"  [-] Port {port} (SMB): CLOSED")

    if open_ports:
        print(color.color_text(f"\n[+] SMB service detected active on {target_ip}.", color.GREEN))
        print(color.color_text("[*] Recommendation: Use specialized enumeration tools like enum4linux or smbclient for deep share discovery.", color.CYAN))
    else:
        print(color.color_text(f"\n[-] No active SMB ports found on {target_ip}.", color.RED))
