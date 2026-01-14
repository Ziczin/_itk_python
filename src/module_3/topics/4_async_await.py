import asyncio


async def example():
    print("Асинхронная функция начала работу")
    await asyncio.sleep(1)
    print("Асинхронная функция завершила работу")


asyncio.run(example())
