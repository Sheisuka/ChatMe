import socket
import select


class Server:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.inputs, self.outputs = [self.sock], []

    
    def setup(self, host, port, max_listen):
        self.sock.bind((host, port))
        self.sock.listen(max_listen)
    
    def handle(self, sock, addr):
        try:
            data = sock.recv(1024)
        except ConnectionError:
            print(f"Client suddenly closed while receiving")
            return False
        print(f"Received from {addr}:\n\t{data}")
        if not data:
            print(f"Dicsonnected {addr}")
            return False

    def receive(self):
        readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
        for sock in readable:
            if sock == self.sock:
                sock, addr = self.sock.accept()
                print(f"Connected by {addr}")
                self.inputs.append(sock)
            else:
                addr = self.sock.getpeername()
                if not self.handle(sock, addr):
                    self.inputs.remove(sock)
                    if sock in self.outputs:
                        self.outputs.remove(sock)
                    sock.close()
    
    
server = Server()
server.setup('127.0.0.1', 9001, 2)
while True:
    server.receive()