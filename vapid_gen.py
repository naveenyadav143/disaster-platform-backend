from py_vapid import Vapid
from cryptography.hazmat.primitives import serialization
import base64

# Generate keys
vapid = Vapid()
vapid.generate_keys()

# Export private key (PEM)
private_pem = vapid.private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode("utf-8")

# Export public key (PEM)
public_pem = vapid.public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode("utf-8")

# Convert private key to Base64
private_b64 = base64.urlsafe_b64encode(
    vapid.private_key.private_numbers().private_value.to_bytes(32, "big")
).decode("utf-8")

# Convert public key to Base64 (manual point encoding)
numbers = vapid.public_key.public_numbers()
x = numbers.x.to_bytes(32, "big")
y = numbers.y.to_bytes(32, "big")
uncompressed_point = b"\x04" + x + y
public_b64 = base64.urlsafe_b64encode(uncompressed_point).decode("utf-8")

print("🔑 VAPID Private PEM:\n", private_pem)
print("🔑 VAPID Public PEM:\n", public_pem)
print("📦 Base64 Private Key:", private_b64)
print("📦 Base64 Public Key:", public_b64)
