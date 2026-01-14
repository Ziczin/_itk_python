import requests


def app(environ, start_response):
    response = requests.get(
        "https://api.exchangerate-api.com/v4/latest/USD", timeout=10
    )

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(response.content))),
        ],
    )

    return iter([response.content])
