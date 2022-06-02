import socket
import threading
import sys
from website.models import Accounts
#from . import db

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

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
        account = Accounts.query.filter_by(username=username).first()
        if account:
            print('Account exists')
            conn.send('exists'.encode(self.FORMAT))

        else:
            print('No such username')
            conn.send('null'.encode(self.FORMAT))

    conn.close()

def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def run():
    print('[STARTING] server is starting... ')
    start()
