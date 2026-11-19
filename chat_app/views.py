import flask
import smtplib
import werkzeug.security
from chat_app.models import User
from chat_app.mail import send_code


def render_reg():

    if flask.request.method == "POST":
        email = flask.request.form.get("email", "").strip()
        password = flask.request.form.get("password")
        confirm_password = flask.request.form.get("confirm_password")

        if email and password and confirm_password:
            if password != confirm_password:
                data = {
                    "error": "Паролі не співпадають",
                    "email": email
                }
                return flask.render_template("registration.html", **data)

            # Перевіряємо, що такої пошти ще немає в БД
            if User.query.filter_by(email = email).scalar():
                data = {
                    "error": "Користувач з такою поштою вже існує",
                    "email": email
                }
                return flask.render_template("registration.html", **data)

            try:
                send_code(email)

            except (smtplib.SMTPException, OSError, RuntimeError) as error:
                print(f"Помилка надсилання листа: {error}")
                data = {
                    "error": "Не вдалося надіслати лист. Перевірте пошту та спробуйте ще раз",
                    "email": email
                }
                return flask.render_template("registration.html", **data)

            flask.session["reg_email"] = email
            flask.session["reg_password_hash"] = werkzeug.security.generate_password_hash(password)

            data = {
                "success": f"Код підтвердження надіслано на {email}",
                "email": email
            }
            return flask.render_template("registration.html", **data)

        else:
            data = {
                "error": "Заповніть усі поля",
                "email": email
            }
            return flask.render_template("registration.html", **data)

    return flask.render_template("registration.html")