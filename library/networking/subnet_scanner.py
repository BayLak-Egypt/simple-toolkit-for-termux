import socket
import concurrent.futures
import ipaddress
import color

DESCRIPTION = "Subnet Host & Service Discovery Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def check_host_port(ip: str, port: int) -> tuple:
    """Check if a specific port is open on an IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((str(ip), port)) == 0:
                return (str(ip), port)
    except Exception:
        pass
    return None

def run():
    print(color.color_text("--- Subnet Service Discovery ---", COLOR))
    
    subnet_input = input("Enter subnet to scan (e.g., 192.168.1.0/24): ").strip()
    if not subnet_input:
        print(color.color_text("[!] Subnet cannot be empty.", color.RED))
        return

    try:
        network = ipaddress.ip_network(subnet_input, strict=False)
    except Exception as e:
        print(color.color_text(f"[!] Invalid subnet format: {e}", color.RED))
        return

    # Targeting common administrative/web ports
    target_ports = [80, 443, 22, 445]
    print(color.color_text(f"\n[+] Scanning {network} for active services on ports {target_ports}...\n", color.GREEN))

    tasks = []
    for ip in network.hosts():
        for port in target_ports:
            tasks.append((ip, port))

    found_services = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_host_port, ip, port): (ip, port) for ip, port in tasks}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                ip_addr, port = res
                found_services.append(res)
                print(color.color_text(f"  [+] Host {ip_addr} -> Port {port} OPEN", color.YELLOW))

    print(color.color_text(f"\n[+] Discovery completed. Total open services found: {len(found_services)}", color.CYAN))
