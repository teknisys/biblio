from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
import jwt
from models import User

config_credentials = dict(dotenv_values(".env"))


class EmailSchema(BaseModel):
    email: EmailStr


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = config_credentials["EMAIL"]
password = config_credentials["PASS"]


async def send_email(email: str, user_instance: User):
    token_data = {"id": user_instance.id, "username": user_instance.username}
    token = jwt.encode(token_data, config_credentials["SECRET"])
    template = ""
    with open("email_template.html") as f:
        template = f.read()
        template = template.replace("{token}", token)

    template = MIMEText(template, "html")
    message = MIMEMultipart("alternative")
    message["Subject"] = "hello"
    message["From"] = sender_email
    # email is of the form ["hello@world.com"]
    # since we are not sending the same verification token to multiple email addresses, we just take the first email address.
    message["To"] = email[0]
    message.attach(template)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
