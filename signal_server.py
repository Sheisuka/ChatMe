import socket
import asyncio
import sqlite3


class SignalServer:
    def __init__(self) -> None:
        self.path_to_db = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ''
        self.port = 9000
        self.max_listen = 2
        self.con_blocking_flag = False
    
    def setup(self) -> None:
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.max_listen)
        self.sock.setblocking(self.con_blocking_flag)
    
    async def handle_connection(self, sock, addr):
        loop = asyncio.get_event_loop()
        print(f"Connected by {addr}")
        while True:
            try:
                data = await loop.sock_recv(sock, self.chunk_size)
            except ConnectionError:
                break
            if not data:
                break
        answer = self.process_request(data)
        sock.send(answer)
        sock.close()
    
    def process_request(self, request):
        ...


    def get_all_chats(self):
        ...
    
    def get_all_members(chat):
        ...
    
    async def run(self) -> None:
        self.setup()
        loop = asyncio.get_event_loop()
        while True:
            sock, addr = await loop.sock_accept(self.sock)
            loop.create_task(self.handle_connection(sock, addr))
