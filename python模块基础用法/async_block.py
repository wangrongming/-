import asyncio


async def hello():
    print("Hello world!")
    await asyncio.sleep(1)
    print("Hello again!")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

