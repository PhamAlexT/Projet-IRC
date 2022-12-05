import sys
import socket
import threading

HOST = "127.0.0.1"
PORT = 50000 if len(sys.argv) == 1 else int(sys.argv[1])
nclients = 100

channel_list = []

def recv(connection):
    while True:
        msg = connection.recv(1024)
        print(msg.decode('utf-8'))

def send(connection):
    while True:
        msg = input()
        msg = msg.encode('utf-8')
        connection.send(msg)

def handle_msg(msg):
    instr = msg.split(" ")
    match msg:
            case "/away": 
                away(instr)
            case "/help": 
                help()
            case "/invite":
                invite(instr)
            case "/join":
                join(instr)
            case "/list":
                list()
            case "/msg":
                msg(instr)
            case "/names":
                names(instr)


def new_connection(sock):
    while True:
        conn, addr = sock.accept()
        print(f"----got connection from {addr}----")
        tr = threading.Thread(target=recv, args=(conn,))
        ts = threading.Thread(target=send, args=(conn,))
        tr.start()
        ts.start()

def serve():
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print(f"----waiting clients on port : {PORT}----")
    s.listen(nclients)
    new_connection(s)

serve()
