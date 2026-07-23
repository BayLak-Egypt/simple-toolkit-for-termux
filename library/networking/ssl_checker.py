import ssl
import socket
import datetime
import color

DESCRIPTION = "SSL/TLS Certificate Expiry & Details Checker"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def check_ssl_certificate(hostname: str, port: int = 443) -> dict:
    """Fetch and parse SSL certificate details from a remote host."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Parse expiration date
                not_after_str = cert.get('notAfter')
                expiry_date = datetime.datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.datetime.utcnow()).days
                
                # Parse issuer and subject
                issuer = dict(x[0] for x in cert.get('issuer', []))
                subject = dict(x[0] for x in cert.get('subject', []))
                
                return {
                    "Subject": subject.get('commonName', 'N/A'),
                    "Issuer": issuer.get('organizationName', 'N/A'),
                    "Expires On": not_after_str,
                    "Days Remaining": days_left,
                    "Version": cert.get('version')
                }
    except Exception as e:
        return {"error": str(e)}

def run():
    print(color.color_text("--- SSL/TLS Certificate Checker ---", COLOR))
    
    hostname = input("Enter target hostname (e.g., github.com): ").strip()
    if not hostname:
        print(color.color_text("[!] Hostname cannot be empty.", color.RED))
        return

    print(color.color_text(f"\n[+] Checking SSL certificate for {hostname}...\n", color.GREEN))
    result = check_ssl_certificate(hostname)
    
    if "error" in result:
        print(color.color_text(f"[!] Error checking SSL certificate: {result['error']}", color.RED))
        return

    for key, value in result.items():
        val_color = color.YELLOW if key != "Days Remaining" or value > 30 else color.RED
        print(f"  {key.ljust(18)} : {color.color_text(str(value), val_color)}")
