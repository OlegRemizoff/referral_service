import smtplib
from app.config import settings




async def send_email(receiver, message):
    sender = settings.EMAIL_SENDER 
    password = settings.EMAIL_PASSWORD

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

        return "The message has been sent successefuly!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"