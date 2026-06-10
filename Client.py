import requests
import json
import hmac
import hashlib
import time

api_key = "[ENCRYPTION_KEY]"
secret_key = "[ENCRYPTION_KEY]"

payload = {
    "method": "get_balance",
    "nonce": int(time.time() * 1000)
}

body = json.dumps(payload, separators=(",", ":"))

signature = hmac.new(
    secret_key.encode('utf-8'),
    body.encode(),
    hashlib.sha512
).hexdigest()

response = requests.post(
    "http://localhost:8000/private",
    headers={
        "X-API-KEY": api_key,
        "X-SIGNATURE": signature,
        "Content-Type": "application/json"
    },
    data=body
)
print(response.json())