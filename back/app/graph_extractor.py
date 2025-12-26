import requests, os, re
from fastapi import HTTPException

GRAPH_URL = "https://graph.microsoft.com/beta/solutions/approval/approvalItems"

def fetch_approvals_from_graph(access_token: str):

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is required")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "ConsistencyLevel": "eventual"
    }

    url = GRAPH_URL
    items = []

    while url:
        r = requests.get(url, headers=headers)
        
        if r.status_code != 200:
            print(f"ERROR DETALLADO: {r.text}")
            raise Exception(f"Graph error: {r.status_code}: {r.text}")

        data = r.json()

        items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")  # paginación
        print (items)

    print(f"--- Se encontraron {len(items)} aprobaciones ---")

    return items
