import sys
import PyQt5
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QHBoxLayout, QPushButton 
from PyQt5.QtGui import QIcon, QPixmap
from pathlib import Path

ICON_PATH = Path(__file__).parent / "UnimaLogo.png"

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NET322: Chat Client")
        self.setWindowIcon(QIcon(QPixmap(str(ICON_PATH))))
        self.resize(400, 300)

        self.socket = QTcpSocket()
        self.socket.connected.connect(lambda: self.log("Connected to server!"))
        self.socket.readyRead.connect(self.receive_data)

        self.layout = QVBoxLayout(self)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        
        # Address and Port Input
        self.address_layout = QHBoxLayout()
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter server address (e.g., 127.0.0.1)")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter port (e.g., 62851)")
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.address_layout.addWidget(self.address_input)
        self.address_layout.addWidget(self.port_input)
        self.address_layout.addWidget(self.connect_button)

        # Chat Output and Input
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type your message here...")
        self.input.returnPressed.connect(self.send_message)

        # Add widgets to the layout
        self.layout.addLayout(self.address_layout)
        self.layout.addWidget(self.output)
        self.layout.addWidget(self.input)
        
    def connect_to_server(self):
        address = self.address_input.text().strip()
        port = self.port_input.text().strip()
        if not address or not port.isdigit():
            self.log("Invalid address or port!")
            return
        self.socket.connectToHost(QHostAddress(address), int(port))


    def log(self, message):
        self.output.append(message)

    def send_message(self):
        message = self.input.text()
        if self.socket.state() == QTcpSocket.ConnectedState:
            self.socket.write(message.encode())
            self.input.clear()
        else:
            self.log("Not connected to any server!")

    def receive_data(self):
        data = self.socket.readAll().data().decode()
        self.log(f"Server: {data}")

def main():
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
