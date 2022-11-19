from flask import current_app, render_template


def index() -> str:
    """Renders the main page."""
    return render_template("index.html", app_config=current_app.config)
