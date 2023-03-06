import socket
import asyncio
import sqlite3
import json



class SignalServer:
    def __init__(self) -> None:
        self.path_to_db = "bd/data.db"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '79.137.198.229'
        self.port = 9000
        self.max_listen = 2
        self.con_blocking_flag = False
        self.db_conn = sqlite3.connect(':memory:')
        self.cur = self.db_conn.cursor()
    
    def create_table(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS addresses(
            addressid INT PRIMARY KEY,
            inaddress TEXT,
            outaddress TEXT,
            name TEXT)""")
        self.db_conn.commit()
    
    async def save_address(self, data) -> None:
        in_address = f"{data['addresses']['in']['host']}:{data['addresses']['in']['port']}"
        out_address = f"{data['addresses']['out']['host']}:{data['addresses']['out']['port']}"
        name = data['name']
        data_to_save = (in_address, out_address, name)
        self.cur.execute("""INSERT INTO addresses(inaddress, outaddress, name)
                            VALUES(?, ?, ?);""", data_to_save)
        self.db_conn.commit()
    
    async def get_address(self, data):
        name = data['name']
        data = self.cur.execute("""SELECT inaddress, outaddress FROM addresses WHERE name=(?);""", name).fetchone()[0]
        inaddress, outaddress = data[0], data[1]
        return inaddress, outaddress

    def setup(self) -> None:
        self.create_table()
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.max_listen)
        self.sock.setblocking(self.con_blocking_flag)
    
    async def handle_connection(self, sock, addr) -> None:
        loop = asyncio.get_event_loop()
        print(f"Connected by {addr}")
        while True:
            try:
                data = await loop.sock_recv(sock, self.chunk_size)
            except ConnectionError:
                break
            if not data:
                break
        answer = self.process_request(json.loads(data, encoding='utf-8'), sock)
        sock.send(answer)
        sock.close()
    
    def process_request(self, data, sock): # Replace with api??
        if data['command'] == 'put':
            self.save_address(data)
        elif data['command'] == 'get':
            self.get_address(data)
        elif data['command'] == 'get_all_servers':
            return self.get_all_servers()


    async def get_all_servers(self, requesting_host, requesting_port):
        servers = self.cur.execute("""SELECT * FROM addresses""").fetchall()
        #for server is servers:
        #    if ping(server) then ...
        return servers
    
    async def get_all_members(chat):
        ...
    
    async def run(self) -> None:
        self.setup()
        loop = asyncio.get_event_loop()
        while True:
            sock, addr = await loop.sock_accept(self.sock)
            loop.create_task(self.handle_connection(sock, addr))


signal_server = SignalServer()
signal_server.run()
