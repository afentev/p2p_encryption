# -*- coding: utf-8 -*-
# TODO: migrate from socket to PyZMQ
# TODO: add address book with MAC-IP  (done, tests)
# TODO: improve work with window size (depends on screen)

import ast
import os
import socket
import sys
import time

import rsa
from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

import msgLib


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        msgLib.initialize(self)

        self.string = ''
        self.connected = False

        self.show()

    def newaddresstobook(self):
        newaddresstobook_ = msgLib.NewAddressToBook(self)
        newaddresstobook_.exec()

    def addressbook(self):
        addressbook_ = msgLib.AddressBook(self)
        addressbook_.exec()

    def close_connection(self):
        try:
            self.connected = False
            self.statusbar.showMessage('Closing connection...', 5000)
            self.sock_receive.close()
            self.sock_send.close()
            self.conn.close()

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
            i = self.decode_chacha.decrypt(self.decode_nonce, i, self.decode_aad).decode('utf8')
            self.textBrowser.append('{}: {}'.format(str(self.addr), i))
            self.decode_nonce = msgLib.byteinc(self.decode_nonce)
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
        finally:
            if self.connected:
                QtCore.QTimer.singleShot(1, self.stack)

    def send(self, arg):
        try:
            if self.connected:
                self.statusbar.showMessage('Sending...')
                text = self.lineEdit.text()
                encrypted = self.encode_chacha.encrypt(self.encode_nonce, text.encode('utf8'), self.encode_aad)
                print(encrypted)
                self.sock_send.send(encrypted)
                self.lineEdit.setText('')
                self.textBrowser.append('me: {}'.format(text))

                self.encode_nonce = msgLib.byteinc(self.encode_nonce)

                self.statusbar.showMessage('Success.', 5000)
        except AttributeError:
            self.statusbar.showMessage('Error. Connection was not established.')

    def connect_to_active_socket(self, receiver_ip, receiver_port, current_port):
        # NWPCK;LNGTH=4096;REQ=MSG;
        # NWPCK;LNGTH=4096;REQ=AADUPD;
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
            encode_send, self.decode_send = rsa.newkeys(2048)
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

            self.encode_aad = os.urandom(32)
            self.encode_key = ChaCha20Poly1305.generate_key()
            # self.nonce = bytes(str(os.urandom(16)), encoding='utf8')
            self.encode_nonce = os.urandom(12)
            self.encode_chacha = ChaCha20Poly1305(self.encode_key)
            text = str(self.encode_aad) + '``' + str(self.encode_nonce) + '``' + str(self.encode_key)
            self.encode_nonce = bytearray(self.encode_nonce)
            encrypted = rsa.encrypt(text.encode('UTF-8'), self.encode_send)
            self.sock_send.send(encrypted)
            string = ''
            time.sleep(1)
            while True:
                try:
                    self.conn.setblocking(False)
                    data = self.conn.recv(1024)
                except BlockingIOError:
                    break
                string += str(data)
            string = repr(string)
            string = ast.literal_eval(ast.literal_eval(string))
            string = rsa.decrypt(string, self.decode_send).decode('utf8')
            self.decode_aad, self.decode_nonce, self.decode_key = string.split('``')
            self.decode_aad, self.decode_nonce, self.decode_key = (ast.literal_eval(self.decode_aad),
                                                                   bytearray(ast.literal_eval(self.decode_nonce)),
                                                                   ast.literal_eval(self.decode_key))
            self.decode_chacha = ChaCha20Poly1305(self.decode_key)

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
        msgLib.retranslate(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())