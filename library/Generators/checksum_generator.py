import zlib
import hashlib
import os
import color

DESCRIPTION = "File & Text Checksum (CRC32, Adler32, SHA256) Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def calculate_checksums(data: bytes) -> dict:
    """Calculate multiple integrity checksums for raw byte data."""
    crc32_val = zlib.crc32(data) & 0xFFFFFFFF
    adler32_val = zlib.adler32(data) & 0xFFFFFFFF
    sha256_val = hashlib.sha256(data).hexdigest()

    return {
        "CRC32 (Hex)": f"{crc32_val:08X}",
        "CRC32 (Dec)": str(crc32_val),
        "Adler-32 (Hex)": f"{adler32_val:08X}",
        "SHA-256": sha256_val
    }

def run():
    print(color.color_text("--- Checksum & Integrity Generator ---", COLOR))
    print(" [1] Calculate Checksum for Text Input")
    print(" [2] Calculate Checksum for File")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        text = input("Enter text string: ").strip()
        if not text:
            print(color.color_text("[!] Input text cannot be empty.", color.RED))
            return

        results = calculate_checksums(text.encode('utf-8'))
        print(color.color_text("\n[+] Text Checksum Results:\n", color.GREEN))
        for key, value in results.items():
            print(f"  {key:<16}: {value}")

    elif choice == "2":
        filepath = input("Enter full path to file: ").strip()
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            print(color.color_text("[!] File does not exist or is invalid.", color.RED))
            return

        try:
            with open(filepath, "rb") as f:
                content = f.read()

            results = calculate_checksums(content)
            print(color.color_text(f"\n[+] File Checksum Results ({os.path.basename(filepath)}):\n", color.GREEN))
            for key, value in results.items():
                print(f"  {key:<16}: {value}")

        except Exception as e:
            print(color.color_text(f"[!] Error reading file: {e}", color.RED))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
