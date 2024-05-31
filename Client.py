import socket
import threading

# Constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_messages():
    
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)
                if msg == DISCONNECT_MESSAGE:
                    print("[DISCONNECTED] The server has closed the connection.")
                    break
        except:
            print("[ERROR] Connection closed.")
            break
    client.close()

def send(msg):
    
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def start():
    
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        message = input()
        if message == DISCONNECT_MESSAGE:
            send(DISCONNECT_MESSAGE)
            break
        send(message)

if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start()
