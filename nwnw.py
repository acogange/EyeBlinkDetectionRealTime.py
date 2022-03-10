import sys
import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *
from tkinter import messagebox
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox, QApplication, QVBoxLayout)
import cv2

form_class = uic.loadUiType("C:/Users/DSL/Desktop/A/B/Eye-Blink-Detection-master./login.ui")[0]

att_db = pymysql.connect(
    host="165.229.125.14",
    user="hello",
    password="1234",
    database="attendance",
)


class WindowClass(QMainWindow, form_class):
    input_id = 0
    cursor = att_db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT st_id FROM STUDENT")
    stid = []
    stid = cursor.fetchall()

    ID = []
    for i in range(len(stid)):
        ID.append(stid[i].get('st_id'))

    cursor.execute("SELECT password FROM STUDENT")

    pw = []
    pw = cursor.fetchall()

    Password = []
    for i in range(len(stid)):
        Password.append(pw[i].get('password'))

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.btn_clicked)



    def btn_clicked(self):
        for i in range(len(self.stid)):
            if self.lineEdit.text() == self.ID[i]:
                WindowClass.input_id = self.lineEdit.text()
                if self.lineEdit_2.text() == self.Password[i]:

                    messagebox.showinfo(title='알림', message='로그인성공')

                    self.close()
                    print("-------111----")


                    break
                else:
                    messagebox.showinfo(title='에러', message='비밀번호오류')
                    break
            elif i == (len(self.stid) - 1):
                messagebox.showinfo(title='에러', message='존재하지않는 회원입니다.')
            else:
                continue


class Example(QWidget):
    global input_id
    def __init__(self):
        super().__init__()

        #self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        listWidget = QListWidget()

        ID = WindowClass.input_id

        query = """SELECT coursename FROM COURSE as C, BUCKET as B WHERE B.b_stid= %s and C.coursenum=B.b_coursenum"""
        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, ID)

        coursename = []
        coursename = cursor.fetchall()

        C_NAME = []
        for i in range(len(coursename)):
            C_NAME.append(coursename[i].get('coursename'))

        for i in range(len(C_NAME)):
            listWidget.addItem(C_NAME[i])

        print("------------------")
#        if listWidget.itemDoubleClicked.connect(self.onClicked):
  #          print("제발")
        listWidget.itemDoubleClicked.connect(self.onClicked)
        print("------------------77")

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


    """
    def onClicked(self, item):
        print("onclick")
        QMessageBox.information(self, "Info", item.text())
        c_name = item.text()
        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        query2 = SELECT url FROM COURSE WHERE coursename=%s
        cursor.execute(query2, c_name)

        courseurl = cursor.fetchone()

        URL = courseurl.get('url')
        self.video = cv2.VideoCapture(URL)
        while (self.video.isOpened()):
            ret, frame = self.video.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', gray)
            cv2.waitKey(1)

        self.video.release()
        cv2.destroyAllWindows()
    """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    #ex=Example()
    #sys.exit(app.exec_())
    app.exec_()
    ex= Example()
    ex.initUI()
    app.exec_()

