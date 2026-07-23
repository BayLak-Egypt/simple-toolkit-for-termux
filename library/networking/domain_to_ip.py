import socket
import color  # Import color module

DESCRIPTION = "Domain to IP Converter"
GROUP_ID = 1
COLOR = color.CYAN  # 🎨 Tool color specification

def run():
    print(color.color_text("\n--- Domain to IP Converter ---", COLOR))
    domain = input("Enter domain name: ").strip()
    if not domain:
        print(color.color_text("[!] No domain entered.", color.RED))
        return

    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

    try:
        ip = socket.gethostbyname(domain)
        print(color.color_text(f"[+] The IP for {domain} is: {ip}", color.GREEN))
    except socket.gaierror:
        print(color.color_text(f"[!] Could not resolve IP for {domain}", color.RED))
