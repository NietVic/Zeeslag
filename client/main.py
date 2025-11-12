from guizero import *
import socket

app = App(title="Zeeslag Game")

def send_message():
    message = text_box.value
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.1.254', 8225))
        s.sendall(message.encode())
        data = s.recv(1024)
    output.value = f"Received: {data.decode()}"

text_box = TextBox(app, width=30)
send_button = PushButton(app, command=send_message, text="Send Message")
output = Text(app, text="Response will appear here")

app.display()
#test