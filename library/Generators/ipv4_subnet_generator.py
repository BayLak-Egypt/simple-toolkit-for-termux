import ipaddress
import color

DESCRIPTION = "IPv4 Subnet & CIDR Calculator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def calculate_subnet(cidr_notation: str) -> dict:
    """Calculate subnet details given an IPv4 CIDR string (e.g. 192.168.1.0/24)."""
    try:
        network = ipaddress.ip_network(cidr_notation, strict=False)
        
        hosts = list(network.hosts())
        first_host = str(hosts[0]) if hosts else "N/A"
        last_host = str(hosts[-1]) if hosts else "N/A"
        
        return {
            "Network Address": str(network.network_address),
            "Netmask": str(network.netmask),
            "Wildcard Mask": str(network.hostmask),
            "Broadcast Address": str(network.broadcast_address),
            "Total IP Addresses": network.num_addresses,
            "Usable Hosts": len(hosts),
            "First Usable Host": first_host,
            "Last Usable Host": last_host,
            "IP Version": network.version
        }
    except ValueError as e:
        return {"error": str(e)}

def run():
    print(color.color_text("--- IPv4 Subnet & CIDR Calculator ---", COLOR))
    
    cidr_input = input("Enter IPv4 CIDR notation (e.g., 192.168.1.0/24, default 10.0.0.0/24): ").strip() or "10.0.0.0/24"
    
    result = calculate_subnet(cidr_input)
    
    if "error" in result:
        print(color.color_text(f"[!] Invalid CIDR input: {result['error']}", color.RED))
        return

    print(color.color_text(f"\n[+] Subnet Details for {cidr_input}:\n", color.GREEN))
    for key, value in result.items():
        print(f"  {key:<20}: {value}")
