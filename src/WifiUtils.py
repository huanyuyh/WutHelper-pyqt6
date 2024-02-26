import json
import platform
import subprocess
import time

import requests

from src import myQdialog
from src.ConfigIni import read_Configs, update_Config

'''
通过重定向地址 获取nasId
'''
def get_redirect_url(url):
    try:
        response = requests.get(url, allow_redirects=False)  # 设置 allow_redirects=False 来禁止自动重定向
        if response.status_code in [301, 302, 303, 307, 308]:
            redirectUrl = response.headers['Location']
            print(redirectUrl)
            if (redirectUrl.find("1.1.1.1") > 0):
                return f"connected"
            else:
                tempStart = redirectUrl.find("/api/r/") + len("/api/r/")
                tempEnd = redirectUrl.find("?userip")
                if (tempEnd and tempStart):
                    print(redirectUrl[tempStart:tempEnd])
                    return redirectUrl[tempStart:tempEnd]
        else:
            return "获取失败，请检测是否链接WIFI并关掉VPN"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"



def handlelogin(username,password,nasId,captcha=None,captchaId=None):
    print(f"登录尝试：用户名 - {username}, 密码 - {password}")
    # url = f"http://172.30.21.100/api/account/login?username={username}&password={password}&nasId={nasId}"
    if not captcha:
        url = f"http://172.30.21.100/api/account/login?username={username}&password={password}&nasId={nasId}"
    else:
        url = f"http://172.30.21.100/api/account/login?username={username}&password={password}&nasId={nasId}&captcha={captcha}&captchaId={captchaId}"
    payload = {}
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control': 'no-cache',
        'connection': 'Keep-Alive',
        'Host': '172.30.21.100',
        'Pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        print(response.text)
        print(result["msg"])
        if (result["msg"] == "认证成功"):
            print(result["online"]["Name"])
            print(result["online"]["UserIpv4"])
            print(result["online"]["UserMac"])
            return result
        else:
            if (result["msg"] == "认证失败"):
                return result["msg"] + ",请检查nasId是否正确"
            elif (result["msg"] == "需要验证码"):
                print(result["captcha"]["picPath"])
                strtemp = str(result["captcha"]["picPath"])
                dlg = CaptchaDialog(strtemp.replace("data:image/png;base64,","").replace("\n",""),str(result["captcha"]["captchaId"]),username,password,nasId)
                dlg.exec()
                return "需要验证码，是否打开网页验证(也可再次点击登录可能会取消验证码)"
            else:
                return "Error:"+result["msg"]
    except OSError as e:
        print(e)
        return "您貌似没有链接wifi"
        pass
    except json.decoder.JSONDecodeError as e:
        print(e)
        return "您貌似没有链接wifi"
        pass
    except:
        pass

def init_login():
    url = f"http://172.30.21.100/api/account/login?username=329&password=123&nasId=14"
    payload = {}
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control': 'no-cache',
        'connection': 'Keep-Alive',
        'Host': '172.30.21.100',
        'Pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        print(result)
        print(result["msg"])
        if (result["msg"] == "认证成功"):
            print(result["msg"])
            print("网络已连接!\n欢迎！"+result["online"]["Name"]+"链接成功")
            return f"网络已连接!\n欢迎"+result["online"]["Name"]+"链接成功"
        else:
            return False
    except:
        return False

def check_internet():
    # 选择适合操作系统的ping命令
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # 运行ping命令
    command = ['ping', param, '1', 'bilibili.com']
    try:
        if platform.system().lower() == 'windows':
            # 在Windows上运行，不显示窗口
            subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            # 在其他操作系统上运行
            subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("网络已链接")
        return True
    except subprocess.CalledProcessError:
        return False

def on_no_internet(loginWindow):
    """ 当网络不可用时执行的操作 """
    # 在这里添加你想执行的命令
    if not hasattr(on_no_internet, "wifiStatus"):
        on_no_internet.wifiStatus = -1  # 初始值
    print(on_no_internet.wifiStatus)
    if check_internet():
        if (on_no_internet.wifiStatus != 6):
            loginWindow.trayIcon.showMessage("网络链接恢复", "流畅的冲浪吧")
        on_no_internet.wifiStatus = 6
    config = read_Configs()
    username = config['username']
    password = config['password']
    nasId = config['nasId']
    url = f"http://172.30.21.100/api/account/login?username={username}&password={password}&nasId={nasId}"

    payload = {}
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control': 'no-cache',
        'connection': 'Keep-Alive',
        'Host': '172.30.21.100',
        'Pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        if(result["msg"] == "认证成功"):
                loginWindow.trayIcon.showMessage("网络断开", "已为您重连")
        else:
            if (result["msg"] == "认证失败"):
                if (on_no_internet.wifiStatus != 1):
                    loginWindow.trayIcon.showMessage("网络断开", result["msg"]+",请检测nasId是否正确")
                on_no_internet.wifiStatus != 1
            elif (result["msg"] == "需要验证码"):
                if (on_no_internet.wifiStatus != 2):
                    on_no_internet.wifiStatus = 2
                    on_no_internet()
            else:
                if (on_no_internet.wifiStatus != 3):
                    loginWindow.trayIcon.showMessage("网络断开", result["msg"])
                on_no_internet.wifiStatus = 3
    except OSError:
        if (on_no_internet.wifiStatus != 4):
            loginWindow.trayIcon.showMessage("网络断开", "您貌似没有链接wifi")
        on_no_internet.wifiStatus = 4
        pass
    except json.decoder.JSONDecodeError:
        if (on_no_internet.wifiStatus != 5):
            loginWindow.trayIcon.showMessage("网络断开", "您貌似没有链接wifi")
        on_no_internet.wifiStatus = 5
        pass
    finally:
        pass
    print("网络不可用，执行特定命令")

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from base64 import b64decode
from io import BytesIO


class CaptchaDialog(QDialog):
    def __init__(self,base64_image_data,captchaId,username,password,nasId):
        self.captchaId =captchaId
        self.base64_image_data = base64_image_data
        self.username = username
        self.password = password
        self.nasId = nasId
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('输入验证码')
        self.setFixedSize(220, 140)

        layout = QVBoxLayout()

        # 显示验证码图片
        self.image_label = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(b64decode(self.base64_image_data))
        self.image_label.setPixmap(pixmap.scaled(200, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))  # 调整尺寸以适应窗口
        layout.addWidget(self.image_label)

        # 输入框
        self.captcha_input = QLineEdit(self)
        self.captcha_input.setPlaceholderText('请输入验证码')
        layout.addWidget(self.captcha_input)

        # 确认按钮
        self.confirm_button = QPushButton('确认', self)
        self.confirm_button.clicked.connect(self.onConfirm)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)
    def showWranningDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Wranning")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
    def onConfirm(self):
        # 获取输入的验证码
        captcha = self.captcha_input.text()
        print("输入的验证码是:", captcha)
        # 这里可以添加发送请求的代码
        # 发送请求代码
        self.accept()
        login_result = handlelogin(self.username, self.password, self.nasId,captcha,self.captchaId)
        print(str(login_result))
        if (str(login_result).find("请检查nasId") != -1):
            self.showWranningDialog(login_result)
            # elif(login_result.find("需要验证码")!=-1):
            #     self.showWranningNeedDialog("需要验证码，是否打开网页验证(也可再次点击登录可能会取消验证码)")
        elif (str(login_result).find("Error") != -1):
            self.showWranningDialog(login_result)
        elif (str(login_result).find("没有链接") != -1):
            self.showWranningDialog(login_result)
        else:
            update_Config('username', self.username)
            update_Config('password', self.password)
            update_Config('nasId', self.nasId)
            try:
                dialog = myQdialog.WutWifiJSONViewer(login_result)
                dialog.exec()
            except:
                pass