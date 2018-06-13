#!/usr/bin/python3
#coding: utf-8

'''
This is a GUI for our fast video tracking system based on KCF
'''

__author__ = "Yelin & Hanxiaohao & Chenxiao"

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import*
from math import*
import cv2
import sys
import os
import numpy as np
import subprocess

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    flag2 = False

    def mousePressEvent(self, event):
        self.flag = True
        self.flag2 = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False
        file_handle=open('ground_truth.txt', mode='w')
        file_handle.write("%d,%d,%d,%d"%(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0)))
        print(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))

    def mouseMoveEvent(self, event):
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

        pqscreen  = QGuiApplication.primaryScreen()
        # pixmap2 = pqscreen.grabWindow(self.winId(), self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))


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
        pixmap = QPixmap("welcome.jpg")
        self.picture1.setPixmap(pixmap)

        self.btn1 = QPushButton('open', self)
        self.btn2 = QPushButton('show', self)
        self.btn2.setDisabled(True)
        self.btn3 = QPushButton('run', self)
        self.btn3.setDisabled(True)
        self.btn4 = QPushButton('rotate 90', self)
        self.btn4.setDisabled(True)
        self.resultEdit = QTextEdit()
        self.btn5 = QPushButton('Show Position', self)
        self.btn5.setDisabled(True)

        self.cb = QComboBox(self)
        self.cb.addItem('gray')
        self.cb.addItem('multiscale')
        self.cb.addItem('hog')
        self.cb.setDisabled(True)


        self.btn1.clicked.connect(self.video2Img)
        self.btn1.clicked.connect(self.enablebtn2)
        self.btn2.clicked.connect(self.showImg)
        self.btn2.clicked.connect(self.enablebtn3)
        self.btn3.clicked.connect(self.runTracker)
        self.btn3.clicked.connect(self.enablebtn5)
        self.btn4.clicked.connect(self.rotate)
        self.btn4.clicked.connect(self.showImg)
        self.btn5.clicked.connect(self.showResult)
        self.cb.activated[str].connect(self.onActivated)

        tips = QLabel('Tips\n'
                      '1. Press open to choose a vedio\n'
                      '2. Press show to show the first frame\n'
                      '3. Press Rotate 90 to rotate 90 degrees counter clockwise\n'
                      '4. Draw a box to choose tracking object\n'
                      '5. Choose feature(Gray value/multiscale/hog/lab)\n'
                      '6. Press run to start tracking\n'
                      '7. Press show position to show the position of the tracking object in each frame\n'
                      '(Leftupper hor, Leftupper ver, width, height)')

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.btn1, 1, 0)
        self.grid.addWidget(self.btn2, 1, 1)
        self.grid.addWidget(self.btn4, 1, 2)
        self.grid.addWidget(self.btn3, 1, 3)
        self.grid.addWidget(self.btn5, 1, 4)
        self.grid.addWidget(self.picture1, 2, 0, 1, 2, Qt.AlignTop)
        self.grid.addWidget(self.resultEdit, 2, 3, 1, 2, Qt.AlignTop)
        self.grid.addWidget(tips, 3, 0, 1, 5)
        #grid.addWidget(self.cb, 4, 0)
        self.grid.addWidget(self.cb, 2, 2, Qt.AlignTop)


        self.setLayout(self.grid)
        self.setGeometry(300, 300, 800, 450)
        self.setCenter()
        self.setWindowTitle('KCF Tracker')
        self.show()

    def resetUI(self):
        pixmap = QPixmap("welcome.jpg")
        self.picture1.setPixmap(pixmap)
        self.grid.addView(self.picture1, 400, 300)

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
                    cv2.waitKey(1)
                vc.release()

    def rotate(self):
        for i in range(1,self.c):
            img = cv2.imread('./ans/' + str(i) + '.jpg')

            imgRotation = np.rot90(img)
            cv2.imwrite('./ans/' + str(i) + '.jpg', imgRotation)

    def enablebtn2(self):
        #self.resetUI()
        self.btn2.setDisabled(False)
        self.btn4.setDisabled(False)
        self.PATH = 'KCF ' + str(self.c - 2)
        self.cb.setDisabled(False)

    def enablebtn3(self):
        self.btn3.setDisabled(False)

    def enablebtn5(self):
        self.btn5.setDisabled(False)

    def KeyPressEvent(self,event):
        if event.key() == Qt.Key_Escape:
            self.btn3.setDisabled(False)

    def showImg(self):
        pixmap = QPixmap("./ans/1.jpg")
        self.picture1.setPixmap(pixmap)
        self.picture1.setCursor(Qt.CrossCursor)

    def showResult(self):
        f = open('output.txt', 'r')
        with f:
            data = f.read()
            self.resultEdit.setText(data)

    #set the window center
    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onActivated(self, text):
        self.PATH =  'KCF ' + str(self.c - 2) + ' ' + text


    def runTracker(self):

        st=subprocess.STARTUPINFO
        st.dwFlags = subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow = subprocess.SW_HIDE
        subprocess.Popen(self.PATH, startupinfo = st)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myShow = MyWindow()
    myShow.show()
    sys.exit(app.exec_())