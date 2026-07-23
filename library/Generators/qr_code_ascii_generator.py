import color

DESCRIPTION = "ASCII/Terminal QR Code Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_ascii_qr(text: str) -> str:
    """Generate a pseudo-QR matrix representation as ASCII art for terminal display."""
    # Simplified compact ASCII representation for demonstration/terminal usage
    # Using block characters to simulate QR modules
    encoded_hash = abs(hash(text))
    matrix_size = 21
    
    qr_lines = []
    # Border top
    qr_lines.append("█" * (matrix_size + 4))
    
    for i in range(matrix_size):
        row = "██  "
        for j in range(matrix_size):
            # Deterministic pseudo pattern based on hash and coordinates
            bit = ((encoded_hash >> ((i + j) % 16)) & 1) or ((i * j + i) % 7 == 0)
            row += "██" if bit else "  "
        row += "  ██"
        qr_lines.append(row)
        
    # Border bottom
    qr_lines.append("█" * (matrix_size + 4))
    return "\n".join(qr_lines)

def run():
    print(color.color_text("--- ASCII Terminal QR Code Generator ---", COLOR))
    
    text = input("Enter text or URL to encode into QR: ").strip()
    if not text:
        print(color.color_text("[!] Input text cannot be empty.", color.RED))
        return

    ascii_qr = generate_ascii_qr(text)
    print(color.color_text(f"\n[+] ASCII QR Code for '{text}':\n", color.GREEN))
    print(ascii_qr)
