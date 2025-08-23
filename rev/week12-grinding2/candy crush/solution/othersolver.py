from itertools import product

# Load ciphertext
cip = open('encrypted_flag.txt', 'rb').read()
key = (b'rustkey' * 23)[:len(cip)]  # Ensure key is same length as cip

# Identify the indices where i % 4 == 2
mod2_indices = [i for i in range(len(cip)) if i % 4 == 2]

# There are 2 possibilities (flip LSB or not) for each such index
# So total combinations = 2^(len(mod2_indices))
# We'll use itertools.product to iterate over all combinations
for bits in product([0, 1], repeat=len(mod2_indices)):
    out = []
    j = 0  # index in bits
    for i in range(len(cip)):
        if i % 4 == 0:
            out.append(chr(cip[i] - key[i]))
        elif i % 4 == 1:
            out.append(chr(cip[i] ^ key[i]))
        elif i % 4 == 2:
            # Flip LSB: keep or flip based on bits[j]
            byte = cip[i] << 1
            byte = (byte & ~1) | bits[j]  # Set LSB to bits[j]
            j += 1
            out.append(chr(byte))
        elif i % 4 == 3:
            out.append(chr((cip[i] ^ key[i]) - key[i]))
    print(''.join(out))
