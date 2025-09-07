enc = '434e43437b596f75275265616c6c795f22e9418a2c719a26dcae3621128fd3496f7691b94c74ead75578059167c5bfb2'
def ltb(x):
    return x.to_bytes(x.bit_length()//8+1, "big")
def btl(x):
    return int.from_bytes(x, "big")
def xor(x, y):
    return ltb(btl(x)^btl(y))
import hashlib
temp = hashlib.md5(b"token++").digest()
temp = temp[:15]+temp[15:]+temp[15:]+temp[:15]
temp = hashlib.sha256(temp).digest()

flag = xor(temp, bytes.fromhex(enc))
assert flag[:5] == b'CNCC{'
assert flag[-1:] == b'}'
assert len(flag) == 48 
assert hashlib.sha256(flag).hexdigest() == '188181617a0d1c49d30eb3cce51867dc39571c595c2a992b3ea2271fba901613'
print(flag.decode())