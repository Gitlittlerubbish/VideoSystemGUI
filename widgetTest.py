import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(100, 100, 500, 500)

        self.myButton = QPushButton(self)
        self.myButton.setObjectName("myButton")
        self.myButton.setText("Test")
        self.myButton.clicked.connect(self.msg)

        self.myButton2 = QPushButton(self)
        self.myButton2.setObjectName("showButton")
        self.myButton2.setText("show")
        self.myButton2.clicked.connect(self.showImage)
        self.myButton2.move(50, 0)

    def msg(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                vc = cv2.VideoCapture(fname[0])
                c = 1
                if vc.isOpened():
                    rval, frame = vc.read()
                else:
                    rval = False
                while rval:
                    rval, frame = vc.read()
                    cv2.imwrite('./ans/' + str(c) + '.jpg', frame)
                    c = c + 1
                    cv2.waitKey(1)
                vc.release()

    def showImage(self):
        hbox = QHBoxLayout(self)
        pixmap = QPixmap("./ans/1.jpg")

        self.lb = myLabel(self)
        self.lb.setGeometry(0, 100, 500, 500)
        self.lb.setPixmap(pixmap)
        hbox.addWidget(self.lb)
        self.setLayout(hbox)
        self.lb.setCursor(Qt.CrossCursor)

class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False
        print(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)

        pqscreen = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))

if __name__=="__main__":
    app = QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())