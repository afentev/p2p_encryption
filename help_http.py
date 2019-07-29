#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import crypto

from tkinter import *


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        #self.self_ip = http.client.HTTPConnection("ifconfig.me").request("GET", "/ip").getresponse().read().strip()
        self.connected = False
        self.string = ''
        self.counter = 0
        self.initUI()

    def initUI(self):
        self.parent.title("Review")
        self.grid()

        self.lbl1 = Label(text="First port", width=13)
        self.lbl1.grid(row=0, column=0, padx=15, pady=15)
        self.entry1 = Entry(width=25)
        self.entry1.grid(row=0, column=1, padx=15)
        self.entry1.insert(0, '8082')
        self.lbl4 = Label(text='Second port', width=13)
        self.lbl4.grid(row=0, column=2, padx=15)
        self.entry4 = Entry(width=25)
        self.entry4.insert(0, '8081')
        self.entry4.grid(row=0, column=3, padx=0)
        self.lbl2 = Label(text="Receiver ip ", width=12)
        self.lbl2.grid(row=1, column=0)
        self.entry2 = Entry(width=25)
        self.entry2.insert(0, '127.0.0.1')
        self.entry2.grid(row=1, column=1)

        self.btn = Button(text='Connect', width=91, height=2, command=self.connect_update)
        self.btn.grid(row=2, column=0, pady=15, columnspan=4, padx=15)

        self.lstbox = Listbox(width=91, height=20)
        self.lstbox.grid(row=3, column=0, pady=15, columnspan=4, padx=15)

        self.txt_entry = Text(width=91, height=3, font='clearlyu 13')
        self.txt_entry.grid(row=4, column=0, pady=5, columnspan=4, padx=15)

        self.snd = Button(text='Send', width=91, height=2, command=self.msg_send)
        self.snd.grid(row=5, column=0, pady=5, columnspan=4, padx=15)

    def __del__(self):
        self.conn.close()
        self.sock_receive.close()

    def connect_to_active_socket(self, receiver_ip, receiver_port, current_port):
        self.sock_send = socket.socket()
        self.sock_send.connect(('localhost' if receiver_ip == '127.0.0.1' else receiver_ip, receiver_port))
        self.sock_receive = socket.socket()
        self.sock_receive.bind(('', current_port))
        self.sock_receive.listen(1)
        self.conn, self.addr = self.sock_receive.accept()

    def connect_update(self):
        if self.connected:
            pass
        else:
            receiver_ip, receiver_port, current_port = self.entry2.get(), int(self.entry1.get()), int(self.entry4.get())
            try:
                self.connect_to_active_socket(receiver_ip, receiver_port, current_port)
            except ConnectionRefusedError:
                self.sock_receive = socket.socket()
                try:
                    self.sock_receive.bind(('', current_port))
                except OSError:
                    self.connect_to_active_socket(receiver_ip, current_port, receiver_port)
                else:
                    self.sock_receive.listen(1)
                    self.conn, self.addr = self.sock_receive.accept()
                    self.sock_send = socket.socket()
                    self.sock_send.connect(('localhost' if receiver_ip == '127.0.0.1' else receiver_ip, receiver_port))
            q = [i for i in crypto.get_rsa_keys(1, 1024)]
            encode_send, self.decode_send = q[0]
            self.sock_send.send(bytes(str(encode_send), encoding='UTF-8'))
            string = ''
            while True:
                try:
                    data = self.conn.recv(1024)
                    self.conn.setblocking(False)
                except BlockingIOError:
                    break
                string += str(data)[2:-1]
            self.encode_send = tuple(map(int, string[1:-1].split(', ')))
            self.conn.setblocking(False)
            self.connected = True
            self.entry1.configure(state=DISABLED)
            self.entry2.configure(state=DISABLED)
            self.entry4.configure(state=DISABLED)

    def msg_send(self):
        try:
            text = self.txt_entry.get("1.0", "end-1c").replace('\n', '')
            if not text:
                return
            encrypted = crypto.encode_function(text, *self.encode_send)
            print(encrypted)
            self.sock_send.send(bytes(encrypted + '\n', encoding='UTF-8'))
            self.lstbox.insert(self.counter, 'me: ' + text)
            self.counter += 1
            self.txt_entry.delete('1.0', END)
        except:
            print(sys.exc_info())
            self.txt_entry.configure(0, text='Unsuccessful')

    def show_(self):
        print(self.string)
        for i in self.string.split('\\n'):
            if i:
                i = crypto.decode_function(i, *self.decode_send)
                self.lstbox.insert(self.counter, '{}: {}'.format(str(self.addr), i))
                self.counter += 1
        self.string = ''

    def stack(self):
        try:
            message = self.conn.recv(128).decode('utf-8')
            if message:
                self.string += str(message)

        # log.insert(END, message)  # ; log.update()
        except:
            if self.string:
                self.show_()
            self.after(1, self.stack)
            return
        self.after(1, self.stack)
        return


def main():
    root = Tk()
    root.geometry("695x612+300+300")
    app = Example(root)
    root.after(1, app.stack)
    root.mainloop()


if __name__ == '__main__':
    main()
