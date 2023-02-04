import selectors
import socket
import asyncio
from typing import Tuple
# import logging

class Server:
    def __init__(self) -> None:
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.logger = logging.getLogger(__name__)
        self.chunk_size = 1024
        self.host = '127.0.0.1'
        self.port = 9002
        self.max_listeners = 2
        self.set_blocking_flag = False

    async def handle_connection(self, sock: socket, addr: Tuple[str, int]):
        loop = asyncio.get_event_loop()
        print(f"Connected by {addr}")
        while True:
            try:
                data = await loop.sock_recv(sock, self.chunk_size)
            except ConnectionError:
                print(f"Client suddenly closed while receiving from {addr}") # replace with logger
                break
            print(f"Received data from {addr} :\n\t{data}") # replace with logger + send message to The Room
            if not data:
                break
        print(f"Disconnected by {addr}") # replace with logger + send message to The Room
        sock.close()

    async def main(self) -> None:
        self.setup()
        print("Server started") # replace with logger + send message to creator

        loop = asyncio.get_event_loop()
        while True:
            print("Waiting for connection") # replace with logger + send message to creator
            sock, addr = await loop.sock_accept(self.serv_sock)
            loop.create_task(self.handle_connection(sock, addr))
    
    def setup(self) -> None:
        self.serv_sock.bind((self.host, self.port))
        self.serv_sock.listen(self.max_listeners)
        self.serv_sock.setblocking(self.set_blocking_flag)




server = Server()
asyncio.run(server.main())

