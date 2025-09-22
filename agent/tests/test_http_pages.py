import pytest
import requests


def validate_index_page(resp: requests.Response):
    """Проверка корректности страницы index"""
    # Проверка заголовков
    content_type = resp.headers.get("Content-Type", "")
    assert "text/html" in content_type, f"Unexpected Content-Type: {content_type}"

    # Проверка содержимого
    text = resp.text
    assert "<title>Test Page</title>" in text, "Missing or incorrect <title>"
    assert "<h1>Hello from Apache!" in text, "Missing expected header text"


@pytest.mark.parametrize(
    "path, expected_status, validator",
    [
        ("/index.html", 200, validate_index_page),
        ("/nonexistent", 404, None),
    ],
)
def test_http_pages(target_config, path, expected_status, validator):
    """HTTP тесты для index и 404 страницы"""
    host = target_config["host"]
    port = target_config["http_port"]
    timeout = target_config["http_timeout"]
    url = f"http://{host}:{port}{path}"

    try:
        resp = requests.get(url, timeout=timeout)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    # Проверка статус-кода
    assert resp.status_code == expected_status, (
        f"{url} returned {resp.status_code}, expected {expected_status}. "
        f"Body snippet: {resp.text[:100]}"
    )

    # Дополнительная валидация (для 200 OK)
    if validator:
        validator(resp)