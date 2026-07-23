import os
import platform
import color

DESCRIPTION = "Host Latency & Ping Check"
GROUP_ID = 2  # Inspection & Analysis Tools
COLOR = color.YELLOW

def run():
    print(color.color_text("--- Host Latency & Ping Check ---", COLOR))
    target = input("Enter IP or Domain: ").strip()
    
    if not target:
        print(color.color_text("[!] No target entered.", color.RED))
        return

    # Clean input
    target = target.replace("https://", "").replace("http://", "").split("/")[0]

    # Set ping count parameter based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = f"ping {param} 4 {target}"

    print(color.color_text(f"\n[i] Sending requests to {target}...\n", color.WHITE))
    response = os.system(command)
    
    if response == 0:
        print(color.color_text(f"\n[+] Connection to {target} successful!", color.GREEN))
    else:
        print(color.color_text(f"\n[!] Failed to connect to {target}.", color.RED))
