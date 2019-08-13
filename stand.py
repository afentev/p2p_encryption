# -*- coding: utf-8 -*-

import socket
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import crypto


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("self")
        self.resize(656, 563)
        self.setMaximumSize(656, 543)
        self.setMinimumSize(656, 543)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 359, 631, 101))
        self.lineEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 470, 631, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(11, 45, 96, 19))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 45, 176, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(470, 45, 171, 25))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(325, 45, 136, 19))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 11, 176, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(11, 11, 120, 19))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 79, 631, 271))
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

        self.pushButton_2.clicked.connect(self.send)

        self.string = ''

        self.show()

    def __del__(self):
        try:
            self.sock_receive.close()
            self.sock_send.close()
        except AttributeError:
            pass

    def show_(self):
        print(self.string)
        for i in self.string.split('\\n'):
            if i:
                i = crypto.decode_function(i, *self.decode_send)
                self.textBrowser.append('{}: {}'.format(str(self.addr), i))
                self.counter += 1
        self.string = ''

    def stack(self):
        try:
            message = self.conn.recv(1024).decode('utf-8')
            if message:
                self.string += str(message)
        except:
            if self.string:
                self.show_()
            QtCore.QTimer.singleShot(1, self.stack)
            return
        QtCore.QTimer.singleShot(1, self.stack)
        return

    def send(self, arg):
        try:
            text = self.lineEdit.text()
            encrypted = crypto.encode_function(text, *self.encode_send)
            print(encrypted)
            self.sock_send.send(bytes(encrypted + '\n', encoding='UTF-8'))
            self.lineEdit.setText('')
            self.textBrowser.append('me: {}'.format(text))
        except AttributeError:
            pass

    def connect_to_active_socket(self, receiver_ip, receiver_port, current_port):
        self.sock_send = socket.socket()
        self.sock_send.connect(('localhost' if receiver_ip == '127.0.0.1' else receiver_ip, receiver_port))
        self.sock_receive = socket.socket()
        self.sock_receive.bind(('', current_port))
        self.sock_receive.listen(1)
        self.conn, self.addr = self.sock_receive.accept()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == 16777216:
            receiver_ip, receiver_port, current_port = (self.lineEdit_3.text(), int(self.lineEdit_2.text()),
                                                        int(self.lineEdit_5.text()))
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
            self.stack()
        elif a0.key() == 16777268:
            self.update_messages(None)
        elif a0.key() == 16777220:
            self.send(None)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.pushButton_2.setText(_translate("self", "Send"))
        self.label_2.setText(_translate("self", "Порт №1"))
        self.lineEdit_2.setText(_translate("self", "8082"))
        self.lineEdit_5.setText(_translate("self", "8081"))
        self.label_3.setText(_translate("self", "Порт №2"))
        self.lineEdit_3.setText(_translate("self", "127.0.0.1"))
        self.label.setText(_translate("self", "ip получения"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
