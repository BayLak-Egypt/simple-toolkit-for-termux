import socket
import color

DESCRIPTION = "Advanced DNS Records Lookup Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def get_dns_records(domain: str) -> dict:
    """Retrieve basic DNS information (IP resolution) using socket."""
    results = {}
    try:
        # Get IPv4 address
        ip_v4 = socket.gethostbyname(domain)
        results["A (IPv4)"] = ip_v4
    except Exception as e:
        results["A (IPv4)"] = f"Not found / Error: {e}"
        
    try:
        # Get extended info (IPv6 and aliases)
        addr_info = socket.getaddrinfo(domain, None)
        ipv6_addresses = set([item[4][0] for item in addr_info if ':' in item[4][0]])
        if ipv6_addresses:
            results["AAAA (IPv6)"] = list(ipv6_addresses)
    except Exception:
        pass
        
    return results

def run():
    print(color.color_text("--- DNS Records Lookup ---", COLOR))
    
    domain = input("Enter domain name (e.g., example.com): ").strip()
    if not domain:
        print(color.color_text("[!] Domain cannot be empty.", color.RED))
        return

    print(color.color_text(f"\n[+] Querying DNS records for {domain}...\n", color.GREEN))
    records = get_dns_records(domain)
    
    for record_type, value in records.items():
        print(f"  {record_type.ljust(15)} : {color.color_text(str(value), color.YELLOW)}")
