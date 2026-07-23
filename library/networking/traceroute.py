import socket
import struct
import time
import platform
import color

DESCRIPTION = "Network Traceroute Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def trace_route(dest_name: str, max_hops: int = 30) -> None:
    """Trace the route to a destination host using UDP packets with increasing TTL."""
    try:
        dest_addr = socket.gethostbyname(dest_name)
    except Exception as e:
        print(color.color_text(f"[!] Unable to resolve {dest_name}: {e}", color.RED))
        return

    print(color.color_text(f"\n[+] Tracing route to {dest_name} [{dest_addr}] with maximum {max_hops} hops:\n", color.GREEN))

    port = 33434
    
    for ttl in range(1, max_hops + 1):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.settimeout(2.0)
        
        try:
            recv_socket.bind(("", port))
        except Exception:
            # If binding raw socket fails due to permissions
            pass

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        start_time = time.time()
        try:
            send_socket.sendto(b"", (dest_addr, port))
            curr_addr = None
            curr_name = None
            
            while True:
                try:
                    data, curr_addr = recv_socket.recvfrom(512)
                    curr_addr = curr_addr[0]
                    try:
                        curr_name = socket.gethostbyaddr(curr_addr)[0]
                    except Exception:
                        curr_name = curr_addr
                    break
                except socket.timeout:
                    break
            
            elapsed = round((time.time() - start_time) * 1000, 2)
            
            if curr_addr:
                print(f"  {str(ttl).ljust(3)} : {color.color_text(f'{curr_name} [{curr_addr}]', color.YELLOW)}  {elapsed} ms")
                if curr_addr == dest_addr:
                    print(color.color_text(f"\n[+] Destination reached successfully at hop {ttl}.", color.CYAN))
                    break
            else:
                print(f"  {str(ttl).ljust(3)} : {color.color_text('*', color.RED)}  Request timed out")

        finally:
            send_socket.close()
            recv_socket.close()

def run():
    print(color.color_text("--- Network Traceroute ---", COLOR))
    
    if platform.system().lower() == "windows":
        print(color.color_text("[!] Note: Raw sockets for ICMP responses require Administrator privileges on Windows.", color.RED))

    target = input("Enter target domain or IP to trace: ").strip()
    if not target:
        print(color.color_text("[!] Target cannot be empty.", color.RED))
        return

    try:
        trace_route(target)
    except PermissionError:
        print(color.color_text("[!] Error: Administrator / Root privileges required to execute traceroute raw sockets.", color.RED))
    except Exception as e:
        print(color.color_text(f"[!] Error running traceroute: {e}", color.RED))
