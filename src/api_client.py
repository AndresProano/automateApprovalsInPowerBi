import requests, logging

log = logging.getLogger(__name__)

def get_my_profile(token: str) -> dict:
    """Obtiene el perfil del usuario asociado al token usando Microsoft Graph /me."""
    url = "https://graph.microsoft.com/v1.0/me"
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    r.raise_for_status()
    data = r.json()
    log.info("Graph /me respondió con displayName=%s", data.get("displayName"))
    return data
