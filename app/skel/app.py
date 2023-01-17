from flask import Flask

from .extensions.config import init_app, load_extensions
from .extensions.flask_sitemap import sitemap


def create_minimal_app(**config) -> Flask:
    """Create a minimal app, suited for testing."""
    app = Flask(__name__)
    init_app(app, **config)

    return app


def create_app(**config) -> Flask:
    """Configure the created app to be fully functional."""
    app = create_minimal_app(**config)
    load_extensions(app.config)

    # Favicon: this works only when the app is in the root path
    @app.route("/favicon.ico")
    def favicon():
        """Send favicon (older browsers and direct url requests)."""
        return app.send_static_file("favicon.ico")

    sitemap.register_urls_from(app)

    return app
