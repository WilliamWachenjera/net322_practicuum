# FTP Client (AsyncIO)
import asyncio

class AsyncFTPClient:
    def __init__(self):
        self.reader = None
        self.writer = None

    async def connect(self, host, port):
        host = input("Enter the ftp server ip:")
        port = int(input("Enter the server port number:"))
        self.reader, self.writer = await asyncio.open_connection(host, port)
        print(f"Connected to {host}:{port}")

    async def send_command(self, command):
        self.writer.write(command.encode() + b'\n')
        await self.writer.drain()
        return await self.reader.read(4096)

    async def list_files(self):
        response = await self.send_command('LIST')
        print("Files:", response.decode())

    async def get_file(self, filename):
        response = await self.send_command(f'GET {filename}')
        if response.startswith(b'ERROR'):
            print(response.decode())
        else:
            with open(filename, 'wb') as f:
                f.write(response)
            print(f"Downloaded {filename}")

    async def put_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"File {filename} not found")
            return
            
        response = await self.send_command(f'PUT {filename}')
        if response.decode() == 'READY':
            self.writer.write(content)
            await self.writer.drain()
            response = await self.reader.read(4096)
            print(response.decode())

    async def quit(self):
        await self.send_command('QUIT')
        self.writer.close()
        await self.writer.wait_closed()

async def main():
    client = AsyncFTPClient()
    await client.connect('localhost', 2121)
    
    # Example usage
    await client.list_files()
    await client.put_file('example.txt')  
    await client.list_files()
    await client.get_file('example.txt')
    await client.quit()

if __name__ == '__main__':
    asyncio.run(main())