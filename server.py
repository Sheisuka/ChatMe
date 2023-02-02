import socket
import asyncio


async def handle_connection(sock, addr):
    loop = asyncio.get_event_loop()
    print(f"Connected by {addr}")
    while True:
        try:
            data = await loop.sock_recv(sock, 1024)
        except ConnectionError:
            print(f"Client suddenly closed while receiving from {addr}")
            break
        print(f"Received data from {addr} :\n\t{data}")
        if not data:
            break
    print(f"Disconnected by {addr}")
    sock.close()

async def main(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((host, port))
        serv_sock.listen(1)
        serv_sock.setblocking(0)
        print("Server started")

        loop = asyncio.get_event_loop()
        while True:
            print("Waiting for connection")
            sock, addr = await loop.sock_accept(serv_sock)
            loop.create_task(handle_connection(sock, addr))


HOST = '127.0.0.1'
PORT = 9001

if __name__ == "__main__":
    asyncio.run(main(HOST, PORT))

