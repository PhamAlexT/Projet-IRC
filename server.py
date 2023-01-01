import sys
import socket
import threading
import pickle
from base.message import *


HOST = "127.0.0.1"
PORT = 50000
nclients = 100

channel_list = []
"""
list of dict of the form
nickname: str
is_active: bool
away_msg: str
connection: a websocket connection
"""
users_list = []

def get_users():
    l = []
    for t in users_list:
        l.append(t["nickname"])
    return l


def get_status_user(nickname):
    index = None
    for i,t in enumerate(users_list):
        if t["nickname"] == nickname:
            index = i

    if index is not None:
        return users_list[index]["is_active"]

    return None

def get_away_msg_user(nickname):
    index = None
    for i,t in enumerate(users_list):
        if t["nickname"] == nickname:
            index = i

    if index is not None:
        return users_list[index]["away_msg"]

    return None

def get_connection_user(nickname):
    index = None
    for i,t in enumerate(users_list):
        print("in loop", t["nickname"])
        if t["nickname"] == nickname:
            index = i
    if index is not None:
        return users_list[index]["connection"]

    return None

def handle_msg(msg,connection):
    instr = msg.split(" ")
    print(instr)
    match instr[0]:
            case "/away":
                    #Get the good status
                    index = None
                    for i,t in enumerate(users_list):
                        if t["connection"] == connection:
                            index = i
                    print("INDEX HERE",index)
                    users_list[index]["is_active"] = not users_list[index]["is_active"]
                    status = users_list[index]["is_active"]

                    answer = "You are now away." if status == False else "You are back."
                    answer = answer.encode("utf-8")
                    connection.send(answer)

                    try:
                        users_list[index]["away_msg"] = instr[1:]
                    except:
                        pass
            case "/help":
                instr = "Voici une liste des commandes:\n"
                instr+= "/away [message]: Signale son absence quand on nous envoie un message en privé (en réponse, un message peut être envoyé). Une nouvelle commande /away réactive l'utilisateur. \n"
                instr+="/help: Affiche la liste des commandes disponibles.\n"
                instr+="/invite <nick>: Invite un utilisateur sur le canal où on se trouve.\n"
                instr+="/join <canal> [clé]: Permet de rejoindre un canal (protégé eventuellement par une clé). Le canal est crée s'il n'existe pas.\n"
                instr+="/list: Affiche la liste des canaux sur IRC.\n"
                instr+="/msg [canal|nick] message: Pour envoyer un message à un utilisateur ou sur un canal (où on est présent ou pas). Les arguments canal ou nick sont optionnels.\n"
                instr+="/names [channel]: Affiche les utilisateurs connectés à un canal. Si le canal n’est pas spécifié affiche tous les utilisateurs de tous les canaux."
                connection.send(instr.encode('utf-8'))
            case "/invite":
                pass
            case "/join":
                pass
            case "/list":
                pass
            case "/msg":
                symbol = instr[1]
                print(symbol)
                if instr[1][0] == "#":
                    print("msg to channel")
                elif instr[1][0] == "@":
                    r_nickname = instr[1][1:]

                    if r_nickname is None:
                        answer = f"{r_nickname} n\'est pas présent.".encode("utf-8")
                        connection.send(answer)
                        return

                    r_msg = " ".join(instr[2:]).encode("utf-8")
                    r_connection = get_connection_user(r_nickname)

                    if r_connection is not None:
                        r_connection.send(r_msg)
                        if get_status_user(r_nickname) == False:
                            connection.send(get_away_msg_user(r_nickname))
                else:
                    print("...")
            case "/names":
                pass

            case "/fp": #hidden command to register nickname/connection
                try:
                    if instr[1] not in get_users():
                        print(instr[1])
                        dic = {
                            "nickname": instr[1],
                            "is_active": True,
                            "away_msg": "Je suis absent.",
                            "connection": connection
                        }
                        users_list.append(dic)

                except:
                    sys.exit("problem when user joined")
            case _:
                print("default, weird...i",instr)


def recv(connection):
    while True:
        msg = connection.recv(1024)
        handle_msg(msg.decode('utf-8'),connection)

def send(connection):
    while True:
        msg = input()
        msg = msg.encode('utf-8')
        connection.send(msg)

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
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))

    print(f"----waiting clients on port : {PORT}----")
    s.listen(nclients)
    new_connection(s)

if __name__ == "__main__":
    serve()
