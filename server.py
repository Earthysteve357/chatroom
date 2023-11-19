import socket
import select

hostname = '192.168.1.145'
port = 16556

clients = []

s = socket.socket()
s.bind((hostname,port))
s.listen()


def broadcast(msg,addr):
    msg = f'<{addr[0]}>' + msg.decode()
    msg = msg.encode()
    for client in clients:
        if client[1] != None: #replace None with addr to stop msg from getting sent to sender
            client[0].sendall(msg)

while True:
    client_list = []
    for client in clients:
        client_list.append(client[0])
    ready_to_read, ready_to_write, error = select.select([s,*client_list],[],[],0.1)
    for sock in ready_to_read:
        if sock == s:
            conn, addr = s.accept()
            clients.append((conn,addr))
            print(addr[0] + ' connected')
        else:
            try:
                msg = sock.recv(1024)
                broadcast(msg,sock.getpeername())
            except (ConnectionResetError,ConnectionAbortedError):
                clients.remove((sock,sock.getpeername()))
                print(clients)
