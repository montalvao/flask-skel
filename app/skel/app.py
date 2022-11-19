from flask import Flask

from .extensions.config import init_app, load_extensions


def create_minimal_app(**config) -> Flask:
    """Create a minimal app, suited for testing."""
    app = Flask(__name__)
    init_app(app, **config)

    return app


def create_app(**config) -> Flask:
    """Configure the created app to be fully functional."""
    app = create_minimal_app(**config)
    load_extensions(app.config)

    return app
