# FTP Server (AsyncIO)
import asyncio
import os
from pathlib import Path

class AsyncFTPServer:
    def __init__(self, root_dir):
        self.root = Path(root_dir).absolute()
        os.makedirs(self.root, exist_ok=True)

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr}")
        
        try:
            while True:
                command = await reader.read(100)
                if not command:
                    break
                    
                command = command.decode().strip()
                parts = command.split()
                if not parts:
                    continue
                    
                cmd = parts[0].upper()
                
                if cmd == 'LIST':
                    files = [f.name for f in self.root.iterdir()]
                    response = '\n'.join(files) if files else "Empty"
                elif cmd == 'GET':
                    if len(parts) < 2:
                        response = "ERROR: Missing filename"
                    else:
                        file_path = self.root / parts[1]
                        if file_path.exists():
                            with open(file_path, 'rb') as f:
                                content = f.read()
                            writer.write(content)
                            await writer.drain()
                            continue
                        else:
                            response = "ERROR: File not found"
                elif cmd == 'PUT':
                    if len(parts) < 2:
                        response = "ERROR: Missing filename"
                    else:
                        writer.write(b"READY")
                        await writer.drain()
                        data = await reader.read(4096)
                        file_path = self.root / parts[1]
                        with open(file_path, 'wb') as f:
                            f.write(data)
                        response = "OK"
                elif cmd == 'QUIT':
                    response = "BYE"
                    writer.write(response.encode())
                    await writer.drain()
                    break
                else:
                    response = "ERROR: Unknown command"
                    
                writer.write(response.encode())
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"Connection with {addr} closed")

async def run_async_ftp_server():
    server = AsyncFTPServer('ftp_root')
    server_coro = await asyncio.start_server(
        server.handle_client, '127.0.0.1', 2121)
    
    async with server_coro:
        print("Async FTP Server running on port 2121")
        await server_coro.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_async_ftp_server())