import requests
url = 'http://127.0.0.1:8000/api/v1/users/?format=json'

cookie = 'sessionid=z7zku5rxki9s842165jeqepb1h64xmdb'
headers = {
    'Cookie': cookie
}
response = requests.get(url, headers=headers)
data = response.json()

for user in data.get('results'):
    print(f"Username: {user.get('username')}, Email: {user.get('email')}, Date joined: {user.get('date_joined')}")
    



