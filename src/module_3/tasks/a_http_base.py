import asyncio
import json
import sys
from typing import Dict, List

from aiohttp import ClientError, ClientSession, ClientTimeout


async def fetch_one(
    session: ClientSession, url: str, sem: asyncio.Semaphore, timeout: ClientTimeout
) -> Dict[str, int]:
    async with sem:
        try:
            async with session.get(url, timeout=timeout) as resp:
                return {url: resp.status}

        except asyncio.TimeoutError:
            print(f"{url} -> timeout", file=sys.stderr)
            return {url: 504}

        except ClientError as e:
            print(f"{url} -> client error: {e}", file=sys.stderr)
            return {url: 4004}

        except Exception as e:
            print(f"{url} -> unexpected error: {e}", file=sys.stderr)
            return {url: 0}


async def fetch_urls(urls: List[str], file_path: str) -> Dict[str, int]:
    timeout = ClientTimeout(total=10)
    sem = asyncio.Semaphore(5)
    results: Dict[str, int] = {}

    async with ClientSession(timeout=timeout) as session:
        tasks = [asyncio.create_task(fetch_one(session, u, sem, timeout)) for u in urls]
        for coro in asyncio.as_completed(tasks):
            res = await coro
            results.update(res)

    with open(file_path, "w", encoding="utf-8") as f:
        for url, status in results.items():
            f.write(
                json.dumps({"url": url, "status": status}, ensure_ascii=False) + "\n"
            )

    return results


if __name__ == "__main__":
    urls = [
        "https://nonexistent.url",
        "https://example.com",
        "https://httpbin.org/delay/3",
        "https://httpbin.org/redirect/2",
        "https://httpbin.org/status/500",
        "https://httpbin.org/status/404",
        "https://httpbin.org/get",
        "https://sha1-intermediate.badssl.com/",
        "http://httpbin.org/absolute-redirect/1",
        "https://self-signed.badssl.com/",
        "https://wrong.host.badssl.com/",
        "https://expired.badssl.com/",
        "https://github.com/",
        "https://api.github.com/",
        "https://www.wikipedia.org/",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/invalidendpoint",
        "https://speed.hetzner.de/100MB.bin",
        "https://www.google.com/",
        "https://httpbin.org/stream/5",
        "https://www.example.invalid",
        "https://localhost:8000/",
        "https://httpstat.us/418",
        "https://httpstat.us/200?sleep=5000",
        "https://api.ipify.org?format=json",
    ]

    out = asyncio.run(fetch_urls(urls, "./results.jsonl"))
    print(out)
