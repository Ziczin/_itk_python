import asyncio


async def hello():
    print("Привет!")
    await asyncio.sleep(2)
    print("Прошло 2 секунды!")


async def main():
    await hello()


asyncio.run(main())
