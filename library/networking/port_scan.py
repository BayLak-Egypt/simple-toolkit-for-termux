import socket
import color

DESCRIPTION = "IP Basic Port Scanner"
GROUP_ID = 2
COLOR = color.YELLOW

def run():
    print(color.color_text("--- Port Scanner Tool ---", COLOR))
    target = input("Enter IP address or domain: ").strip()
    if not target:
        print(color.color_text("[!] No target entered.", color.RED))
        return

    common_ports = [21, 22, 80, 443, 8080]
    
    print(color.color_text(f"\n[i] Scanning common ports for {target}...\n", color.WHITE))
    
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target, port))
        if result == 0:
            print(color.color_text(f"  [+] Port {port:<5} : Open", color.GREEN))
        else:
            print(color.color_text(f"  [-] Port {port:<5} : Closed", color.RED))
        s.close()
