import subprocess
import platform
import concurrent.futures
import ipaddress
import color

DESCRIPTION = "Local Network Ping Sweep Scanner"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def ping_host(ip: str) -> str:
    """Ping a single IP address to check if it's alive."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-w", "1000", ip] if platform.system().lower() == "windows" else ["ping", param, "1", "-W", "1", ip]
    
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return ip
    except Exception:
        pass
    return None

def run():
    print(color.color_text("--- Network Ping Sweep Scanner ---", COLOR))
    
    subnet_input = input("Enter network subnet to sweep (e.g., 192.168.1.0/24): ").strip()
    if not subnet_input:
        print(color.color_text("[!] Subnet cannot be empty.", color.RED))
        return

    try:
        network = ipaddress.ip_network(subnet_input, strict=False)
    except Exception as e:
        print(color.color_text(f"[!] Invalid network format: {e}", color.RED))
        return

    print(color.color_text(f"\n[+] Scanning network {network} for active hosts...\n", color.GREEN))
    
    active_hosts = []
    hosts_to_scan = [str(ip) for ip in network.hosts()]
    
    # Use ThreadPoolExecutor for fast concurrent pinging
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_host, ip): ip for ip in hosts_to_scan}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                active_hosts.append(result)
                print(color.color_text(f"  [+] Active Host Found: {result}", color.YELLOW))

    print(color.color_text(f"\n[+] Scan completed. Total active hosts found: {len(active_hosts)}", color.CYAN))
