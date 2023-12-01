import socket
import threading


def broadcast(msg,addr):
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
            print(f'"{msg}" received from {addr[1]}')
            broadcast(msg,addr)
        except ConnectionResetError:
            index = 0
            while (conn,addr) != clients[index]:
                index += 1
            clients.pop(index)
            print(clients)
            print(f'{addr} disconnected')
            return

hostname = socket.gethostbyname(socket.gethostname())
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
