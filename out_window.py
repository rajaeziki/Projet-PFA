import logging
import os
import time
import cv2
import pickle
import datetime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QTimer, QDate
from PyQt5.uic import loadUi
import face_recognition
import firebase_admin
from firebase_admin import credentials, db, storage
import pywhatkit
from PyQt5 import QtWidgets
import Encoding
Encoding.main()


class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        self.Date_Label.setText("")
        self.Time_Label.setText("")
        self.imgLabel.setText("")

        self.initUI()
        #self.initFirebase()
        self.load_known_faces()

        # Timer for delayed message sending
        self.message_timer = QTimer(self)
        self.message_timer.setSingleShot(True)
        self.message_timer.timeout.connect(self.send_unrecognized_message)
        self.matches_found = False

    def initUI(self):
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        self.image = None

    def load_known_faces(self):
        try:
            MyFoldimg = 'C:\\Users\\ULTRA PC\\source\\repos\\myFirstPyProject\\images\\'
            imgpathlist = os.listdir(MyFoldimg)
            MyfoldList = [cv2.imread(os.path.join(MyFoldimg, el)) for el in imgpathlist]

            with open('EncodeFile.p', 'rb') as file:
                enKnownANDNames = pickle.load(file)
            self.enKnown, self.MyfoldListName = enKnownANDNames

            logging.info("Loaded known faces.")
        except Exception as e:
            logging.error("Failed to load known faces: %s", e)
            QMessageBox.critical(self, "Load Error", "Failed to load known faces.")

    def startVideo(self, source):
        self.cap = cv2.VideoCapture(int(source))
        if not self.cap.isOpened():
            logging.error("Failed to open video source.")
            QMessageBox.critical(self, "Camera Error", "Failed to open video source.")
            return
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(40)

    @pyqtSlot()
    def send_unrecognized_message(self):
        if not self.matches_found:
            num = os.getenv('num', '+212658773297')
            if not num:
                logging.error("Environment variable 'num' is not set.")
                return

            try:
                pywhatkit.sendwhatmsg_instantly(num, "Hi maj, an unknown person is here")
                logging.info("Message sent successfully!")
                self.capture_image()
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                time.sleep(10)

    def update_frame(self):
        ret, img = self.cap.read()
        if not ret:
            logging.warning("Failed to capture frame from camera.")
            return

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        self.matches_found = False
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(self.enKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.enKnown, encodeFace)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = (x1 - 10, y1 - 10, x2 - x1, y2 - y1)
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if True in matches:
                self.findChild(QtWidgets.QLabel, 'Status_Label').setText('known')
                self.matches_found = True

        self.display_image(img)

        # Start the timer if no matches found, stop if matches are found
        if self.matches_found:
            self.message_timer.stop()
        else:
            if not self.message_timer.isActive():
                self.findChild(QtWidgets.QLabel, 'Status_Label').setText('unknown')
                self.message_timer.start(5000)  # 5 seconds delay

    def display_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.imgLabel.setPixmap(pixmap)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = buffer.tobytes()
            bucket = storage.bucket()
            timestamp = int(time.time())
            filename = f"image_{timestamp}.jpg"
            blob = bucket.blob(filename)
            blob.upload_from_string(image_data, content_type='image/jpeg')
            logging.info("Image captured and uploaded.")
        else:
            logging.error("Failed to capture image")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = Ui_OutputDialog()
    dialog.show()
    sys.exit(app.exec_())
