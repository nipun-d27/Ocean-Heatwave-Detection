import os
import subprocess

# -----------------------
# Paths
# -----------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_DIR = SCRIPT_DIR  # submissions folder itself
PUBLIC_KEY = os.path.join(os.path.dirname(SCRIPT_DIR), "encryption", "public_key.pem")

AES_KEY_PATH = os.path.join(SUBMISSION_DIR, "aes_key.hex")
AES_KEY_ENC_PATH = os.path.join(SUBMISSION_DIR, "aes_key.enc")

# -----------------------
# Step 1: Generate AES key
# -----------------------
print("Generating AES key...")
result = subprocess.run(
    ["openssl", "rand", "-hex", "32"], capture_output=True, text=True, check=True
)
aes_key = result.stdout.strip()
with open(AES_KEY_PATH, "w") as f:
    f.write(aes_key)

# -----------------------
# Step 2: Encrypt all CSVs
# -----------------------
csv_files = [
    f for f in os.listdir(SUBMISSION_DIR)
    if f.endswith(".csv") and f != "sample_submission.csv"
]

for csv_file in csv_files:
    input_path = os.path.join(SUBMISSION_DIR, csv_file)
    output_path = os.path.splitext(input_path)[0] + ".enc"
    
    print(f"Encrypting {csv_file}...")
    subprocess.run(
        [
            "openssl", "enc", "-aes-256-cbc", "-pbkdf2",
            "-in", input_path,
            "-out", output_path,
            "-pass", f"file:{AES_KEY_PATH}"
        ],
        check=True
    )

# -----------------------
# Step 3: Encrypt AES key with RSA public key
# -----------------------
print("Encrypting AES key with RSA...")
subprocess.run(
    [
        "openssl", "pkeyutl", "-encrypt", "-pubin",
        "-inkey", PUBLIC_KEY,
        "-in", AES_KEY_PATH,
        "-out", AES_KEY_ENC_PATH
    ],
    check=True
)

print("Encryption completed. All CSVs encrypted and AES key secured.")
