import requests
import json

headers = {'Content-Type': 'application/json'}

data = {
    'question': 'Q1',
    'options': ['A1', 'A2', 'A3']
}

res = requests.post('http://127.0.0.1:5000/open', data=json.dumps(data), headers=headers)     # json.dumps(data) - data 객체를 JSON 문자열로 변환
print(res.text)