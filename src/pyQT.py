import webbrowser
import WIFI_rc
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QIcon, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QVBoxLayout, QMessageBox, \
    QSystemTrayIcon, QMenu, QHBoxLayout, QGridLayout, QComboBox
import threading
import time
import myQdialog
import os, sys
from qt_material import apply_stylesheet
from qt_material import list_themes

from AutoRun import AutoRun
from CustomTitleBars import CustomTitleBar
from WifiUtils import get_redirect_url, handlelogin, init_login, check_internet, on_no_internet
from src.ConfigIni import read_Configs, read_Services, update_Config, init_Configs, init_Services, init_Users
from src.CourseHTML import parse_course_html, load_courses_from_csv, weeks_from, CourseTable
from src.CustomWidget import AccountManagerWindow
from src.WebOpen import webOpen, JWCwebOpen


class LoginWindow(QWidget):
    def __init__(self,parent):
        self.services = read_Services()
        print(list(self.services))
        super().__init__()
        self.selectedTheme = "11"
        self.parent = parent
        self.username = ""
        self.password = ""
        self.nasId = ""
        self.isRemember = False
        self.isBack = False
        self.isStartUp = False
        self.isWebAutoLogin = False
        script_path = os.path.abspath(sys.argv[0])
        path = os.path.dirname(script_path) + "/config.txt"
        self.configPath = path
        self.initUI()
        self.initSystemTray()
        self.service_thread = None
        self.service_action = {'run': False}
        self.process = None
        self.loadCredentials()
        #self.init_login()
    def updateLayout(self):
        # 创建网格布局实例
        self.services = read_Services()
        numRow = 4
        numColumn = len(self.services)
        isColumn = numColumn % numRow
        print(isColumn)
        numColumn = int(numColumn / numRow)
        print(numColumn)
        if (isColumn) > 0:
            numColumn += 1
        # 创建一系列按钮
        positions = [(i, j) for i in range(numColumn) for j in range(numRow)]
        for position in positions:
            columns, rows = position
            # print(columns)
            # print(rows)
            key = list(self.services)
            if (columns * 4 + rows) < len(key):
                name = key[columns * 4 + rows]
                button = QPushButton(f"{name}")
                button.clicked.connect(lambda checked, pos=position: self.on_button_clicked(pos))
                self.grid.addWidget(button, *position)
    def initSystemTray(self):
        self.trayIcon = QSystemTrayIcon(QIcon(':/WIFI.png'), self)  # 使用你自己的图标
        self.trayIcon.setToolTip('WUT网络检查服务控制')
        self.trayIcon.activated.connect(self.onTrayIconActivated)
        # 创建一个菜单
        self.trayMenu = QMenu()

        # 添加一个退出动作
        exitAction = QAction('退出', self)
        exitAction.triggered.connect(self.closeApplication)  # 修改这里
        showAction = QAction('打开主界面', self)
        showAction.triggered.connect(self.showApplication)  # 修改这里
        self.trayMenu.addAction(showAction)
        self.trayMenu.addAction(exitAction)
        # 设置托盘图标的菜单
        self.trayIcon.setContextMenu(self.trayMenu)
        # 显示托盘图标
        self.trayIcon.show()
    def initUI(self):
        # 设置布局
        layout = QVBoxLayout()
        # 创建控件
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 隐藏默认标题栏
        self.titleBar = CustomTitleBar("WUT小助手",self)
        layout.addWidget(self.titleBar)

        self.usernameLabel = QLabel('用户名:', self)
        self.usernameInput = QLineEdit(self)
        self.usernameInput.textChanged.connect(self.userChange)
        self.userBox = QHBoxLayout()
        self.userBox.addWidget(self.usernameLabel)
        self.userBox.addWidget(self.usernameInput)

        self.nasIdLabel = QLabel('nasId:', self)
        self.nasIdInput = QLineEdit(self)
        self.nasIdInput.textChanged.connect(self.nasIdChange)
        # 创建一个 QDoubleValidator 对象
        validator = QIntValidator()
        validator.setBottom(0)  # 设置最小值，例如0
        # 设置验证器到 QLineEdit
        self.nasIdInput.setValidator(validator)
        self.nasBox = QHBoxLayout()
        self.nasBox.addWidget(self.nasIdLabel)
        self.nasBox.addWidget(self.nasIdInput)

        self.userNasBox = QHBoxLayout()
        self.userNasBox.addLayout(self.userBox)
        self.userNasBox.addLayout(self.nasBox)
        layout.addLayout(self.userNasBox)

        self.passwordLabel = QLabel('密码:', self)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordInput.textChanged.connect(self.passChange)
        self.passBox = QHBoxLayout()
        self.passBox.addWidget(self.passwordLabel)
        self.passBox.addWidget(self.passwordInput)

        self.showPassCheckBox = QCheckBox('显示密码', self)
        self.showPassCheckBox.stateChanged.connect(self.togglePasswordVisibility)

        self.showPassBox = QHBoxLayout()
        self.showPassBox.addLayout(self.passBox)
        self.showPassBox.addWidget(self.showPassCheckBox)
        layout.addLayout(self.showPassBox)


        self.loginButton = QPushButton('登录', self)
        self.loginButton.clicked.connect(self.tryHandleLogin)

        self.rememberCheckBox = QCheckBox('记住密码', self)
        #remeber信号槽在后面函数写的

        self.loginBox = QHBoxLayout()
        self.loginBox.addWidget(self.rememberCheckBox)
        self.loginBox.addWidget(self.loginButton)
        layout.addLayout(self.loginBox)

        self.noLoginWebButton = QPushButton('认证页面打不开请点我(172.30.21.100)',self)
        self.noLoginWebButton.clicked.connect(self.handleWebNoOpen)

        self.loginWebButton = QPushButton('打开认证界面（1.1.1.1）', self)
        self.loginWebButton.clicked.connect(self.handleWebOpen)

        self.getNasId = QPushButton("尝试获取nasId", self)
        self.getNasId.clicked.connect(self.try_get_redirect_url)

        self.webLoginBox = QHBoxLayout()
        self.webLoginBox.addWidget(self.loginWebButton)
        self.webLoginBox.addWidget(self.noLoginWebButton)
        self.webLoginBox.addWidget(self.getNasId)
        layout.addLayout(self.webLoginBox)


        self.autoLogincheckBox = QCheckBox('使用web自动登录', self)
        self.autoLogincheckBox.stateChanged.connect(self.toggle_autoWebLogin)
        self.backcheckBox = QCheckBox('启动/停止后台网络保活服务', self)
        self.backcheckBox.stateChanged.connect(self.toggle_service)
        self.startCheckBox = QCheckBox('设置开机自启动', self)
        self.otherAutoBox = QHBoxLayout()
        self.otherAutoBox.addWidget(self.backcheckBox)
        self.otherAutoBox.addWidget(self.startCheckBox)
        self.otherAutoBox.addWidget(self.autoLogincheckBox)
        layout.addLayout(self.otherAutoBox)
        self.ServicesLabel = QLabel('校园平台快捷方式', self)
        layout.addWidget(self.ServicesLabel)
        # 创建网格布局实例
        self.grid = QGridLayout()
        numRow = 4
        numColumn = len(self.services)
        isColumn = numColumn%numRow
        print(isColumn)
        numColumn = int(numColumn/numRow)
        print(numColumn)
        if(isColumn)>0:
            numColumn+=1
        # 创建一系列按钮
        positions = [(i, j) for i in range(numColumn) for j in range(numRow)]
        for position in positions:
            columns,rows = position
            # print(columns)
            # print(rows)
            key = list(self.services)
            if(columns*4+rows)<len(key):
                name = key[columns * 4+rows]
                button = QPushButton(f"{name }")
                button.clicked.connect(lambda checked, pos=position: self.on_button_clicked(pos))
                self.grid.addWidget(button, *position)
        layout.addLayout(self.grid)

        self.addWebButton = QPushButton('添加快捷方式', self)
        self.addWebButton.clicked.connect(self.handleAddWebOpen)
        self.removeWebButton = QPushButton('删除/修改快捷方式', self)
        self.removeWebButton.clicked.connect(self.handleRemoveWebOpen)
        self.userManagerButton = QPushButton('管理账号密码', self)
        self.userManagerButton.clicked.connect(self.handleUserManager)
        self.webButtonBox = QHBoxLayout()
        self.webButtonBox.addWidget(self.addWebButton)
        self.webButtonBox.addWidget(self.removeWebButton)
        self.webButtonBox.addWidget(self.userManagerButton)
        layout.addLayout(self.webButtonBox)
        self.courseInsertDailog = QPushButton('进行课表导入', self)
        self.courseShowDailog = QPushButton('查询课程表', self)
        self.courseShowDailog.clicked.connect(self.handleShowCourse)
        self.courseInsertDailog.clicked.connect(self.handleInsertCourse)
        self.courseBox = QHBoxLayout()
        self.courseBox.addWidget(self.courseInsertDailog)
        self.courseBox.addWidget(self.courseShowDailog)
        layout.addLayout(self.courseBox)

        self.huanyuIdLabel = QLabel('BY: 偶尔下雨huanyu\nBUG反馈-QQ:1771944242', self)
        layout.addWidget(self.huanyuIdLabel)
        self.themeLabel = QLabel("主题选择:")
        self.themeSelected = QComboBox(self)
        themeList = {
                    "黑暗琥珀色": "dark_amber.xml",
                    "黑暗蓝色": "dark_blue.xml",
                    "黑暗青色": "dark_cyan.xml",
                    "黑暗浅绿色": "dark_lightgreen.xml",
                    "黑暗医疗色": "dark_medical.xml",
                    "黑暗粉色": "dark_pink.xml",
                    "黑暗紫色": "dark_purple.xml",
                    "黑暗红色": "dark_red.xml",
                    "黑暗蓝绿色": "dark_teal.xml",
                    "黑暗黄色": "dark_yellow.xml",
                    "浅暗琥珀色": "light_amber.xml",
                    "浅暗蓝色": "light_blue.xml",
                    "浅蓝色 500": "light_blue_500.xml",
                    "浅暗青色": "light_cyan.xml",
                    "浅青色 500": "light_cyan_500.xml",
                    "浅暗浅绿色": "light_lightgreen.xml",
                    "浅浅绿色 500": "light_lightgreen_500.xml",
                    "浅暗橙色": "light_orange.xml",
                    "浅暗粉色": "light_pink.xml",
                    "浅粉色 500": "light_pink_500.xml",
                    "浅暗紫色": "light_purple.xml",
                    "浅紫色 500": "light_purple_500.xml",
                    "浅暗红色": "light_red.xml",
                    "浅红色 500": "light_red_500.xml",
                    "浅暗蓝绿色": "light_teal.xml",
                    "浅蓝绿色 500": "light_teal_500.xml",
                    "浅暗黄色": "light_yellow.xml"
                }

        for name,str in themeList.items():
            self.themeSelected.addItem(name, str)
        print(list_themes())
        self.themeBox = QHBoxLayout()
        self.themeBox.addWidget(self.themeLabel)
        self.themeBox.addWidget(self.themeSelected)
        self.themeSelected.setCurrentIndex(11)
        self.themeSelected.currentIndexChanged.connect(self.handleselectedTheme)
        layout.addLayout(self.themeBox)

        self.themeBox.addStretch(1)

        layout.addStretch(1)
        self.setLayout(layout)
        self.setWindowTitle('WUT小助手')
        self.setWindowIcon(QIcon(':/WIFI.png'))
        self.resize(600,400)
    '''
    输入框改变函数
    '''
    def userChange(self):
        self.username = self.usernameInput.text()
    def passChange(self):
        self.password = self.passwordInput.text()
    def nasIdChange(self):
        self.nasId = self.nasIdInput.text()
        update_Config('nasId', str(self.nasId))
    '''
    复选框改变函数
    '''
    def handleRememberPassword(self, state):
        self.isRemember = self.rememberCheckBox.isChecked()
        if state == 2:
        # 处理记住密码
            self.saveCredentials()
            self.rememberCheckBox.stateChanged.connect(self.handleRememberPassword)
        else:
            self.removeUserPass()
            self.rememberCheckBox.stateChanged.connect(self.handleRememberPassword)
    def toggle_startup(self,state):
        self.isStartUp = self.startCheckBox.isChecked()
        """开机自启动函数"""
        update_Config('isStartUp',str(self.isStartUp))
        if state == 2:
            AutoRun(switch='open', key_name='WIFIHY')  # 键的名称应该起得特别一些，起码和已经存在的自启动软件名称不一致
        else:
            AutoRun(switch='close', key_name='WIFIHY')
    def toggle_service(self, state):
        self.isBack = self.backcheckBox.isChecked()
        update_Config('isBack', str(self.isBack))
        if state == 2:  # 复选框被选中
            if not self.service_thread:
                self.start_service()

        else:  # 复选框未被选中
            if self.service_thread:
                self.stop_service()

    def togglePasswordVisibility(self, checked):
        if checked:
            self.passwordInput.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)
    '''
    按钮操作函数
    '''
    def handleInsertCourse(self):
        driver = JWCwebOpen(self.isWebAutoLogin,'智慧理工大','http://sso.jwc.whut.edu.cn/Certification/index2.jsp')

    def handleShowCourse(self):
        parse_course_html(os.path.dirname(script_path) + "/jwc.html")
        courses = load_courses_from_csv(os.path.dirname(script_path) + "/courses.csv")
        target_date_str = "2023-09-03"  # 请将此替换为你的目标日期
        # weeks = weeks_from(target_date_str)
        self.courseTable = CourseTable(courses, 1)
        self.courseTable.show()
    def handleUserManager(self):
        self.accountManager = AccountManagerWindow()
        self.accountManager.show()
    def on_button_clicked(self, position):
        columns, rows = position
        key = list(self.services)
        print(key)
        name = key[columns * 4 + rows]
        print(self.services[name])
        url = eval(self.services[name])['platUrl']
        print(url)
        useUser = eval(self.services[name])['useUser']
        try:
            webOpen(self.isWebAutoLogin,useUser,url)
        except Exception as e:
            print(f"Error:{e}")
            pass
        # webbrowser.open(url)
        print(f"Button at position {position} clicked")
    def tryHandleLogin(self):
        if (self.service_action['run'] == True and self.isBack):
            self.stop_service()
        username = self.username
        password = self.password
        nasId = self.nasId
        try_test_login = init_login()
        if not try_test_login:
            login_result = handlelogin(username,password,nasId)
            if(str(login_result).find("请检查nasId")!=-1):
                self.showWranningDialog(login_result)
            # elif(login_result.find("需要验证码")!=-1):
            #     self.showWranningNeedDialog("需要验证码，是否打开网页验证(也可再次点击登录可能会取消验证码)")
            elif (str(login_result).find("Error") != -1):
                self.showWranningDialog(login_result)
            elif(str(login_result).find("没有链接") != -1):
                self.showWranningDialog(login_result)
            else:
                self.saveCredentials()
                try:
                    dialog = myQdialog.WutWifiJSONViewer(login_result)
                    dialog.exec()
                    self.tryHandleLogin.wifiStatus = 0
                except:
                    pass

        else:
            self.showInformationDialog(try_test_login)
        if (self.service_action['run'] == False and self.isBack):
            self.start_service()
    def try_get_redirect_url(self):
        url = "http://1.1.1.1"
        red_result: str = get_redirect_url(url)
        if red_result.find("connected")!=-1:
            self.showInformationDialog("网络畅通无法获取，获取请链接校园网但不登录")
        elif red_result.find("Error")!=-1:
            self.showErrorDialog("获取失败" + red_result)
        elif red_result.find("获取失败")!=-1:
            self.showInformationDialog(red_result)
        else:
            self.nasId = red_result
            self.showInformationDialog(
                f"获取成功，您的id为{self.nasId}\n如果还是登录失败\n请使用您浏览器登录界面地址栏nasId=xx")
            self.nasIdInput.setText(self.nasId)


    def handleselectedTheme(self):
        self.selectedTheme = str(self.themeSelected.currentIndex())
        update_Config('selectedTheme',self.selectedTheme)
        print(self.themeSelected.currentData())
        apply_stylesheet(self.parent, theme=self.themeSelected.currentData())  # 选择一个主题
    def handleRemoveWebOpen(self):
        dialog = myQdialog.EditDialog(self.services,self)
        dialog.show()
        dialog.exec()
    def handleAddWebOpen(self):
        dialog = myQdialog.addWebDialog(self)
        dialog.show()
        dialog.exec()

    def handleWebNoOpen(self):
        if(len(self.nasId)>0):
            url = f"http://172.30.21.100/tpl/whut/login.html?nasId={self.nasId}"
            webOpen(self.isWebAutoLogin,'校园网',"http://1.1.1.1")
        else:
            self.showInformationDialog("请先填写nasId")
    def toggle_autoWebLogin(self):
        self.isWebAutoLogin = self.autoLogincheckBox.isChecked()
        update_Config('isWebAutoLogin',str(self.isWebAutoLogin))

    def handleWebOpen(self):
        # url = "http://1.1.1.1"
        # webbrowser.open(url)
        webOpen(self.isWebAutoLogin,'校园网',"http://1.1.1.1")


    def onTrayIconActivated(self, reason):
        # 检查是否是双击
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
    def showApplication(self):
        self.show()
    def closeApplication(self):
        if self.service_thread:
            self.service_action['run'] = False
            self.service_thread.join()  # 等待后台线程结束
        QApplication.instance().quit()

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            self.hide()  # 隐藏窗口，而不是完全退出
            event.ignore()
    def showErrorDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
    def showWranningDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Wranning")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
    def showWranningNeedDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("需要验证码")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        ret = msgBox.exec()
        if (ret == QMessageBox.StandardButton.Ok):
            url = f"http://172.30.21.100/tpl/whut/login.html?nasId={self.nasId}"
            webbrowser.open(url)

    def showInformationDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle("Information")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        ret = msgBox.exec()


    def showMsgDialog(self, message,title):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowIcon(QIcon(':/WIFI.png'))
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def saveCredentials(self):
        update_Config('username',self.username)
        update_Config('password', self.password)
        update_Config('nasId', self.nasId)
        update_Config('isremember', str(self.isRemember))
        update_Config('isback', str(self.isBack))
        update_Config('isstartup', str(self.isStartUp))
        update_Config('iswebautologin', str(self.isWebAutoLogin))
        update_Config('selectedtheme', self.selectedTheme)
    def removeUserPass(self):
        update_Config('username', '')
        update_Config('password', '')
        update_Config('isremember', str(self.isRemember))
    def loadCredentials(self):
        # 加载凭据和复选框状态
        config = read_Configs()
        self.username = config['username']
        self.password = config['password']
        self.nasId = config['nasId']
        self.isRemember = config['isRemember'] == 'True'
        self.isBack = config['isBack'] == 'True'
        self.isStartUp = config['isStartUp'] == 'True'
        self.isWebAutoLogin = config['isWebAutoLogin'] == 'True'
        self.selectedTheme = config['selectedTheme']

        if (self.isBack):
            self.backcheckBox.setChecked(self.isBack)
        if (self.isStartUp):
            self.startCheckBox.setChecked(self.isStartUp)
        if (self.isWebAutoLogin):
            self.autoLogincheckBox.setChecked(self.isWebAutoLogin)
        if (self.isRemember):
            self.usernameInput.setText(self.username)
            self.passwordInput.setText(self.password)
            self.rememberCheckBox.setChecked(self.isRemember)

        self.nasIdInput.setText(self.nasId)
        self.themeSelected.setCurrentIndex(int(self.selectedTheme))
        self.rememberCheckBox.stateChanged.connect(self.handleRememberPassword)
        self.startCheckBox.stateChanged.connect(self.toggle_startup)


    # def toggle_startup(self, state):
    #     write_to_specific_line(self.configPath, 6, str(self.startCheckBox.isChecked()))
    #     if state == 2:  # 复选框被选中
    #         self.add_to_startup()
    #     else:  # 复选框未被选中
    #         self.remove_from_startup()
    def write_to_specific_line(self,file_name, line_number, text):
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()

            # 确保指定的行号在文件行数范围内
            if 1 <= line_number <= len(lines):
                # 修改指定行的内容
                lines[line_number - 1] = text + '\n'
            else:
                # 如果指定行超出现有行数，可以选择添加新行
                # 这取决于你的具体需求
                lines.append(text + '\n')

                # 将修改后的内容写回文件
            with open(file_name, 'w') as file:
                file.writelines(lines)
        except FileNotFoundError:
            # 文件不存在，不做任何事情
            username = self.usernameInput.text()
            password = self.passwordInput.text()
            nasId = self.nasIdInput.text()
            self.saveCredentials(username, password, nasId, self.remember,
                                 self.isBack, self.isStartUp,self.isWebAutoLogin)
            return False
            pass




    def start_service(self):
        self.service_action['run'] = True
        self.service_thread = threading.Thread(target=background_service, args=(self.service_action,), daemon=True)
        self.service_thread.start()
        print("后台服务已启动")
    def stop_service(self):
        self.service_action['run'] = False
        self.service_thread.join()
        self.service_thread = None
        print("后台服务已停止")

def background_service(action):
    """ 后台服务，用于检查网络连接 """
    while action['run']:
        if not check_internet():
            on_no_internet(loginWindow)
            # 这里添加网络不可用时的逻辑
        for _ in range(100):  # 将长时间等待分解为多个短时间等待
            if not action['run']:
                break
            time.sleep(0.1)  # 每次睡眠1秒


def loadCredentials():
    script_path = os.path.abspath(sys.argv[0])
    path = os.path.dirname(script_path) + "/config.txt"
    # 加载凭据和复选框状态
    try:
        with open(path, "r") as file:
            username = file.readline().strip()
            password = file.readline().strip()
            nasId = file.readline().strip()
            remember = file.readline().strip() == 'True'

            return username,password,nasId
    except FileNotFoundError:
        # 文件不存在，不做任何事情
        pass
def loadServiceOn():
    # 加载凭据和复选框状态
    try:
        with open("serviceon.txt", "r") as file:
            backrember = file.readline().strip() == 'True'
            return backrember
    except FileNotFoundError:
        # 文件不存在，不做任何事情
        return False
        pass


if __name__ == '__main__':
    wifiStatus = 0
    script_path = os.path.abspath(sys.argv[0])
    print(os.path.dirname(script_path))
    path = os.path.dirname(script_path) + "/config.txt"
    app = QApplication(sys.argv)
    # 应用样式
    apply_stylesheet(app, theme='light_blue.xml')  # 选择一个主题

    loginWindow = LoginWindow(app)
    if len(sys.argv) > 1:
        # 循环遍历所有参数
        for arg in sys.argv[1:]:
            if arg == "-autorun":
                print("Autorun argument detected.")

                # 在这里执行你的自启动逻辑
                # ...
    else:
        loginWindow.show()
    print(os.path.abspath(sys.argv[0]))
    script_path = os.path.abspath(sys.argv[0])
    print(os.path.dirname(script_path))
    sys.exit(app.exec())