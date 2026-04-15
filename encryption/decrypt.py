from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load private key
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Read encrypted data
with open("encrypted_message.bin", "rb") as file:
    encrypted_data = file.read()

# Decrypt the data
decrypted_data = private_key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Convert bytes to string
decrypted_text = decrypted_data.decode("utf-8")

# Print result
print("🔓 Decrypted Message:")
print(decrypted_text)
