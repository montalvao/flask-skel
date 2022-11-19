import pytest


def test_app_is_created(app):
    assert (
        app.name == "skel.app"
    ), f"The app name should be 'skel.app', not f'{app.name}'."


# Configuration tests


def test_config_testing_value(config):
    assert config.get("TESTING"), "The app should be in 'TESTING' mode."


def test_config_debugging_value(config):
    assert config.get("DEBUG") is False, "The debug mode should be False during tests."


@pytest.mark.options(debug=True)
def test_config_set_debug_to_true(config):
    assert config.get("DEBUG"), "The test couldn't set the debug mode to True."


def test_config_has_the_extensions_property(config):
    assert (
        "EXTENSIONS" in config
    ), "The app config should have a property called 'EXTENSIONS'."


def test_config_extensions_is_a_populated_list(config):
    assert (
        isinstance(config.get("EXTENSIONS"), list) and config.EXTENSIONS
    ), "The app.config.EXTENSIONS should be a list of extensions."
