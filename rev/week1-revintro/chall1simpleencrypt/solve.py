encrpted_falg = "MGJLPXBF[GNtYN]NYXNV"

key = 0x2B

flag = ''.join([chr(ord(c) ^ key) for c in encrpted_falg])
print(flag)