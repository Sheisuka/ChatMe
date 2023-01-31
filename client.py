import socket


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def send_messages(self):
        while True:
            message = input('Enter text to be sent -> ')
            if message == 'bye':
                break
            self.sock.send(message.encode())
        self.sock.close()


client = Client()
client.connect('127.0.0.1', 9000)
client.send_messages()