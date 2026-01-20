from aiohttp import ClientSession


async def app(scope, receive, send):
    if scope["type"] == "http":
        async with (
            ClientSession(
                # timeout=ClientTimeout(total=10)
            ) as session
        ):
            async with session.get(
                "https://api.exchangerate-api.com/v4/latest/USD"
            ) as resp:
                body = await resp.read()
                await send(
                    {
                        "type": "http.response.start",
                        "status": 200,
                        "headers": [
                            [b"content-type", b"application/json"],
                            [b"content-length", str(len(body))],
                        ],
                    }
                )

                await send({"type": "http.response.body", "body": body})
