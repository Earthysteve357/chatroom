import socket
import threading

class Server:
    def __init__(self,hostname,port):
        self.server = socket.socket()
        self.server.bind((hostname,port))
        self.acceptor = threading.Thread(target=self.accept,daemon=True)
        self.rooms = []
        self.rooms.append(Room('test room', '1',None))
    def accept(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.setup,args=(conn,addr),daemon=True).start()
    def setup(self,conn,addr,retry=False):
        try:
            if not retry:
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
                if room_names == b'':
                    conn.sendall('[0]'.encode())
                else:
                    conn.sendall(room_names)
            choice = int(conn.recv(1024).decode())
            conn.sendall('1'.encode())
            if choice == 0: # Create Room
                name = conn.recv(1024).decode()
                conn.sendall('1'.encode())
                password = conn.recv(1024).decode()
                self.rooms.append(Room(name,password,(conn,addr)))
                conn.sendall('1'.encode())
            elif choice == 1: # Join Room
                room_choice = conn.recv(1024).decode()
                conn.sendall('1'.encode())
                password = conn.recv(1024).decode()
                for room in self.rooms:
                    if room.name == room_choice:
                        if room.password == password:
                            room.add_user((conn,addr))
                            conn.sendall('1'.encode())
                            room.broadcast(f'{addr[0]} has joined the chat',None)
                            return
                        else:
                            conn.sendall('0'.encode())
                            self.setup(conn,addr,True)
                    else:
                        conn.sendall('0'.encode())
                        self.setup(conn,addr,True)
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
    def broadcast(self,msg,addr):
        for user in self.users:
            if not user.addr == addr:
                user.conn.sendall((f'<{addr[0]}>'+msg).encode())
                print(f'sent: {msg}')
    def add_user(self,user):
        if not user == None:
            self.users.append(User(user))
            threading.Thread(target=self.listen,args=(user,)).start()
    def listen(self,user):
        while True:
            try:
                data = user[0].recv(1024).decode()
                if not data == '':
                    self.broadcast(data,user[1])
            except ConnectionResetError:
                return

server = Server('localhost',16556)
server.acceptor.start()

running = True
while running:
    pass