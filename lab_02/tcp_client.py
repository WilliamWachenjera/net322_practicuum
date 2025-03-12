"""
This module implements a simple TCP client that connects to a TCP server
and iteratively sends message until closure
"""
import socket
import logging
import sys

# Sets up app logging
APP_LOGGER = logging.getLogger(name="TCP CLIENT")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt=logging.Formatter(fmt="[%(levelname)s] %(name)s : %(asctime)s > %(message)s",
                                                   datefmt="%Y-%m-%d %H:%M:%S"))
APP_LOGGER.addHandler(hdlr=logging_handler)


def main():
    server_address = input("Enter server address: ")
    server_port = int(input("Enter server port: "))
    
    client_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    
    client_socket.connect((server_address,server_port))
    
    APP_LOGGER.debug(f"Connected to server running on IP address: {server_address} on port {server_port}")
    
    while True:
        message = input("Enter message to send: ")
        
        client_socket.send(message.encode('utf-8'))
        
        response = client_socket.recv(1024)
        
        remote_server_address = client_socket.getpeername()
        
        APP_LOGGER.info(f"Received echo message: {response.decode('utf-8')} from server {remote_server_address}")
        
        if "quit" in response.decode('utf-8').lower() or 'exit' in response.decode('utf-8').lower():
            break
    
    client_socket.close()
    sys.exit(0)
    
    
if __name__ == "__main__":
    main()