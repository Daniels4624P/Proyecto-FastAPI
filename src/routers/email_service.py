from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

async def send_email(to_email: str, subject: str ,body: str):
    msg = MIMEMultipart()
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["From"] = "gola2010sa@gmail.com"

    msg.attach(MIMEText(body, "plain"))

    await aiosmtplib.send(msg, hostname= "smtp.gmail.com", port=587, username="gola2010sa@gmail.com", password="yvammjotufcmquai", use_tls=True)

    