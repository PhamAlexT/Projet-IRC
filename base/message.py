from datetime import datetime
import sys

class Message():
    def __init__(self, author: str, payload: str):
        self.author = author
        self.payload = payload
        self.date = datetime.now()

    def __str__(self):
        res = 20*"-"+"\n"
        res+= f"Sent by {self.author} at {self.date}.\n"
        res+=(20*"-")

        return res

    def get_payload(self):
        return self.payload

    def get_date(self):
        return self.date

    def get_author(self):
        return self.author


class MessageAway(Message):
    def __init__(self,author,date,answer=None):
        super().__init__(author,date)
        self.answer = answer

    def __str__(self):
        res = 20*"-"+"\n" + "AWAY" + "\n"
        res+= f"Sent by {self.author} at {self.date}.\n"
        res+= f"Answer if messaged: {self.answer}"
        res+=(20*"-")

        return res

class MessageHelp(Message):
    def __init__(self,author,date):
        super().__init__(author,date)

    def __str__(self):
        res = 20*"-"+"\n" + "HELP" + "\n"
        res+= f"Sent by {self.author} at {self.date}.\n"
        res+=(20*"-")

        return res

class MessageInvite(Message):
    def __init__(self,author,date,receiver):
        super().__init__(author,date)
        self.receiver = receiver

    def __str__(self):
        res = 20*"-"+"\n" + "INVITE" + "\n"
        res+= f"Sent by {self.author} at {self.date} to {self.receiver}.\n"
        res+=(20*"-")

        return res

class MessageJoin(Message):
    def __init__(self,author,date,canal,key):
        super().__init__(author,date)
        self.canal = canal
        self.key = key

    def __str__(self):
        res = 20*"-"+"\n" + "JOIN" + "\n"
        res+= f"Sent by {self.author} at {self.date}.\n"
        res+=f"Canal: {self.canal} with key {self.key}.\n"
        res+=(20*"-")

        return res

class MessageList(Message):
    def __init__(self,author,date):
        super().__init__(author,date)

    def __str__(self):
        res = 20*"-"+"\n" + "LIST" + "\n"
        res+= f"Sent by {self.author} at {self.date}.\n"
        res+=(20*"-")

        return res

class MessageMsg(Message):
    def __init__(self,author,date,recipient,content):
        super().__init__(author,date)
        self.recipient = recipient
        self.content = content

    def __str__(self):
        res = 20*"-"+"\n" + "MESSAGE" + "\n"
        res+= f"Sent by {self.author} at {self.date} to {self.receiver}.\n"
        res+= f"Content: {self.content}\n"
        res+=(20*"-")

        return res

class MessageNames(Message):
    def __init__(self,author,date,channel):
        super().__init__(author,date)
        self.channel = channel

    def __str__(self):
        res = 20*"-"+"\n" + "INVITE" + "\n"
        res+= f"Sent by {self.author} at {self.date}.\n"
        res+= f"{self.channel}\n"
        res+=(20*"-")

        return res


def process_msg(msg,author,**kwargs):
    instr = msg.split(" ")
    date = datetime.now()
    msg_o = None

    match instr[0]:
            case "/away":
                try:
                    answer = instr[1:]
                    msg_o = MessageAway(author,date,answer)
                except:
                    msg_o = msg_o = MessageAway(author,date)

            case "/help":
                msg_o = MessageHelp(author,date)
            case "/invite":
                msg_o = MessageInvite(author,date,receiver)
            case "/join":
                msg_o = MessageJoin(author,date,canal,key)
            case "/list":
                msg_o = MessageList(author,date)
            case "/msg":
                receiver = None
                content = None
                if (instr[1][0] == "#") or (instr[1][0] == "@") :
                    receiver = instr[1][1:]
                    content = " ".join([m for m in instr[2:]])

                receiver = receiver
                content = " ".join([m for m in instr[1:]])
                msg_o = MessageMsg(author,date,receiver,content)
            case "/names":
                msg_o = MessageNames(author,date,channel)
            case _:
                sys.exit(f"Error to process f{msg}")

    return msg_o
"""
def process_msg_rec(msg):
    match type(msg):
        case MessageAway:
            pass
        case MessageHelp:
            pass
        case MessageInvite:
            pass
        case MessageJoin:
            pass
        case MessageList:
            pass
        case MessageMsg:
            pass
        case MessageNames:
            pass
"""
