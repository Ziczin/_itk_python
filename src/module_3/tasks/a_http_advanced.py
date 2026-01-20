import asyncio
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

import aiohttp
import orjson
from aiohttp import ClientTimeout


async def fetch_single_url(session, url, semaphore, loop, pool_executor):
    async with semaphore:
        try:
            print(f"Processing: {url}")
            timeout = ClientTimeout(total=60, connect=10, sock_read=30)

            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                text = response.text()

                with pool_executor as pool:
                    data = await loop.run_in_executor(pool, orjson.loads, text)

                return {"url": url, "data": data}

        except asyncio.TimeoutError:
            print(f"Timeout for: {url}")
            return None

        except aiohttp.ClientError as e:
            print(f"Client error for: {url}: {e}")
            return None

        except Exception as e:
            print(f"Error for: {url}: {e}")
            return None


async def main():
    input_file = "urls.txt"
    output_file = "result.jsonl"
    max_concurrent = 5

    loop = asyncio.get_event_loop()
    pool_executor = ProcessPoolExecutor(max_workers=cpu_count())

    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        with open(input_file) as f:
            urls = [line.strip() for line in f if line.strip()]

        tasks = []
        for url in urls:
            task = asyncio.create_task(
                fetch_single_url(session, url, semaphore, loop, pool_executor)
            )
            tasks.append(task)

        with open(output_file, "w") as out_f:
            for task in asyncio.as_completed(tasks):
                try:
                    result = await asyncio.wait_for(task, timeout=70)
                    if result:
                        json_line = {result["url"]: result["data"]}
                        out_f.write(orjson.dumps(json_line, ensure_ascii=False) + "\n")
                        out_f.flush()

                except asyncio.TimeoutError:
                    continue


if __name__ == "__main__":
    asyncio.run(main())
