import datetime
import ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import color

DESCRIPTION = "Self-Signed SSL/TLS Certificate Generator"
GROUP_ID = 4  # Generators & Security Utilities
COLOR = color.CYAN

def generate_self_signed_cert(common_name: str = "localhost") -> dict:
    """Generate a private key and a self-signed SSL certificate in PEM format."""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Subject and Issuer details
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "DevSecOps Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    
    # Build certificate
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Serialize to PEM
    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")
    
    return {
        "Certificate": cert_pem,
        "PrivateKey": key_pem
    }

def run():
    print(color.color_text("--- Self-Signed SSL/TLS Certificate Generator ---", COLOR))
    
    common_name = input("Enter Common Name (CN) / Domain (default 'localhost'): ").strip() or "localhost"

    print(color.color_text(f"\n[+] Generating SSL Certificate for {common_name}...\n", color.GREEN))
    result = generate_self_signed_cert(common_name)
    
    print(color.color_text("--- Private Key (PEM) ---", color.YELLOW))
    print(result["PrivateKey"])
    print(color.color_text("--- Certificate (PEM) ---", color.YELLOW))
    print(result["Certificate"])
