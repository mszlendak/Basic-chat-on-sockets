import socket
from tkinter import *
import threading



class ClientConnect():
    def __init__(self):
        self.start_socket()

    def start_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.33.60', 8081))

    def start_getting_msg(self, msg_list,):

        while True:
            msg_list.insert(END, self.sock.recv(800).decode())
            msg_list.see(END)


    def send(self, message, my_msg ,event=None):
        self.sock.send(message.encode())
        my_msg.set('')


    def close_connection(self):
        self.sock.send('!quit'.encode())



class Window(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master

        self.init_window()

    def init_window(self):
        self.socket_client = ClientConnect()

        self.master.title("Pogadu-Pogadu")

        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)

        file.add_command(label="Exit", command=self.client_exit)

        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)

        menu.add_cascade(label="Edit", menu=edit)

        scrollbar = Scrollbar(self)
        self.msg_list = Listbox(self, height=15, width=50,
                                   yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack()

        self.my_msg = StringVar()  # For the messages to be sent.
        self.my_msg.set("Type your messages here.")

        entry_field = Entry(self, textvariable=self.my_msg)
        entry_field.bind("<Return>", lambda event=None: self.socket_client.send(self.my_msg.get(), self.my_msg))
        entry_field.pack()

        send_button = Button(self, text="Send", command=lambda : self.socket_client.send(self.my_msg.get(), self.my_msg))

        send_button.pack()


        threading.Thread(target=self.socket_client.start_getting_msg, args=(self.msg_list,)).start()



    def client_exit(self):
        try:
            self.socket_client.close_connection()
            root.destroy()
        except OSError:
            root.destroy()
root = Tk()



root.geometry("400x300")
icon = PhotoImage(file='favicon.ico')
root.tk.call('wm', 'iconphoto', root._w, icon)

app = Window(root)
root.protocol('WM_DELETE_WINDOW', app.client_exit)

app.configure(background='orange')


root.mainloop()
