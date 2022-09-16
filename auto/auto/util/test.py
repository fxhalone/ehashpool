import requests
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
response = requests.get(url='http://ehashapi.test.poolx.io/pool/v1/miner/Home', headers=headers)

assert int(response.json()['code']) == 200