import flask
from .settings import main_app
from chat_app.views import render_reg
from chat_app.app import chat_app_blueprint

main_app.add_url_rule(
    rule = "/",
    view_func = lambda: flask.redirect("/reg"),
    endpoint = "index"
)

main_app.add_url_rule(
    rule = "/reg",
    view_func = render_reg,
    methods = ["GET", "POST"]
)


main_app.register_blueprint(blueprint = chat_app_blueprint)
