import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = 'like="Austin"&to="Houston"&radius=50'

response = requests.post('https://drxbackend.azurewebsites.net/send_city', headers=headers, data=data)

print(response.text)
