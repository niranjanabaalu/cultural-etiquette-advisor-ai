import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='cultural_advisor/.env')

api_key = os.getenv('NVIDIA_API_KEY')
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
if not api_key:
    print("API key not found")
    exit(1)

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "meta/llama-3.1-70b-instruct",
    "messages": [
        {"role": "system", "content": "You are a professional Cultural Etiquette Advisor. Respond briefly and clearly."},
        {"role": "user", "content": "tell me about japan"}
    ],
    "temperature": 0.6,
    "max_tokens": 250
}

print("Making API request...")
response = requests.post(url, headers=headers, json=data, timeout=120)  # Increased timeout for large model
print(f"Response status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("Full response:", result)
    if 'choices' in result and result['choices']:
        print("API key is valid. Response:", result['choices'][0]['message']['content'].strip())
    else:
        print("API returned 200 but no content.")
elif response.status_code == 401:
    print("Unauthorized: Invalid API key.")
elif response.status_code == 429:
    print("Rate limited: Too many requests.")
elif response.status_code == 404:
    print("Model not found.")
else:
    print(f"API error: {response.status_code} - {response.text}")