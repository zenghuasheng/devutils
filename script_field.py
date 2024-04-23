import requests

url = "https://addfield.k3s-dev.myones.net/project/api/project/team/A3yNUJpj/floatScript"

payload = ""
headers = {
    'Ones-Check-Id': 'A3yNUJpj',
    'Ones-Plugin-Id': '37461d34',
    'ones-check-point': 'team',
    'Ones-User-Id': 'To1g58p6'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
