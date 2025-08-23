import re
import math
from difflib import SequenceMatcher
from itertools import product

# Load ciphertext
cip = open('encrypted_flag.txt', 'rb').read()
key = (b'rustkey' * 23)[:len(cip)]  # Ensure key is same length as cip

# Indices where i % 4 == 2
mod2_indices = [i for i in range(len(cip)) if i % 4 == 2]

# Known dictionary words
known_words = {"rust", "is", "best", "language", "on", "the", "world"}
target_phrase = "rust is best language on the world"

# Helpers
def shannon_entropy(s):
    freq = {c: s.count(c) for c in set(s)}
    length = len(s)
    return -sum((f / length) * math.log2(f / length) for f in freq.values())

def normalize(s):
    return re.sub(r'[^a-z]', '', s.lower())

def count_dict_words(s):
    words = re.findall(r'[a-zA-Z]+', s.lower())
    return sum(1 for w in words if w in known_words)

def similarity_score(s):
    return SequenceMatcher(None, normalize(s), normalize(target_phrase)).ratio()

# Leet-to-plain substitutions
leet_map = str.maketrans({
    '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '6': 'g', '7': 't', '8': 'b', '9': 'g'
})

def visual_similarity_score(s):
    leet_normalized = normalize(s.translate(leet_map))
    return SequenceMatcher(None, leet_normalized, normalize(target_phrase)).ratio()

def score(candidate):
    if not re.match(r'^CNCC\{[a-zA-Z0-9_]+\}$', candidate):
        return 0
    dict_score = count_dict_words(candidate)
    sim_score = similarity_score(candidate)
    visual_score = visual_similarity_score(candidate)
    entropy_score = shannon_entropy(candidate)
    return dict_score * 2 + sim_score * 3 + visual_score * 4 + entropy_score

# Store and score candidates
scored = []

for bits in product([0, 1], repeat=len(mod2_indices)):
    out = []
    j = 0
    for i in range(len(cip)):
        if i % 4 == 0:
            out.append(chr(cip[i] - key[i]))
        elif i % 4 == 1:
            out.append(chr(cip[i] ^ key[i]))
        elif i % 4 == 2:
            byte = cip[i] << 1
            byte = (byte & ~1) | bits[j]
            j += 1
            out.append(chr(byte))
        elif i % 4 == 3:
            out.append(chr((cip[i] ^ key[i]) - key[i]))
    candidate = ''.join(out)
    s = score(candidate)
    if s > 0:
        scored.append((s, candidate))

# Sort and display top results
scored.sort(reverse=True)
print("Top flag candidates:")
for s, c in scored[:5]:
    print(f"[Score: {s:.3f}] {c}")
