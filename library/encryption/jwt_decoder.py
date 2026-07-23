import base64
import json
import color

DESCRIPTION = "JWT (JSON Web Token) Header & Payload Decoder"
GROUP_ID = 3  # Miscellaneous Tools
COLOR = color.CYAN

def base64url_decode(input_str: str) -> bytes:
    """Decode base64url-encoded string with padding correction."""
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    # Replace URL-safe characters
    input_str = input_str.replace('-', '+').replace('_', '/')
    return base64.b64decode(input_str)

def decode_jwt(jwt_token: str):
    parts = jwt_token.strip().split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format (Must contain 3 parts separated by dots).")

    header_b64, payload_b64, signature_b64 = parts

    # Decode Header
    header_json = base64url_decode(header_b64).decode('utf-8')
    header_data = json.loads(header_json)

    # Decode Payload
    payload_json = base64url_decode(payload_b64).decode('utf-8')
    payload_data = json.loads(payload_json)

    return header_data, payload_data, signature_b64

def run():
    print(color.color_text("--- JWT Token Decoder ---", COLOR))
    token = input("Enter JWT Token: ").strip()

    if not token:
        print(color.color_text("[!] Token cannot be empty.", color.RED))
        return

    try:
        header, payload, signature = decode_jwt(token)
        
        print(color.color_text("\n[+] Header:", color.GREEN))
        print(json.dumps(header, indent=4))

        print(color.color_text("\n[+] Payload (Claims):", color.GREEN))
        print(json.dumps(payload, indent=4))

        print(color.color_text("\n[+] Raw Signature (Base64URL):", color.GREEN))
        print(signature)

    except Exception as e:
        print(color.color_text(f"\n[!] Failed to decode JWT: {e}", color.RED))
