import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "The answer to  universe is which number",
})
print(output)