from flask import Blueprint, Flask

from .resources import make_sitemap

BP_NAME = "seo"

bp = Blueprint(
    BP_NAME,
    __name__,
    template_folder="templates",
)

bp.add_url_rule("/sitemap/", view_func=make_sitemap)
bp.add_url_rule("/sitemap.xml", view_func=make_sitemap)


def init_app(app: Flask) -> None:
    """Registers the 'seo' blueprint"""
    app.register_blueprint(bp)
