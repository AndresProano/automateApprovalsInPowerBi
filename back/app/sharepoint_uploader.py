import requests, os
from app.config import BACKEND_TENANT_ID, BACKEND_CLIENT_ID, BACKEND_CLIENT_SECRET, SITE_ID, DRIVE_ID

def get_app_token():
    url = f"https://login.microsoftonline.com/{BACKEND_TENANT_ID}/oauth2/v2.0/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    body = {
        "grant_type": "client_credentials",
        "client_id": BACKEND_CLIENT_ID,
        "client_secret": BACKEND_CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default" 
    }
    
    response = requests.post(url, headers=headers, data=body)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error obteniendo token: {response.text}")


def upload_to_sharepoint(file_path):
    try: 
        token = get_app_token()
    except Exception as e:
        raise Exception(f"Error obtaining app token: {str(e)}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "csv"
    }
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{filename}:/content"
        r = requests.put(url, headers=headers, data=f)
    if r.status_code not in (200, 201):
        raise Exception(f"Upload failed: {r.text}")
