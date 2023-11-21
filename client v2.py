import socket
import threading
import PySimpleGUI as sg

def receive_msg():
    global text
    while True:
        msg = s.recv(1024).decode()
        text = text + msg + '\n'
        window['multiline'].update(text)


text = ''
layout = [[sg.Multiline(default_text=text,size=(50,20),disabled=True,key='multiline')],
          [sg.InputText(key='msg'),sg.Button('Send')],
          [sg.InputText(size=(31,1),key='name'),sg.Button('Change Display Name')]]
window = sg.Window('Chatroom',layout,finalize=True)

# hostname = socket.gethostbyname('evolved-really-tahr.ngrok-free.app')
hostname = '10.157.129.236'
port = 16556

s = socket.socket()
s.connect((hostname,port))

display_name = s.getsockname()[1]
window['name'].update(s.getsockname()[1])

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
        s.sendall(f'<{display_name}>{msg}'.encode())
    if event == 'Change Display Name':
        display_name = values['name']
