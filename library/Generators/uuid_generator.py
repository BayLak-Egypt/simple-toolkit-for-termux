import uuid
import secrets
import time
import color

DESCRIPTION = "UUID (v1/v4) & Unique ID Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_uuid_v4(count: int = 1) -> list:
    """Generate cryptographically random UUIDs (Version 4)."""
    return [str(uuid.uuid4()) for _ in range(count)]

def generate_uuid_v1(count: int = 1) -> list:
    """Generate time-based UUIDs (Version 1)."""
    return [str(uuid.uuid1()) for _ in range(count)]

def run():
    print(color.color_text("--- UUID & Unique ID Generator ---", COLOR))
    print(" [1] Generate Random UUID v4 (Recommended for Security/General Use)")
    print(" [2] Generate Time-Based UUID v1")
    
    choice = input("\nSelect option: ").strip()

    try:
        count = int(input("How many IDs to generate? (default 1): ").strip() or "1")
        if count < 1:
            count = 1
    except ValueError:
        count = 1

    if choice == "1":
        ids = generate_uuid_v4(count)
        print(color.color_text(f"\n[+] Generated UUID v4 ({count}):", color.GREEN))
        for item in ids:
            print(f"  {item}")

    elif choice == "2":
        ids = generate_uuid_v1(count)
        print(color.color_text(f"\n[+] Generated UUID v1 ({count}):", color.GREEN))
        for item in ids:
            print(f"  {item}")

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
