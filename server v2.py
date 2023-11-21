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
            if not msg:
                print(clients)
                clients.remove((conn,addr))
                print(clients)
                print(f'{addr} disconnected')
                continue
            print(f'"{msg}" received from {addr[1]}')
            broadcast(msg,addr)
        except TimeoutError:
            time.sleep(1)
            continue

hostname = 'localhost'
port = 16556

clients = []
threads = []

s = socket.socket()
s.bind((hostname,port))
s.listen()

while True:
    conn,addr = s.accept()
    conn.settimeout(0.05)
    clients.append((conn,addr))
    thread = threading.Thread(target=handle_client(conn,addr),daemon=True)
    threads.append(thread)
    print(f'{addr} connected')
