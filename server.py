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
        try:
            room_names = []
            for room in self.rooms:
                room_names.append(room.name)
            print(room_names)
            room_names = str(room_names)
            room_names = room_names.replace("'", '')
            room_names = room_names.replace('[', '')
            room_names = room_names.replace(']', '').encode()
            length = len(room_names)
            print(room_names)
            conn.sendall('[0]'.encode())#(room_names)
            choice = int(conn.recv(1024).decode())
            if choice == 0:
                name = conn.recv(1024).decode()
                conn.sendall('1'.encode())
                password = conn.recv(1024).decode()
                conn.sendall('1'.encode())
                self.rooms.append(Room(name,password,(conn,addr)))
                conn.sendall('1'.encode())
            elif choice == 1:
                room = conn.recv(1024).decode()
        except (ConnectionResetError, ValueError):
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
        # self.listener = threading.Thread(target=self.listen)
    def broadcast(self,msg):
        print(msg)
    def add_user(self,user):
        self.users.append(User(user))
        threading.Thread(target=self.listen,args=(user[0],)).start()
    def listen(self,user):
        while True:
            data = user.recv(1024).decode()
            if not data == '':
                self.broadcast(data)

server = Server('localhost',16556)
server.acceptor.start()

running = True
while running:
    pass