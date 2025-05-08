# HTTP Server (AsyncIO)
import asyncio
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "World")
    # Simulate I/O operation
    await asyncio.sleep(0.1)
    # Simulate CPU-bound operation
    data = {k: v for k, v in request.query.items()}
    return web.json_response({
        "message": f"Hello, {name}!",
        "query_params": data,
        "status": "success"
    })

async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/{name}', handle)
    return app

async def run_async_http_server():
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("Async HTTP Server running at http://localhost:8080")
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(run_async_http_server())