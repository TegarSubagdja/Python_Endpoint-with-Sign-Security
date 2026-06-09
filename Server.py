from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import json

app = FastAPI()

# Simulasi database API key
API_KEYS = {
    "[ENCRYPTION_KEY]": {
        "secret_key": "[ENCRYPTION_KEY]",
        "last_nonce": 0
    }
}


def verify_signature(secret_key: str, raw_body: bytes, signature: str) -> bool:
    expected = hmac.new(
        secret_key.encode("utf-8"),
        raw_body,
        hashlib.sha512
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


@app.post("/private")
async def private_api(request: Request):

    # =========================
    # 1. Ambil header
    # =========================
    api_key = request.headers.get("X-API-KEY")
    signature = request.headers.get("X-SIGNATURE")

    if not api_key or not signature:
        raise HTTPException(status_code=401, detail="Missing API Key or Signature")

    # =========================
    # 2. Validasi API key
    # =========================
    client = API_KEYS.get(api_key)
    if not client:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    secret_key = client["secret_key"]

    # =========================
    # 3. Ambil raw body (penting untuk HMAC)
    # =========================
    raw_body = await request.body()

    # =========================
    # 4. Verifikasi signature
    # =========================
    if not verify_signature(secret_key, raw_body, signature):
        raise HTTPException(status_code=401, detail="Invalid Signature")

    # =========================
    # 5. Parse JSON setelah signature valid
    # =========================
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # =========================
    # 6. Validasi nonce (anti replay attack)
    # =========================
    nonce = payload.get("nonce")

    if nonce is None:
        raise HTTPException(status_code=400, detail="Nonce required")

    if not isinstance(nonce, int):
        raise HTTPException(status_code=400, detail="Nonce must be integer")

    if nonce <= client["last_nonce"]:
        raise HTTPException(status_code=401, detail="Nonce must be greater than previous")

    client["last_nonce"] = nonce

    # =========================
    # 7. Response
    # =========================
    return {
        "success": True,
        "message": "Request authenticated by king Tegar",
        "nonce": nonce
    }