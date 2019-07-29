#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import socket

from tkinter import *

primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
          367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
          499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
          643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
          797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
          947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
          1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
          1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319,
          1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471,
          1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
          1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723,
          1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
          1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999]


def check(x, y):
    while True:
        if y == 0:
            return x
        x = x % y
        if x == 0:
            return y
        y = y % x


def get(a, m):
    b, c, i, j = m, a, 0, 1
    while c != 0:
        x, y, b = *divmod(b, c), c
        c = y
        y = j
        j = i - j * x
        i = y
    if i < 0:
        i += m
    return i


def toBinary(n):
    return tuple(map(int, tuple(str(bin(n))[2:])))


def MillerRabin(n, s):
    for j in range(1, s + 1):
        a = random.randint(1, n - 1)
        b = toBinary(n - 1)
        d = 1
        for i in range(len(b) - 1, -1, -1):
            x = d
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                return True  # Составное
            if b[i] == 1:
                d = (d * a) % n
                if d != 1:
                    return True  # Составное
                return False  # Простое


def ferma(n, a):
    return pow(a, n - 1, n) == 1


def prime(n):
    if n % 2 == 0:
        return False
    for prime_ in primes:
        if n % prime_ == 0 and n != prime_:
            return False
    for i in range(50):
        a = random.randint(0, 10 ** 12)
        if not MillerRabin(n, a) or not ferma(n, a):
            break
    else:
        return True
    return False


def get_keys(n, bytes_=1024):
    def generate():
        p = random.randint(10 ** size, 10 ** (size + 1))
        while not prime(p):
            p = random.randint(10 ** size, 10 ** (size + 1))
        q = random.randint(10 ** size, 10 ** (size + 1))
        while not prime(q):
            q = random.randint(10 ** size, 10 ** (size + 1))
        return p, q

    size = int(math.log10(2 ** bytes_)) + 1
    for i in range(n):
        p, q = generate()
        while p == q:
            p, q = generate()
        n = p * q
        f = (p - 1) * (q - 1)

        i = 2 ** 16 + 1  # для избежания малого значения открытой экспоненты
        if not check(i, f):
            for i in range(2, f):
                if check(i, f) == 1:
                    break
        e = i
        d = get(e, f)

        yield ((e, n), (d, n))


def encode_function(a, e, n):
    encode_array = []
    a = list(map(lambda b: ord(b), a))
    a.insert(0, random.randint(1, 10 ** 5))
    for i in range(1, len(a)):
        a[i] = (a[i - 1] + a[i]) % n
    for index in range(len(a)):
        encode_array.append(hex(pow(a[index], e, n)))
    return ' '.join(tuple(map(lambda a: str(a), encode_array)))


def decode_function(a, d, n):
    text = list(map(lambda z: int(z, 16), a.split()))
    decode_array = []
    for index in range(len(text)):
        try:
            decode_array.append(pow(text[index], d, n))
        except OverflowError:
            print('a')
    new_array = []
    for i in range(1, len(decode_array)):
        new_array.append((decode_array[i] - decode_array[i - 1]) % n)
    decode_string = ''.join(tuple(map(lambda a: chr(a), new_array)))
    return decode_string


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
            q = [i for i in get_keys(1, 32)]
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
            encrypted = encode_function(text, *self.encode_send)
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
                i = decode_function(i, *self.decode_send)
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
