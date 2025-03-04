"""
This module implements a simple UDP clients that sends messages to a given server
on a given port.
The client terminates when the client receives an echo message from the server.
"""
import socket

def main():
    server_address = input("Enter server address: ")
    server_port = int(input("Enter server port: "))
    
    client_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
    
    while True:
        message = input("Enter message to send: ")
        
        client_socket.sendto(message.encode('utf-8'), 
                             (server_address,server_port))
        
        response, _ = client_socket.recvfrom(1024)
        
        print(f"Received echo message: {response.decode('utf-8')}")
        
        if response.decode('utf-8') == message:
            break
    
    client_socket.close()
    
if __name__ == "__main__":
    main()