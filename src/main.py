import logging, io, csv
from utils import setup_logging
from token_provider import get_access_token
from api_client import get_my_profile
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

    csv_bytes = _profile_to_csv_bytes(profile)
    log.info("Enviando perfil por correo...")
    send_mail_with_attachment(csv_bytes)
    log.info("Correo enviado con la información del perfil.")

if __name__ == "__main__":
    main()
