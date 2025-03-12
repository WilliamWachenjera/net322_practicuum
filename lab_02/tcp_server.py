"""
This module implements a simple TCP server that listens for incoming connections
on a given port.
The server listens on all interfaces and IP addresses on the machine.
The server echoes any messages sent to it.
"""
import socket
import logging

# Sets up app logging
APP_LOGGER = logging.getLogger(name="TCP SERVER")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt=logging.Formatter(fmt="[%(levelname)s] %(name)s : %(asctime)s > %(message)s",
                                                   datefmt="%Y-%m-%d %H:%M:%S"))
APP_LOGGER.addHandler(hdlr=logging_handler)


def main():
    # Creates TCP server socket
    server_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    
    # Enables reusing the same address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_)

    # Binds socket on all interfaces and dynamically chooes a port
    server_socket.bind(('127.0.0.1',12580))
    
    # Listens for incoming connections maintaining a 3-connection queue backlog
    server_socket.listen(3)
    
    
    # Logs address info - server is running on
    APP_LOGGER.debug(msg=f"Server is running on {server_socket.getsockname()}")

    while True:
        # Attends to incoming connections and accepts wher possible.
        # Returns a client connection handle on accepting an incoming connection
        client_socket_handle, client_address = server_socket.accept()
        
        # Logs client address
        APP_LOGGER.debug(msg=f"Accepted connection from {client_address}")
        
        while True:

            # Handles client connection
            client_message = client_socket_handle.recv(1024)
            
            received_message = client_message.decode('utf-8')
            
            APP_LOGGER.info(msg=f"Received this: {received_message} from {client_address}")
            
            if "quit" in received_message.lower() or 'exit' in received_message.lower():
                client_socket_handle.close()
                break
            
            # Echo received message back to client
            encoded_message = received_message.encode('utf-8')
            client_socket_handle.send(encoded_message)
            
            APP_LOGGER.info(msg=f"Sent this message {encoded_message.decode('utf-8')} to {client_address}")
    
    server_socket.close()

if __name__ == "__main__":
    main()