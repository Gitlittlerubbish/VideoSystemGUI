#!/usr/bin/python3
#coding: utf-8

'''
This is a GUI for our fast video tracking system based on KCF
'''

__author__ = "Yelin & Hanxiaohao & Chenxiao"

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import*
import cv2
import sys
import os

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self,event):
        self.flag = False
        file_handle=open('ground_truth.txt', mode='w')
        file_handle.write("%d,%d,%d,%d"%(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0)))
        print(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))

    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.c = 0
        self.setWindowIcon(QIcon('favicon.ico'))

    def initUI(self):
        if os.path.exists("./ans"):
            os.system("rmdir /s/q ans")
        os.system("mkdir ans")

        self.picture1 = MyLabel(self)

        btn1 = QPushButton('open', self)
        btn1.clicked.connect(self.video2Img)

        btn2 = QPushButton('show', self)
        btn2.clicked.connect(self.showImg)

        btn3 = QPushButton('run', self)
        btn3.clicked.connect(self.runTracker)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(btn1, 1, 0)
        grid.addWidget(btn2, 2, 0)
        grid.addWidget(btn3, 3, 0)
        grid.addWidget(self.picture1, 1, 1, 3, 1, Qt.AlignTop)

        self.setLayout(grid)
        self.setGeometry(300, 300, 1600, 900)
        self.setCenter()
        self.setWindowTitle('KCF Tracker')
        self.show()

    def video2Img(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                vc = cv2.VideoCapture(fname[0])
                self.c = 1
                if vc.isOpened():
                    rval, frame = vc.read()
                else:
                    rval = False
                while vc.read()[0]:
                    cv2.imwrite('./ans/' + str(self.c) + '.jpg', vc.read()[1])
                    self.c = self.c + 1
                    cv2.waitKey(50)
                vc.release()

    def showImg(self):
        pixmap = QPixmap("./ans/1.jpg")
        self.picture1.setPixmap(pixmap)
        self.picture1.setCursor(Qt.CrossCursor)

    #set the window center
    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def runTracker(self):
        PATH = 'KCF ' + str(self.c - 1)
        os.system(PATH)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myShow = MyWindow()
    myShow.show()
    sys.exit(app.exec_())