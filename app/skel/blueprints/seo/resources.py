import datetime
from urllib.parse import urlparse

from flask import Flask, Response, current_app, make_response, render_template, request

EXCEPTIONS = ["/admin", "/user", "/sitemap", "/logout"]


def get_static_urls(app: Flask, host_base: str) -> list[dict[str, str]]:
    """Return all static urls from app registered rules."""
    static_urls = []

    for rule in app.url_map.iter_rules():
        if any(str(rule).startswith(s) for s in EXCEPTIONS):
            continue

        if "GET" in rule.methods and len(rule.arguments) == 0:
            static_urls.append({"loc": f"{host_base}{str(rule)}"})

    return static_urls


def get_dynamic_urls(app: Flask, host_base: str) -> list[dict[str, str]]:
    """Return dynamic urls. To be used if the project has models with dynamic URLs, such as a blog."""
    dynamic_urls = []

    for path, lastmod in []:  # Replace [] with dynamic models data, if any
        dynamic_urls.append(
            {
                "loc": f"{host_base}/{path}",
                "lastmod": lastmod.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )

    return dynamic_urls


def make_sitemap() -> Response:
    """Make the sitemap and provide it as an HTTP reponse object."""

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    xml_sitemap = render_template(
        "sitemap.xml",
        static_urls=get_static_urls(current_app, host_base),
        dynamic_urls=get_dynamic_urls(current_app, host_base),
        host_base=host_base,
    )

    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response
