import pytest

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
