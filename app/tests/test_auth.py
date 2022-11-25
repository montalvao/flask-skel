from skel.extensions.auth import is_logged_in

ADMIN_TEST_CREDENTIALS = {"username": "test_admin", "password": "test_password_admin"}
ADMIN_TEST_WRONG_CREDENTIALS = {"username": "wrong", "password": "test_password_wrong"}


def test_admin_login_requires_token(app, client):
    response = client.post(
        app.url_for("simplelogin.login"), data=ADMIN_TEST_CREDENTIALS
    )
    assert response.status_code == 200
    assert "csrf_token The CSRF token is missing" in str(response.data)


def test_admin_login_requires_valid_token(app, client):
    response = client.post(
        app.url_for("simplelogin.login"),
        data=dict(**ADMIN_TEST_CREDENTIALS, csrf_token="invalid"),
    )
    assert response.status_code == 200
    assert "csrf_token The CSRF token is invalid" in str(response.data)


def test_admin_login_redirection(app, client):
    response = client.get(app.url_for("webui.admin"), follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.history[0].status_code == 302
    assert response.request.path == app.url_for("simplelogin.login")


def test_admin_login_logout_sucessful(app, csrf_token_for):
    assert is_logged_in() is False
    with app.test_client() as test_client:
        test_client.get(app.url_for("simplelogin.login"))
        response = test_client.post(
            app.url_for("simplelogin.login", next=app.url_for("webui.admin")),
            data=dict(
                **ADMIN_TEST_CREDENTIALS,
                csrf_token=csrf_token_for(app),
            ),
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.history[0].status_code == 302
        assert response.request.path == app.url_for("webui.admin")
        assert is_logged_in() is True
        test_client.get(app.url_for("simplelogin.logout"))
        assert is_logged_in() is False


def test_admin_login_unsucessful(app, csrf_token_for):
    assert is_logged_in() is False
    with app.test_client() as test_client:
        test_client.get(app.url_for("simplelogin.login"))
        response = test_client.post(
            app.url_for("simplelogin.login"),
            data=dict(
                **ADMIN_TEST_WRONG_CREDENTIALS,
                csrf_token=csrf_token_for(app),
            ),
            follow_redirects=True,
        )
        assert response.status_code == 401
    assert is_logged_in() is False
