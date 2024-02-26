import os

from bs4 import BeautifulSoup
import csv




def save_courses_to_csv(courses, filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Day", "Position", "Teacher", "Start Node", "End Node", "Start Week", "End Week", "Note", "Credit", "Extra1", "Extra2"])
        for course in courses:
            writer.writerow([course.name, course.day, course.position, course.teacher, course.start_node, course.end_node, course.start_week, course.end_week, course.note, course.credit, course.extra1, course.extra2])

def load_courses_from_csv(filename):
    courses = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            if row:  # 确保行不是空的
                course = Course(*row)
                courses.append(course)
    return courses
class Course:
    def __init__(self, name, day, position, teacher, start_node, end_node, start_week, end_week, note,credit="",  extra1="", extra2=""):
        self.name = name
        self.day = day
        self.position = position
        self.teacher = teacher
        self.start_node = start_node
        self.end_node = end_node
        self.start_week = start_week
        self.end_week = end_week
        self.credit = credit
        self.note = note
        self.extra1 = extra1
        self.extra2 = extra2

    def __str__(self):
        return f"{self.name} {self.day} {self.position} {self.teacher} {self.start_node} {self.end_node} {self.start_week} {self.credit}"

class CourseInfo:
    def __init__(self, name, day, position, time, note):
        self.name = name
        self.day = day
        self.position = position
        self.time = time
        self.note = note
    def __str__(self):
        return f"{self.name} {self.day} {self.position} {self.time}{self.note}"
class OnlyCourseInfo:
    def __init__(self, name, teacher,day, position, time, credit,note):
        self.name = name
        self.teacher =teacher
        self.day = day
        self.position = position
        self.time = time
        self.credit = credit
        self.note = note
    def __str__(self):
        return f"{self.name} {self.day} {self.position} {self.time}{self.note}"
def parse_course_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    element_with_id = soup.find(id="xqkb")

    if element_with_id:
        # print("Element with id 'xqkb':", element_with_id)
        table = element_with_id.find('table')
        rows = table.find_all('tr')

        # 第一行通常包含星期的标题
        weekdays = [th.get_text() for th in rows[0].find_all('th')]
        courseInfoList = list()
        # 遍历剩下的行来提取课程信息
        for row in rows[1:]:
            isMoreOneColumn = False  #因为上午下午两个文字导致多了一行
            for i, cell in enumerate(row.find_all('td')):
                cellStr = str(cell)
                if(i==0):
                    if(cellStr.find("午")>0 or cellStr.find("晚")>0):
                        isMoreOneColumn = True
                    else:
                        isMoreOneColumn = False
                    # print(i)
                    # print(str(cell))
                # if(i==1):
                #     # print(i)
                #     #print(str(cell))
                #     if(cellStr.find("target=\"_blank\">")>0):
                #         name = cellStr[cellStr.find("target=\"_blank\">")+len("target=\"_blank\">"):cellStr.find("<p>")]
                #         print(name)
                #         if(not isMoreOneColumn):
                #             weekDay = i
                #             print("周"+str(weekDay))
                else:
                    #print(i)
                    # print(str(cell))
                    while (cellStr.find("target=\"_blank\">") > 0):
                        name = cellStr[
                               cellStr.find("target=\"_blank\">") + len("target=\"_blank\">"):cellStr.find("<p>")]
                        name = name.replace("\n","").replace(" ","").replace("\t","")
                        #print(name)
                        cellStr = cellStr[cellStr.find("<p>")+len("<p>"):]
                        position = cellStr[:cellStr.find("</p>")]
                        #print(position)
                        cellStr = cellStr[cellStr.find("</p>") + len("</p>"):]
                        times = cellStr[cellStr.find("<p>")+len("<p>"):cellStr.find("</p>")]
                        #print(times)
                        cellStr = cellStr[cellStr.find("</p>") + len("</p>"):]
                        # print(cellStr)
                        cellTempHaveNote = cellStr[:cellStr.find("</a>")]
                        if (isMoreOneColumn):
                            weekDay = i-1
                            #print("周" + str(weekDay))
                        else:
                            weekDay = i
                            #print("周" + str(weekDay))
                        if(cellTempHaveNote.find("<p>")>0):
                            note = cellTempHaveNote[cellTempHaveNote.find("<p>")+len("<p>"):cellTempHaveNote.find("</p>")]
                            #print(note)
                            cellStr = cellStr[cellStr.find("</div>"):]
                            courseInfo = CourseInfo(name,weekDay,position,times,note)
                            courseInfoList.append(courseInfo)
                        else:
                            courseInfo = CourseInfo(name, weekDay, position, times, "")
                            courseInfoList.append(courseInfo)
        courseList = list()
        weekDaySet = {1:"周一",
                      2:"周二",
                      3:"周三",
                      4:"周四",
                      5:"周五",
                      6:"周六",
                      7:"周日"}
        for courseInfo in courseInfoList:
            print(courseInfo)
            tempStr = courseInfo.time
            temNodes = str(tempStr)[str(tempStr).find("("):].replace("(","").replace("节)","")
            temNodes = (str(temNodes).split("-"))
            print(temNodes)
            start_node = temNodes[0]
            stop_node = temNodes[1]
            print(start_node+"-"+stop_node)
            temWeeks = str(tempStr)[:str(tempStr).find("(")].replace("◇第","").replace("周","")
            temWeeks = str(temWeeks).split(",")
            for weeks in temWeeks:
                temp = str(weeks).split("-")
                start_week = temp[0]
                stop_week = temp[1]
                print(temp)
                course = Course(courseInfo.name,courseInfo.day,courseInfo.position,"",int(start_node),int(stop_node),int(start_week),int(stop_week),courseInfo.note)
                courseList.append(course)


        teacherInfos = soup.find('div',class_="table-inner table-long table-renwu")
        tableInfos = teacherInfos.find('table')
        # print(tableInfos)
        rows = tableInfos.find_all('tr')
        print("开始")
        for row in rows[2:]:
            print("开始1")
            name = ""
            teacher = ""
            credit = ""
            for i, cell in enumerate(row.find_all('td')):
                tempStr = cell.get_text()
                if(i==0):
                    name = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==1:
                    credit = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==2:
                    qq = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==3:
                    weeks = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==4:
                    teacher = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==5:
                    for course in courseList:
                        if(course.name == name):
                            course.teacher = teacher
                            course.credit = credit
        onlyCourseInfoList = list()
        print(len(onlyCourseInfoList))
        for course in courseList:
            isHaveCourse = False
            # print(course)
            # if(len(onlyCourseInfoList)==0):
            #     onlyCourseInfo = OnlyCourseInfo(course.name,course.teacher,course.day,
            #                                 course.position,
            #                                 f"第{course.start_week}-{course.end_week}周"
            #                                 f"第{course.start_node}-{course.end_node}节",course.credit,course.note)
            #     onlyCourseInfoList.append(onlyCourseInfo)
            for onlyCourse in onlyCourseInfoList:
                if(onlyCourse.name==course.name):
                    onlyCourse.time = onlyCourse.time+f"\n第{course.start_week}-{course.end_week}周 第{course.start_node}-{course.end_node}节"
                    isHaveCourse = True
            if(isHaveCourse == False):
                onlyCourseInfo = OnlyCourseInfo(course.name, course.teacher, course.day,
                                                course.position,
                                                f"第{course.start_week}-{course.end_week}周"
                                                f"第{course.start_node}-{course.end_node}节", course.credit,
                                                course.note)
                onlyCourseInfoList.append(onlyCourseInfo)
        for onlyCourse in onlyCourseInfoList:
            print(onlyCourse)
        script_path = os.path.abspath(sys.argv[0])
        path = os.path.dirname(script_path) + "/courses.csv"
        save_courses_to_csv(courseList,path)







                    # weekday = weekdays[i]
                    # weekdayInfo = str(weekday).replace("\n", "").replace("\t", "")
                    # weekdayInfo = weekdayInfo.replace(" ", "")
                    # course_info = cell.get_text()
                    # if course_info.strip():
                    #     name = ""
                    #     day = ""
                    #     position = ""
                    #     start_node = ""
                    #     end_node = ""
                    #     start_week = ""
                    #     end_week = ""
                    #     note = ""
                    #     # print(
                    #     #     f"1上课时间: {weekdayInfo}")
                    #     # print(cell)
                    #     texts = cell.get_text(separator='|').split('|')
                    #     # print(texts)
                    #     num = -1
                    #     for text in texts:
                    #
                    #         if(len(text)>1):
                    #             num = num + 1
                    #             tempStr = text.strip().replace("\n", "").replace("\t", "")
                                # print(tempStr)
                                # print(num)
                                # if num == 0:
                                #     name = str(tempStr)
                                #     print(name)
                                # elif num ==1:
                                #     position = str(tempStr).replace("@","")
                                #     print(position)
                                # elif num ==2:
                                #     temNodes = str(tempStr)[str(tempStr).find("("):].replace("(","").replace("节)","")
                                #     temNodes = (str(temNodes).split("-"))
                                #     start_node = temNodes[0]
                                #     stop_node = temNodes[1]
                                #     print(start_node+"-"+stop_node)
                                #     temWeeks = str(tempStr)[:str(tempStr).find("(")].replace("◇第","").replace("周","")
                                #
                                #     temWeeks =(str(temWeeks).split(","))
                                #     for temWeek in temWeeks:
                                #         temWeek = temWeek.split("-")
                                #         # print(temWeek)
                                #         start_week = temWeek[0]
                                #         stop_week = temWeek[1]
                                #         print(start_week+"-"+stop_week)
                                # elif num ==3:
                                #     print("name"+name)
                                #     if(str(tempStr).find(name[1:])>0):
                                #
                                #         print("yes")
                                #     # if(str(tempStr))
                                #     print(tempStr)
                                # elif num == 4:
                                #     print(tempStr)
                                # elif num == 5:
                                #     print(tempStr)
                                # elif num == 6:
                                #     print(tempStr)
                                # elif num == 7:
                                #     print(tempStr)
                                # elif num == 8:
                                #     print(tempStr)
                                # elif num == 9:
                                #     print(tempStr)

                # print(cell.find_all('a'))
                # if course_info.strip():  # 如果单元格有课程信息
                #     weekday = weekdays[i]
                #     courseInfo = str(course_info)
                #     courseInfo = courseInfo.replace("\n","").replace("\t", "")
                #     courseInfo = courseInfo.replace(" ", "")
                #     weekdayInfo = str(weekday).replace("\n","").replace("\t", "")
                #     weekdayInfo = weekdayInfo.replace(" ", "")
                    # print(
                    #     f"课程信息: {courseInfo}, "
                    #       f"上课时间: {weekdayInfo}")
        # for row in table.find_all('tr'):
        #     for cell in row.find_all('td'):
        #         # 获取链接
        #         link = cell.find('a')['href'] if cell.find('a') else "No Link"
        #         # 获取文本内容
        #         texts = cell.get_text(separator='|').split('|')
        #         # 打印提取的信息
        #         print(f"Link: {link}")
        #         for text in texts:
        #             print(text.strip())
        # with open("./test.txt", 'w', encoding='utf-8') as file:
        #     file.write(element_with_id.text)
    else:
        print("No element with id 'xqkb' found.")

# 测试代码
# file_path = f"C:/Users/HUANYU/Downloads/jwc.htm"  # 替换为你的 HTML 文件路径
# parse_course_html(file_path)

from datetime import datetime, timedelta

def weeks_from(target_date_str):
    # 将字符串格式的日期转换为 datetime 对象
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d')

    # 获取当前日期
    current_date = datetime.now()

    # 计算两个日期之间的差异
    delta = current_date - target_date

    # 计算完整周数
    full_weeks = delta.days // 7

    return full_weeks

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox
from qt_material import apply_stylesheet
class CourseTable(QMainWindow):
    def __init__(self, courses,weeks):
        super().__init__()
        self.selectedWeek = weeks
        self.courses = courses
        self.needResize = list()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("课程表")
        self.setGeometry(100, 100, 800, 600)

        # 创建周数选择的下拉框
        self.weekComboBox = QComboBox()
        self.weekComboBox.addItems([f"第 {i} 周" for i in range(1, 19)])  # 假设总共有 16 周
        self.weekComboBox.currentIndexChanged.connect(self.handleselectedWeek)
        self.tableWidget = QTableWidget()
        # 假设每周有 5 天课，每天有 8 个时间段
        self.tableWidget.setRowCount(5)  # 时间段
        self.tableWidget.setColumnCount(7)  # 周一至周五

        # 设置水平（星期）和垂直（时间段）标题
        self.tableWidget.setHorizontalHeaderLabels(["星期一", "星期二", "星期三", "星期四", "星期五","星期六","星期日"])
        self.tableWidget.setVerticalHeaderLabels(["1-2 节", "3-5 节", "6-8 节", "9-10 节", "11-13 节"])
        print(self.selectedWeek)
        # 填充课程数据
        for course in self.courses:
            if (int(course.start_week) <= self.selectedWeek and int(course.end_week) >= self.selectedWeek):
                # 注意：这里假设 day 和 start_node 正好对应表格的行和列
                # 你可能需要根据实际情况调整逻辑
                item = QTableWidgetItem(f"{course.name}\n{course.position}\n{course.teacher}"
                                        f"\n第{course.start_node}-{course.end_node}节")
                positionTmp=0
                startNode = int(course.start_node)
                endNode =int(course.end_node)
                if(startNode>0 and endNode<3):
                    positionTmp = 0
                elif(startNode>2 and endNode<6):
                    positionTmp = 1
                elif (startNode > 5 and endNode < 9):
                    positionTmp = 2
                elif (startNode > 8 and endNode < 11):
                    positionTmp = 3
                elif (startNode > 10 and endNode < 14):
                    positionTmp = 4
                self.tableWidget.setItem(positionTmp, int(course.day) - 1, item)
                self.needResize.append(positionTmp)
                self.tableWidget.resizeRowToContents(positionTmp)  # 调整行高以适应内容
            # self.tableWidget.resizeColumnsToContents()

        self.setCentralWidget(QWidget())
        layout = QVBoxLayout()
        layout.addWidget(self.weekComboBox)
        layout.addWidget(self.tableWidget)
        self.centralWidget().setLayout(layout)
    def showEvent(self, event):
        super().showEvent(event)
        # self.tableWidget.resizeColumnsToContents()
        for row in self.needResize:
            self.tableWidget.resizeRowToContents(row)
    def handleselectedWeek(self):
        self.selectedWeek = str(self.weekComboBox.currentIndex()+1)
        print(self.selectedWeek)
        self.updateTable(self.selectedWeek)

    def updateTable(self, index):
        selected_week = int(str(index))  # 周数是从 1 开始的
        self.tableWidget.clearContents()  # 清除现有内容

        # 填充课程数据
        for course in self.courses:
            if(int(course.start_week)<=selected_week and int(course.end_week)>=selected_week):
                # 注意：这里假设 day 和 start_node 正好对应表格的行和列
                # 你可能需要根据实际情况调整逻辑
                item = QTableWidgetItem(f"{course.name}\n{course.position}\n{course.teacher}"
                                        f"\n第{course.start_node}-{course.end_node}节")
                positionTmp = 0
                startNode = int(course.start_node)
                endNode = int(course.end_node)
                if (startNode > 0 and endNode < 3):
                    positionTmp = 0
                elif (startNode > 2 and endNode < 6):
                    positionTmp = 1
                elif (startNode > 5 and endNode < 9):
                    positionTmp = 2
                elif (startNode > 8 and endNode < 11):
                    positionTmp = 3
                elif (startNode > 10 and endNode < 14):
                    positionTmp = 4
                self.tableWidget.setItem(positionTmp, int(course.day) - 1, item)
                self.needResize.append(positionTmp)
                self.tableWidget.resizeRowToContents(positionTmp)  # 调整行高以适应内容

if __name__ == '__main__':
    file_path = f"C:/Users/HUANYU/Downloads/jwc.htm"  # 替换为你的 HTML 文件路径
    parse_course_html(file_path)
    courses = load_courses_from_csv("courses.csv")
    for course in courses:
        print(course)
    app = QApplication(sys.argv)
    # 应用样式
    target_date_str = "2023-09-03"  # 请将此替换为你的目标日期
    weeks = weeks_from(target_date_str)
    apply_stylesheet(app, theme='light_blue.xml')  # 选择一个主题
    ex = CourseTable(courses,weeks+1)
    ex.show()
    sys.exit(app.exec())