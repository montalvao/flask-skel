import pytest


def test_request_returns_http_404(client):
    response = client.get("/this_path_does_not_exist")
    assert (
        response.status_code == 404
    ), "A request to '/this_path_does_not_exist' should return HTTP 404."


def test_all_simple_routes_return_http_200(client, simple_routes):
    http_200_responses = [True]

    for route in simple_routes:
        status_code = client.get(route, follow_redirects=True).status_code
        print(f"route: {route}, status_code: {status_code}")
        http_200_responses.append(status_code == 200)

    assert all(
        http_200_responses
    ), "One or more simple routes are not returning HTTP 200."
