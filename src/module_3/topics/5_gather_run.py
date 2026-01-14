import asyncio


async def fetch_data_1():
    await asyncio.sleep(1)
    print("Данные 1 получены")


async def fetch_data_2():
    await asyncio.sleep(2)
    print("Данные 2 получены")


async def fetch_both():
    await asyncio.gather(fetch_data_1(), fetch_data_2())


asyncio.run(fetch_both())
