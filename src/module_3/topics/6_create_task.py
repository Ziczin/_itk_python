import asyncio


async def fetch_data():
    print("Получение данных...")
    await asyncio.sleep(1)
    print("Данные получены")


async def main():
    task = asyncio.create_task(fetch_data())
    print("Продолжаем выполнять другие задачи")
    await task


asyncio.run(main())
