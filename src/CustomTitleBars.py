from PyQt6.QtCore import QPointF, Qt, QPoint
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QLabel, QPushButton

'''
自定义标题栏
'''
class CustomTitleBar(QWidget):
    def __init__(self,title, parent):
        super(CustomTitleBar, self).__init__()
        self.title =title
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 标题标签
        self.title = QLabel(self.title)
        self.title.setFixedHeight(30)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 控制按钮
        btn_size = 30
        self.minimizeBtn = QPushButton("-")
        self.minimizeBtn.setFixedSize(btn_size, btn_size)
        self.minimizeBtn.clicked.connect(self.parent.showMinimized)

        self.maximizeBtn = QPushButton("□")
        self.maximizeBtn.setFixedSize(btn_size, btn_size)
        self.maximizeBtn.clicked.connect(self.toggleMaximize)

        self.closeBtn = QPushButton("X")
        self.closeBtn.setFixedSize(btn_size, btn_size)
        self.closeBtn.clicked.connect(self.parent.close)

        # 添加小部件到布局
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minimizeBtn)
        self.layout.addWidget(self.maximizeBtn)
        self.layout.addWidget(self.closeBtn)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def toggleMaximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            startF = QPointF(self.start)
            # 直接使用全局坐标进行计算
            movement = event.globalPosition() - startF

            # 更新窗口位置
            self.parent.move(self.parent.pos() + movement.toPoint())

            # 更新起始点坐标
            self.start = event.globalPosition()

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False