import socket
import logging
import sys

APP_LOGGER = logging.getLogger(name = "TCP Client")
APP_LOGGER.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setFormatter(fmt = logging.Formatter(fmt = "[%(levelname)s] %(name)s; %(asctime)s > %(message)s, datefmt = %Y-%m-%d %H:%M:%S"))

def main():
    server_address = input("Enter the server address: ")
    server_port = int(input("Enter the server port:"))

    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    client_socket.connect(server_address, server_port)
    APP_LOGGER.debug(f"connection successful to {server_address} running on port {server_port}")

    while True:
        message = input("Enter the message to send")
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024)
        answer_res = response.decode('utf-8')
        remote_server_socket = client_socket.getpeername()

        APP_LOGGER.info(f"Rceived message: {answe_res} from {remote_server_address}" )

        if "quit" in answer_res or "exit" in answer_res:
            break

    client_socket.close()
    sys.exit(0)

if __name__ == "__main__":
    main()

