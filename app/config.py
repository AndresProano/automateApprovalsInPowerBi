# app/config.py
import os

# === Autenticación Microsoft Graph ===
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT_ID = os.environ.get("TENANT_ID")
GRAPH_SCOPE = os.environ.get("GRAPH_SCOPE", "https://graph.microsoft.com/.default")
TARGET_USER_ID = os.environ.get("APPROVALS_USER_ID")

# === SharePoint ===
SITE_ID = os.environ.get("SITE_ID")
DRIVE_ID = os.environ.get("DRIVE_ID")

# === General ===
OUTPUT_FILENAME = os.environ.get("OUTPUT_FILENAME", "approvals.csv")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# === Validación mínima ===
required = {
    "CLIENT_ID": CLIENT_ID,
    "CLIENT_SECRET": CLIENT_SECRET,
    "TENANT_ID": TENANT_ID,
    "SITE_ID": SITE_ID,
    "DRIVE_ID": DRIVE_ID,
    "APPROVALS_USER_ID": TARGET_USER_ID
}

missing = [key for key, val in required.items() if not val]
if missing:
    raise EnvironmentError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
