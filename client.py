import sys
import socket 
import threading
import random
from base.user import User
import pickle
from base.message import process_msg
HOST = "127.0.0.1"
PORT = 50000

class Client:
    def __init__(self,nickname,controller):
        self.nickname = nickname
        self.controller = controller
        self.connect()

    def recv(self, connection):
        while True:
            msg = connection.recv(1024)
            d = pickle.loads(msg)
            msg,author = d["payload"], d["author"]
            #print(msg.decode('utf-8'))
            self.controller.display_msg(msg,author)

    def send(self,connection):
        while True:
            msg = input()
            user.add_msg(nickname,msg)
            msg = msg.encode('utf-8')

            connection.send(msg)
            print(user.get_msgs())

    def send_msg(self,msg):
        self.s.send(msg.encode("utf-8"))

    def connect(self):
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print(f"----connected to server on port : {PORT}----")
        ts = threading.Thread(target=self.recv, args=(self.s,))
        tr = threading.Thread(target=self.send, args=(self.s,))
        ts.start()
        tr.start()
        self.s.send(f"/fp {self.nickname}".encode("utf-8")) #Hidden command for the server to get the nickname
