import sys
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QObject, QByteArray
from PyQt5.QtGui import QIcon, QPixmap
from pathlib import Path

ICON_PATH = Path(__file__).parent / "UnimaLogo.png"

class Communicate(QObject):
    message_received = pyqtSignal(str)

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.comm = Communicate()
        self.comm.message_received.connect(self.display_message)
        self.initUI()
        self.client_socket = QTcpSocket()
        self.client_socket.connected.connect(self.on_connected)
        self.client_socket.readyRead.connect(self.receive_data)
        self.client_socket.errorOccurred.connect(self.on_error)

    def initUI(self):
        self.setWindowTitle('Net322: Messaging Client')
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(QPixmap(str(ICON_PATH))))
        layout = QVBoxLayout(self)

        # Server connection inputs
        server_layout = QHBoxLayout()
        self.server_ip = QLineEdit()
        self.server_ip.setPlaceholderText("Enter Server IP")
        self.server_port = QLineEdit()
        self.server_port.setPlaceholderText("Enter Server port number")
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.connect_to_server)
        server_layout.addWidget(QLabel('IP:'))
        server_layout.addWidget(self.server_ip)
        server_layout.addWidget(QLabel('Port:'))
        server_layout.addWidget(self.server_port)
        server_layout.addWidget(self.connect_btn)
        layout.addLayout(server_layout)

        # Message display
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        layout.addWidget(self.message_display)

        # Message input and send button
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type the message to send")
        self.message_input.returnPressed.connect(self.send_message)
        self.send_btn = QPushButton('Enter to Send')
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)

        self.send_btn.setEnabled(False)

    def display_message(self, message):
        self.message_display.append(message)

    def log(self, message):
        self.display_message(message)

    def on_connected(self):
        self.connect_btn.setEnabled(False)
        self.send_btn.setEnabled(True)
        self.log("Connected to messaging server!")

    def on_error(self, socket_error):
        self.log(f"Connection error: {self.client_socket.errorString()}")

    def connect_to_server(self):
        ip = self.server_ip.text().strip()
        port_text = self.server_port.text().strip()
        
        if not ip or not port_text.isdigit():
            self.log("Invalid address or port number! Try again with a valid IP and port number")
            return
            
        port = int(port_text)
        self.client_socket.connectToHost(QHostAddress(ip), port)

    def receive_data(self):
        while self.client_socket.bytesAvailable() > 0:
            data = self.client_socket.readAll().data().decode('utf-8')
            self.comm.message_received.emit(data)

    def send_message(self):
        message = self.message_input.text().strip()
        if message and self.client_socket.state() == QTcpSocket.ConnectedState:
            data = QByteArray(message.encode('utf-8'))
            self.client_socket.write(data)
            self.message_input.clear()

    def closeEvent(self, event):
        if self.client_socket.state() == QTcpSocket.ConnectedState:
            self.client_socket.disconnectFromHost()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())