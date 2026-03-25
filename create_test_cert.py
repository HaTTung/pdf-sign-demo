from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12

PASSWORD = b"123456"

# 1) Tạo private key RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 2) Tạo subject / issuer (self-signed => subject = issuer)
name = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "School Project"),
    x509.NameAttribute(NameOID.COMMON_NAME, "Ha Thanh Tung Signed"),
])

# 3) Tạo self-signed certificate
now = datetime.now(timezone.utc)

cert = (
    x509.CertificateBuilder()
    .subject_name(name)
    .issuer_name(name)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now)
    .not_valid_after(now + timedelta(days=365))
    .add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    )
    .add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=True,   # tương đương nonRepudiation/contentCommitment
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    )
    .add_extension(
        x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
        critical=False,
    )
    .add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(private_key.public_key()),
        critical=False,
    )
    .sign(private_key, hashes.SHA256())
)

# 4) Xuất private key PEM
with open("key.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

# 5) Xuất certificate PEM
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# 6) Xuất PKCS#12 (.p12) để pyHanko dùng
p12_data = pkcs12.serialize_key_and_certificates(
    name=b"Test Signer",
    key=private_key,
    cert=cert,
    cas=None,
    encryption_algorithm=serialization.BestAvailableEncryption(PASSWORD),
)

with open("test_cert.p12", "wb") as f:
    f.write(p12_data)

print("Da tao xong:")
print("- key.pem")
print("- cert.pem")
print("- test_cert.p12")
print("Mat khau file p12: 123456")