import asyncio


async def send_one():
    n = 0
    while True:
        n += 1
        await asyncio.sleep(1)
        print(f'Прошло {n} сек.')


async def send_three():
    while True:
        await asyncio.sleep(3)
        print(f'Прошло еще 3 сек.')


async def main():
    task1 = asyncio.create_task(send_one())
    task2 = asyncio.create_task(send_three())

    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
