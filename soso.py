#영상목록 영상 재생
import sys
import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox, QApplication, QVBoxLayout)
import cv2

global input_id
form_class = uic.loadUiType("C:/Users/DSL/Desktop/A/B/Eye-Blink-Detection-master./login.ui")[0]

att_db = pymysql.connect(
    host="165.229.125.14",
    user="hello",
    password="1234",
    database="attendance",
)


class Example(QWidget):
    global input_id

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        listWidget = QListWidget()

        # listWidget.addItem("sparrow")

        ID = 'idid'
        query="""SELECT coursename FROM COURSE as C, BUCKET as B WHERE B.b_stid= %s and C.coursenum=B.b_coursenum"""
        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query,ID)
        coursename = []
        coursename = cursor.fetchall()
        print(coursename)

        C_NAME = []
        for i in range(len(coursename)):
            C_NAME.append(coursename[i].get('coursename'))

        for i in range(len(C_NAME)):
            listWidget.addItem(C_NAME[i])
        print("------------------")
        listWidget.itemDoubleClicked.connect(self.onClicked)
        print("------------------")
        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QListWidget')
        self.show()

    def onClicked(self, item):
        print("클릭성공")
        QMessageBox.information(self, "Info", item.text())
        c_name=item.text()
        print(c_name)
        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        query2="""SELECT url FROM COURSE WHERE coursename=%s"""
        cursor.execute(query2,c_name)
        courseurl = cursor.fetchone()
        URL = courseurl.get('url')
        print(URL)
        self.video = cv2.VideoCapture(URL)

        while (self.video.isOpened()):
            ret, frame = self.video.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', gray)
            cv2.waitKey(1)

        self.video.release()
        cv2.destroyAllWindows()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    # myWindow = WindowClass()
    # myWindow.show()
    ex = Example()
    sys.exit(app.exec_())
    app.exec_()



