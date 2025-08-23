from pwn import *
from itertools import *

cip = open('encrypted_flag.txt','rb').read()
key = b'rustkey'*23
lis = []
for k in range(2):
	ans = ''
	for i in range(len(cip)):
		if i%4==0:
			ans+=(chr(cip[i]-key[i]))
		elif i%4==1:
			ans+=(chr(cip[i]^key[i]))
		elif i%4==2:
			otw = cip[i]<<1
			tes = bin(otw)[2:][:len(bin(otw)[2:])-1]
			tes = tes+str(k)
			ans+=(chr(int(tes,2)))
		elif i%4==3:
			ans+=(chr((cip[i]^key[i])-key[i]))
	lis.append(ans)

# you can xor two flag candidate to get the false string
wrong = xor(lis[0].encode(),lis[1].encode())
repair1 = lis[0].encode()
repair2 = lis[1].encode()
print(repair1,repair2)
right = []
otw = []
for i in range(len(wrong)):
	if wrong[i]==1:
		right.append([repair1[i],repair2[i]])
		otw.append(0)
		print(i)
	else:
		otw.append(repair1[i])
print(right)

all_combinations = list(product(*right))

# Example: print first 10 combinations
print("Sample combinations:")
for combo in all_combinations:
    otw[2] = combo[0]
    otw[6] = combo[1]
    otw[10] = combo[2]
    otw[14] = combo[3]
    otw[18] = combo[4]
    otw[22] = combo[5]
    otw[26] = combo[6]
    otw[30] = combo[7]
    otw[34] = combo[8]
    otw[38] = combo[9]
    if 'CNCC' in ''.join([chr(x) for x in otw]):
        print(''.join([chr(x) for x in otw]))

print(f"Total combinations: {len(all_combinations)}")
		