import os, requests, logging
log = logging.getLogger(__name__)

def get_token():
    token_url = os.environ["TOKEN_URL"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    scope = os.environ["SCOPE"]
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
        "grant_type": "client_credentials"
    }
    r = requests.post(token_url, data=data, timeout=60)
    r.raise_for_status()
    return r.json()["access_token"]

def download_csv(token: str) -> bytes:
    url = os.environ["API_CSV_URL"]
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=120)
    r.raise_for_status()
    if "text/csv" not in r.headers.get("Content-Type",""):
        log.warning("Content-Type no es text/csv: %s", r.headers.get("Content-Type"))
    return r.content