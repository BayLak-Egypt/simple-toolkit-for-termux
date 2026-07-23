import ipaddress
import color

DESCRIPTION = "IPv4 Subnet & Range Calculator Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def calculate_subnet(ip_str: str, netmask_str: str) -> dict:
    """Calculate subnet details from IP and CIDR/Netmask."""
    ip_net = ipaddress.IPv4Network(f"{ip_str}/{netmask_str}", strict=False)
    
    hosts = list(ip_net.hosts())
    first_host = str(hosts[0]) if hosts else "N/A"
    last_host = str(hosts[-1]) if hosts else "N/A"

    return {
        "Network Address": str(ip_net.network_address),
        "Broadcast Address": str(ip_net.broadcast_address),
        "Netmask": str(ip_net.netmask),
        "Wildcard Mask": str(ip_net.hostmask),
        "CIDR Notation": f"/{ip_net.prefixlen}",
        "Total Addresses": ip_net.num_addresses,
        "Usable Hosts": len(hosts),
        "Usable IP Range": f"{first_host} - {last_host}"
    }

def run():
    print(color.color_text("--- IPv4 Subnet Calculator Generator ---", COLOR))
    
    ip_input = input("Enter IP Address (e.g. 192.168.1.50): ").strip() or "192.168.1.1"
    mask_input = input("Enter Subnet Mask or CIDR Prefix (e.g. 24 or 255.255.255.0): ").strip() or "24"

    try:
        details = calculate_subnet(ip_input, mask_input)
        print(color.color_text("\n[+] Subnet Calculation Results:\n", color.GREEN))
        for key, value in details.items():
            print(f"  {key:<20}: {value}")
            
    except Exception as e:
        print(color.color_text(f"\n[!] Invalid IP or Subnet Mask: {e}", color.RED))
