import socket
import threading
import time


def broadcast(msg,addr):
    msg = f'<{addr[1]}>{msg.decode()}'
    msg = msg.encode()
    print(f'preparing to send {msg}')
    for client in clients:
        print('checking for sender overlap')
        if client[1] != addr:
            print(f'Sending "{msg}" to {client[1]}')
            client[0].sendall(msg)

def handle_client(conn,addr):
    while True:
        try:
            msg = conn.recv(1024)
            print(msg)
            '''
            if not msg:
                print(1)
                print(clients)
                # clients.remove((conn,addr))
                index = clients.index((conn,addr))
                clients.pop(index)
                print(clients)
                print(f'{addr} disconnected')
                continue
            '''
            print(f'"{msg}" received from {addr[1]}')
            broadcast(msg,addr)
        except ConnectionResetError:
            print(2)
            print(clients)
            # index = clients.index((conn,addr))
            # clients.pop(index)
            print(f'{addr} disconnected')

hostname = 'localhost'
port = 16556

clients = []
threads = []

s = socket.socket()
s.bind((hostname,port))
s.listen()

while True:
    conn,addr = s.accept()
    print(f'{addr} connected')
    clients.append((conn,addr))
    thread = threading.Thread(target=handle_client,args=(conn,addr),daemon=True)
    thread.start()
    threads.append(thread)
