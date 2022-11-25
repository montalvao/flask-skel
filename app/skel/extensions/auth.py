from flask import Flask
from flask_simplelogin import SimpleLogin, is_logged_in

_sl = SimpleLogin()


def init_app(app: Flask) -> None:
    """Initialize the app using Flask Simple Login."""

    _sl.init_app(app)
