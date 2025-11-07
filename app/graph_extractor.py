import requests, os
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET

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
