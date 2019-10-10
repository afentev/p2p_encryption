import os
import subprocess

from PyQt5 import QtWidgets, QtCore


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


def retranslate(self):
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


def initialize(self):
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


def byteinc(byte):
    for index in range(len(byte) - 1, -1, -1):
        if byte[index] != 255:
            byte[index] += 1
            return byte
    return bytearray(12)
