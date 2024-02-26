import os
import sys
import json
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox
import WIFI_rc
from src.ConfigIni import read_Users, update_Service


class JSONViewer(QDialog):
    def __init__(self, json_data):
        super().__init__()
        self.initUI(json_data)

    def initUI(self, json_data):
        layout = QVBoxLayout()

        # 解析JSON数据，并将其添加到布局中
        for key, value in json_data.items():
            if isinstance(value, dict):  # 如果值是字典，进一步解析
                for sub_key, sub_value in value.items():
                    label = QLabel(f"{sub_key}: {sub_value}")
                    layout.addWidget(label)
            else:
                label = QLabel(f"{key}: {value}")
                layout.addWidget(label)

        self.setLayout(layout)
        self.setWindowTitle("登陆成功")
        self.setWindowIcon(QIcon(':/WIFI.png'))

class addWebDialog(QDialog):
    def __init__(self,parent):
        script_path = os.path.abspath(sys.argv[0])
        self.path = os.path.dirname(script_path) + "/serviceList.txt"
        self.parent = parent
        self.platName = ""
        self.platUrl = ""
        self.selectedUser = ""
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.platformNameLabel = QLabel('名称:', self)
        self.platformName = QLineEdit(self)
        self.platformName.textChanged.connect(self.platformNameChange)
        namelayout = QHBoxLayout()
        namelayout.addWidget(self.platformNameLabel)
        namelayout.addWidget(self.platformName)
        layout.addLayout(namelayout)

        self.platformUrlLabel = QLabel('网址:', self)
        self.platformUrl = QLineEdit(self)
        self.platformUrl.textChanged.connect(self.platformUrlChange)
        urllayout = QHBoxLayout()
        urllayout.addWidget(self.platformUrlLabel)
        urllayout.addWidget(self.platformUrl)
        layout.addLayout(urllayout)

        self.userLineLabel = QLabel("账号所属平台:")
        self.userQComboBox = QComboBox(self)
        userList = read_Users()
        print(userList.keys())
        for name in userList.keys():
            print(name)
            self.userQComboBox.addItem(name)
        self.userQComboBox.currentIndexChanged.connect(self.handleSelectedUserChange)
        self.selectedUser = self.userQComboBox.currentText()
        selecteduser = QHBoxLayout()
        selecteduser.addWidget(self.userLineLabel)
        selecteduser.addWidget(self.userQComboBox)
        layout.addLayout(selecteduser)

        self.addButton = QPushButton("添加",self)
        self.addButton.clicked.connect(self.handleAdd)
        layout.addWidget(self.addButton)
        self.setLayout(layout)

        self.resize(400, 200)
        self.setWindowTitle("添加快捷方式")
        self.setWindowIcon(QIcon(':/WIFI.png'))

    # def closeEvent(self, event):
    #     # 当子窗口关闭时，更新父窗口
    #     if self.parent:
    #         self.parent.updateLayout()
    #     super().closeEvent(event)
    def handleSelectedUserChange(self):
        self.selectedUser = self.userQComboBox.currentText()
    def handleAdd(self):
        if(len(self.platName)>0 and len(self.platUrl)>0):
            if (self.platUrl.find("http")==-1 and self.platUrl.find("www")==-1 and self.platUrl.find(".")==-1):
                self.showInformationDialog("你的地址可能不正确，不过还是为你添加啦！")
            update_Service(self.platName, self.platUrl, self.selectedUser)
            # self.parent.close()
            # self.parent.__init__()
            # self.parent.show()
            self.parent.updateLayout()
            self.destroy()
        else:
            self.showErrorDialog("信息不能为空")

    def showInformationDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Information")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        ret = msgBox.exec()
    def showErrorDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def platformNameChange(self):
        self.platName = self.platformName.text()
        print(self.platName)
    def platformUrlChange(self):
        self.platUrl = self.platformUrl.text()
        print(self.platUrl)
class EditDialog(QDialog):
    def __init__(self,services, parent = None):
        self.services = dict(services)
        self.urlText = ""
        self.selectedUser = ""
        self.parent = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("修改快捷方式")
        self.setWindowIcon(QIcon(":/WIFI.png"))
        layout = QVBoxLayout(self)
        self.selectedLabel = QLabel("网站名称:")
        self.selectedWeb = QComboBox(self)
        selectedBox = QHBoxLayout(self)
        selectedBox.addWidget(self.selectedLabel)
        selectedBox.addWidget(self.selectedWeb)
        layout.addLayout(selectedBox)
        for name,url in self.services.items():
            self.selectedWeb.addItem(name, url)
        self.selectedWeb.currentIndexChanged.connect(self.handleselectedWebChange)

        self.urlLineLabel = QLabel("url:")
        self.urlLineEdit = QLineEdit(self)
        self.urlLineEdit.textChanged.connect(self.handleUrlTextChange)
        self.urlLineEdit.setText(eval(self.selectedWeb.currentData())['platUrl'])
        selectedUrl = QHBoxLayout(self)
        selectedUrl.addWidget(self.urlLineLabel)
        selectedUrl.addWidget(self.urlLineEdit)
        layout.addLayout(selectedUrl)

        self.userLineLabel = QLabel("账号所属平台:")
        self.userQComboBox = QComboBox(self)
        userList = read_Users()
        print(userList.keys())
        for name in userList.keys():
            print(name)
            self.userQComboBox.addItem(name)
        self.userQComboBox.currentIndexChanged.connect(self.handleSelectedUserChange)
        self.userQComboBox.setCurrentText(eval(self.selectedWeb.currentData())['useUser'])
        selecteduser = QHBoxLayout()
        selecteduser.addWidget(self.userLineLabel)
        selecteduser.addWidget(self.userQComboBox)
        layout.addLayout(selecteduser)

        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.onSave)
        layout.addWidget(self.saveButton)

        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.clicked.connect(self.onDelete)
        layout.addWidget(self.deleteButton)
        self.resize(400,200)
    def handleSelectedUserChange(self):
        self.selectedUser = self.userQComboBox.currentText()
    def handleUrlTextChange(self):
        self.urlText = self.urlLineEdit.text()
    def handleselectedWebChange(self):
        self.urlLineEdit.setText(eval(self.selectedWeb.currentData())['platUrl'])
        self.userQComboBox.setCurrentText(eval(self.selectedWeb.currentData())['useUser'])
        # print(self.selectedWeb.currentData())

    def onSave(self):
        update_Service(self.selectedWeb.currentText(), self.urlText, self.selectedUser)

    def showErrorDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
    def onDelete(self):
        name = self.selectedWeb.currentText()
        removed_value = self.services.pop(name, "Key not found")
        print(removed_value)
        print(self.services)
        self.saveServices()
        self.parent.close()
        self.parent.__init__()
        self.parent.show()
        self.close()
        self.__init__(self.services,self.parent)
        self.show()

class removeWebDialog(QDialog):
    def __init__(self,parent):
        script_path = os.path.abspath(sys.argv[0])
        self.path = os.path.dirname(script_path) + "/serviceList.txt"
        self.parent = parent
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Table Example")

        self.tableWidget = QTableWidget(5, 3, self)  # 5 rows, 3 columns
        self.setCentralWidget(self.tableWidget)

        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f"Item {i + 1}-{j + 1}")
                self.tableWidget.setItem(i, j, item)

        self.tableWidget.doubleClicked.connect(self.editItem)

    def editItem(self, index):
        self.editDialog = EditDialog(self)
        self.currentItem = self.tableWidget.item(index.row(), index.column())
        self.editDialog.lineEdit.setText(self.currentItem.text())
        self.editDialog.show()

    def updateItem(self, text):
        self.currentItem.setText(text)

    def deleteItem(self):
        self.tableWidget.removeRow(self.currentItem.row())
class WutWifiJSONViewer(QDialog):
    def __init__(self, json_data):
        super().__init__()
        self.initUI(json_data)

    def initUI(self, json_data):
        layout = QVBoxLayout()
        msg = json_data["msg"]
        name = json_data["online"]["Name"]
        ipv4 = json_data["online"]["UserIpv4"]
        mac = json_data["online"]["UserMac"]
        label = QLabel(f"欢迎! {name}")
        layout.addWidget(label)
        label = QLabel(f"msg: {msg}")
        layout.addWidget(label)
        label = QLabel(f"ipv4: {ipv4}")
        layout.addWidget(label)
        label = QLabel(f"MAC: {mac}")
        layout.addWidget(label)

        self.setLayout(layout)
        self.setWindowTitle("登陆成功")
        self.setWindowIcon(QIcon(':/WIFI.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # JSON数据
    json_string = '{"authCode":"","authMsg":"","code":0,"dialCode":"ok:dialup","dialMsg":"已拨号成功","enableDial":true,"msg":"认证成功","online":{"AddTime":"2023-12-12T16:10:01+08:00","BytesIn4":"33988801","Name":"","UserIpv4":"10.76.15.99","UserMac":"b4:8c:9d:aa:7c:bb","UserSourceType":"local","Username":""}}'
    json_data = json.loads(json_string)

    dialog = JSONViewer(json_data)
    dialog.show()

    sys.exit(app.exec_())
