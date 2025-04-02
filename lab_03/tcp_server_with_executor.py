"""
This module implements a multithreaded TCP echo server 
that listens for incoming connections
on a given port.
The server listens on all interfaces and IP addresses on the machine.
The server echoes any messages sent to it.

The server is capable of handling multiple clients concurrently 
by delegating to an executor
with a fixed number of threads responsible for handling client connections.
"""
import socket
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="A simple multithreaded TCP echo server using executor.")
    parser.add_argument("--host", type=str, default="0.0.0.0", 
                        help="Host address to bind to")
    parser.add_argument("--port", type=int,
                        required=True, 
                        help="Port to bind to")
    parser.add_argument("--max-clients", type=int, default=5, 
                        help="Maximum number of clients to handle concurrently")
    return parser.parse_args()

# Sets up app logging
APP_LOGGER = logging.getLogger(name="TCP MULTISERVER")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt=logging.Formatter(fmt="[%(levelname)s] %(name)s : %(asctime)s > %(message)s",
                                                   datefmt="%Y-%m-%d %H:%M:%S"))
APP_LOGGER.addHandler(hdlr=logging_handler)


## TODO : Refine implementation to ensure listen-accept operation observes a finite queue length of pending connections
def main():
    # Parse commandline arguments
    args = parse_args()
    host_address = args.host
    port = args.port
    max_clients = args.max_clients
    
    # Creates TCP server socket
    server_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    
    # Enables reusing the same address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_)

    # Binds socket on all interfaces and dynamically chooes a port
    server_socket.bind((host_address, port))
    
    # Listens for incoming connections maintaining a 3-connection queue backlog
    server_socket.listen(3)
    
    
    # Logs address info - server is running on
    APP_LOGGER.debug(msg=f"Server is running on {server_socket.getsockname()}")
    
    
    executor = ThreadPoolExecutor(max_workers=max_clients)
    

    while True:
        try:
            # Attends to incoming connections and accepts wher possible.
            # Returns a client connection handle on accepting an incoming connection
            client_socket_handle, client_address = server_socket.accept()
            
            # ClientHandler(client_socket_handle).start()
            
            ## Instead of delegating to a new thread created on demand, we delegate to an executor
            future = executor.submit(handle_client, client_socket_handle)
            
            if future.exception() is not None:
                raise future.exception()
            
            # Logs client address
            APP_LOGGER.info(msg=f"Accepted connection from {client_address}")
        except Exception as e:
            APP_LOGGER.error(msg=f"An error occurred while accepting a connection: {e}")
            break
        
    server_socket.close()
    executor.shutdown(wait=True)
    
def handle_client(client_socket : socket.socket):
    client_address = client_socket.getsockname()
    
    while True:
        # Handles client connection
        client_message = client_socket.recv(1024)

        received_message = client_message.decode('utf-8')

        APP_LOGGER.info(msg=f"Received this: {received_message} \
            from {client_address}")

        if "quit" in received_message.lower() or 'exit' in received_message.lower():
            client_socket.close()
            break
        
        if "bomb" in received_message.lower():
            raise Exception("Terrorist in sight!")


        # Echo received message back to client
        encoded_message = received_message.encode('utf-8')
        client_socket.send(encoded_message)

        APP_LOGGER.info(msg=f"Sent this message {encoded_message.decode('utf-8')}\
            to {client_address}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        APP_LOGGER.error(msg=f"Signal received signal to terminate the server. Shutting down...")
    except Exception as e:
        APP_LOGGER.error(msg=f"An error occurred: {e}")
        sys.exit(1)