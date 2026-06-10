from hashlib import sha256
import hmac

secret_key = "[]"
message = '[]'

signature = hmac.new(
    secret_key.encode(),
    message.encode(),
    sha256
).hexdigest()

print(secret_key.encode())
print(message.encode())

print(list(secret_key.encode()))
print(list(message.encode()))

print(signature)