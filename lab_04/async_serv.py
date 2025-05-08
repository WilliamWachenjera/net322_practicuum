import asyncio
from datetime import datetime

async def handle_request(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r} at {datetime.now()}")

    try:
        response = writer.recv(1024)
    except Exception as e:
        print(f"Error occured as {e}")

    # Simulate I/O-bound operation
    await asyncio.sleep(1)
    
    # Simulate CPU-bound operation (not ideal in pure async)
    result = sum(i*i for i in range(10000))
    
    response = f"Processed {message}. Result: {result}"
    writer.write(response.encode())
    await writer.drain()
    writer.close()

async def async_server():
    server = await asyncio.start_server(
        handle_request, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(async_server())