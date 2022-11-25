import pytest
from flask import session
from itsdangerous import URLSafeTimedSerializer

from skel.app import create_app


def pytest_report_header(config):
    header_text = f"Project skell.app."
    return header_text


@pytest.fixture(scope="session")
def app():
    app = create_app(force_env="testing")
    return app


@pytest.fixture(scope="session")
def simple_routes(app):
    return [str(r) for r in app.url_map.iter_rules() if "<" not in str(r)]


@pytest.fixture
def csrf_token_for():
    """Fixture from the simplelogin example."""

    def generator(app):
        serializer = URLSafeTimedSerializer(
            app.config["SECRET_KEY"], salt="wtf-csrf-token"
        )
        return serializer.dumps(session["csrf_token"])

    return generator
