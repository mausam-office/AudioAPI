import requests

response = requests.get('http://localhost:8000/audioapi/', params={'device_name':'Atm3'})
print(response, response.text)