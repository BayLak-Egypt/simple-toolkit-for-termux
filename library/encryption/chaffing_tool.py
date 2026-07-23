import hashlib
import hmac
import json
import base64
import color

DESCRIPTION = "Chaffing & Winnowing Security Tool"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def generate_mac(data: str, secret_key: str) -> str:
    """Generate SHA256 HMAC for authentication."""
    return hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

def chaff_message(secret_msg: str, secret_key: str) -> str:
    """Add fake/chaff packets alongside authentic packets."""
    packets = []
    fake_counter = 0
    
    for idx, char in enumerate(secret_msg):
        # 1. Authentic packet
        mac_valid = generate_mac(f"{idx}:{char}", secret_key)
        packets.append({"seq": idx, "data": char, "mac": mac_valid})
        
        # 2. Add fake (chaff) packet with invalid MAC
        fake_char = chr((ord(char) + 3) % 126 + 32)
        mac_fake = generate_mac(f"{idx}:{fake_char}_fake", secret_key)
        packets.append({"seq": idx, "data": fake_char, "mac": mac_fake})
        fake_counter += 1

    json_data = json.dumps(packets)
    return base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

def winnow_message(payload_b64: str, secret_key: str) -> str:
    """Filter out invalid packets and restore original text."""
    raw_json = base64.b64decode(payload_b64.encode('utf-8')).decode('utf-8')
    packets = json.loads(raw_json)
    
    recovered = {}
    for pkt in packets:
        seq = pkt["seq"]
        data = pkt["data"]
        received_mac = pkt["mac"]
        
        # Verify MAC authenticity
        expected_mac = generate_mac(f"{seq}:{data}", secret_key)
        if hmac.compare_digest(received_mac, expected_mac):
            recovered[seq] = data

    # Reconstruct text by sequence
    sorted_seqs = sorted(recovered.keys())
    return "".join(recovered[s] for s in sorted_seqs)

def run():
    print(color.color_text("--- Chaffing & Winnowing Tool ---", COLOR))
    print(" [1] Add Chaff (Disguise Message)")
    print(" [2] Winnow Message (Extract Authentic Text)")
    
    choice = input("\nSelect an option: ").strip()
    
    if choice == "1":
        text = input("Enter secret text: ").strip()
        key = input("Enter authentication key: ").strip()
        
        if not text or not key:
            print(color.color_text("[!] Text and key cannot be empty.", color.RED))
            return
            
        payload = chaff_message(text, key)
        print(color.color_text(f"\n[+] Chaffed Output (Base64 Payload):\n{payload}", color.GREEN))
        
    elif choice == "2":
        payload_b64 = input("Enter Chaffed Base64 Payload: ").strip()
        key = input("Enter authentication key: ").strip()
        
        try:
            result = winnow_message(payload_b64, key)
            if result:
                print(color.color_text(f"\n[+] Winnowed Result:\n{result}", color.GREEN))
            else:
                print(color.color_text("\n[!] Authentication failed for all packets.", color.RED))
        except Exception:
            print(color.color_text("\n[!] Invalid payload format.", color.RED))
            
    else:
        print(color.color_text("[!] Invalid option.", color.RED))
