from pwn import *

# conn = process('./newtest.py')
conn = remote('52.74.141.216','6003')
# respon = conn.recvline()
# print(respon)
maxim = int('1'*12,2)
bba, bbb, bbc = 0, 0, 0
baa, bab, bac = maxim, maxim, maxim
inc = 0
try:
    while True:
        inc += 1 
        print(str(inc)+'process')
        a = (bba+baa)//2
        b = (bbb+bab)//2
        c = (bbc+bac)//2
        send = f'{a} {b} {c}'.encode()
        conn.sendline(send)
        respon = conn.recvline()
        print(respon.decode())
        res = respon.decode().strip().split(' ')
        if(res[0] == 'l'): resa = 0
        elif(res[0] == 'd'): resa = 1
        else: resa = 2
        
        if(res[1] == 'q'): resb = 0
        elif(res[1] == 'v'): resb = 1
        else: resb = 2
        
        if(res[2] == 'w'): resc = 0
        elif(res[2] == 'n'): resc = 1
        else: resc = 2
        
        if(resa==1): bba = (bba+baa)//2 + 1
        elif(resa==2): baa = (bba+baa)//2 - 1
        
        if(resb==1): bbb = (bbb+bab)//2 + 1
        elif(resb==2): bab = (bbb+bab)//2 - 1
        
        if(resc==1): bbc = (bbc+bac)//2 + 1
        elif(resc==2): bac = (bbc+bac)//2 - 1
except:
    pass
finally:
    conn.close()