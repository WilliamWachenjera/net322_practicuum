# HTTP Client (AsyncIO)
import aiohttp
import asyncio

async def fetch(session, url, params=None):
    async with session.get(url, params=params) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        # Simple request
        response = await fetch(session, 'http://localhost:8080/')
        print("Response 1:", response)
        
        # Request with path parameter
        response = await fetch(session, 'http://localhost:8080/Alice')
        print("Response 2:", response)
        
        # Request with query parameters
        params = {'param1': 'value1', 'param2': 'value2'}
        response = await fetch(session, 'http://localhost:8080/Bob', params)
        print("Response 3:", response)

if __name__ == '__main__':
    asyncio.run(main())