from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import jwt
from models import User

config_credentials = dict(dotenv_values(".env"))
conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(email: list, user_instance: User):

    token_data = {"id": user_instance.id, "username": user_instance.username}

    token = jwt.encode(token_data, config_credentials["SECRET"])

    template = ""
    with open("email_template.html") as f:
        template = f.read()
        template = template.replace("{token}", token)

    message = MessageSchema(
        subject="Biblio Account Verification Mail",
        recipients=email,
        body=template,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
