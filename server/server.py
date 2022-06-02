import socket
import threading
import sys

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                sys.exit()
    
            print(f"[{addr}] {msg}")
        #from ..models import Accounts
        print('Imported models')
        username = msg
        try:
            print('Checking if account exists')
            account = username
            #account = Accounts.query.filter_by(username=username).first()
        except:
            print('Unable to access Database')

        if account:
            print('Account exists')
            conn.send('exists'.encode(FORMAT))
        else:
            print('No such username')
            conn.send('null'.encode(FORMAT))

    conn.close()

def start():
    print('[STARTING] server is starting... ')
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

#start()

if __name__ == '__main__':
    start()