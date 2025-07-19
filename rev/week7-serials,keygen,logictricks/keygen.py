'''
1. length must be 8
2. index 0 times index 1 must be 5250.
3. sum of digits (index 2-5) equals 17.
4. bytesum equals to index 6
5. xor equals to index 7
'''

for a in range(ord('A'), ord('z')+1):
    for b in range(ord('A'), ord('z')+1):
        if a * b != 5250:
            continue
        
        for d1 in range(10):
            for d2 in range(10):
                for d3 in range(10):
                    for d4 in range(10):
                        digits_sum = d1 + d2 + d3 + d4
                        if digits_sum != 17:
                            continue
                        
                        serial = f"{chr(a)}{chr(b)}{d1}{d2}{d3}{d4}"
                        bytesum = sum(ord(c) for c in serial)
                        
                        xor_value = 0
                        for c in serial:
                            xor_value ^= ord(c)
                            
                        bytesum_char = (bytesum % 94) + 33
                        xor_char = (xor_value % 94) + 33
                        
                        serial += chr(bytesum_char) + chr(xor_char)
                        print(serial)
                        break

                        
                        
                