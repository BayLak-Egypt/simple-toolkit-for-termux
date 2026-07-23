import socket
import concurrent.futures
import color

DESCRIPTION = "Fast TCP Port Scanner"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def scan_port(target_ip: str, port: int) -> int:
    """Check if a specific TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None

def run():
    print(color.color_text("--- TCP Port Scanner ---", COLOR))
    
    target = input("Enter target IP or domain to scan: ").strip()
    if not target:
        print(color.color_text("[!] Target cannot be empty.", color.RED))
        return

    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        print(color.color_text(f"[!] Could not resolve target: {e}", color.RED))
        return

    print(color.color_text(f"\n[+] Scanning common ports on {target_ip}...\n", color.GREEN))
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in common_ports}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
                print(color.color_text(f"  [+] Port {port} is OPEN", color.YELLOW))

    print(color.color_text(f"\n[+] Scan completed. Total open ports found: {len(open_ports)}", color.CYAN))
