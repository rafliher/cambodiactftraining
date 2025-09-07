def rol(value, shift, bits=8):
    """Rotate left"""
    return ((value << shift) & (2**bits - 1)) | (value >> (bits - shift))


def ror(value, shift, bits=8):
    """Rotate right"""
    return ((value >> shift) | (value << (bits - shift))) & (2**bits - 1)


def shift_array(buf, amount):
    """Rotate whole array by amount"""
    amount %= len(buf)
    return buf[-amount:] + buf[:-amount]


def transform_data_decrypt(data: bytearray, key: bytes):
    v4 = len(key)
    # run backwards (32 → 0)
    for i in reversed(range(32)):
        # Step 4: subtract 7*i
        for n in range(len(data)):
            data[n] = (data[n] - 7 * i) & 0xFF

        # Step 3: undo array shift
        v7 = sum(key)
        data = shift_array(data, -(v7 % len(data)))

        # Step 2: undo bit rotation (original was left 3, so now right 3)
        for k in range(len(data)):
            data[k] = ror(data[k], 3)

        # Step 1: undo XOR with key
        for j in range(len(data)):
            data[j] ^= key[j % v4]

    return data


def extract_secret(filepath: str, key: str):
    # read file
    with open(filepath, "rb") as f:
        content = f.read()

    # find marker
    marker = b"|^#~"
    idx = content.find(marker)
    if idx == -1:
        raise ValueError("Marker not found in file")

    # encrypted hex string
    enc_hex = content[idx + len(marker):].decode()
    enc_bytes = bytearray.fromhex(enc_hex)

    # decrypt
    plain_bytes = transform_data_decrypt(enc_bytes, key.encode())
    return plain_bytes.decode(errors="ignore")


if __name__ == "__main__":
    filename = "th15_h45_f149_1n_1t.m4a"  # your stego MP3/M4A file
    key = "best_music_ever"
    flag = extract_secret(filename, key)
    print("Flag:", flag)
