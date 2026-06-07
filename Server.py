from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()

API_KEYS = {
    "[ENCRYPTION_KEY]": {
        "secret_key": "[ENCRYPTION_KEY]",
        "last_nonce": 0
    }
}

@app.post("/api/private")
async def private_api(request: Request):

    api_key = request.headers.get("X-API-KEY")
    signature = request.headers.get("X-SIGNATURE")

    if not api_key or api_key not in API_KEYS:
        raise HTTPException(401, "Invalid API Key")

    secret_key = API_KEYS[api_key]["secret_key"]

    raw_body = await request.body()

    expected_signature = hmac.new(
        secret_key.encode(),
        raw_body,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(401, "Invalid Signature")

    payload = await request.json()

    nonce = payload.get("nonce")

    if nonce is None:
        raise HTTPException(400, "Nonce required")

    if nonce <= API_KEYS[api_key]["last_nonce"]:
        raise HTTPException(401, "Nonce must be greater than previous")

    API_KEYS[api_key]["last_nonce"] = nonce

    return {
        "success": True,
        "message": "Request authenticated"
    }