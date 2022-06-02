import socket
import threading
import sys

class Server:
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5080
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '!DISCONNECT'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                    sys.exit()
                    
                print(f"[{addr}] {msg}")
            username = msg
            if username:
                print('Account exists')
                conn.send('exists'.encode(self.FORMAT))
            else:
                print('No such username')
                conn.send('null'.encode(self.FORMAT))

        conn.close()

    def start(self):
        self.server.listen()
        print(f'[LISTENING] Server is listening on {self.SERVER}')
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def run(self):
        print('[STARTING] server is starting... ')
        self.start()

if __name__ == "__main__":
    app = Server()
    app.run()
    sys.exit(app.exec_())