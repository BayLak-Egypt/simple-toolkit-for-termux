import psutil
import color

DESCRIPTION = "Network Interfaces & IP Configuration Viewer"
GROUP_ID = 2  # Networking Tools
COLOR = color.BLUE

def run():
    print(color.color_text("--- Network Interfaces Configuration ---", COLOR))
    print(color.color_text("\n[+] Fetching active network interfaces and IP addresses...\n", color.GREEN))

    try:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for interface_name, addresses in interfaces.items():
            is_up = stats[interface_name].isup if interface_name in stats else False
            status_color = color.GREEN if is_up else color.RED
            status_text = "UP" if is_up else "DOWN"
            
            print(f"  Interface: {color.color_text(interface_name, color.CYAN)} [{color.color_text(status_text, status_color)}]")
            
            for addr in addresses:
                family = str(addr.family).split('.')[-1]
                print(f"    - Family: {family.ljust(6)} | IP: {color.color_text(addr.address, color.YELLOW)}")
                if addr.netmask:
                    print(f"      Netmask: {addr.netmask}")
                if addr.broadcast:
                    print(f"      Broadcast: {addr.broadcast}")
            print("-" * 40)

    except Exception as e:
        print(color.color_text(f"[!] Error retrieving network interfaces: {e}", color.RED))
