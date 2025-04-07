# NET322 - Network Programming and Application Development

## Introduction to GUI Programming with PyQt

## Lab Instructions
### Getting Started with Qt
1. Implement a coordinating server for a messaging board, where the server simultaneously allows multiple client applications send messages to a chat board.
2. Using the example barebons dummy chat application provided in `../lab_05/qt_chat_client.py` as reference,
   - Implement a simple client application for the messaging, on connecting, a client should specify IP address and port number of messaging coordinator.
   - The messaging board coordinator should be able to identify each client using an 8-digit `SHA1-hash` of their socket address and port number.
   - Thus, each tabbed message line in the messaging board application, should have 
    ```bash
       XXXXXXXX :  <Content>   
    ``` 
    where XXXXXXXX is the 8-character hash of the client socket address info.
   - The messaging board should show a listing of messages sent during an active chat session from various client applications

## Instructions for Submission
Using the source files provided in this directory, implement the two applications. Create a zipped archive and submit with the following filename format `<registration-number>-net322-assignment-1.zip` e.g., `bsc-03-16-net322-assignment-1.zip`

**NOTE** : _Use PyQt5 for the client application and AsyncIO for the messaging coordinator_.<br/>

**Plagiarism and/or unattributed work shall be penalized accordingly!**