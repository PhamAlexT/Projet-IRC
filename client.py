import sys
import socket 
import threading

HOST = "127.0.0.1"
PORT = 50000 if len(sys.argv) == 1 else int(sys.argv[1])

def recv(connection):
    while True:
        msg = connection.recv(1024)
        print(msg.decode('utf-8'))

def send(connection):
    while True:
        msg = input()
        msg = msg.encode('utf-8')
        connection.send(msg)

def connect():
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 
    s.connect((HOST, PORT))
    print(f"----connected to server on port : {PORT}----")
    ts = threading.Thread(target=recv, args=(s,))
    tr = threading.Thread(target=send, args=(s,))
    ts.start()
    tr.start()

connect()
