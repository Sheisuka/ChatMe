import socket
import json
from utility.connections import set_out_address
from utility.requests import generate_get_all_request


class Client:
    def __init__(self):
        self.sig_server_host = '127.0.0.1'
        self.sig_server_port = 9002

        self.name = 'test_client'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def get_available_servers(self):
        request = generate_get_all_request(self.name)
        request_bytes = bytes(json.dumps(request), encoding="utf-8")
        self.sock.send(request_bytes)
    
    def send_message(self):
        message = input('Enter text to be sent -> ')
        self.sock.send(message.encode())

    async def setup(self) -> None:
        self.out_host, self.out_port = set_out_address()


client = Client()
client.connect('127.0.0.1', 9002)
client.send_messages()