import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import qdarkstyle


# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)
 
class App(QWidget):
    # TODO: 当最大化后，双击标题栏要窗口化
    # 四周边距
    Margins = 2
    left_mem = 1277
    top_mem = 265
    # print(self.left_init)
    # print(self.top_init)
    width_mem = 300
    height_mem = 335

    def __init__(self):
        super().__init__()
        self.str = []
        if not os.path.exists("./text.txt"):
            f = open("./text.txt","w")
            f.close()
        with open("./text.txt","r") as f:
            self.str=f.readlines()
 
        if not os.path.exists("./ini_sticky.txt"):
            f = open("./ini_sticky.txt","w")
            f.close()
        with open("./ini_sticky.txt","r") as f:
            self.geo=f.readlines()
 
        # print(self.str)
        # print(self.geo)
        if self.geo != []:  
            self.max_init = bool(self.geo[0].replace("\n",""))
            self.left_init = int(self.geo[1].replace("\n",""))
            self.top_init = int(self.geo[2].replace("\n",""))
            # print(self.left_init)
            # print(self.top_init)
            self.width_init = int(self.geo[3].replace("\n",""))
            self.height_init = int(self.geo[4].replace("\n",""))
        else:
            self.max_init = False
            self.left_init = 1277
            self.top_init = 265
            # print(self.left_init)
            # print(self.top_init)
            self.width_init = 300
            self.height_init = 335

        self.ontop = True
        self._pressed = False
        self.Direction = None
        self.initUI()
        # self.setMouseTracking(True)
 
    def initUI(self):
        # frame
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowOpacity(0.7)
        self.setGeometry(self.left_init, self.top_init, self.width_init, self.height_init)

        # label
        lb2 = QLabel("Kyle's Memo", self)
        lb2.setGeometry(QtCore.QRect(30, 0, 100, 30))
 
        # control frame
        # close
        self.btn_close = QPushButton("", self)
        self.btn_close.setGeometry(QtCore.QRect(self.width_init-20, 8, 15, 15))
        self.btn_close.clicked.connect(self.cc_close)
        self.btn_close.setStyleSheet(
            '''QPushButton{background:#FC05AE;border-radius:7px;} QPushButton:hover{background:#BD0483;}''')
        # minimize
        self.btn_mini = QPushButton("", self)
        self.btn_mini.setGeometry(QtCore.QRect(self.width_init-40, 8, 15, 15))
        self.btn_mini.clicked.connect(self.cc_mini)
        self.btn_mini.setStyleSheet(
            '''QPushButton{background:#25F6AF;border-radius:7px;} QPushButton:hover{background:#1CB983;}''')
        self.btn_ontop = QPushButton("", self)
        self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
        self.btn_ontop.clicked.connect(self.cc_ontop)
        self.btn_ontop.setStyleSheet(
            '''QPushButton{background:#1621C6;border-radius:7px;} QPushButton:hover{background:#111995;}''')

        # text board
        self.text = QPlainTextEdit("".join(self.str),self)
        self.text.setGeometry(QtCore.QRect(1, 30, self.width_init-2, self.height_init-31))
        self.text.setStyleSheet('font-size:14px')
        self.show()

        # if self.max_init == False:
        self.setGeometry(self.left_init, self.top_init, self.width_init, self.height_init)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # else:
            # self.showMaximized()

 
    # @pyqtSlot()
    # def mousePressEvent(self,event):
    #     # print(1)
    #     self.pressX = event.x()
    #     self.pressY = event.y()
    #     # self.setCursor(QtCore.Qt.SizeFDiagCursor)
    def move(self, pos):
        if self.windowState() == QtCore.Qt.WindowMaximized or self.windowState() == QtCore.Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(App, self).move(pos)

    # def showMaximized(self):
    #     super(App, self).showMaximized()
    #     self.btn_close.setGeometry(QtCore.QRect(self.width()-20, 8, 15, 15))
    #     self.btn_mini.setGeometry(QtCore.QRect(self.width()-40, 8, 15, 15))
    #     self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
    #     self.text.setGeometry(QtCore.QRect(1, 30, self.width()-2, self.height()-31))

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super(App, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        super(App, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None
    
    # def mouseDoubleClickEvent(self, event):
    #     super(App, self).mouseDoubleClickEvent(event)
    #     print(1)
    #     if self.Direction == None:
    #         if not self.isMaximized():
    #             self.showMaximized()
    #         else:
    #             self.setGeometry(self.left_mem, self.top_mem, self.width_mem, self.height_mem)
    #             self.btn_close.setGeometry(QtCore.QRect(self.width()-20, 8, 15, 15))
    #             self.btn_mini.setGeometry(QtCore.QRect(self.width()-40, 8, 15, 15))
    #             self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
    #             self.text.setGeometry(QtCore.QRect(1, 30, self.width()-2, self.height()-31))
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        super(App, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            return
        if event.buttons() == QtCore.Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            self.moveWidget(pos)
            # print(1)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # 上面
            self.Direction = Top
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(QtCore.Qt.SizeVerCursor)
        else:
            self.Direction = None
            self.setCursor(QtCore.Qt.ArrowCursor)
    def moveWidget(self, pos):
        # print(pos)
        #     # print(3)
        # # print(self.mousePressEvent)
        # # super(App, self).mouseMoveEvent(event)
        x = pos.x()
        y = pos.y()   #获取移动后的坐标
        # print([x,y])
        if self.Direction == None:
            moveX = x-self._mpos.x()
            moveY = y-self._mpos.y()  #计算移动了多少
            positionX = self.frameGeometry().x() + moveX
            positionY = self.frameGeometry().y() + moveY    #计算移动后主窗口在桌面的位置
            self.setGeometry(QtCore.QRect(positionX, positionY, self.width_init, self.height_init))    #移动主窗口
            self.left_init = self.geometry().left()
            self.top_init = self.geometry().top()
        else:
            return

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)
        self.btn_close.setGeometry(QtCore.QRect(w-20, 8, 15, 15))
        self.btn_mini.setGeometry(QtCore.QRect(w-40, 8, 15, 15))
        self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
        self.text.setGeometry(QtCore.QRect(1, 30, w-2, h-31))
        self.left_init = x
        self.top_init = y
        # print(self.left_init)
        # print(self.top_init)
        self.width_init = w
        self.height_init = h
    # def mouseMoveEvent(self, event):
    #     # print(3)
    #     # print(self.mousePressEvent)
    #     super(FramelessWindow, self).mouseMoveEvent(event)
    #     x = event.x()
    #     y = event.y()   #获取移动后的坐标
    #     # print([x,y])
    #     try:
    #         moveX = x-self.pressX
    #         moveY = y-self.pressY  #计算移动了多少
    #         positionX = self.frameGeometry().x() + moveX
    #         positionY = self.frameGeometry().y() + moveY    #计算移动后主窗口在桌面的位置
    #         self.move(positionX, positionY)    #移动主窗口
    #         self.left_init = self.geometry().left()
    #         self.top_init = self.geometry().top()
    #     except:
    #         pass
 
    def cc_close(self):
        self.str = self.text.toPlainText()
        with open("./text.txt", "w") as f:
            f.write(self.str)
        f.close()
 
        with open("./ini_sticky.txt", "w") as f:
            s = str(self.isMaximized() or self.isFullScreen())+"\n"+str(self.left_init)+"\n"+str(self.top_init)+"\n" + str(self.geometry().width())+"\n" + str(self.geometry().height())
            f.write(s)
        f.close()
        self.close()
 
    def cc_mini(self):
        self.showMinimized()

    def cc_ontop(self):
        if self.ontop:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Widget)
            self.ontop = False
            # print(self.ontop)
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.ontop = True
            # print(self.ontop)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())