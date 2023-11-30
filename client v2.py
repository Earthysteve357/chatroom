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

def send():
    event, values = window.read(timeout=1)
    msg = values['msg']
    if msg == '':
        return
    global text
    window['msg'].update('')
    text = text + f'<you>{msg}\n'
    window['multiline'].update(text)
    print(f'sending {msg}')
    s.sendall(f'<{display_name}>{msg}'.encode())

def update_gui():
    global display_name
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            s.close()
        if event == 'Send':
            send()
        if event == 'Change Display Name':
            if not len(values['name']) > 15:
                display_name = values['name']

text = ''
layout = [[sg.Multiline(default_text=text,size=(50,20),disabled=True,key='multiline')],
          [sg.InputText(key='msg'),sg.Button('Send')],
          [sg.InputText(size=(31,1),key='name'),sg.Button('Change Display Name')]]
window = sg.Window('Chatroom',layout,finalize=True)


hostname = socket.gethostbyname(socket.gethostname())
port = 16556

s = socket.socket()
s.connect((hostname,port))

display_name = s.getsockname()[1]
window['name'].update(s.getsockname()[1])

sock_thread = threading.Thread(target=receive_msg,daemon=True)
gui_thread = threading.Thread(target=update_gui,daemon=True)
sock_thread.start()
gui_thread.start()

while True:
    if keyboard.read_key() == 'enter':
        send()