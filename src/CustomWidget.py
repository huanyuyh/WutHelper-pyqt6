import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QLabel, QLineEdit, QComboBox, QHBoxLayout, QMessageBox, QCheckBox)

from src.ConfigIni import read_Users, update_User


class AccountManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selectedPlatformIndex = 0
        self.username = ''
        self.password = ''
        self.selectedPlatform = ''
        self.userList = read_Users()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('账号密码管理')
        layout = QVBoxLayout()

        # 平台选择下拉框
        self.platformComboBox = QComboBox(self)

        items = self.userList.keys()
        self.platformComboBox.addItems(items)  # 可以添加更多平台
        self.platformComboBox.currentIndexChanged.connect(self.handleselectedPlatform)
        layout.addWidget(self.platformComboBox)

        # 账号输入框
        self.accountLineEdit = QLineEdit(self)
        self.accountLineEdit.setPlaceholderText('账号')
        self.accountLineEdit.textChanged.connect(self.handleUserChange)
        layout.addWidget(self.accountLineEdit)

        # 密码输入框
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setPlaceholderText('密码')
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)  # 设置为密码模式
        self.passwordLineEdit.textChanged.connect(self.handlePassChange)
        layout.addWidget(self.passwordLineEdit)

        # 显示密码复选框
        self.showPasswordCheckBox = QCheckBox('显示密码', self)
        layout.addWidget(self.showPasswordCheckBox)
        self.showPasswordCheckBox.toggled.connect(self.togglePasswordVisibility)

        # 保存和取消按钮
        buttonsLayout = QHBoxLayout()
        self.saveButton = QPushButton('保存', self)
        self.cancelButton = QPushButton('取消', self)
        buttonsLayout.addWidget(self.saveButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)

        self.setLayout(layout)

        # 连接按钮的信号
        self.saveButton.clicked.connect(self.saveAccountInfo)
        self.cancelButton.clicked.connect(self.close)
        self.platformComboBox.setCurrentIndex(1)
        self.platformComboBox.setCurrentIndex(0)
    def handleUserChange(self):
        self.username = self.accountLineEdit.text()
    def handlePassChange(self):
        self.password = self.passwordLineEdit.text()
    def handleselectedPlatform(self):
        self.selectedPlatformIndex = self.platformComboBox.currentIndex()
        self.selectedPlatform = self.platformComboBox.currentText()
        print(self.selectedPlatform)
        self.accountLineEdit.setText(self.userList[self.selectedPlatform]['username'])
        self.passwordLineEdit.setText(self.userList[self.selectedPlatform]['password'])

    def togglePasswordVisibility(self, checked):
        if checked:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def saveAccountInfo(self):
        # 这里应该添加保存账号密码的逻辑
        update_User(self.selectedPlatform,self.username,self.password)
        # ...

        QMessageBox.information(self, "信息", "账号密码已保存")
        self.close()