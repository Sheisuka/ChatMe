import socket


class Server:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def setup(self, host, port, max_listen):
        self.sock.bind((host, port))
        self.sock.listen(max_listen)

    def receive(self):
        conn, address = self.sock.accept()
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Get from {address[0]}:\n\t{data}")
        conn.close()
    
server = Server()
server.setup('127.0.0.1', 9000, 2)
server.receive()