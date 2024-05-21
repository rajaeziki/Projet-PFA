from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import sqlite3
import os
from os import path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication
from mainwindow import Ui_Dialog
# Execute the main function from encoding.py

cred=credentials.Certificate("C:\\Users\\ULTRA PC\\Downloads\\pfa1-3687a-firebase-adminsdk-hkao1-2db974ef46.json")


bucket = storage.bucket()
MyFoldimg='C:\\Users\\ULTRA PC\\source\\repos\\myFirstPyProject\\images\\'

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main_window.ui"))

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('cameras.db')
c = conn.cursor()

# Create the cameras table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS cameras
             (camera_id TEXT PRIMARY KEY,
              camera_name TEXT,
              camera_location TEXT)''')
conn.commit()

# Create the persons table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS persons
             (person_id TEXT PRIMARY KEY,
              person_name TEXT,
              person_role TEXT,
              pic BLOB)''')
conn.commit()

class CustomDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CustomDelegate, self).__init__(parent)
    
    def sizeHint(self, option, index):
        # Set custom row height
        size = super(CustomDelegate, self).sizeHint(option, index)
        size.setHeight(100)  # Adjust this value to make the row larger
        return size
        
        
class MainWindow(QMainWindow, FORM_CLASS):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # This is where the UI file gets loaded

        # Set custom delegate for QListWidget
        self.personListWidget.setItemDelegate(CustomDelegate(self))

        # Set icon size
        self.personListWidget.setIconSize(QSize(80, 80))  # Adjust this to fit your needs

        # Connect buttons to functions
        self.btn_face_recognition.clicked.connect(self.run_face_recognition)
        self.btn_add_camera.clicked.connect(self.send_add_camera_request)
        self.btn_modify_camera.clicked.connect(self.send_modify_camera_request)
        self.btn_display_camera.clicked.connect(self.send_display_camera_request)
        self.btn_delete_camera.clicked.connect(self.send_delete_camera_request)
        self.btn_add_person.clicked.connect(self.send_add_person_request)
        self.btn_modify_person.clicked.connect(self.send_modify_person_request)
        self.btn_display_person.clicked.connect(self.send_display_person_request)
        self.btn_delete_person.clicked.connect(self.send_delete_person_request)
        self.btn_exit.clicked.connect(self.exit_application)

    def run_face_recognition(self):
        # Here you can place the code to execute when the Face Recognition button is clicked
        # For example:
        self.show_main_window()

    def show_main_window(self):
        self._main_window = Ui_Dialog()
        self._main_window.show()

    def send_add_camera_request(self):
        camera_id, ok_id = QInputDialog.getText(self, 'Enter Camera ID', 'Camera ID:')
        camera_name, ok_name = QInputDialog.getText(self, 'Enter Camera Name', 'Camera Name:')
        camera_location, ok_location = QInputDialog.getText(self, 'Enter Camera Location', 'Camera Location:')

        if ok_id and ok_name and ok_location:
            # Add camera data to SQLite
            c.execute("INSERT INTO cameras (camera_id, camera_name, camera_location) VALUES (?, ?, ?)",
                      (camera_id, camera_name, camera_location))
            conn.commit()
            print("Camera added successfully")

    def send_modify_camera_request(self):
        camera_id, ok = QInputDialog.getText(self, 'Enter Camera ID', 'Camera ID:')
        if ok:
            camera_name, ok_name = QInputDialog.getText(self, 'Enter New Camera Name', 'New Camera Name:')
            camera_location, ok_location = QInputDialog.getText(self, 'Enter New Camera Location', 'New Camera Location:')
            if ok_name or ok_location:
                # Retrieve and update camera data in SQLite
                c.execute("SELECT * FROM cameras WHERE camera_id = ?", (camera_id,))
                camera_ref = c.fetchone()
                if camera_ref:
                    if ok_name:
                        c.execute("UPDATE cameras SET camera_name = ? WHERE camera_id = ?", (camera_name, camera_id))
                    if ok_location:
                        c.execute("UPDATE cameras SET camera_location = ? WHERE camera_id = ?", (camera_location, camera_id))
                    conn.commit()
                    print("Camera modified successfully")
                else:
                    print("Camera not found")
            else:
                print("No modifications provided")

    def send_display_camera_request(self):
        # Retrieve all cameras from SQLite
        c.execute("SELECT * FROM cameras")
        cameras = c.fetchall()
        if cameras:
            message = ""
            for camera in cameras:
                message += f"Camera ID: {camera[0]}, Name: {camera[1]}, Location: {camera[2]}\n"
            msg_box = QMessageBox()
            msg_box.setText("Cameras:")
            msg_box.setInformativeText(message)
            msg_box.setWindowTitle("Display Cameras")
            msg_box.exec_()
        else:
            print("No cameras found")

    def send_delete_camera_request(self):
        camera_id, ok = QInputDialog.getText(self, 'Enter Camera ID', 'Camera ID:')
        if ok:
            # Delete camera data from SQLite
            c.execute("DELETE FROM cameras WHERE camera_id = ?", (camera_id,))
            conn.commit()
            print("Camera deleted successfully")

    def send_add_person_request(self):
        person_id, ok_id = QInputDialog.getText(self, 'Enter Person ID', 'Person ID:')
        person_name, ok_name = QInputDialog.getText(self, 'Enter Person Name', 'Person Name:')
        person_role, ok_role = QInputDialog.getText(self, 'Enter Person Role', 'Person Role:')
        picture_path, ok_picture = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image files (*.jpg *.png)')

        if ok_id and ok_name and ok_role and ok_picture:
            with open(picture_path, 'rb') as file:
                pic_blob = file.read()
            # Add person data to SQLite
            c.execute("INSERT INTO persons (person_id, person_name, person_role, pic) VALUES (?, ?, ?, ?)",
                      (person_id, person_name, person_role, pic_blob))
            conn.commit()
            print("Person added successfully")
            
            blob = bucket.blob(f"C:\\Users\\ULTRA PC\\source\\repos\\myFirstPyProject\\images\\/{person_id}.jpg")  # Change the path/name as per your requirement
            blob.upload_from_filename(picture_path)
            print("Image uploaded to Firebase Storage")

    def send_modify_person_request(self):
        person_id, ok = QInputDialog.getText(self, 'Enter Person ID', 'Person ID:')
        if ok:
            person_name, ok_name = QInputDialog.getText(self, 'Enter New Person Name', 'New Person Name:')
            person_role, ok_role = QInputDialog.getText(self, 'Enter New Person Role', 'New Person Role:')
            picture_path, ok_picture = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image files (*.jpg *.png)')

            if ok_name or ok_role or ok_picture:
                # Retrieve and update person data in SQLite
                c.execute("SELECT * FROM persons WHERE person_id = ?", (person_id,))
                person_ref = c.fetchone()
                if person_ref:
                    if ok_name:
                        c.execute("UPDATE persons SET person_name = ? WHERE person_id = ?", (person_name, person_id))
                    if ok_role:
                        c.execute("UPDATE persons SET person_role = ? WHERE person_id = ?", (person_role, person_id))
                    if ok_picture:
                        with open(picture_path, 'rb') as file:
                            pic_blob = file.read()
                        c.execute("UPDATE persons SET pic = ? WHERE person_id = ?", (pic_blob, person_id))
                    conn.commit()
                    print("Person modified successfully")
                else:
                    print("Person not found")
            else:
                print("No modifications provided")

    def send_display_person_request(self):
        # Retrieve all persons from SQLite
        c.execute("SELECT * FROM persons")
        persons = c.fetchall()
        self.personListWidget.clear()
        if persons:
            for person in persons:
                item = QListWidgetItem(f"ID: {person[0]}, Name: {person[1]}, Role: {person[2]}")
                if person[3]:
                    pixmap = QPixmap()
                    pixmap.loadFromData(person[3])
                    icon = QIcon(pixmap)
                    item.setIcon(icon)
                self.personListWidget.addItem(item)
        else:
            print("No persons found")

    def send_delete_person_request(self):
        person_id, ok = QInputDialog.getText(self, 'Enter Person ID', 'Person ID:')
        if ok:
            # Delete person data from SQLite
            c.execute("DELETE FROM persons WHERE person_id = ?", (person_id,))
            conn.commit()
            print("Person deleted successfully")

    def exit_application(self):
        conn.close()
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
