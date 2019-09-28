# -*- coding: utf-8 -*-
# TODO: migrate from socket to PyZMQ
# TODO: add address book with MAC-IP  (done, tests)
# TODO: improve work with window size (depends on screen)

import ast
import os
import socket
import subprocess
import sys

import rsa
from PyQt5 import QtCore, QtGui, QtWidgets


class NewAddressToBook(QtWidgets.QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        if os.geteuid() != 0:
            label = QtWidgets.QLabel('Not permitted. Run program with sudo')
            button = QtWidgets.QPushButton('Ok')
            self.layout.addWidget(label)
            self.layout.addWidget(button)
            button.clicked.connect(self.deleteLater)
        else:
            self.counter = 0
            self.rescan()

    def chkbox(self, arg):
        if arg:
            self.counter += 1
        else:
            self.counter -= 1
        if self.counter == 0:
            self.add_button.setDisabled(True)
        else:
            self.add_button.setDisabled(False)

    def rescan(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        result = subprocess.check_output(['arp-scan', '-l'], encoding='UTF-8').split('\n')[2:-4]
        self.checkboxes = []
        for i in result:
            checkbox = QtWidgets.QCheckBox(i.replace('\t', ' ' * 5), self)
            checkbox.clicked.connect(self.chkbox)
            self.checkboxes.append(checkbox)
            self.layout.addWidget(checkbox)
        self.add_button = QtWidgets.QPushButton('Add addresses to book')
        self.rescan_button = QtWidgets.QPushButton('Rescan')
        self.add_button.setDisabled(True)
        self.rescan_button.clicked.connect(self.rescan)
        self.add_button.clicked.connect(self.add)
        self.layout.addWidget(self.rescan_button)
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

    def add(self):
        try:
            with open('address_book.txt') as file:
                data = set(map(str.strip, file.readlines()))
        except FileNotFoundError:
            data = set()
        for i in self.checkboxes:
            if i.isChecked():
                data.add(i.text())
        with open('address_book.txt', 'w') as file:
            for position in data:
                print(position, file=file)
        self.deleteLater()


class AddressBook(QtWidgets.QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.execute()

    def execute(self):
        self.button = QtWidgets.QPushButton('Try it')
        self.button.clicked.connect(self.try_)
        self.button.setDisabled(True)

        try:
            with open('address_book.txt') as file:
                data = {}
                for pos in file.readlines():
                    pos = pos.strip().split(maxsplit=2)
                    data[pos[1]] = [pos[0] + ' (?)', pos[2]]
        except FileNotFoundError:
            data = {}

        try:
            result = subprocess.check_output(['arp-scan', '-l'], encoding='UTF-8').split('\n')[2:-4]
        except subprocess.CalledProcessError:  # not permitted
            result = []
        for i in result:
            i = i.split('\t')
            if i[1] in data:
                data[i[1]][0] = data[i[1]][0][:-4]

        self.radioboxes = []
        for mac, info in data.items():
            radiobox = QtWidgets.QRadioButton(info[0] + ' ' * 5 + mac + ' ' * 5 + info[1], self)
            radiobox.clicked.connect(self.rdbox)
            self.radioboxes.append(radiobox)
            self.layout.addWidget(radiobox)
        self.layout.addWidget(self.button)

    def rdbox(self, arg):
        if arg:
            self.button.setDisabled(False)

    def try_(self):
        for i in self.radioboxes:
            if i.isChecked():
                self.main.lineEdit_3.setText(i.text().split(' ' * 5)[0].replace(' (?)', ''))
                self.deleteLater()


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("self")
        self.resize(656, 603)
        self.setMaximumSize(656, 603)
        self.setMinimumSize(656, 603)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 400, 631, 101))
        self.lineEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 511, 631, 34))
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
        self.address_button = QtWidgets.QPushButton(self.centralwidget)
        self.address_button.setGeometry(QtCore.QRect(491, 11, 150, 26))
        self.address_button.setObjectName("pushButton_2")
        self.new_address_button = QtWidgets.QPushButton(self.centralwidget)
        self.new_address_button.setGeometry(QtCore.QRect(325, 11, 150, 26))
        self.new_address_button.setObjectName("pushButton_2")
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
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(10, 80, 631, 34))
        self.connect_button.setObjectName("pushButton_2")
        self.connect_button.clicked.connect(self.cn)
        self.address_book = set()
        self.new_address_button.clicked.connect(self.newaddresstobook)
        self.address_button.clicked.connect(self.addressbook)

        self.retranslateUi()

        self.pushButton_2.clicked.connect(self.send)

        self.string = ''
        self.connected = False

        self.show()

    def newaddresstobook(self):
        newaddresstobook_ = NewAddressToBook(self)
        newaddresstobook_.exec()

    def addressbook(self):
        addressbook_ = AddressBook(self)
        addressbook_.exec()

    def close_connection(self):
        try:
            self.connected = False
            self.statusbar.showMessage('Closing connection...', 5000)
            self.sock_receive.close()
            self.sock_send.close()
            self.conn.close()
            # self.sock_receive.shutdown(socket.SHUT_RDWR)
            # self.sock_send.shutdown(socket.SHUT_RDWR)
            # self.conn.shutdown(socket.SHUT_RDWR)

            # del self.sock_send
            # del self.sock_receive
            # del self.conn

            # cursor = self.textBrowser.textCursor()
            # cursor.clearSelection()
            # self.textBrowser.setTextCursor(cursor)
            self.textBrowser.clear()
            self.textBrowser.append('-----Connection was closed-----')

            self.connect_button.setText('Connect')
        except AttributeError:
            print(sys.exc_info())

    def __del__(self):
        self.close_connection()

    def show_(self):
        i = self.string
        self.statusbar.showMessage('Decoding...')
        if i:
            i = repr(i)
            i = ast.literal_eval(ast.literal_eval(i))
            i = rsa.decrypt(i, self.decode_send).decode('utf8')
            self.textBrowser.append('{}: {}'.format(str(self.addr), i))
            self.statusbar.showMessage('')
        self.string = ''

    def stack(self):
        try:
            message = self.conn.recv(1024)
            if message:
                self.string += str(message)
        except BlockingIOError:
            if self.string:
                self.show_()
        except OSError:
            er = QtWidgets.QErrorMessage(self)
            er.showMessage('Connection was closed, disconnecting :(')
            er.show()
            print(1111111)
        finally:
            if self.connected:
                QtCore.QTimer.singleShot(1, self.stack)

    def send(self, arg):
        try:
            print(self.connected)
            if self.connected:
                self.statusbar.showMessage('Sending...')
                text = self.lineEdit.text()
                print(self.encode_send)
                encrypted = rsa.encrypt(text.encode('UTF-8'), self.encode_send)
                print(encrypted)
                self.sock_send.send(encrypted)
                self.lineEdit.setText('')
                self.textBrowser.append('me: {}'.format(text))
                self.statusbar.showMessage('Success.', 5000)
        except AttributeError:
            self.statusbar.showMessage('Error. Connection was not established.')

    def connect_to_active_socket(self, receiver_ip, receiver_port, current_port):
        self.sock_send = socket.socket()
        self.sock_send.connect(('localhost' if receiver_ip == '127.0.0.1' else receiver_ip, receiver_port))
        self.sock_receive = socket.socket()
        self.sock_receive.bind(('', current_port))
        self.sock_receive.listen(1)
        self.conn, self.addr = self.sock_receive.accept()

    def cn(self):
        if not self.connected:
            self.statusbar.showMessage('Connecting...')
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
            self.statusbar.showMessage('Connection is established. Exchanging keys...')
            encode_send, self.decode_send = rsa.newkeys(512)
            self.sock_send.send(bytes(str(encode_send)[9:], encoding='UTF-8'))
            string = ''
            while True:
                try:
                    data = self.conn.recv(1024)
                    self.conn.setblocking(False)
                except BlockingIOError:
                    break
                string += str(data)[2:-1]
            keys = tuple(map(int, string[1:-1].split(', ')))
            self.encode_send = rsa.key.PublicKey(keys[0], keys[1])
            self.statusbar.showMessage('Ok.', 5000)
            self.connected = True
            self.conn.setblocking(False)
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit_3.setReadOnly(True)
            self.lineEdit_5.setReadOnly(True)
            self.connect_button.setText('Disconnect')

            QtCore.QTimer.singleShot(1, self.stack)
        else:
            self.close_connection()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == 16777216:
            self.cn()
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
        self.connect_button.setText(_translate("self", "Connect"))
        self.address_button.setText(_translate("self", "Address book"))
        self.new_address_button.setText(_translate("self", "Add new address"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
