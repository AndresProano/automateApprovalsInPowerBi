import requests, os
from app.config import TENANT_ID, CLIENT_ID, CLIENT_SECRET
import httpx
import jwt
from fastapi import HTTPException
#from jwt import PyJWKClient

_openid_cfg_cache = {}
_jwk_cache = {}

GRAPH_URL = "https://graph.microsoft.com/beta/approvalSolution/approvalItems"

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
    r = requests.post(url, data=data)
    return r.json()["access_token"]

def resolve_user_id(email: str, token: str) -> str:
    url = f"https://graph.microsoft.com/v1.0/users/{email}"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get("id")

def get_approvals(token, assigned_user_id=None):
    approvals = []
    headers = {"Authorization": f"Bearer {token}"}
    params = None
    if assigned_user_id:
        params = {
            "$filter": f"assignedTo/any(u:u/id eq '{assigned_user_id}')"
        }
    url = GRAPH_URL
    while url:
        r = requests.get(
            url,
            headers=headers,
            params=params if url == GRAPH_URL else None
        )
        params = None
        data = r.json()
        approvals.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return approvals

def _get_openid_config():
    if "cfg" in _openid_cfg_cache:
        return _openid_cfg_cache["cfg"]
    url = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"
    resp = httpx.get(url, timeout=10)
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail="No se pudo obtener OpenID config.")
    data = resp.json()
    _openid_cfg_cache["cfg"] = data
    return data

'''
def validate_id_token(id_token: str):
    cfg = _get_openid_config()
    jwks_uri = cfg["jwks_uri"]
    if jwks_uri not in _jwk_cache:
        _jwk_cache[jwks_uri] = PyJWKClient(jwks_uri)
    signing_key = _jwk_cache[jwks_uri].get_signing_key_from_jwt(id_token).key
    try:
        claims = jwt.decode(
            id_token,
            signing_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            options={"verify_exp": True}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido.")
    email = claims.get("preferred_username") or claims.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="No se encontró email en el token.")
    return email
'''