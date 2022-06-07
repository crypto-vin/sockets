import socket
import threading
import sys
import csv

class Server:
    def __init__(self):
        self.HEADER = 64
        port = 3389
        self.PORT = port
        #self.SERVER = '127.0.0.1'
        self.SERVER = ''
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        self.user_list = ['Admin', 'Shawn', 'Alpha', 'Graham', 'Loudah', 'Brian', 'Frank', 'Chica', 'Simon', 'Gideon']
        self.passwords = ['Vin2am@254', '7840', '6135', '0738445022Gm', 'mikinduri', '1997', 'Mombasaraha', 'SmartCity', '1234', 'Zi@nn@2020']
        self.phones = ['+254712897106 +254713136333 +254726681927 +254724134384', 
                       '+254724134384 +254707650522 +254704987711',
                       '+254703132910 +254741312043', 
                       '+254726681927 +254796456350 +254702341472', 
                       '+254742528303 +254703553315',
                       '+254790886393', 
                       '+254725540276', 
                       '+254728603208 +254703535853',
                       '+254707116045',
                       '+254701043240 +254718303340']

        self.allowed_accs = ['william.cabello logan.gavin graham.john cynthia.mathias petra.jane',
                             'doris.stevens.25912 cynthia.mathias', 
                             'logan.gavin william.cabello', 
                             'graham.john petra.jane',
                             'dennis.nemian.15079',
                             'jason.cooper',
                             'kevin.brian.21243',
                             'william.cabello logan.gavin',
                             'marcus.alina',
                             'immaculate.njoki']

        self.primary_num = ['', '', '', '+254726681927', '', '', '', '', '', '']
        f = open("data.csv", 'w', newline='')
        writer = csv.writer(f)
        parameters = (self.user_list, self.passwords, self.phones, self.allowed_accs, self.primary_num)
        for parameter in parameters:
            writer.writerow(parameter)
        print('Data writen!')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
    
    def strip_msg(self, msg):
        half = msg.find(' ')
        username = (msg[: half ])
        password = (msg[half + 1 :])
        self.username, self.password = username, password

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")

        connected = True
        while connected:
            account = False
            passwd = False
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            except:
                break
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                    sys.exit()
                    
                print(f"[{addr}] {msg}")
            
            self.strip_msg(msg)

            try:
                if self.username in self.user_list:
                    account = True

                if self.password in self.passwords:
                    passwd = True

                if account:
                    ind = self.user_list.index(self.username)
                    print(f'{self.username} exists')
                    if self.password == self.passwords[ind]:
                        conn.send(f'exists, {self.allowed_accs[ind]}- {self.phones[ind]}> {self.username}< {self.primary_num[ind]}'.encode(self.FORMAT))
                        break             
                    else:
                        conn.send('incorrect_pwd'.encode(self.FORMAT))
                        break
                else:
                    print(f'{self.username} does not exist')
                    conn.send('null'.encode(self.FORMAT))
                    break

            except Exception as err:
                print(err)
                break
                
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