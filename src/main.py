import datetime
import io
import logging
import os
import pathlib
import csv

from utils import setup_logging
from token_provider import get_access_token
from api_client import get_my_profile, upload_file_to_sharepoint
from mailer import send_mail_with_attachment

setup_logging()
log = logging.getLogger("main")

def _profile_to_csv_bytes(profile: dict) -> bytes:
    """Serializa campos relevantes del perfil a un CSV simple."""
    fields = [
        "id",
        "displayName",
        "userPrincipalName",
        "mail",
        "jobTitle",
        "businessPhones",
        "mobilePhone",
        "officeLocation",
    ]
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(fields)

    row = []
    for field in fields:
        value = profile.get(field, "")
        if isinstance(value, list):
            value = " | ".join(str(v) for v in value)
        row.append(value if value is not None else "")
    writer.writerow(row)
    return buf.getvalue().encode("utf-8")

def main():
    token = get_access_token()
    log.info("Token listo; consultando Graph /me...")
    profile = get_my_profile(token)
    log.info(
        "Perfil obtenido: %s (%s)",
        profile.get("displayName"),
        profile.get("userPrincipalName"),
    )

    site_id = os.environ["SHAREPOINT_SITE_ID"]
    drive_id = os.environ["SHAREPOINT_DRIVE_ID"]
    folder_path = os.environ.get("SHAREPOINT_FOLDER_PATH", "")
    output_dir = pathlib.Path(os.environ.get("OUTPUT_DIR", "/app/tmp"))
    output_dir.mkdir(parents=True, exist_ok=True)

    fecha_actual = datetime.strftime("%Y-%m-%d")
    csv_bytes = _profile_to_csv_bytes(profile)

    filename = f"Approvals_{fecha_actual}.csv"
    file_path = output_dir / filename
    file_path.write_bytes(csv_bytes)
    log.info("Archivo temporal generado: %s", file_path)

    upload_file_to_sharepoint(
        token=token,
        site_id=site_id,
        drive_id=drive_id,
        folder_path=folder_path,
        filename=filename,
        file_bytes=csv_bytes,
    )
    log.info("Archivo %s cargado a SharePoint mediante Graph.", filename)

if __name__ == "__main__":
    main()
