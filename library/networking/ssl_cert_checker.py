import ssl
import socket
import datetime
import color

DESCRIPTION = "SSL/TLS Certificate Analyzer"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def check_ssl_certificate(hostname: str, port: int = 443):
    """Retrieve and analyze SSL/TLS certificate details for a domain."""
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                print(color.color_text(f"\n[+] Successfully connected to {hostname}:{port} via SSL/TLS.\n", color.GREEN))
                
                # Subject details
                subject = dict(x[0] for x in cert.get('subject', []))
                common_name = subject.get('commonName', 'N/A')
                organization = subject.get('organizationName', 'N/A')
                
                # Issuer details
                issuer = dict(x[0] for x in cert.get('issuer', []))
                issuer_name = issuer.get('commonName', 'N/A')
                
                # Validity dates
                not_before = cert.get('notBefore', '')
                not_after = cert.get('notAfter', '')
                
                print(color.color_text("  [+] Certificate Details:", color.CYAN))
                print(f"      - Common Name (CN): {color.color_text(common_name, color.YELLOW)}")
                print(f"      - Organization (O): {organization}")
                print(f"      - Issuer: {issuer_name}")
                print(f"      - Valid From: {not_before}")
                print(f"      - Valid Until: {not_after}")
                
                # Expiry check
                try:
                    expiry_date = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    days_left = (expiry_date - datetime.datetime.utcnow()).days
                    
                    if days_left > 0:
                        print(color.color_text(f"      - Status: VALID ({days_left} days remaining)", color.GREEN))
                    else:
                        print(color.color_text(f"      - Status: EXPIRED ({abs(days_left)} days ago)", color.RED))
                except Exception:
                    pass
                
                # SAN (Subject Alternative Names)
                sans = cert.get('subjectAltName', [])
                if sans:
                    print(color.color_text("\n  [+] Subject Alternative Names (SAN):", color.CYAN))
                    for alt_type, alt_val in sans:
                        print(f"      - {alt_type}: {alt_val}")

    except socket.gaierror as e:
        print(color.color_text(f"[!] Host resolution error: {e}", color.RED))
    except ssl.SSLError as e:
        print(color.color_text(f"[!] SSL/TLS Error: {e}", color.RED))
    except Exception as e:
        print(color.color_text(f"[!] Error connecting to target: {e}", color.RED))

def run():
    print(color.color_text("--- SSL/TLS Certificate Analyzer ---", COLOR))
    
    target = input("Enter target domain (e.g., example.com): ").strip()
    if not target:
        print(color.color_text("[!] Domain cannot be empty.", color.RED))
        return

    # Clean domain input if URL was provided
    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("//")[-1].split("/")[0]

    try:
        port = int(input("Enter port (default 443): ").strip() or "443")
    except ValueError:
        port = 443

    print(color.color_text(f"\n[+] Analyzing SSL certificate for {target}...\n", color.GREEN))
    check_ssl_certificate(target, port)
