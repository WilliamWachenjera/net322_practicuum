import asyncio
import logging
import argparse

# Sets up app logging
APP_LOGGER = logging.getLogger(name="TCP ASYNCIO SERVER")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt=logging.Formatter(fmt="[%(levelname)s] %(name)s : %(asctime)s > %(message)s",
                                                   datefmt="%Y-%m-%d %H:%M:%S"))
APP_LOGGER.addHandler(hdlr=logging_handler)

def parse_args():
    parser = argparse.ArgumentParser(description="A simple multithreaded TCP echo server using executor.")
    parser.add_argument("--host", type=str, default="0.0.0.0", 
                        help="Host address to bind to")
    parser.add_argument("--port", type=int,
                        required=True, 
                        help="Port to bind to")
    
    return parser.parse_args()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    APP_LOGGER.debug(f"Connected to {addr}")

    try:
        while True:
            # Read data from the client
            data = await reader.read(100)
            if not data:
                APP_LOGGER.debug(f"Connection closed by {addr}")
                break

            message = data.decode()
            APP_LOGGER.info(f"Received {message} from {addr}")
            
            if "quit" in message:
                break

            # Echo the message back to the client
            writer.write(data)
            await writer.drain()
            APP_LOGGER.info(f"Sent {message} to {addr}")
    except asyncio.CancelledError:
        APP_LOGGER.debug(f"Connection with {addr} was cancelled.")
    finally:
        writer.close()
        await writer.wait_closed()
        APP_LOGGER.debug(f"Disconnected from {addr}")

async def main():
    """
    This is the main server function. 
    """
    # Parse commandline arguments
    args = parse_args()
    host_address = args.host
    port = args.port
    
    
    tcp_server = await asyncio.start_server(handle_client, host_address, port)
    addr = tcp_server.sockets[0].getsockname()
    APP_LOGGER.debug(f"Serving on {addr}")

    async with tcp_server:
        await tcp_server.serve_forever() 


if __name__ == "__main__":
    asyncio.run(main())