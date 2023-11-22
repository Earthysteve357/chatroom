import socket
import threading
import keyboard
import PySimpleGUI as sg

def receive_msg():
    global text
    while True:
        msg = s.recv(1024).decode()
        text = text + msg + '\n'
        window['multiline'].update(text)

def send(msg):
    global text
    window['msg'].update('')
    text = text + f'<you>{msg}\n'
    window['multiline'].update(text)
    print(f'sending {msg}')
    s.sendall(f'<{display_name}>{msg}'.encode())

text = ''
layout = [[sg.Multiline(default_text=text,size=(50,20),disabled=True,key='multiline')],
          [sg.InputText(key='msg'),sg.Button('Send')],
          [sg.InputText(size=(31,1),key='name'),sg.Button('Change Display Name')]]
window = sg.Window('Chatroom',layout,finalize=True)

# hostname = socket.gethostbyname('evolved-really-tahr.ngrok-free.app')
hostname = '192.168.1.174'
port = 16556

s = socket.socket()
s.connect((hostname,port))

display_name = s.getsockname()[1]
window['name'].update(s.getsockname()[1])

thread = threading.Thread(target=receive_msg,daemon=True)
thread.start()

while True:
    event,values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED:
        window.close()
        s.close()
        break
    if event == 'Send':
        send(values['msg'])
    if event == 'Change Display Name':
        display_name = values['name']
    if keyboard.read_key() == 'enter':
        send(values['msg'])