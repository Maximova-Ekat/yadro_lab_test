import pytest
import requests

@pytest.mark.parametrize(
    "path, expected_status",
    [
        ("/index.html", 200),
        ("/nonexistent", 404),
    ],
)
def test_http_pages(target_config, path, expected_status):
    """HTTP тесты для /index и 404 страницы"""
    host = target_config["host"]
    port = target_config["http_port"]
    timeout = target_config["http_timeout"]
    url = f"http://{host}:{port}{path}"

    try:
        with requests.get(url, timeout=timeout) as resp:
            assert resp.status_code == expected_status, f"{url} returned {resp.status_code}"
            if expected_status == 200:
                assert "Hello from Apache" in resp.text
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")