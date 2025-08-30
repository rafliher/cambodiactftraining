import requests

flag = b'CNCC{malware_zero_bug_gravity_firewall_defuse_fusebox_bytebomb}'


headers = {
    'Authorization': 'Bearer your_token_here',
    'Content-Type': 'application/json'
}

data = {
    "flag": flag.decode()
}

response = requests.post("http://localhost:8080/check-flag", headers=headers, json=data)

print(response.json())