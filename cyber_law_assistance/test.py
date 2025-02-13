import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HEADERS = {"Authorization": "Bearer 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"}

payload = {"inputs": "What is cyber law?"}

response = requests.post(API_URL, headers=HEADERS, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
