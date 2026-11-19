import os
import random
import smtplib
from email.message import EmailMessage
from chat_app.models import MailSettings


IMAGE_PATH = os.path.join(os.path.dirname(__file__), "static", "img", "small_illustration.png")
IMAGE_CID = "<small_illustration@worldit>"

def send_code(to_email):
    settings = MailSettings.query.first()

    if settings is None:
        raise RuntimeError("SMTP не налаштовано в БД. Додайте рядок у таблицю mail_settings")

    message = EmailMessage()
    message["Subject"] = "Код підтвердження World IT"
    message["From"] = settings.email
    message["To"] = to_email

    message.set_content("Вас вітає команда World IT! Підтвердіть свою пошту, щоб завершити реєстрацію.")

    message.add_alternative(
            f"""\
    <html>
    <body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; color: #000;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                style="width: 100%; border: 1px solid #999; border-radius: 12px;
                        border-collapse: separate;">
        <tr>
            <td align="center" style="padding: 32px 12px;">
            <table role="presentation" width="540" cellpadding="0" cellspacing="0" border="0"
                    style="max-width: 540px; width: 100%;">
            <tr><td style="padding: 0;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                <td style="padding-bottom: 20px;">
                    <h1 style="margin: 0; font-size: 26px; font-weight: bold; color: #000;">
                    Вас вітає команда World IT !
                    </h1>
                </td>
                </tr>
                <tr>
                <td style="padding-bottom: 16px; font-size: 16px; line-height: 1.4; color: #000;">
                    Щоб завершити реєстрацію та переконатися, що саме ви є власником
                    цієї електронної адреси, будь ласка, підтвердіть свою пошту.
                </td>
                </tr>
                <tr>
                <td style="padding-bottom: 24px;">
                    <a href="#"
                    style="display: block; background-color: #050a1c; color: #ffffff;
                            text-align: center; text-decoration: none; font-size: 15px;
                            padding: 12px 0; border-radius: 4px;">
                    Підтвердити пошту
                    </a>
                </td>
                </tr>
                <tr>
                <td align="center" style="padding-bottom: 24px; border-bottom: 1px solid #ddd;">
                    <img src="cid:{IMAGE_CID[1:-1]}" width="340" alt="World IT"
                        style="display: block; width: 340px; max-width: 100%; height: auto; border: 0;">
                </td>
                </tr>
                <tr>
                <td style="padding-top: 12px; font-size: 14px; line-height: 1.4; color: #000;">
                    Якщо у вас виникнуть питання — ми завжди раді допомогти!<br>
                    З найкращими побажаннями, команда World IT Academy
                </td>
                </tr>
            </table>
            </td></tr>
            </table>
            </td>
        </tr>
        </table>
    </body>
    </html>
    """,
            subtype = "html"
        )

    with open(IMAGE_PATH, "rb") as image_file:
        message.get_payload()[-1].add_related(
            image_file.read(),
            maintype = "image",
            subtype = "png",
            cid = IMAGE_CID,
            filename = "small_illustration.png",
            disposition = "inline"
        )
    
    if settings.port == 465:
        with smtplib.SMTP_SSL(settings.host, settings.port, timeout = 20) as server:
            server.login(settings.email, settings.password)
            server.send_message(message)
    else:
        with smtplib.SMTP(settings.host, settings.port, timeout = 20) as server:
            server.starttls()
            server.login(settings.email, settings.password)
            server.send_message(message)