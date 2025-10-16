import os, json, time, pathlib
import msal

TENANT_ID  = os.environ.get("TENANT_ID")
CLIENT_ID  = os.environ.get("CLIENT_ID")
SCOPE      = os.environ.get("SCOPE", "https://graph.microsoft.com/.default")
AUTHORITY  = f"https://login.microsoftonline.com/{TENANT_ID}"
CACHE_DIR  = os.environ.get("TOKEN_CACHE_DIR", "/.token_cache")  # montar como volumen
CACHE_PATH = str(pathlib.Path(CACHE_DIR) / "msal.bin")

def _looks_like_jwt(tok: str) -> bool:
    return isinstance(tok, str) and tok.count(".") == 2

def _is_expired_or_near(exp_ts: int, skew: int = 60) -> bool:
    return int(time.time()) >= (int(exp_ts) - skew)

def _parse_jwt_exp(tok: str) -> int | None:
    try:
        import base64, json
        payload_b64 = tok.split(".")[1] + "==="
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        return int(payload.get("exp"))
    except Exception:
        return None

def get_access_token() -> str:
    # 1) ACCESS_TOKEN directo
    env_tok = os.environ.get("ACCESS_TOKEN")
    if env_tok:
        # Opcional: advertir si está por vencer
        exp = _parse_jwt_exp(env_tok)
        if exp and _is_expired_or_near(exp):
            raise RuntimeError("ACCESS_TOKEN vencido o por expirar; vuelve a proporcionarlo o usa DEVICE_CODE=1")
        return env_tok

    # 2) Device Code (public client)
    if os.environ.get("DEVICE_CODE") == "1":
        cache = msal.SerializableTokenCache()
        try:
            if os.path.exists(CACHE_PATH):
                cache.deserialize(open(CACHE_PATH, "r").read())
        except Exception:
            pass

        app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)
        accounts = app.get_accounts()
        # Intento silencioso si hay cache
        if accounts:
            result = app.acquire_token_silent([SCOPE], account=accounts[0])
            if result and "access_token" in result:
                return result["access_token"]

        # Disparar device flow
        flow = app.initiate_device_flow(scopes=[SCOPE])
        if "user_code" not in flow:
            raise RuntimeError("No se pudo iniciar device flow")
        print(f"👉 Abre {flow['verification_uri']} y escribe el código: {flow['user_code']}")
        result = app.acquire_token_by_device_flow(flow)
        if "access_token" not in result:
            raise RuntimeError(result.get("error_description", "No access token"))
        # Persistir cache
        pathlib.Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
        open(CACHE_PATH, "w").write(cache.serialize())
        return result["access_token"]

    # 3) Client credentials (si hay secret)
    client_secret = os.environ.get("CLIENT_SECRET")
    if client_secret:
        app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=client_secret)
        result = app.acquire_token_for_client(scopes=[SCOPE])
        if "access_token" not in result:
            raise RuntimeError(result.get("error_description", "No access token (client_credentials)"))
        return result["access_token"]

    raise RuntimeError("No token method configured. Proporciona ACCESS_TOKEN, o DEVICE_CODE=1, o CLIENT_SECRET.")