import socket
import asyncio
from typing import Tuple
import stun
import json
from utility.requests import generate_put_request
from utility.connections import set_out_address
# import logging

class Server:
    def __init__(self) -> None:
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.logger = logging.getLogger(__name__)

        self.members = []

        self.name = 'test_server'

        self.sig_server_host = '127.0.0.1'
        self.sig_server_port = 9002

        self.in_host = '127.0.0.1'
        self.in_port = 9000

        self.out_host = ''
        self.out_port = 0

        self.max_listeners = 2
        self.set_blocking_flag = False

    def send_to_all(self, message: str):
        """Sends message to all current members"""
        for member in self.members:
            try:
                member.send(message)
            except: #add catching exceptions
                pass
    
    def put_address_to_sig(self) -> None:
        """Gets a server's an out address and puts it to a signal server"""
        request  = generate_put_request(self.in_host, self.in_port, self.out_host, self.out_port, self.name)
        request_bytes = bytes(json.dumps(request), encoding="utf-8")
        sig_serv_address = (self.sig_server_host, self.sig_server_port)
        sig_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sig_con.connect(sig_serv_address)
        sig_con.sendto(request_bytes, sig_serv_address)
        sig_con.close()

    async def handle_connection(self, sock: socket, addr: Tuple[str, int]) -> None:
        """Connects with a new member"""
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
        self.members.remove(sock)
        sock.close()

    async def main(self) -> None:
        """Main loop, gets messages and process connections"""
        self.setup()
        print("Server started") # replace with logger + send message to creator
        loop = asyncio.get_event_loop()
        while True:
            print("Waiting for connection") # replace with logger + send message to creator
            sock, addr = await loop.sock_accept(self.serv_sock)
            self.members.append(sock)
            loop.create_task(self.handle_connection(sock, addr))
            
    def setup(self) -> None:
        """Sets out basic setting such as max members count, out address, etc"""
        self.serv_sock.bind((self.in_host, self.in_port))
        self.serv_sock.listen(self.max_listeners)
        self.serv_sock.setblocking(self.set_blocking_flag)
        self.out_host, self.out_port = set_out_address()
        self.put_address_to_sig()


server = Server()
asyncio.run(server.main())

