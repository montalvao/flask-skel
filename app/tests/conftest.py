import pytest

from skel.app import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app(force_env="testing")
    return app


@pytest.fixture(scope="module")
def simple_routes(app):
    return [str(r) for r in app.url_map.iter_rules() if "<" not in str(r)]
