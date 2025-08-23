import base64

def xor_decrypt(base64_data: str, key: str) -> str:
    encrypted = base64.b64decode(base64_data.strip())
    decrypted = ''.join(
        chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(encrypted)
    )
    return decrypted

# Values extracted from CTF_PREFS.xml
pin = "6536"
encrypted_master_key = "XmxqYHF0YEQEA1xaUHB2Z2NefXRFQARdZ2Z/RWRFfkA="
encrypted_data_key = "ABcVDh9yIx5dUjcNLxM9BWNaN3oJNmNeJykjGQUlfEA="
encrypted_data = """KwAPGyNDHAkcBT0FJjgMNUVaFF0OLCZQFA8GBjMhWV8bLSQ5NF8EBAYXLAAiMwsjV0gNVxUvO1sR
Bw==""".replace("\n", "").strip()


for pin_int in range(10000):
    pin = str(pin_int).zfill(4)
    # Step 1: Decrypt master key using PIN
    master_key = xor_decrypt(encrypted_master_key, pin)

    # Step 2: Decrypt random key using master key
    data_key = xor_decrypt(encrypted_data_key, master_key)

    # Step 3: Decrypt secret using data key
    secret = xor_decrypt(encrypted_data, data_key)
    if not all(32 <= ord(c) <= 126 for c in secret):
        continue
    
    if "CNCC" in secret:
        print(f"[+] PIN FOUND: {pin}")
        print(f"[+] Master Key: {master_key}")
        print(f"[+] Data Key: {data_key}")
        print(f"[+] Secret: {secret}")
        break
