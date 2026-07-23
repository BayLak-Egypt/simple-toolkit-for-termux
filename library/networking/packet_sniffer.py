import socket
import struct
import platform
import color

DESCRIPTION = "Basic Raw Socket Packet Sniffer"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def run():
    print(color.color_text("--- Basic Network Packet Sniffer ---", COLOR))
    
    # Raw sockets require administrative/root privileges
    if platform.system().lower() == "windows":
        print(color.color_text("[!] Note: Windows requires administrator privileges and specific interface binding for raw sockets.", color.RED))
        host = socket.gethostbyname(socket.gethostname())
    else:
        host = "0.0.0.0"

    print(color.color_text(f"[+] Binding to host: {host}", color.GREEN))
    print(color.color_text("[*] Listening for incoming packets (Capturing first 5 packets)...\n", color.CYAN))

    try:
        # Create raw socket
        if platform.system().lower() == "windows":
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            s.bind((host, 0))
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

        packet_count = 0
        while packet_count < 5:
            raw_data, addr = s.recvfrom(65535)
            packet_count += 1
            print(color.color_text(f"  [+] Packet #{packet_count} received from Source IP: {addr[0]} (Size: {len(raw_data)} bytes)", color.YELLOW))

        if platform.system().lower() == "windows":
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        s.close()
        print(color.color_text("\n[+] Packet sniffing session finished successfully.", color.GREEN))

    except PermissionError:
        print(color.color_text("[!] Error: Raw sockets require Administrator / Root privileges. Please run the script as administrator.", color.RED))
    except Exception as e:
        print(color.color_text(f"[!] Error running packet sniffer: {e}", color.RED))
