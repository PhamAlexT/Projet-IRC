from tkinter import Frame, Tk, Label, StringVar, END
from tkinter import ttk
import sys
import random
from client import Client
from base.utils import formated_datetime

# The window
root = Tk()
root.config(bg="aquamarine")
#root.attributes('-fullscreen', True)

# Channel frame (left)
left_frame = Frame(root, width=200, height=400)
left_frame.grid(row=0, column=0, padx=40, pady=20)
left_frame.config(bg="red")

# Message display
msg_display = Frame(root, width=900, height=400)
msg_display.grid(row=0, column=1, padx=40, pady=20)
msg_display.config(bg="yellow")

# Message input area (bottom right)
msg_var = StringVar()
msg_area = ttk.Entry(root, textvariable=msg_var, width=100)
msg_area.grid(column=1, row=1, padx=40, pady=20)

# To make everything scale according to the main window
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
# To make messages scale
msg_display.rowconfigure(0, weight=1)
msg_display.columnconfigure(0, weight=1)


class ClientController():
    def __init__(self, msg_display):
        self.msg_display = msg_display

    def display_msg(self, message,author):
        msg_headers = f"Vous avez reçu le {formated_datetime()} de {author}"
        headers_label = Label(self.msg_display,
                              text=msg_headers,
                              justify="left").pack(side="top")
        msg_label = Label(self.msg_display,
                          text=message,justify="left").pack(side="top")


if __name__ == "__main__":
    try:
        nickname = sys.argv[1]

    except:
        nickname = f"User_{random.randint(100,200)}"

    controller = ClientController(msg_display)

    client = Client(nickname, controller)

    def sender(e):
        m = msg_area.get()
        msg_headers = f"Vous avez envoyé le {formated_datetime()}"

        headers_label = Label(msg_display,
                              text=msg_headers,
                              justify="left").pack(side="top")
        to_display = Label(msg_display,
                           text=m,
                           justify="left").pack(side="top")
        client.send_msg(m)

        msg_area.delete(0, END)

    root.bind("<Return>", sender)

    root.title(f"{nickname}")
    root.mainloop()
