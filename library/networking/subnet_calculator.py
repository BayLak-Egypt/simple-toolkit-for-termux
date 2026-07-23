import ipaddress
import color

DESCRIPTION = "IPv4 Subnet Calculator & Network Analyzer"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def calculate_subnet(network_str: str) -> dict:
    """Calculate subnet details for a given IPv4 network or IP/CIDR."""
    try:
        net = ipaddress.ip_network(network_str, strict=False)
        return {
            "Network Address": str(net.network_address),
            "Netmask": str(net.netmask),
            "Broadcast Address": str(net.broadcast_address),
            "Total IP Addresses": net.num_addresses,
            "Usable Hosts": max(0, net.num_addresses - 2) if net.prefixlen < 31 else net.num_addresses,
            "Wildcard Mask": str(net.hostmask),
            "IP Version": f"IPv{net.version}"
        }
    except Exception as e:
        return {"error": str(e)}

def run():
    print(color.color_text("--- IPv4 Subnet Calculator ---", COLOR))
    
    net_input = input("Enter IP and Subnet (e.g., 192.168.1.0/24): ").strip()
    if not net_input:
        print(color.color_text("[!] Input cannot be empty.", color.RED))
        return

    print(color.color_text(f"\n[+] Analyzing network {net_input}...\n", color.GREEN))
    result = calculate_subnet(net_input)
    
    if "error" in result:
        print(color.color_text(f"[!] Invalid network format: {result['error']}", color.RED))
        return

    for key, value in result.items():
        print(f"  {key.ljust(20)} : {color.color_text(str(value), color.YELLOW)}")
