key = b'supersecretkey'

with open('flag.enc', 'rb') as f:
    data = f.read()
    plaintext = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    print(plaintext)