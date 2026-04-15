from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load public key
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

# Input message to encrypt
message = input("Enter message to encrypt: ")

# Convert to bytes
message_bytes = message.encode("utf-8")

# Encrypt the message
encrypted_data = public_key.encrypt(
    message_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save encrypted data to file
with open("encrypted_message.bin", "wb") as file:
    file.write(encrypted_data)

print("🔐 Message encrypted and saved to encrypted_message.bin")
