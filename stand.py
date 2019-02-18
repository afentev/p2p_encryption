# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crypto.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import math
import random
import socket
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

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


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("self")
        self.resize(656, 612)
        self.setMaximumSize(656, 612)
        self.setMinimumSize(656, 612)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 400, 631, 101))
        self.lineEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 510, 631, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(11, 11, 120, 19))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 11, 176, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(470, 11, 171, 25))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(325, 11, 136, 19))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 45, 176, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(11, 45, 96, 19))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(11, 79, 631, 34))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(325, 45, 112, 19))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(470, 45, 171, 25))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 120, 631, 271))
        self.textBrowser.setObjectName("textBrowser")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 656, 31))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.update_messages)
        self.pushButton_2.clicked.connect(self.send)
        # self.lineEdit_3.textEdited.connect(self.ip_updated)

        self.show()

    def send(self, arg):
        text = self.lineEdit.text()
        encrypted = encode_function(text, *self.encode_send)
        print(encrypted)
        self.sock_send.send(bytes(encrypted + '\n', encoding='UTF-8'))
        self.lineEdit.setText('')

    def update_messages(self, arg):
        string = ''
        while True:
            try:
                data = self.conn.recv(1024)
            except BlockingIOError:
                break
            string += str(data)[2:-1]
        for i in string.split('\\n'):
            if i:
                i = decode_function(i, *self.decode_send)
                self.textBrowser.append('{}: {}'.format(str(self.addr), i))

    def ip_updated(self, arg):
        # print(arg)
        pass

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == 16777216:
            try:
                self.sock_send = socket.socket()
                ip, port = self.lineEdit_4.text(), self.lineEdit_5.text()
                self.sock_send.connect(('localhost', 8080))
                self.sock_receive = socket.socket()
                self.sock_receive.bind(('', 8081))
                self.sock_receive.listen(1)
                self.conn, self.addr = self.sock_receive.accept()
            except ConnectionRefusedError:
                self.sock_receive = socket.socket()
                self.sock_receive.bind(('', 8080))
                self.sock_receive.listen(1)
                self.conn, self.addr = self.sock_receive.accept()
                self.sock_send = socket.socket()
                ip, port = self.lineEdit_4.text(), self.lineEdit_5.text()
                self.sock_send.connect(('localhost', 8081))
            q = [i for i in get_keys(1, 512)]
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

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.pushButton_2.setText(_translate("self", "Send"))
        self.label_2.setText(_translate("self", "Порт получения"))
        self.lineEdit_2.setText(_translate("self", "8081"))
        self.lineEdit_5.setText(_translate("self", "8082"))
        self.label_3.setText(_translate("self", "Порт отправления"))
        self.lineEdit_3.setText(_translate("self", "127.0.0.1"))
        self.label.setText(_translate("self", "ip получения"))
        self.pushButton.setText(_translate("self", "Update"))
        self.label_4.setText(_translate("self", "ip отправления"))
        self.lineEdit_4.setText(_translate("self", "127.0.0.1"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
