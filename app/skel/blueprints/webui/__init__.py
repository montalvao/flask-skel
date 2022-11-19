from flask import Blueprint, Flask

from .views import index

BP_NAME = "webui"

static_url_path = f"/{BP_NAME}/static"

bp = Blueprint(
    BP_NAME,
    __name__,
    static_folder="static",
    static_url_path=static_url_path,
    template_folder="templates",
)

bp.add_url_rule("/", view_func=index)


def init_app(app: Flask) -> None:
    """Registers the 'webui' blueprint"""
    app.register_blueprint(bp)
