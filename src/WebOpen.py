import os
import sys
import webbrowser
from telnetlib import EC

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait

from src.ConfigIni import read_Users

# #指定Edge WebDriver的路径
# webdriver_path = './edgeDriver/msedgedriver.exe'  # 替换为实际的路径
#
# # 设置无头模式
# options = webdriver.EdgeOptions()
# options.use_chromium = True
# # options.add_argument("--headless")  # 启用无头模式
#
# # 设置Service对象
# service = Service(webdriver_path)
#
# # 初始化Edge WebDriver
# driver = webdriver.Edge(options=options)
#
# # 打开登录页面
# driver.get("http://sso.jwc.whut.edu.cn/Certification/index2.jsp")
# # 等待页面加载完成
# driver.implicitly_wait(1000)  # 可以根据需要调整等待时间
# # 获取并打印页面源代码
# #print(driver.page_source)
# # 找到用户名和密码输入框，并输入你的凭据
# # 注意：根据实际网页元素修改下面的选择器
# username_input = driver.find_element(By.ID, "un")
# password_input = driver.find_element(By.ID, "pd")
# driver.implicitly_wait(10)  # 可以根据需要调整等待时间
# username_input.send_keys("0122109361613")
# password_input.send_keys("nyh314nyh")
# driver.implicitly_wait(10)  # 可以根据需要调整等待时间
# # 找到登录按钮并点击
# # 注意：根据实际网页元素修改下面的选择器
# login_button = driver.find_element(By.ID, "index_login_btn")
# login_button.click()
#
# # 等待页面加载完成
# driver.implicitly_wait(10000)  # 可以根据需要调整等待时间
# time.sleep(10)
# # 获取并打印登录后的页面源代码
# print(driver.page_source)
#
# #关闭浏览器
# driver.quit()


global_driver = None
def webOpen(autoLogin,platform,url):
    if(autoLogin):
        # 指定Edge WebDriver的路径
        # webdriver_path = './edgeDriver/msedgedriver.exe'  # 替换为实际的路径
        # 设置无头模式
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        print(platform)

        # # 设置Service对象
        # service = Service(webdriver_path)
        global global_driver
        # 初始化Edge WebDriver
        try:
            global_driver = webdriver.Edge(options=options)

            # 打开登录页面
            global_driver.get(url)
            # 等待页面加载完成
            # global_driver.implicitly_wait(1000)  # 可以根据需要调整等待时间
            # 获取并打印页面源代码
            #print(driver.page_source)
            # 找到用户名和密码输入框，并输入你的凭据
            # 注意：根据实际网页元素修改下面的选择器
            # 检查页面是否加载完毕
            ready_state = global_driver.execute_script("return document.readyState")
            if ready_state == "complete":
                print("网页加载完毕")
                userList = read_Users()
                if(userList[platform]['username'] and userList[platform]['password']):
                    print("账号密码存在")
                    try:
                        global_driver.execute_script(
                            userList[platform]['nameJs'] + '\'' + userList[platform]['username'] + '\'')
                        global_driver.execute_script(
                            userList[platform]['passJs'] + '\'' + userList[platform]['password'] + '\'')
                        global_driver.execute_script(userList[platform]['loginJs'])
                    except Exception as e:
                        print(f"Error:{e}")
                        pass
                else:
                    print("账号密码不存在")

            else:
                print("网页还在加载中")

            # username_input = driver.find_element(By.ID, "un")
            # password_input = driver.find_element(By.ID, "pd")
            # driver.implicitly_wait(10)  # 可以根据需要调整等待时间
            # username_input.send_keys("0122109361613")
            # password_input.send_keys("nyh314nyh")
            # driver.implicitly_wait(10)  # 可以根据需要调整等待时间
            # 找到登录按钮并点击
            # 注意：根据实际网页元素修改下面的选择器
            # login_button = driver.find_element(By.ID, "index_login_btn")
            # login_button.click()

            # 等待页面加载完成
            # global_driver.implicitly_wait(10000)  # 可以根据需要调整等待时间
            # time.sleep(10)
            return global_driver
            # # 获取并打印登录后的页面源代码
            # print(driver.page_source)
        except WebDriverException as e:
            print(e)
            pass
    else:
        webbrowser.open(url)

def JWCwebOpen(autoLogin,platform,url):
    if(autoLogin):
        # 指定Edge WebDriver的路径
        # webdriver_path = './edgeDriver/msedgedriver.exe'  # 替换为实际的路径
        # 设置无头模式
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        print(platform)

        # 设置Service对象
        # service = Service(webdriver_path)
        global global_driver
        # 初始化Edge WebDriver
        try:
            global_driver = webdriver.Edge(options=options)

            # 打开登录页面
            global_driver.get(url)
            # 等待页面加载完成
            # global_driver.implicitly_wait(1000)  # 可以根据需要调整等待时间
            # 获取并打印页面源代码
            #print(driver.page_source)
            # 找到用户名和密码输入框，并输入你的凭据
            # 注意：根据实际网页元素修改下面的选择器
            # 检查页面是否加载完毕
            ready_state = global_driver.execute_script("return document.readyState")
            if ready_state == "complete":
                print("网页加载完毕")
                userList = read_Users()
                if(userList[platform]['username'] and userList[platform]['password']):
                    print("账号密码存在")
                    try:
                        global_driver.execute_script(
                            userList[platform]['nameJs'] + '\'' + userList[platform]['username'] + '\'')
                        global_driver.execute_script(
                            userList[platform]['passJs'] + '\'' + userList[platform]['password'] + '\'')
                        global_driver.execute_script(userList[platform]['loginJs'])
                    except Exception as e:
                        print(f"Error:{e}")
                        pass
                else:
                    print("账号密码不存在")

            else:
                print("网页还在加载中")

            # username_input = driver.find_element(By.ID, "un")
            # password_input = driver.find_element(By.ID, "pd")
            # driver.implicitly_wait(10)  # 可以根据需要调整等待时间
            # username_input.send_keys("0122109361613")
            # password_input.send_keys("nyh314nyh")
            # driver.implicitly_wait(10)  # 可以根据需要调整等待时间
            # 找到登录按钮并点击
            # 注意：根据实际网页元素修改下面的选择器
            # login_button = driver.find_element(By.ID, "index_login_btn")
            # login_button.click()

            # 等待页面加载完成
            global_driver.implicitly_wait(10000)  # 可以根据需要调整等待时间
            element = global_driver.find_element(By.ID, 'xqkb')  # 替换为你的元素定位
            # 现在元素已经加载，可以执行你的操作了
            print(global_driver.page_source)
            script_path = os.path.abspath(sys.argv[0])
            path = os.path.dirname(script_path) + "/" + 'jwc.html'

            with open(path, 'w', encoding='utf-8') as file:
                file.write(global_driver.page_source)
            # time.sleep(10)

            return global_driver
            # # 获取并打印登录后的页面源代码
            # print(driver.page_source)
        except WebDriverException as e:
            print(e)
            pass
    else:
        webbrowser.open(url)