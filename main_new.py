import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import qdarkstyle

# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)

class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.restore_setting()
        self.init_ui()
        self._pressed = False
        self.Direction = None

    def init_ui(self):
        self.set_main_window()
        self.set_label()
        self.set_btn()
        self.set_text_box()
        self.set_save_timer()

    def restore_setting(self):
        self.settings = QtCore.QSettings("config.ini",QtCore.QSettings.IniFormat)
        self.main_window_geometry = self.settings.value("main_window/geometry",QtCore.QRect(1277, 265, 300, 335))
        self.on_top = bool(self.settings.value("general/on_top",True))
        self.text_word = self.settings.value("general/text_word","")
        self.auto_save = bool(self.settings.value("general/auto_save",True))
        self.font_size = self.settings.value("text_box/font_size","14")
    def set_save_timer(self):
        self.save_timer = QtCore.QTimer()
        self.save_timer.setInterval(10000)
        if self.auto_save == True:
            self.save_timer.start()
        else:
            self.save_timer.stop()
        self.save_timer.timeout.connect(self.save_text)
        # self.save_timer.timeout.connect(self.print_hello)

    def print_hello(self):
        print("hello")

    def set_btn(self):
        # control frame
        # close
        self.btn_close = QPushButton("", self)
        self.btn_close.setGeometry(QtCore.QRect(self.main_window_geometry.width()-20, 8, 15, 15))
        self.btn_close.clicked.connect(self.close)
        self.btn_close.setStyleSheet(
            '''QPushButton{background:#FC05AE;border-radius:7px;} QPushButton:hover{background:#BD0483;}''')
        # minimize
        self.btn_mini = QPushButton("", self)
        self.btn_mini.setGeometry(QtCore.QRect(self.main_window_geometry.width()-40, 8, 15, 15))
        self.btn_mini.clicked.connect(self.showMinimized)
        self.btn_mini.setStyleSheet(
            '''QPushButton{background:#25F6AF;border-radius:7px;} QPushButton:hover{background:#1CB983;}''')
        self.btn_ontop = QPushButton("", self)
        self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
        self.btn_ontop.clicked.connect(self.chg_ontop)
        self.btn_ontop.setStyleSheet(
            '''QPushButton{background:#1621C6;border-radius:7px;} QPushButton:hover{background:#111995;}''')

    def set_label(self):
        lb2 = QLabel("Kyle's Memo", self)
        lb2.setGeometry(QtCore.QRect(30, 0, 100, 30))

    def set_main_window(self):
        if self.on_top:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowOpacity(0.7)
        self.setGeometry(self.main_window_geometry)

    def set_text_box(self):
        self.text_box = QPlainTextEdit("".join(self.text_word),self)
        self.text_box.setGeometry(QtCore.QRect(1, 30, self.main_window_geometry.width()-2, self.main_window_geometry.height()-31))
        self.text_box.setStyleSheet('font-size:'+str(self.font_size)+'px')
        # self.text_box.cursorPositionChanged.connect(self.save_text)

    def chg_ontop(self):
        if self.on_top:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Widget)
            self.on_top = False
            # print(self.ontop)
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.on_top = True
            # print(self.ontop)
        self.show()

    def move(self, pos):
        if self.windowState() == QtCore.Qt.WindowMaximized or self.windowState() == QtCore.Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(App, self).move(pos)

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

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        super(App, self).mouseMoveEvent(event)
        margins = 2
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - margins, self.height() - margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            return
        if event.buttons() == QtCore.Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            self.moveWidget(pos)
            # print(1)
            return
        if xPos <= margins and yPos <= margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif xPos <= margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif 0 <= xPos <= margins and margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif margins <= xPos <= wm and 0 <= yPos <= margins:
            # 上面
            self.Direction = Top
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(QtCore.Qt.SizeVerCursor)
        else:
            self.Direction = None
            self.setCursor(QtCore.Qt.ArrowCursor)

    def moveWidget(self, pos):
        x = pos.x()
        y = pos.y()   #获取移动后的坐标
        if self.Direction == None:
            moveX = x-self._mpos.x()
            moveY = y-self._mpos.y()  #计算移动了多少
            positionX = self.geometry().x() + moveX
            positionY = self.geometry().y() + moveY    #计算移动后主窗口在桌面的位置
            self.setGeometry(QtCore.QRect(positionX, positionY, self.geometry().width(), self.geometry().width()))    #移动主窗口
            self.main_window_geometry.setX(self.geometry().x())
            self.main_window_geometry.setY(self.geometry().y())
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
        # self.setGeometry(x, y, w, h)
        # self.btn_close.setGeometry(QtCore.QRect(w-20, 8, 15, 15))
        # self.btn_mini.setGeometry(QtCore.QRect(w-40, 8, 15, 15))
        # self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
        # self.text.setGeometry(QtCore.QRect(1, 30, w-2, h-31))
        # self.left_init = x
        # self.top_init = y
        # self.width_init = w
        # self.height_init = h
        self.update_geometry(QtCore.QRect(x,y,w,h))

    def update_geometry(self, geometry):
        self.main_window_geometry = geometry
        self.setGeometry(geometry)
        self.btn_close.setGeometry(QtCore.QRect(geometry.width()-20, 8, 15, 15))
        self.btn_mini.setGeometry(QtCore.QRect(geometry.width()-40, 8, 15, 15))
        self.btn_ontop.setGeometry(QtCore.QRect(8, 8, 15, 15))
        self.text_box.setGeometry(QtCore.QRect(1, 30, geometry.width()-2, geometry.height()-31))

    def save_setting(self):
        self.settings.setValue("main_window/geometry", self.geometry())
        self.settings.setValue("general/on_top", self.on_top)
        self.settings.setValue("text_box/font_size",self.font_size)

    def save_text(self):
        self.settings.setValue("general/text_word", self.text_box.toPlainText())
        # print("hello")

    def closeEvent(self,event):
        self.save_setting()
        self.save_text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())