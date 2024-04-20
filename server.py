import socket
import threading

class Server:
    def __init__(self,hostname,port):
        self.server = socket.socket()
        self.server.bind((hostname,port))
        self.acceptor = threading.Thread(target=self.accept,daemon=True)
        self.rooms = []
    def accept(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.setup,args=(conn,addr),daemon=True).start()
    def setup(self,conn,addr):
        print(conn)
        print(addr)
        try:
            room_names = []
            for room in self.rooms:
                room_names.append(room['name'])
            room_names = str(room_names)
            room_names = room_names.replace("'", '')
            room_names = room_names.replace('[', '')
            room_names = room_names.replace(']', '').encode()
            print('ready to send')
            conn.sendall(room_names)
            print('sent')
            choice = int(conn.recv(1024).decode())
            if choice == 0:
                print('create room')
                name = conn.recv(1024).decode()
                conn.sendall('1'.encode())
                print(name)
                password = conn.recv(1024).decode()
                conn.sendall('1'.encode())
                print(password)
                self.rooms.append(Room(name,password,(conn,addr)))
                conn.sendall('1'.encode())
        except ConnectionResetError:
            return

class User:
    def __init__(self,user):
        self.conn, self.addr = user

class Room:
    def __init__(self,name,password,user):
        self.name = name
        self.password = password
        self.users = []
        self.add_user(user)
        self.listener = threading.Thread(target=self.listen)
    def broadcast(self,msg):
        print(msg)
    def add_user(self,user):
        self.users.append(User(user))
        threading.Thread(target=self.listen,args=user).start()
    def listen(self,user):
        while True:
            data = user[0].recv(1024)
            print(data)
            self.broadcast(data)

server = Server('localhost',16556)
server.acceptor.start()

running = True
while running:
    pass