import requests, os
from config import SITE_ID, DRIVE_ID

def upload_to_sharepoint(token, file_path):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "text/csv"
    }
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root:/{filename}:/content"
        r = requests.put(url, headers=headers, data=f)
    if r.status_code not in (200, 201):
        raise Exception(f"Upload failed: {r.text}")
