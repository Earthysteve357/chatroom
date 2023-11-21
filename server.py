import socket
import select

hostname = 'localhost'
port = 16556

clients = []

s = socket.socket()
s.bind((hostname,port))
s.listen()


def broadcast(msg,addr):
    msg = f'<{addr[1]}> {msg.decode()}'
    msg = msg.encode()
    for client in clients:
        if client[1] != addr:
            print(f'sending "{msg}" to client {client[1]}')
            client[0].sendall(msg)

while True:
    client_num = 0
    client_list = []
    for client in clients:
        client_list.append(client[0])
    ready_to_read, ready_to_write, error = select.select([s,*client_list],[],[],0.1)
    if not error == []:
        print(error)
    for sock in ready_to_read:
        if sock == s:
            conn, addr = s.accept()
            clients.append((conn,addr))
            print(addr[0] + ' connected')
        else:
            msg = sock.recv(1024)
            if not msg:
                print(f'{msg} caused error')
                clients.pop(client_num)
                print(clients)
                print(f'{sock.getpeername()} disconnected')
                continue
            print(f'{msg} being sent')
            broadcast(msg,sock.getpeername())
            client_num += 1
