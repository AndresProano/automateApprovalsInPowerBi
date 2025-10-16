import os, smtplib, ssl
from email.message import EmailMessage
from datetime import datetime, timezone

def send_mail_with_attachment(csv_bytes: bytes):
    msg = EmailMessage()
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = os.environ["MAIL_TO"]
    subj = os.environ.get("MAIL_SUBJECT","Approvals CSV")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    msg["Subject"] = f"{subj} {ts}"
    msg.set_content("Adjunto el CSV de approvals.\n")

    filename = f"approvals_{ts}.csv"
    msg.add_attachment(csv_bytes, maintype="text", subtype="csv", filename=filename)

    host = os.environ["SMTP_HOST"]; port = int(os.environ["SMTP_PORT"])
    user = os.environ["SMTP_USER"]; pwd = os.environ["SMTP_PASS"]

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as s:
        s.starttls(context=context)
        s.login(user, pwd)
        s.send_message(msg)