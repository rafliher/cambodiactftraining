import hashlib

flag = b'CNCC{malware_zero_bug_gravity_firewall_defuse_fusebox_bytebomb}'

data = flag.split(b"CNCC{")[1].split(b"}")[0]
data = data.split(b"_")

temp = []
for i in range(len(data)):
    if(i%3==0):
        temp += [hashlib.md5(data[i]).hexdigest()]
    if(i%3==1):
        temp += [hashlib.sha1(data[i]).hexdigest()]
    if(i%3==2):
        temp += [hashlib.sha256(data[i]).hexdigest()]

for i in temp:
    print(i)