# 영상처리만 완벽 구현

import numpy as np
from tkinter import *
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
import cv2
import dlib
from scipy.spatial import distance as dist
import threading
import tkinter as tk
import os
import sys
import pymysql
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox, QApplication, QVBoxLayout)

form_class = uic.loadUiType("C:/Users/DSL/Desktop/A/B/Eye-Blink-Detection-master./login.ui")[0]

att_db = pymysql.connect(
    host="165.229.125.58",
    user="hi",
    password="1234",
    database="attendance",
)



# 로그인 UI

class WindowClass(QMainWindow, form_class):
    input_id = 0
    cursor = att_db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT st_id FROM STUDENT order by st_id")
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
        tkk1 = Tk()
        for i in range(len(self.stid)):
            if self.lineEdit.text() == self.ID[i]:
                WindowClass.input_id = self.lineEdit.text()
                if self.lineEdit_2.text() == self.Password[i]:
                    tkk1.destroy()
                    self.close()
                    break
                else:
                    messagebox.showinfo(title='에러', message='비밀번호오류')
                    tkk1.destroy()

                    break
            elif i == (len(self.stid) - 1):
                messagebox.showinfo(title='에러', message='존재하지않는 회원입니다.')

            else:
                continue
            tkk1.destroy()



class Example(QWidget):

    # global input_id
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()

        ID = WindowClass.input_id

        query = """SELECT coursename FROM COURSE as C, HAS as B WHERE B.st_id= %s and C.coursenum=B.coursenum"""
        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, ID)

        coursename = []
        coursename = cursor.fetchall()

        C_NAME = []
        for i in range(len(coursename)):
            C_NAME.append(coursename[i].get('coursename'))

        for i in range(len(C_NAME)):
            listWidget.addItem(C_NAME[i])

        listWidget.itemDoubleClicked.connect(self.onClicked)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)
        # listWidget.itemDoubleClicked.connect(self.onClicked)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QListWidget')
        self.show()

    def onClicked(self, item):

        QMessageBox.information(self, "Info", item.text())
        Example.c_name = item.text()

        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        query2 = """SELECT url FROM COURSE WHERE coursename=%s"""
        cursor.execute(query2, Example.c_name)

        courseurl = cursor.fetchone()

        Example.URL = courseurl.get('url')
        # self.video = cv2.VideoCapture(URL)
        self.close()




# 눈 비율
def eye_aspect_ratio(eye):  # 눈의 면적 비율 구하는 함수
    # 눈 세로 거리
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # 눈 가로 거리 계산

    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2 * C)
    return ear


class Message:
    def __init__(self, gui_obj,level):
        self.timer = 0  # 초 세는 변수
        self.timeText = 0  # 센 초 출력 변수
        self.running = False
        self.obj = gui_obj
        self.level=level
        self.Messagebox = Tk()  # 팝업  Tk:인터페이스
        self.Messagebox.geometry('400x250')  # 팝업 사이즈
        self.Messagebox.resizable(0, 0)
        self.Messagebox.title("Messagebox")  # 팝업 이름
        if(self.level==1):
            # Label: 팝업에 텍스트 및 이미지 표시하는 역할
            Text = Label(self.Messagebox, text="강의수강\n제대로 해주세요\n결석까지 남은시간:", font=("Helvetica", 20))  # 팝업에 시간 출력 양식 맟추기
            Text.pack(side="top")
            self.timeText = Label(self.Messagebox, text="0", font=("Helvetica", 10))
            self.timeText.pack()
            continuetButton = Button(self.Messagebox, text='확인', bg="yellow", command=self.contiune_func)
            continuetButton.pack(fill=tk.BOTH)

            self.startTimer()  # 시간측정 시간
            self.Messagebox.mainloop()
        elif (self.level == 2):
            Text2 = Label(self.Messagebox, text="동영상 대리출석 방지 팝업\n결석까지 남은시간:",font=("Helvetica", 15))  # 팝업에 시간 출력 양식 맟추기
            Text2.pack(side="top")
            self.timeText = Label(self.Messagebox, text="0", font=("Helvetica", 10))
            self.timeText.pack()
            continuetButton = Button(self.Messagebox, text='확인', bg="yellow", command=self.contiune_func)
            continuetButton.pack(fill=tk.BOTH)

            self.startTimer()  # 시간측정 시간
            self.Messagebox.mainloop()

    def contiune_func(self):  # 멈추는 함수
        self.Messagebox.destroy()  # 프로그램 종료

    def startTimer(self):  # 초 세고 종료시키는 함수
        self.running = True  # 함수 실행
        if (self.running):  # 실행중이면
            self.timer += 1  # 시간 카운팅
            self.timeText.configure(text=int(self.timer/60))  # 시간 출력
            if (self.timer > 600):  # 제한시간동안 팝업 확인 안하면
                self.Messagebox.destroy()  # 팝업 종료
                self.obj.pause = True
                self.obj.window.destroy()
        else:  # 실행중이 아니면
            self.timer = 0  # 세던 시간 초기화
        self.Messagebox.after(10, self.startTimer)


class GUI:  # 변수 초기화 및 포맷
    def __init__(self):
        self.timer2=0
        self.JAWLINE_POINTS = list(range(0, 17))
        self.RIGHT_EYE_POINTS = list(range(36, 42))
        self.LEFT_EYE_POINTS = list(range(42, 48))
        self.RIGHT_EYEBROW_POINTS = list(range(17, 22))
        self.LEFT_EYEBROW_POINTS = list(range(22, 27))
        self.NOSE_POINTS = list(range(27, 36))
        self.MOUTH_OUTLINE_POINTS = list(range(48, 61))
        self.MOUTH_INNER_POINTS = list(range(61, 68))

        self.EYE_AR_THRESH = 0.22  # 0.22 ->0.11(x) -> 0.22
        self.EYE_AR_CONSEC_FRAMES = 2  # 3->2
        self.EAR_AVG = 0
        self.DOWN_COUNTER = 0
        self.TOTAL = 0
        self.UP_COUNTER = 0
        self.flag = 1
        self.delay = 15  # ms
        self.width = 640
        self.height = 480
        self.pause = False
        # 눈 미인식 부분 변수
        self.eyeleft = 0
        self.eyeright = 0
        self.eyeframe = 0

        self.window = Tk()
        self.window.title("Video Player")  # 비디오 제목
        bottom_layout = Frame(self.window)
        bottom_layout.pack(side="bottom", pady=5)
        video_layout = Frame(self.window, relief="solid", bd=1)
        video_layout.pack(side="left", fill="both", expand=True)  # 왼쪽에 영상
        self.webcam_layout = Label(self.window, relief="solid", bd=1)
        self.webcam_layout.pack(side="right", fill="both", expand=True)  # 오른쪽에 웹캠
        self.canvas = Canvas(video_layout)
        self.canvas.pack()
        self.canvas.config(width=self.width, height=self.height)
        # 각 열 영상 버튼 구현
        self.btn_play = Button(bottom_layout, text="Play", width=15, command=self.video_func)
        self.btn_play.grid(row=0, column=1)
        self.btn_pause = Button(bottom_layout, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=0, column=2)
        self.btn_resume = Button(bottom_layout, text="resume", width=15, command=self.resume_video)
        self.btn_resume.grid(row=0, column=3)
        self.cursor = att_db.cursor(pymysql.cursors.DictCursor)
        self.open_file()  # 파일 오픈 시작
        self.window.mainloop()
        os._exit(1)

    def open_file(self):  # 인강과 웹캠 여는 함수

        self.pause = False  # 중지한 상태가 아니면
        # 인강과 웹캠 열기
        real_url = Example.URL
        self.video = cv2.VideoCapture(real_url)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        print('video fps:',self.fps)
        self.webcam = cv2.VideoCapture(0)
        now_coursename = Example.c_name
        query = """SELECT coursenum FROM COURSE WHERE coursename=%s"""
        self.cursor.execute(query, now_coursename)

        now_coursenum = self.cursor.fetchone()
        cnum = (now_coursenum.get('coursenum'))

        query = """SELECT time FROM course where coursenum='%s'"""
        self.cursor.execute(query, cnum)
        aaaa = self.cursor.fetchone()
        long = (aaaa.get('time'))

        # long=self.cursor.execute("SELECT time FROM course where coursenum='%d'"%(cnum))


        self.time = np.random.randint(int(long*self.fps*(1/3)), int(long*self.fps*(3/4)))
        #영상길이의 1/3 ~ 3/4 지점에 랜덤으로 팝업
        print('랜덤팝업:',int(self.time/self.fps),'s에 출력')


    def get_frame(self):
        try:
            if self.video.isOpened():  # 인강 연다
                ret, frame = self.video.read()  # 인강 읽어오기
                resize = cv2.resize(frame, (640, 480))  # 영상 크기 조정

                return (ret, cv2.cvtColor(resize, cv2.COLOR_BGR2RGB))  # 영상 출력
        except:  # 인강 끝나면
            now_coursename = Example.c_name
            query = """SELECT coursenum FROM COURSE WHERE coursename=%s"""
            self.cursor.execute(query, now_coursename)

            now_coursenum = self.cursor.fetchone()
            self.c_num = (now_coursenum.get('coursenum'))

            DB_ID = WindowClass.input_id

            self.cursor.execute("UPDATE HAS SET attendance ='o' WHERE st_id='%s' and coursenum='%s'" % (DB_ID, self.c_num))

            att_db.commit()

            messagebox.showinfo(title='', message='수강을 완료하였습니다.')
            # sys.exit()
            os._exit(1)



    def webcam_func(self):  # 웹캠 분석
        detector = dlib.get_frontal_face_detector()  # dlib 이용 기본 얼굴 검출기
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # 랜드마크 정보


        if (self.webcam):  # 웹캠 실행되면
            while not self.pause:  # 영상 중지 아니면
                ret, frame = self.webcam.read()  # 웹캠 불러오기
                if ret:
                    cv2.putText(frame, "left eye {}".format(self.eyeleft), (10, 150), cv2.FONT_HERSHEY_DUPLEX, 0.7,(0, 255, 255), 1)
                    cv2.putText(frame, "right eye {}".format(self.eyeright), (10, 180), cv2.FONT_HERSHEY_DUPLEX, 0.7,(0, 255, 255), 1)
                    self.timer2 += 1

                    # 눈 미인식시
                    if self.eyeframe > 100:
                        self.eyeframe = 0
                        Message(self,1)
                    if (self.eyeleft < 4 or self.eyeleft > 6) and (self.eyeright < 4 or self.eyeright > 6):  # 눈 찾는 점이 4~6개 아니면 (눈감지 x-> 사람없다고인지)
                        self.eyeframe += 1  # 프레임 증가
                    else:  # 찾는 점이 4~6개면
                        self.eyeleft = 0  # 눈 찾는 점 변수 초기화
                        self.eyeright = 0  # 눈 찾는 점 변수 초기화
                        self.eyeframe = 0
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    rects = detector(gray, 0)
                    for rect in rects:  # 웹캠 단위 쪼개서 분석 시작

                        # 웹캠 좌표
                        x = rect.left()
                        y = rect.top()
                        x1 = rect.right()
                        y1 = rect.bottom()
                        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])
                        # 얼굴에 랜드마크 찍기
                        left_eye = landmarks[self.LEFT_EYE_POINTS]
                        right_eye = landmarks[self.RIGHT_EYE_POINTS]

                        left_eye_hull = cv2.convexHull(left_eye)
                        right_eye_hull = cv2.convexHull(right_eye)
                        self.eyeleft = len(left_eye_hull)
                        self.eyeright = len(right_eye_hull)
                        cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
                        cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
                        ear_left = eye_aspect_ratio(left_eye)
                        ear_right = eye_aspect_ratio(right_eye)
                        ear_avg = (ear_left + ear_right) / 2.0  # 양쪽 눈 면적 평균

                        if self.UP_COUNTER > 100:  # 눈 계속 떴을때
                            # 팝업 열기전 프레임 초기화
                            self.UP_COUNTER = 0
                            self.DOWN_COUNTER = 0
                            Message(self,1)
                        print(self.DOWN_COUNTER)
                        if self.DOWN_COUNTER > 100:  # 눈을 계속 감고있을때
                            # 팝업 열기전 프레임 초기화
                            self.UP_COUNTER = 0
                            self.DOWN_COUNTER = 0
                            Message(self,1)
                            # window.mainloop()
                        if ear_avg < self.EYE_AR_THRESH:
                            self.DOWN_COUNTER += 1
                            self.UP_COUNTER = 0
                        else:
                            self.UP_COUNTER += 1
                            if self.DOWN_COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                                self.TOTAL += 1

                            self.DOWN_COUNTER = 0


                        if(int(self.timer2/9)==int(self.time/self.fps)): #webcam 평균fps 9

                            self.timer2+=10
                            Message(self,2)

                        # 웹캠 왼쪽 상단 눈 깜빡임 횟수 및 눈 비율 출력
                        cv2.putText(frame, "Blinks{}".format(self.TOTAL), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                                    (0, 255, 255), 1)
                        cv2.putText(frame, "EAR {}".format(ear_avg), (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                                    (0, 255, 255), 1)

                # 영상 컬러 변환
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 영상 컬러로 수정후 불러오기
                image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
                self.webcam_layout.configure(image=image)
                self.webcam_layout.image = image

    def video_func(self):  # 영상 재생
        ret, frame = self.get_frame()

        if self.flag == 1:
            self.thread = threading.Thread(target=self.webcam_func, args=())
            self.thread.start()
            # self.thread.join()
            self.flag = 0
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        if not self.pause:
            self.window.after(self.delay, self.video_func)

    def webcam_start(self):
        ret, frame = self.webcam.read()
        if self.flag == 1:
            self.thread = threading.Thread(target=self.video_func, args=())
            self.thread.start()
            # self.thread.join()
            self.flag = 0
        if ret:
            self.webcam_func()

    def pause_video(self):  # 영상 정지를 위한 함수
        self.pause = True

    def resume_video(self):  # 영상 다시 재생하는 함수
        self.pause = False
        self.video_func()
        # self.webcame= cv2.VideoCapture(0)#아무 변화 없음
        self.flag=1

    def __del__(self):
        self.pause = True  # 영상 재생 정지 선택시
        if self.video.isOpened():  # 영상 재생되고있으면
            self.video.release()  # 영상 정지
        if self.webcam.isOpened():  # 웹캠 실행되고있으면
            self.webcam.release()  # 웹캠 정지


def main():
    GUI()


if __name__ == "__main__":
    # main()
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()

    app.exec_()
    ex = Example()
    ex.initUI()
    app.exec_()
    main()
# 로그인 UI

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
        tkk1 = Tk()

        for i in range(len(self.stid)):
            if self.lineEdit.text() == self.ID[i]:
                WindowClass.input_id = self.lineEdit.text()
                if self.lineEdit_2.text() == self.Password[i]:
                    tkk1.destroy()
                    self.close()

                    break
                else:
                    messagebox.showinfo(title='에러', message='비밀번호오류')
                    tkk1.destroy()

                    break
            elif i == (len(self.stid) - 1):
                messagebox.showinfo(title='에러', message='존재하지않는 회원입니다.')

            else:
                continue
            tkk1.destroy()



class Example(QWidget):

    # global input_id
    def __init__(self):
        super().__init__()
        self.initUI()

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

        listWidget.itemDoubleClicked.connect(self.onClicked)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)
        # listWidget.itemDoubleClicked.connect(self.onClicked)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QListWidget')
        self.show()

    def onClicked(self, item):

        QMessageBox.information(self, "Info", item.text())
        Example.c_name = item.text()

        cursor = att_db.cursor(pymysql.cursors.DictCursor)
        query2 = """SELECT url FROM COURSE WHERE coursename=%s"""
        cursor.execute(query2, Example.c_name)

        courseurl = cursor.fetchone()

        Example.URL = courseurl.get('url')
        # self.video = cv2.VideoCapture(URL)
        self.close()




# 눈 비율
def eye_aspect_ratio(eye):  # 눈의 면적 비율 구하는 함수
    # compute the euclidean distance between the vertical eye landmarks
    # 눈 세로 거리
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # 눈 가로 거리 계산
    # compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])

    # compute the EAR
    ear = (A + B) / (2 * C)
    return ear


class Message:
    def __init__(self, gui_obj,level):
        self.timer = 0  # 초 세는 변수
        self.timeText = 0  # 센 초 출력 변수
        self.running = False
        self.obj = gui_obj
        self.level=level
        self.Messagebox = Tk()  # 팝업  Tk:인터페이스
        self.Messagebox.geometry('400x250')  # 팝업 사이즈
        self.Messagebox.resizable(0, 0)
        self.Messagebox.title("Messagebox")  # 팝업 이름
        if(self.level==1):
            # Label: 팝업에 텍스트 및 이미지 표시하는 역할
            Text = Label(self.Messagebox, text="강의수강\n제대로 해주세요\n결석까지 남은시간:", font=("Helvetica", 20))  # 팝업에 시간 출력 양식 맟추기
            Text.pack(side="top")
            self.timeText = Label(self.Messagebox, text="0", font=("Helvetica", 10))
            self.timeText.pack()
            continuetButton = Button(self.Messagebox, text='확인', bg="yellow", command=self.contiune_func)
            continuetButton.pack(fill=tk.BOTH)

            self.startTimer()  # 시간측정 시간
            self.Messagebox.mainloop()
        elif (self.level == 2):
            Text2 = Label(self.Messagebox, text="동영상 대리출석 방지 팝업\n결석까지 남은시간:",font=("Helvetica", 15))  # 팝업에 시간 출력 양식 맟추기
            Text2.pack(side="top")
            self.timeText = Label(self.Messagebox, text="0", font=("Helvetica", 10))
            self.timeText.pack()
            continuetButton = Button(self.Messagebox, text='확인', bg="yellow", command=self.contiune_func)
            continuetButton.pack(fill=tk.BOTH)

            self.startTimer()  # 시간측정 시간
            self.Messagebox.mainloop()

    def contiune_func(self):  # 멈추는 함수
        self.Messagebox.destroy()  # 프로그램 종료

    def startTimer(self):  # 초 세고 종료시키는 함수
        self.running = True  # 함수 실행
        if (self.running):  # 실행중이면
            self.timer += 1  # 시간 카운팅
            self.timeText.configure(text=int(self.timer/60))  # 시간 출력
            if (self.timer > 500):  # 제한시간동안 팝업 확인 안하면
                self.Messagebox.destroy()  # 팝업 종료
                self.obj.pause = True
                self.obj.window.destroy()
        else:  # 실행중이 아니면
            self.timer = 0  # 세던 시간 초기화
        self.Messagebox.after(10, self.startTimer)


class GUI:  # 변수 초기화 및 포맷
    def __init__(self):
        self.timer2=0
        self.JAWLINE_POINTS = list(range(0, 17))
        self.RIGHT_EYE_POINTS = list(range(36, 42))
        self.LEFT_EYE_POINTS = list(range(42, 48))
        self.RIGHT_EYEBROW_POINTS = list(range(17, 22))
        self.LEFT_EYEBROW_POINTS = list(range(22, 27))
        self.NOSE_POINTS = list(range(27, 36))
        self.MOUTH_OUTLINE_POINTS = list(range(48, 61))
        self.MOUTH_INNER_POINTS = list(range(61, 68))

        self.EYE_AR_THRESH = 0.22  # 0.22 ->0.11(x) -> 0.22
        self.EYE_AR_CONSEC_FRAMES = 2  # 3->2
        self.EAR_AVG = 0
        self.DOWN_COUNTER = 0
        self.TOTAL = 0
        self.UP_COUNTER = 0
        self.flag = 1
        self.delay = 15  # ms
        self.width = 640
        self.height = 480
        self.pause = False
        # 눈 미인식 부분 변수
        self.eyeleft = 0
        self.eyeright = 0
        self.eyeframe = 0

        self.window = Tk()
        self.window.title("Video Player")  # 비디오 제목
        bottom_layout = Frame(self.window)
        bottom_layout.pack(side="bottom", pady=5)
        video_layout = Frame(self.window, relief="solid", bd=1)
        video_layout.pack(side="left", fill="both", expand=True)  # 왼쪽에 영상
        self.webcam_layout = Label(self.window, relief="solid", bd=1)
        self.webcam_layout.pack(side="right", fill="both", expand=True)  # 오른쪽에 웹캠
        self.canvas = Canvas(video_layout)
        self.canvas.pack()
        self.canvas.config(width=self.width, height=self.height)
        # 각 열 영상 버튼 구현
        self.btn_play = Button(bottom_layout, text="Play", width=15, command=self.video_func)
        self.btn_play.grid(row=0, column=1)
        self.btn_pause = Button(bottom_layout, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=0, column=2)
        self.btn_resume = Button(bottom_layout, text="resume", width=15, command=self.resume_video)
        self.btn_resume.grid(row=0, column=3)

        self.open_file()  # 파일 오픈 시작
        self.window.mainloop()
        os._exit(1)

    def open_file(self):  # 인강과 웹캠 여는 함수

        self.pause = False  # 중지한 상태가 아니면
        # 인강과 웹캠 열기
        real_url = Example.URL
        self.video = cv2.VideoCapture(real_url)
        self.webcam = cv2.VideoCapture(0)

    def get_frame(self):
        try:
            if self.video.isOpened():  # 인강 연다
                ret, frame = self.video.read()  # 인강 읽어오기
                resize = cv2.resize(frame, (640, 480))  # 영상 크기 조정
                return (ret, cv2.cvtColor(resize, cv2.COLOR_BGR2RGB))  # 영상 출력
        except:  # 인강 끝나면
            cursor = att_db.cursor(pymysql.cursors.DictCursor)
            now_coursename = Example.c_name
            query = """SELECT coursenum FROM COURSE WHERE coursename=%s"""
            cursor.execute(query, now_coursename)

            now_coursenum = cursor.fetchone()
            c_num = (now_coursenum.get('coursenum'))


            DB_ID = WindowClass.input_id

            cursor.execute("UPDATE BUCKET SET attendance ='o' WHERE b_stid='%s' and b_coursenum='%s'" % (DB_ID, c_num))
            # query="""UPDATE BUCKET SET attendance ='o' WHERE b_stid=%s and b_coursenum=%s"""
            # cursor.execute(query,(DB_ID, c_num))

            att_db.commit()

            messagebox.showinfo(title='', message='수강을 완료하였습니다.')
            # sys.exit()
            os._exit(1)



    def webcam_func(self):  # 웹캠 분석
        detector = dlib.get_frontal_face_detector()  # dlib 이용 기본 얼굴 검출기
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # 랜드마크 정보

        cursor1 = att_db.cursor(pymysql.cursors.DictCursor)
        long=cursor1.excute("SELECT time FROM course where coursenum='%s'"%(self.c_num))



        self.time=np.random.randint(0,long)

        if (self.webcam):  # 웹캠 실행되면
            while not self.pause:  # 영상 중지 아니면
                ret, frame = self.webcam.read()  # 웹캠 불러오기

                if ret:
                    cv2.putText(frame, "left eye {}".format(self.eyeleft), (10, 150), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                                (0, 255, 255), 1)
                    cv2.putText(frame, "right eye {}".format(self.eyeright), (10, 180), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                                (0, 255, 255), 1)
                    # 눈 미인식시
                    if self.eyeframe > 100:
                        self.eyeframe = 0
                        Message(self,1)
                    if (self.eyeleft < 4 or self.eyeleft > 6) and (
                            self.eyeright < 4 or self.eyeright > 6):  # 눈 찾는 점이 4~6개 아니면
                        self.eyeframe += 1  # 프레임 증가
                    else:  # 찾는 점이 4~6개면
                        self.eyeleft = 0  # 눈 찾는 점 변수 초기화
                        self.eyeright = 0  # 눈 찾는 점 변수 초기화
                        self.eyeframe = 0
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    rects = detector(gray, 0)
                    for rect in rects:  # 웹캠 단위 쪼개서 분석 시작
                        # 웹캠 좌표
                        x = rect.left()
                        y = rect.top()
                        x1 = rect.right()
                        y1 = rect.bottom()
                        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])
                        # 얼굴에 랜드마크 찍기
                        left_eye = landmarks[self.LEFT_EYE_POINTS]
                        right_eye = landmarks[self.RIGHT_EYE_POINTS]

                        left_eye_hull = cv2.convexHull(left_eye)
                        right_eye_hull = cv2.convexHull(right_eye)
                        self.eyeleft = len(left_eye_hull)
                        self.eyeright = len(right_eye_hull)
                        cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
                        cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
                        ear_left = eye_aspect_ratio(left_eye)
                        ear_right = eye_aspect_ratio(right_eye)
                        ear_avg = (ear_left + ear_right) / 2.0  # 양쪽 눈 면적 평균

                        if self.UP_COUNTER > 100:  # 눈 계속 떴을때
                            # 팝업 열기전 프레임 초기화
                            self.UP_COUNTER = 0
                            self.DOWN_COUNTER = 0
                            Message(self,1)
                        print(self.DOWN_COUNTER)
                        if self.DOWN_COUNTER > 100:  # 눈을 계속 감고있을때
                            # 팝업 열기전 프레임 초기화
                            self.UP_COUNTER = 0
                            self.DOWN_COUNTER = 0

                            Message(self,1)
                            # window.mainloop()
                        if ear_avg < self.EYE_AR_THRESH:
                            self.DOWN_COUNTER += 1
                            self.UP_COUNTER = 0
                        else:
                            self.UP_COUNTER += 1
                            if self.DOWN_COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                                self.TOTAL += 1

                            self.DOWN_COUNTER = 0
                        self.timer2 +=1

                        if(self.timer2==self.time):
                            Message(self,2)

                        # 웹캠 왼쪽 상단 눈 깜빡임 횟수 및 눈 비율 출력
                        cv2.putText(frame, "Blinks{}".format(self.TOTAL), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                                    (0, 255, 255), 1)
                        cv2.putText(frame, "EAR {}".format(ear_avg), (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                                    (0, 255, 255), 1)

                # 영상 컬러 변환
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 영상 컬러로 수정후 불러오기
                image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
                self.webcam_layout.configure(image=image)
                self.webcam_layout.image = image

    def video_func(self):  # 영상 재생
        ret, frame = self.get_frame()
        if self.flag == 1:
            self.thread = threading.Thread(target=self.webcam_func, args=())
            self.thread.start()
            # self.thread.join()
            self.flag = 0
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        if not self.pause:
            self.window.after(self.delay, self.video_func)

    def webcam_start(self):
        ret, frame = self.webcam.read()
        if self.flag == 1:
            self.thread = threading.Thread(target=self.video_func, args=())
            self.thread.start()
            # self.thread.join()
            self.flag = 0
        if ret:
            self.webcam_func()

    def pause_video(self):  # 영상 정지를 위한 함수
        self.pause = True

    def resume_video(self):  # 영상 다시 재생하는 함수
        self.pause = False
        self.video_func()
        # self.webcame= cv2.VideoCapture(0)#아무 변화 없음
        self.flag=1

    def __del__(self):
        self.pause = True  # 영상 재생 정지 선택시
        if self.video.isOpened():  # 영상 재생되고있으면
            self.video.release()  # 영상 정지
        if self.webcam.isOpened():  # 웹캠 실행되고있으면
            self.webcam.release()  # 웹캠 정지


def main():
    GUI()


if __name__ == "__main__":
    # main()
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()

    app.exec_()
    ex = Example()
    ex.initUI()
    app.exec_()
    main()