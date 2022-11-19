from dynaconf import FlaskDynaconf
from dynaconf.contrib import DynaconfConfig
from flask import Flask


def init_app(app: Flask, **config) -> None:
    """Adds FlaskDynaconf to the app instance."""
    FlaskDynaconf(app, environments=True, **config)


def load_extensions(app_config) -> None:
    """Load extensions into the app instance."""
    if not isinstance(app_config, DynaconfConfig):
        raise TypeError("app_config must be a DynaconfConfig instance.")

    app_config.load_extensions()
