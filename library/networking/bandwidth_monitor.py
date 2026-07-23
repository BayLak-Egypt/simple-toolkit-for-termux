import time
import psutil
import color

DESCRIPTION = "Network Interface Bandwidth & Traffic Monitor"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def get_network_stats():
    """Get total bytes sent and received across network interfaces."""
    return psutil.net_io_counters()

def run():
    print(color.color_text("--- Network Bandwidth Monitor ---", COLOR))
    print(color.color_text("[*] Press Ctrl+C to stop monitoring.\n", color.CYAN))

    try:
        # Initial stats
        net_start = get_network_stats()
        time_start = time.time()
        
        time.sleep(1)
        
        net_end = get_network_stats()
        time_end = time.time()
        
        time_diff = time_end - time_start
        
        sent_speed = (net_end.bytes_sent - net_start.bytes_sent) / time_diff
        recv_speed = (net_end.bytes_recv - net_start.bytes_recv) / time_diff
        
        print(color.color_text(f"  [+] Upload Speed   : {round(sent_speed / 1024, 2)} KB/s", color.YELLOW))
        print(color.color_text(f"  [+] Download Speed : {round(recv_speed / 1024, 2)} KB/s", color.YELLOW))
        print(color.color_text(f"  [+] Total Sent     : {round(net_end.bytes_sent / (1024 * 1024), 2)} MB", color.GREEN))
        print(color.color_text(f"  [+] Total Received : {round(net_end.bytes_recv / (1024 * 1024), 2)} MB", color.GREEN))
        
    except KeyboardInterrupt:
        print(color.color_text("\n[!] Monitoring stopped by user.", color.RED))
    except Exception as e:
        print(color.color_text(f"[!] Error monitoring bandwidth: {e}", color.RED))
