import socket
import threading
import PySimpleGUI as sg

def receive_msg():
    global text
    while True:
        try:
            msg = s.recv(1024).decode()
            text = text + msg + '\n'
            window['multiline'].update(text)
        except Exception:
            print(Exception)


text = ''
layout = [[sg.Multiline(default_text=text,size=(50,20),disabled=True,key='multiline')],
          [sg.InputText(key='msg'),sg.Button('Send')]]
window = sg.Window('Chatroom',layout,finalize=True)

# hostname = socket.gethostbyname('evolved-really-tahr.ngrok-free.app')
hostname = 'localhost'
port = 16556

s = socket.socket()
s.connect((hostname,port))

thread = threading.Thread(target=receive_msg,daemon=True)
thread.start()

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        window.close()

        s.close()
        break
    if event == 'Send':
        msg = values['msg']
        window['msg'].update('')
        text = text + f'<you>{msg}\n'
        window['multiline'].update(text)
        print(f'sending {msg}')
        s.sendall(msg.encode())
