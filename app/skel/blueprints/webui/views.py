from flask import current_app, render_template
from flask_simplelogin import login_required


def index() -> str:
    """Renders the main page."""
    return render_template("index.html", app_config=current_app.config)


@login_required
def admin() -> str:
    """Renders the admin page."""

    return render_template("admin.html", logout="simplelogin.logout")
