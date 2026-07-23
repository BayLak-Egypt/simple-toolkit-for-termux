import secrets
import color

DESCRIPTION = "Random & OUI-based MAC Address Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

# Common Vendor OUI Prefixes
COMMON_OUIS = {
    "Cisco": "00:00:0C",
    "Intel": "00:1B:21",
    "Apple": "00:17:F2",
    "Dell": "00:14:22",
    "VMware": "00:50:56"
}

def generate_random_mac(oui: str = None) -> str:
    """Generate a formatted MAC address with optional vendor OUI."""
    if oui:
        # Clean custom OUI input
        cleaned_oui = oui.replace("-", ":").replace(".", "").strip().upper()
        parts = cleaned_oui.split(":")
        if len(parts) == 3:
            bytes_list = [int(p, 16) for p in parts] + [secrets.randbelow(256) for _ in range(3)]
        else:
            bytes_list = [secrets.randbelow(256) for _ in range(6)]
    else:
        bytes_list = [secrets.randbelow(256) for _ in range(6)]
        # Set locally administered bit (bit 1 of 1st byte) and clear multicast bit (bit 0)
        bytes_list[0] = (bytes_list[0] & 0xFE) | 0x02

    return ":".join(f"{b:02X}" for b in bytes_list)

def run():
    print(color.color_text("--- MAC Address Generator ---", COLOR))
    print(" [1] Generate Random Locally Administered MAC")
    print(" [2] Generate MAC with Vendor OUI (Cisco, Intel, Apple, etc.)")
    print(" [3] Generate MAC with Custom OUI Prefix")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        mac = generate_random_mac()
        print(color.color_text(f"\n[+] Generated Random MAC:\n{mac}", color.GREEN))

    elif choice == "2":
        print("\nSelect Vendor OUI:")
        vendors = list(COMMON_OUIS.keys())
        for idx, vendor in enumerate(vendors, 1):
            print(f" [{idx}] {vendor} ({COMMON_OUIS[vendor]})")
        
        v_choice = input("\nSelect vendor number: ").strip()
        if v_choice.isdigit() and 1 <= int(v_choice) <= len(vendors):
            vendor_name = vendors[int(v_choice) - 1]
            prefix = COMMON_OUIS[vendor_name]
            mac = generate_random_mac(oui=prefix)
            print(color.color_text(f"\n[+] Generated {vendor_name} MAC:\n{mac}", color.GREEN))
        else:
            print(color.color_text("[!] Invalid vendor selection.", color.RED))

    elif choice == "3":
        custom_oui = input("Enter 3-byte OUI prefix (e.g. 00:11:22 or 001122): ").strip()
        if not custom_oui:
            print(color.color_text("[!] OUI cannot be empty.", color.RED))
            return
        
        try:
            mac = generate_random_mac(oui=custom_oui)
            print(color.color_text(f"\n[+] Generated Custom MAC:\n{mac}", color.GREEN))
        except Exception as e:
            print(color.color_text(f"[!] Error parsing OUI: {e}", color.RED))

    else:
        print(color.color_text("[!] Invalid option.", color.RED))
