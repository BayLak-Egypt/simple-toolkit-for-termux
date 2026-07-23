import math
import color

DESCRIPTION = "Shannon Entropy Calculator for Data/Files"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon Entropy of a bytes object (0.0 to 8.0)."""
    if not data:
        return 0.0

    entropy = 0.0
    length = len(data)
    
    # Count occurrence of each byte
    counts = {}
    for byte in data:
        counts[byte] = counts.get(byte, 0) + 1

    # Calculate p * log2(p)
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy

def interpret_entropy(entropy: float) -> str:
    """Provide security context based on entropy score."""
    if entropy < 3.5:
        return "Low Entropy (Plain text, repetitive data, or simple structured code)"
    elif entropy < 6.0:
        return "Medium Entropy (Normal source code, executable code, or structured binary)"
    elif entropy < 7.5:
        return "High Entropy (Compressed data, packed code, or obfuscated text)"
    else:
        return "Very High Entropy (~8.0) (Strongly encrypted data or high-quality randomness)"

def run():
    print(color.color_text("--- Shannon Entropy Calculator ---", COLOR))
    print(" [1] Calculate entropy of input text")
    print(" [2] Calculate entropy of a file")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        text = input("Enter text/string: ").strip()
        if not text:
            print(color.color_text("[!] Text cannot be empty.", color.RED))
            return
        
        raw_bytes = text.encode('utf-8')
        entropy = calculate_entropy(raw_bytes)
        
        print(color.color_text(f"\n[+] Length: {len(raw_bytes)} bytes", color.CYAN))
        print(color.color_text(f"[+] Shannon Entropy: {entropy:.4f} / 8.0000", color.GREEN))
        print(color.color_text(f"[+] Assessment: {interpret_entropy(entropy)}", color.YELLOW))

    elif choice == "2":
        filepath = input("Enter file path: ").strip()
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            entropy = calculate_entropy(data)
            print(color.color_text(f"\n[+] File Size: {len(data)} bytes", color.CYAN))
            print(color.color_text(f"[+] Shannon Entropy: {entropy:.4f} / 8.0000", color.GREEN))
            print(color.color_text(f"[+] Assessment: {interpret_entropy(entropy)}", color.YELLOW))
        except FileNotFoundError:
            print(color.color_text("\n[!] File not found.", color.RED))
        except Exception as e:
            print(color.color_text(f"\n[!] Error reading file: {e}", color.RED))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
