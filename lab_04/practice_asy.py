import asyncio
import time

async def name():
    print(f"New time | {time.strftime("%H:%M:%S")}")
    await asyncio.sleep(2)
    print(f"Updated time | {time.strftime("%H:%M:%S")}")

async def surname():
    print(f"Next  Time | {time.strftime("%H:%M:%S")}")
    await asyncio.sleep(5)
    print(f"New Next Time | {time.strftime("%H:%M:%S")}")

async def main():
    await asyncio.gather(name(), surname())

if __name__ == "__main__":
     asyncio.run(main())