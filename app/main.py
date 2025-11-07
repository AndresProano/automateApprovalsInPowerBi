from graph_extractor import get_access_token, get_approvals
from csv_transformer import to_csv
from sharepoint_uploader import upload_to_sharepoint
import os
from config import SITE_ID, DRIVE_ID

def main():
    token = get_access_token()
    approvals = get_approvals(token)
    csv_path = to_csv(approvals, "approvals.csv")

    # Ejecuta tu script adicional de organización
    os.system("python app/limpiezaDatos.py approvals.csv approvals_cleaned.csv")

    upload_to_sharepoint(
        token,
        "approvals.csv",
        SITE_ID,
        DRIVE_ID
    )

if __name__ == "__main__":
    main()
