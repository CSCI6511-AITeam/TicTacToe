import requests
url = 'https://www.notexponential.com/aip2pgaming/api/index.php'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "x-api-key": "22271ea923794747f8d3",
        "userId": "856"
    }
data = {
        "type": "member",
        "teamId": "1239",
        "userId": "856"
    }

response = requests.post(url, data=data, headers=headers)
print(response.text)