# app/config.py
import os

# === Autenticación Microsoft Graph ===
BACKEND_TENANT_ID = os.getenv("MS_TENANT_ID")
BACKEND_CLIENT_ID = os.getenv("MS_CLIENT_ID") or os.getenv("CLIENT_ID")
BACKEND_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
BACKEND_REDIRECT_URI = os.getenv("ENV_REDIRECT_URI")


GRAPH_SCOPE = os.environ.get(
    "GRAPH_SCOPE", 
    "User.Read Approvals.Read.All Sites.ReadWrite.All"
).split()

# === SharePoint ===
SITE_ID = os.environ.get("SITE_ID")
DRIVE_ID = os.environ.get("DRIVE_ID")

# === General ===
OUTPUT_FILENAME = os.environ.get("OUTPUT_FILENAME", "approvals.csv")
CLEAN_OUTPUT_FILENAME = os.environ.get("CLEAN_OUTPUT_FILENAME", "datos_completos_power_bi.csv")

TARGET_USER_ID = os.environ.get("APPROVALS_USER_ID")
#TARGET_USER_EMAIL = os.environ.get("APPROVALS_USER_EMAIL")

POWERBI_REPORT_URL = os.environ.get(
    "POWERBI_REPORT_URL",
    "https://app.powerbi.com/groups/me/reports/ad626174-0c20-4536-93b5-46e5a198a061/f583d9fad842f89f238e?ctid=9f119962-8c62-431c-a8ef-e7e0a42d11fc&experience=power-bi"
)

FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:8080")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
