import requests

url = "https://p1103-k3s-2.k3s-dev.myones.net/project/api/project/team/SZK3eYEJ/floatScript"

payload = ""
headers = {
    'Ones-Check-Id': 'SZK3eYEJ',
    'Ones-Plugin-Id': '89f63271',
    'ones-check-point': 'team',
    'Ones-User-Id': 'DXYngJj7',
    'Manhours': '200000'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
