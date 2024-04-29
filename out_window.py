from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate
from PyQt5.QtWidgets import QDialog, QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        self.image = None

        # Firebase initialization
        cred = credentials.Certificate("C:\\Users\\ULTRA PC\\Downloads\\pfa1-3687a-firebase-adminsdk-hkao1-2db974ef46.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://pfa1-3687a-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self.ref = db.reference('/attendance')

        # Camera initialization
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # Timer for updating frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(40)

        # Load known faces
        self.enKnown, self.MyfoldListName = self.load_known_faces()

    def load_known_faces(self):
        MyFoldimg = 'C:\\Users\\ULTRA PC\\source\\repos\\myFirstPyProject\\images\\'
        imgpathlist = os.listdir(MyFoldimg)
        MyfoldList = []
        for el in imgpathlist:
            MyfoldList.append(cv2.imread(os.path.join(MyFoldimg, el)))
        print('load encoding file')
        file = open('EncodeFile.p', 'rb')
        enKnownANDNames = pickle.load(file)
        file.close()
        enKnown, MyfoldListName = enKnownANDNames
        print('end load encoding file')
        print(len(MyfoldList))
        print(MyfoldListName)
        return enKnown, MyfoldListName

    @pyqtSlot()
    def update_frame(self):
        ret, img = self.cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            print("bla")
            print("encodeFace shape:", encodeFace.shape)
            encodeFace = encodeFace.flatten()
            matches = face_recognition.compare_faces(self.enKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.enKnown, encodeFace)
            print("matches: ", matches)
            print("faceDis: ", faceDis)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = (x1 - 10, y1 - 10, x2 - x1, y2 - y1)
            img = cvzone.cornerRect(img, bbox, rt=0)
            self.mark_attendance(matches)
        self.display_image(img)

    def display_image(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.imgLabel.setPixmap(pixmap)

    def mark_attendance(self, matches):
        date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        for match in matches:
            name = "unknown"
            if match:
                name = "known"
            self.ref.push({'name': name, 'date_time': date_time_string})

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = Ui_OutputDialog()
    dialog.show()
    sys.exit(app.exec_())
