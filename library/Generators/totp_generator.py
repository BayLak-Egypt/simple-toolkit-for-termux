import secrets
import base64
import urllib.parse
import color

DESCRIPTION = "2FA / TOTP Secret Key & URI Generator"
GROUP_ID = 4
COLOR = color.CYAN

def generate_totp_secret() -> str:
    """Generate a random 16-character Base32 secret for TOTP."""
    raw_bytes = secrets.token_bytes(10)
    return base64.b32encode(raw_bytes).decode('utf-8')

def build_totp_uri(secret: str, account_name: str, issuer: str) -> str:
    """Build a standard otpauth:// URI for authenticator apps."""
    label = f"{issuer}:{account_name}" if issuer else account_name
    params = {
        'secret': secret,
        'issuer': issuer
    }
    return f"otpauth://totp/{urllib.parse.quote(label)}?{urllib.parse.urlencode(params)}"

def run():
    print(color.color_text("--- 2FA / TOTP Secret Generator ---", COLOR))
    
    account = input("Enter Account Name (e.g. user@example.com): ").strip() or "User"
    issuer = input("Enter Issuer/Service Name (e.g. MyApp): ").strip() or "Service"

    secret = generate_totp_secret()
    uri = build_totp_uri(secret, account, issuer)

    print(color.color_text(f"\n[+] Generated TOTP Secret Key (Base32):\n{secret}", color.GREEN))
    print(color.color_text(f"\n[+] Authenticator App URI:\n{uri}", color.GREEN))
    print(color.color_text("\n[*] Tip: You can convert the URI above into a QR code for mobile scanning.", color.YELLOW))
