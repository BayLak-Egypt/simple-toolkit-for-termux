import socket
import color

DESCRIPTION = "SMTP User Enumeration Tool"
GROUP_ID = 1  # Networking Tools
COLOR = color.BLUE

def check_smtp_user(target_ip: str, port: int, username: str) -> str:
    """Check if a username exists using VRFY, EXPN, or RCPT TO commands."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target_ip, port))
        banner = s.recv(1024).decode('utf-8', errors='ignore')
        
        # Send HELO command
        s.send(b"HELO scanner.local\r\n")
        s.recv(1024)
        
        # Try VRFY command
        s.send(f"VRFY {username}\r\n".encode())
        response = s.recv(1024).decode('utf-8', errors='ignore')
        s.send(b"QUIT\r\n")
        s.close()
        
        return response.strip()
    except Exception as e:
        return f"Error: {e}"

def run():
    print(color.color_text("--- SMTP User Enumeration Tool ---", COLOR))
    
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
        port = int(input("Enter SMTP port (default 25): ").strip() or "25")
    except ValueError:
        port = 25

    username = input("Enter username to check (e.g., admin, root, support): ").strip()
    if not username:
        print(color.color_text("[!] Username cannot be empty.", color.RED))
        return

    print(color.color_text(f"\n[+] Querying SMTP server at {target_ip}:{port} for user '{username}'...\n", color.GREEN))
    result = check_smtp_user(target_ip, port, username)
    
    print(color.color_text(f"  [+] Server Response:\n{result}", color.YELLOW))
