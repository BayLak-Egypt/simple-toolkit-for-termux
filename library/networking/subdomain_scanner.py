import socket
import threading
import color

DESCRIPTION = "Subdomain Enumeration Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
    "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
    "ns", "blog", "pop3", "dev", "www1", "admin", "forum", "news", "vpn",
    "ns3", "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx",
    "static", "docs", "chat", "search", "shop", "file", "api", "dashboard"
]

def check_subdomain(domain: str, subdomain: str, results: list):
    """Check if a subdomain resolves to an IP address."""
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        results.append((full_domain, ip))
        print(color.color_text(f"  [FOUND]     {full_domain} -> {ip}", color.YELLOW))
    except socket.gaierror:
        pass
    except Exception:
        pass

def run():
    print(color.color_text("--- Subdomain Enumeration Tool ---", COLOR))
    
    domain = input("Enter base domain name (e.g., example.com): ").strip()
    if not domain:
        print(color.color_text("[!] Domain name cannot be empty.", color.RED))
        return

    # Clean domain if full URL was provided
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = domain.split("//")[-1].split("/")[0]

    print(color.color_text(f"\n[+] Scanning common subdomains for {domain}...\n", color.GREEN))

    results = []
    threads = []

    for sub in COMMON_SUBDOMAINS:
        t = threading.Thread(target=check_subdomain, args=(domain, sub, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(color.color_text(f"\n[+] Scan completed. Found {len(results)} active subdomains.", color.CYAN))
