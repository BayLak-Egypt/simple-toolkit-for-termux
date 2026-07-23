import subprocess
import platform
import color

DESCRIPTION = "Network Packet Traceroute Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def trace_route(target: str, max_hops: int = 30) -> list:
    """Trace route to target host using system traceroute/tracert command."""
    param = "-n" if platform.system().lower() == "windows" else "-n"
    max_hop_param = "-h" if platform.system().lower() == "windows" else "-m"
    
    if platform.system().lower() == "windows":
        command = ["tracert", max_hop_param, str(max_hops), target]
    else:
        command = ["traceroute", "-m", str(max_hops), target]
        
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_lines = []
        for line in process.stdout:
            output_lines.append(line.strip())
        return output_lines
    except Exception as e:
        return [f"Error executing traceroute: {str(e)}"]

def run():
    print(color.color_text("--- Network Traceroute Tool ---", COLOR))
    
    target = input("Enter target domain or IP (e.g., example.com): ").strip()
    if not target:
        print(color.color_text("[!] Target cannot be empty.", color.RED))
        return

    try:
        max_hops = int(input("Enter max hops (default 20): ").strip() or "20")
        if max_hops < 1:
            max_hops = 20
    except ValueError:
        max_hops = 20

    print(color.color_text(f"\n[+] Tracing route to {target} (Max Hops: {max_hops})...\n", color.GREEN))
    results = trace_route(target, max_hops)
    
    for line in results:
        print(f"  {line}")
