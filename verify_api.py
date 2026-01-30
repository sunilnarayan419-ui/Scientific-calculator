import requests
import json

url = "http://127.0.0.1:8000/solve"
payload = {
    "expression": "x**2 + 2*x + 1",
    "mode": "solve"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
