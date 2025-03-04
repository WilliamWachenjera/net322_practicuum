"""
This module implements a simple UDP server that listens for incoming messages
on a given port.
The server listens on all interfaces and IP addresses on the machine.
The server echoes any messages sent to it.
"""
import socket
import logging

# Sets up app logging
APP_LOGGER = logging.getLogger(name="UDP SERVER")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt=logging.Formatter(fmt="[%(levelname)s] %(name)s : %(asctime)s > %(message)s",
                                                   datefmt="%Y-%m-%d %H:%M:%S"))
APP_LOGGER.addHandler(hdlr=logging_handler)

def main():
  # Creates server socket
  server_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
  
  # Enables reusing address
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  # Binds socket on all interfaces and dynamically chooes a port
  server_socket.bind(('127.0.0.1',12580))
  
  
  # Logs address info - server is running on
  APP_LOGGER.debug(msg=f"Server is running on {server_socket.getsockname()}")
  
  while True:
    # Receives incoming message
    # message, client_address = server_socket.recvfrom(1024)
    client_info = server_socket.recvfrom(1024)
    message = client_info[0] 
    client_address = client_info[1]
    
    
    received_message = message.decode('utf-8')
    # Logs message and client address
    APP_LOGGER.info(msg=f"Received message from {client_address} : {received_message}")
    
    # Echoes message back to client
    server_socket.sendto(received_message.encode('utf-8'), 
                         client_address)
    
    # Logs message sent back to client
    APP_LOGGER.debug(msg=f"Sent message back to {client_address} : {received_message}")

  server_socket.close()

if __name__ == '__main__':
    main()