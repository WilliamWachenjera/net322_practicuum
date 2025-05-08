import asyncio
import hashlib
from typing import List, Dict, Tuple
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.clients  : List[asyncio.StreamWriter] = []
        self.message_history : List[Tuple[str, str, datetime]] = []  # (client_hash, message, timestamp)
        self.lock = asyncio.Lock()
        self.client_names : Dict[str, str] = {}  # client_hash -> display name
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        ip, port = addr
        client_hash = hashlib.sha1(f"{ip} : {port}".encode()).hexdigest()[:8]
        
        async with self.lock:
            self.clients.append(writer)
            # Send welcome message and history to new client
            welcome_msg = f"Welcome to the chat! Your ID: {client_hash}\nEnter close() or quit() or exit() to close the connection!"
            writer.write(welcome_msg.encode())
            await writer.drain()
            
            # Send message exchange history
            if self.message_history:
                history_header = "\n---Start of Message History ---\n"
                writer.write(history_header.encode())
                for hash_, msg, timestamp in self.message_history:
                    display_name = self.client_names.get(hash_, hash_)
                    formatted = f"[{timestamp.strftime('%H:%M:%S')}] {display_name}: {msg}\n"
                    writer.write(formatted.encode())
                writer.write("--- End of History ---\n\n".encode())
                await writer.drain()
        
        print(f"New connection: {addr} as {client_hash}")
        
        try:
            while True:
                try:
                    # Add timeout for idle clients (300 seconds = 5 minutes)
                    data = await asyncio.wait_for(reader.read(1024), timeout=300)
                    if not data:
                        break
                    
                    message = data.decode().strip()
                    if not message:
                        continue
                        
                    if message.lower() in ("quit()", "close()", "exit()"):
                        print(f"Client {client_hash} requested disconnection!")
                        break
                    
                    timestamp = datetime.now()
                    display_name = self.client_names.get(client_hash, client_hash)
                    formatted = f"[{timestamp.strftime('%H:%M:%S')}] {display_name}: {message}\n"
                    
                    # Add to history before broadcasting
                    async with self.lock:
                        self.message_history.append((client_hash, message, timestamp))
                        if len(self.message_history) > 100:  # Keep last 100 messages
                            self.message_history.pop(0)
                    
                    await self.broadcast(formatted, sender=writer)
                    
                except asyncio.TimeoutError:
                    print(f"Client {client_hash} disconnected due to inactivity")
                    break
                    
        except (ConnectionError, asyncio.CancelledError) as e:
            print(f"Client {client_hash} disconnected: {e}")
        finally:
            async with self.lock:
                if writer in self.clients:
                    self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()
            print(f"Connection closed: {client_hash}")
    
    async def broadcast(self, message: str, sender: asyncio.StreamWriter):
        async with self.lock:
            clients_copy = self.clients.copy()
        
        tasks = []
        for client in clients_copy:
            try:
                client.write(message.encode())
                tasks.append(client.drain())
            except ConnectionError:
                async with self.lock:
                    if client in self.clients:
                        self.clients.remove(client)
                client.close()
                await client.wait_closed()
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self, host: str = '127.0.0.1', port: int = 12345):
        server = await asyncio.start_server(
            self.handle_client, host, port
        )
        
        print(f"Server running on {host} : {port}")
        print("Press Ctrl+C to stop the server")
        
        async with server:
            try:
                await server.serve_forever()
            except asyncio.CancelledError:
                print("\nServer is shutting down...")
                # Close all client connections
                async with self.lock:
                    for writer in self.clients:
                        writer.close()
                        await writer.wait_closed()
                print("All connections closed.")

if __name__ == "__main__":
    try:
        server = ChatServer()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\nServer shutdown complete.")