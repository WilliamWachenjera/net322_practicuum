import asyncio
import time

async def say_hello():
    print(f"Hello! | {time.strftime("%H:%M:%S")} ")
    await asyncio.sleep(2)
    print(f"Hello again! | {time.strftime("%H:%M:%S")}")

async def say_goodbye():
    print(f"Goodbye! | {time.strftime("%H:%M:%S")}")
    await asyncio.sleep(3)
    print(f"Goodbye again! | {time.strftime("%H:%M:%S")}")

async def main():
    # Run tasks concurrently
    await asyncio.gather(say_hello(), say_goodbye())

if __name__ == "__main__":
    asyncio.run(main())