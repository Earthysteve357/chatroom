import socket
import keyboard
import random
import select
import PySimpleGUI as sg

text = ''

layout = [[sg.Multiline(default_text=text,size=(50,20),disabled=True,key='multiline')],
          [sg.InputText(key='msg'),sg.Button('Send')]]
window = sg.Window('Chatroom',layout)

# hostname = socket.gethostbyname('evolved-really-tahr.ngrok-free.app')
hostname = 'localhost'
port = 16556

s = socket.socket()
s.connect((hostname,port))

while True:
    ready_to_read, ready_to_write, error = select.select([s],[],[],0.1)
    if not ready_to_read == []:
        msg = s.recv(1024).decode()
        print(msg)
        text = text + msg + '\n'
        window['multiline'].update(text)
    event,values = window.read(timeout=1)
    if event == sg.WIN_CLOSED:
        window.close()
        s.close()
        break
    if event == 'Send':
        msg = values['msg']
        window['msg'].update('')
        text = text + '<you>' + msg + '\n'
        window['multiline'].update(text)
        print(f'sending {msg}')
        s.sendall(msg.encode())