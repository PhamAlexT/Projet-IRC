import sys
import socket
import threading
import pickle
from base.message import *


HOST = "127.0.0.1"
PORT = 50000
nclients = 100

"""
list of dict of the form
name: str;
password: str or None
participants: list(str)
"""
channels_list = []

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

def get_nickname(connection):
    index = None
    for i,t in enumerate(users_list):
        print("in loop", t["nickname"])
        if t["connection"] == connection:
            index = i
    if index is not None:
        return users_list[index]["nickname"]

    return None

"""
This function will return a dict that every client knows how to interpret it
The message has to be traced back (a client has to know who sent the message)
The recipient will know if it is a personnal message or not depending of @ or #
If author is the server, author = Server
"""
def create_msg(payload,author):
    # The message has to be traced back.
    d = {
        "payload": payload,
        "author": author
        }
    print("to be serialized",d)
    return pickle.dumps(d)

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
                    users_list[index]["is_active"] = not users_list[index]["is_active"]
                    status = users_list[index]["is_active"]

                    answer = "You are now away." if status == False else "You are back."
                    #answer = answer.encode("utf-8")

                    msg_to_send = create_msg(answer,"Server")
                    connection.send(msg_to_send)

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

                connection.send(create_msg(instr,"Server"))
            case "/invite":
                pass
            case "/join":
                channel,key = None,None
                try:
                    channel = instr[1]
                    key = instr[2]
                except:
                    pass

                #Case 1: We create the channel
                if channel not in [c["name"] for c in channels_list]:
                    d = {"name": channel,
                         "password": key,
                         "participants": [get_nickname(connection)]
                        }
                    channels_list.append(d)
                #The channel already exists.
                else:
                    #get the index of the channel in the list
                    index = None
                    for i,c in enumerate(channels_list):
                        if c["name"] == channel:
                            index = i

                    if key == channels_list[index]["password"]:
                        channels_list[index]["participants"].append(get_nickname(connection))

            case "/list":
                pass
            case "/msg":
                author = get_nickname(connection)
                if instr[1][0] == "#":
                    channel = instr[1][1:]
                    if channel in [c["name"] for c in channels_list]:
                        index = None
                        for i,c in enumerate(channels_list):
                            print(c["name"],channel)
                            if c["name"] == channel:
                                index = i
                        for user in channels_list[index]["participants"]:
                            connection_r = get_connection_user(user)
                            connection_r.send(create_msg(instr,author))

                elif instr[1][0] == "@":
                    r_nickname = instr[1][1:]

                    if r_nickname is None:
                        answer = f"{r_nickname} n\'est pas présent.".encode("utf-8")
                        connection.send(answer)
                        return

                    r_msg = " ".join(instr[2:]).encode("utf-8")
                    r_connection = get_connection_user(r_nickname)

                    if r_connection is not None:
                        r_connection.send(create_msg(r_msg,author))
                        if get_status_user(r_nickname) == False:
                            connection.send(create_msg(get_away_msg_user(r_nickname),r_nickname))
                else:
                    print("...")
            case "/names":
                channel = None
                try:
                    channel = instr[1]
                except:
                    pass
                to_send = "List of users:"
                index = None
                for i,c in enumerate(channels_list):
                        if c["name"] == channel:
                            index = i

                if channel != None:
                    for user in channels_list[index]["participants"]:
                        to_send+=f"\n_{user}"
                else:
                    for user in get_users():
                        to_send+=f"\n_{user}"
                connection.send(create_msg(to_send,"Serveur"))
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
                pass


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
