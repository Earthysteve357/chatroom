import customtkinter as ctk
import socket
import threading

class Window:
    def __init__(self, width, height):
        self.root = ctk.CTk()
        self.root.minsize(width, height)
        self.root.wm_title('Chatroom')
        self.inrm_frame = Frame(self.root)
        self.inrm_frame.textbox = ctk.CTkTextbox(master=self.inrm_frame.frame,state='disabled')
        self.inrm_frame.textbox.pack(fill='both',expand=True)
        self.inrm_frame.message = ctk.CTkEntry(master=self.inrm_frame.frame)
        self.inrm_frame.message.pack(fill='x')
        self.inrm_frame.button = ctk.CTkButton(master=self.inrm_frame.frame,text='Send',command=server.send(self.inrm_frame.message.get()))
        self.inrm_frame.button.pack()
        self.newrm_frame = Frame(self.root)
        self.newrm_frame.button = ctk.CTkButton(master=self.newrm_frame.frame, text='Create Room',command=server.createrm_thread.start).grid(row=0,column=1)
        self.newrm_frame.text1 = ctk.CTkLabel(master=self.newrm_frame.frame,text='Name: ').grid(row=1,column=0)
        self.newrm_frame.name = ctk.CTkEntry(master=self.newrm_frame.frame)
        self.newrm_frame.name.grid(row=1,column=1)
        self.newrm_frame.text2 = ctk.CTkLabel(master=self.newrm_frame.frame,text='Password: ').grid(row=2,column=0)
        self.newrm_frame.password = ctk.CTkEntry(master=self.newrm_frame.frame,)
        self.newrm_frame.password.grid(row=2,column=1)
        self.joinrm_frame = Frame(self.root)
        self.joinrm_frame.button = ctk.CTkButton(master=self.joinrm_frame.frame,text='Join Room').grid(row=0,column=0)
        self.joinrm_frame.menu = ctk.CTkOptionMenu(master=self.joinrm_frame.frame, values=server.rooms)
        self.joinrm_frame.menu.grid(row=0,column=1)
        self.joinrm_frame.text1 = ctk.CTkLabel(master=self.joinrm_frame.frame,text='Password:').grid(row=1,column=0)
        self.joinrm_frame.password = ctk.CTkEntry(master=self.joinrm_frame.frame)
        self.joinrm_frame.password.grid(row=1,column=1)
        self.joinrm_frame.frame.pack()
        self.newrm_frame.frame.pack(pady=20)
        
class Frame:
    def __init__(self,master):
        self.frame = ctk.CTkFrame(master=master)

class Connection:
    def __init__(self,hostname,port):
        self.server = socket.socket()
        self.server.connect((hostname,port))
        self.createrm_thread = threading.Thread(target=self.createrm)
        print('ready to recive')
        self.rooms = self.server.recv(1024)
        print('recieved')
        self.rooms = (self.rooms).decode()
        self.rooms = self.rooms.split(',')
        x = 0
        for room in self.rooms:
            room = room.strip()
            self.rooms[x] = room
            x += 1
        print('done')
    def createrm(self):
        name = window.newrm_frame.name.get()
        name = name.strip()
        password = window.newrm_frame.password.get()
        password = password.strip()
        if name == '' and not password == '':
            
            return
        else:
            print(name,password)
            self.server.sendall('0'.encode())
            self.server.sendall(name.encode())
            self.server.recv(1)
            self.server.sendall(password.encode())
            self.server.recv(1)
            response = int(self.server.recv(1).decode())
            print(response)
            window.root.wm_title(f'Chatroom - {name}')
            window.newrm_frame.frame.pack_forget()
            window.joinrm_frame.frame.pack_forget()
            window.inrm_frame.frame.pack(fill='both',expand=True)
    def send(self,msg):
        print(msg)
    def listen(self):
        while True:
            data = self.server.recv(1024)
            if not data == '':
                print(data)

server = Connection('localhost',16556)
window = Window(350, 500)
# threading.Thread(target=window.root.mainloop)
window.root.mainloop()