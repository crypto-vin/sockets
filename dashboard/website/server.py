import socket
import threading
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func    
from website import create_app

db = SQLAlchemy()
DB_NAME = "database.db"

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
        self.username = 'Vin'

    def handle_client(self, conn, addr):
        app = create_app()
        app.app_context().push()
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
            self.username = username

            try:
                account = db.session.query(Accounts).filter(Accounts.username==username).first()
                if account:
                    print(f'{username} exists')
                    conn.send('exists'.encode(self.FORMAT))
                    return True
                else:
                    print(f'{username} does not exist')
                    conn.send('null'.encode(self.FORMAT))
                    return False

            except Exception as err:
                print(err)
                
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