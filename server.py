import selectors
import socket

def run(main):
    loop = get_event_loop()
    loop.run_forever(main)

loop = None 

def get_event_loop():
    global loop
    if not loop:
        loop = SelectorLoop()
    return loop

class SelectorLoop:
    def __init__(self) -> None:
        super().__init__()
        self._selector = selectors.DefaultSelector()
        self._current_gen = None
        self._ready = []
        self._run_forever_gen = None

    def run_forever(self, main_gen):
        self.create_task(main_gen)
        while True:
            self._run_once()

    def create_task(self, gen):
        self._ready.append(gen)
    
    def wait_for(self, fileobj):
        self._selector.register(fileobj, selectors.EVENT_READ, self._current_gen)
        yield

    def _run_once(self):
        self.process_tasks(self._ready)
        print("Waiting for connections or data...")
        events = self._selector.select()
        self._process_events(events)
    
    def process_tasks(self, tasks):
        while tasks:
            self._run(tasks.pop(0))
    
    def process_events(self, events):
        for key, mask in events:
            self._selector.unregister(key.fileobj)
            gen = key.data
            self._run(gen)
    
    def _run(self, gen):
        self._current_gen = gen
        try:
            next(gen)
        except StopIteration:
            pass

    def sock_accept(self, serv_sock):
        try:
            sock, addr = serv_sock.accept()
            sock.setblocking(0)
            return sock, addr
        except (BlockingIOError, InterruptedError):
            yield from self.wait_for(serv_sock)
            return (yield from self.sock_accept(serv_sock))
        
    def sock_recv(self, sock, nbytes):
        try:
            sock.recv(nbytes)
        except (BlockingIOError, InterruptedError):
            yield from self.wait_for(sock)
            return (yield from self.sock_recv(sock, nbytes))
    
    def sock_sendall(self, sock, data):
        sock.send(data)


def main(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((host, port))
        serv_sock.listen(1)
        loop = get_event_loop()
        while True:
            sock, addr = yield from loop.sock_accept(serv_sock)
            loop.create_task(handle_connection(sock, addr))

def handle_connection(sock, addr):
    while True:
        # Receive
        try:
            yield loop.wait_for(sock)
            data = yield from loop.sock_recv(sock, 1024)  # Should be ready after wait_for()
        except ConnectionError: 
            print(f"Client suddenly closed while receiving")
            break
        print(f"Received {data} from: {addr}")
        if not data:
            break
        # Process
        if data == b"close":
            break
        data = data.upper()
        # Send
        print(f"Send: {data} to: {addr}")
        try:
            sock.send(data)  # Hope it won't block
        except ConnectionError:
            print(f"Client suddenly closed, cannot send")
            break
    sock.close()
    print("Disconnected by", addr)


if __name__ == '__main__':
    run(main('127.0.0.1', 9006))