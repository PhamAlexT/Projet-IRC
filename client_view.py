from tkinter import Frame,Tk, Label,StringVar,END,BOTTOM,TOP
from tkinter import ttk
import sys
import random
from client import Client

#The window
root = Tk()
root.config(bg="aquamarine")
#root.attributes('-fullscreen', True)

#Channel frame (left)
left_frame = Frame(root, width=200, height=400)
left_frame.grid(row=0, column=0, padx=40, pady=20)
left_frame.config(bg="red")

#Message display
msg_display = Frame(root,width=900,height=400)
msg_display.grid(row=0,column=1,padx=40, pady=20)
msg_display.config(bg="yellow")
#Message input area (bottom right)
msg_var = StringVar()
msg_area = ttk.Entry(root,textvariable=msg_var,width=100)
msg_area.grid(column=1,row=1,padx=40, pady=20)



#To make everything scale according to the main window
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
#To make messages scale
msg_display.rowconfigure(0, weight=1)
msg_display.columnconfigure(0, weight=1)

class ClientController():
    def __init__(self,msg_display):
        self.msg_display = msg_display

    def display_msg(self,message):
        msg = f"Vous avez reçu:\n {message}"
        to_display = Label(self.msg_display,text=msg).pack(side=TOP)


if __name__ == "__main__":
    try:
        nickname = sys.argv[1]

    except:
        nickname = f"User_{random.randint(100,200)}"

    controller = ClientController(msg_display)

    client = Client(nickname,controller)

    def sender(e):
        m = msg_area.get()
        msg = msg = f"Vous avez envoyé:\n {m}"
        to_display = Label(msg_display,text=msg).pack(side=TOP)
        client.send_msg(m)

        msg_area.delete(0, END)

    root.bind("<Return>", sender )

    root.title(f"{nickname}")
    root.mainloop()

