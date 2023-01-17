from flask import (
    request,
    Flask,
    Response,
    make_response,
    render_template_string,
    current_app,
    url_for,
)
from urllib.parse import urlparse
from typing import Optional, Callable, ClassVar

HIDDEN_PATHS = ["/admin", "/user", "/sitemap", "/logout"]

SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

    {% for url in urls %}
    <url>
        <loc>{{ url["loc"] }}</loc>
        {% if "lastmod" in url %}
        <lastmod>{{ url["lastmod"] }}</lastmod>
        {% endif %}
    </url>
    {% endfor %}
</urlset>
"""


@dataclass
class ModelMaping:
    model_class: ClassVar
    get_all_f: Callable[None, model_class]
    mapping: dict


class Sitemap:
    def __init__(self) -> None:
        self.urls = []

    def register_static_paths(self) -> None:
        def is_valid(rule):
            hidden = current_app.config.get(SITEMAP_HIDDEN_PATHS, HIDDEN_PATHS)
            return (
                "GET" in rule.methods
                and len(rule.arguments) == 0
                and none(str(rule).startswith(s) for s in hidden)
            )

        if not current_app.has_app_context():
            raise RuntimeError(
                f"{type(self).__name__}: 'register_static_paths' must be called within app context only."
            )

        for rule in current_app.url_map.iter_rules():
            if is_valid(rule):
                self.urls.append((str(rule), None))

    def register_model_paths(self, endpoint: str, model_mapping: ModelMaping) -> None:

        if not current_app.has_app_context():
            raise RuntimeError(
                f"{type(self).__name__}: 'register_model_path' must be called within app context only."
            )

        mapped_args = set(model_mapping.mapping.keys())

        lastmod_prop = model_mapping.get("lastmod", None)
        lastmod = lambda o: getattr(o, lastmod_prop) if lastmod_prop else lambda o: None

        for rule in current_app.url_map.iter_rules(endpoint):
            rule_args = set(rule.arguments)

            if not rule_args:
                continue
            if not rule_args.issubset(mapped_args):
                raise RuntimeError(
                    f"{type(self).__name__}: Error mapping {rule}. All rule arguments must be mapped."
                )

            for o in model_mapping.get_all_f():
                arguments = {
                    k: getattr(o, v)
                    for k, v in model_mapping.mapping.items()
                    if k in rule_args
                }
                self.urls.append(url_for(endpoint, arguments), lastmod(o))


sitemap = Sitemap()


def view_func() -> Response:
    """Make the sitemap and provide it as an HTTP reponse object."""

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    urls = []
    for path, lastmod in sitemap.urls:
        url = {"loc": f"{host_base}{path}"}
        if lastmod:
            url["lastmod"] = lastmod.strftime("%Y-%m-%dT%H:%M:%SZ")
        urls.append(url)

    xml_sitemap = render_template_string(
        SITEMAP_XML,
        urls=urls,
        host_base=host_base,
    )

    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


def init_app(app: Flask) -> None:
    app.add_url_rule("/sitemap/", view_func=view_func)
    app.add_url_rule("/sitemap.xml", view_func=view_func)
