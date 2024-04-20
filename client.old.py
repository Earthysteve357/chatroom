import socket
import threading
import keyboard
import PySimpleGUI as sg

def receive_msg():
    while True:
        msg = s.recv(1024).decode()
        window['multiline'].print(msg)

def send(msg):
    window['msg'].update('')
    msg = msg.strip()
    if msg == '':
        return
    window['multiline'].print(f'<you>{msg}',justification='right')
    print(f'sending {msg}')
    s.sendall(f'<{display_name}>{msg}'.encode())

hostname = input('Enter server hostname: ')
port = 16556

layout = [[sg.Multiline(size=(50,20),disabled=True,autoscroll=True,key='multiline')],
          [sg.InputText(key='msg'),sg.Button('Send')],
          [sg.InputText(size=(31,1),key='name'),sg.Button('Change Display Name')]]
window = sg.Window('Chatroom',layout,finalize=True)


s = socket.socket()
s.connect((hostname,port))

display_name = s.getsockname()[1]
window['name'].update(s.getsockname()[1])


s_thread = threading.Thread(target=receive_msg,daemon=True)
s_thread.start()

while True:
    event,values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        window.close()
        s.close()
        break
    if event == 'Send':
        send(values['msg'])
    if event == 'Change Display Name':
        if len(values['name']) > 15:
            window['name'].update(display_name)
        else:
            display_name = values['name']
    if keyboard.is_pressed('enter'):
        while keyboard.is_pressed('enter'):
            pass
        send(values['msg'])
