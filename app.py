import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QInputDialog, QMessageBox

# Firebase configuration
firebase_url = "https://pfa1-3687a-default-rtdb.europe-west1.firebasedatabase.app"
cameras_endpoint = f"{firebase_url}/cameras.json"

# PyQt5 application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mido")
        self.setGeometry(100, 100, 400, 200)

        # Create widgets
        self.label = QLabel("Welcome to Cameras Management System", self)
        self.btn_add = QPushButton("Add Camera", self)
        self.btn_modify = QPushButton("Modify Camera", self)
        self.btn_display = QPushButton("Display Cameras", self)
        self.btn_delete = QPushButton("Delete Camera", self)
        self.btn_exit = QPushButton("Exit", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_modify)
        layout.addWidget(self.btn_display)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_exit)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect buttons to functions
        self.btn_add.clicked.connect(self.send_add_request)
        self.btn_modify.clicked.connect(self.send_modify_request)
        self.btn_display.clicked.connect(self.send_display_request)
        self.btn_delete.clicked.connect(self.send_delete_request)
        self.btn_exit.clicked.connect(self.exit_application)

    def send_add_request(self):
        camera_id, ok_id = QInputDialog.getText(self, 'Enter Camera ID', 'Camera ID:')
        camera_name, ok_name = QInputDialog.getText(self, 'Enter Camera Name', 'Camera Name:')
        camera_location, ok_location = QInputDialog.getText(self, 'Enter Camera Location', 'Camera Location:')
        
        if ok_id and ok_name and ok_location:
            # Add camera data to Firebase
            new_camera_data = {
                "camera_id": camera_id,
                "camera_name": camera_name,
                "camera_location": camera_location
            }
            response = requests.post(cameras_endpoint, json=new_camera_data)
            if response.status_code == 200:
                print("Camera added successfully")
            else:
                print("Failed to add camera")

    def send_modify_request(self):
        camera_id, ok = QInputDialog.getText(self, 'Enter Camera ID', 'Camera ID:')
        if ok:
            camera_name, ok_name = QInputDialog.getText(self, 'Enter New Camera Name', 'New Camera Name:')
            camera_location, ok_location = QInputDialog.getText(self, 'Enter New Camera Location', 'New Camera Location:')
            if ok_name or ok_location:
                # Retrieve camera data from Firebase
                response = requests.get(f"{firebase_url}/cameras/{camera_id}.json")
                if response.status_code == 200:
                    camera_data = response.json()
                    if ok_name:
                        camera_data["camera_name"] = camera_name
                    if ok_location:
                        camera_data["camera_location"] = camera_location
                    # Update camera data in Firebase
                    response = requests.put(f"{firebase_url}/cameras/{camera_id}.json", json=camera_data)
                    if response.status_code == 200:
                        print("Camera modified successfully")
                    else:
                        print("Failed to modify camera")
                else:
                    print("Camera not found")
            else:
                print("No modifications provided")

    def send_display_request(self):
        # Retrieve all cameras from Firebase
        response = requests.get(cameras_endpoint)
        if response.status_code == 200:
            cameras_data = response.json()
            if cameras_data:
                message = ""
                for camera_id, camera_data in cameras_data.items():
                    message += f"Camera ID: {camera_data['camera_id']}, Name: {camera_data['camera_name']}, Location: {camera_data['camera_location']}\n"
                msg_box = QMessageBox()
                msg_box.setText("Cameras:")
                msg_box.setInformativeText(message)
                msg_box.setWindowTitle("Display Cameras")
                msg_box.exec_()
            else:
                print("No cameras found")
        else:
            print("Failed to retrieve cameras")

    def send_delete_request(self):
        camera_id, ok = QInputDialog.getText(self, 'Enter Camera ID', 'Camera ID:')
        if ok:
            # Delete camera data from Firebase
            response = requests.delete(f"{firebase_url}/cameras/{camera_id}.json")
            if response.status_code == 200:
                print("Camera deleted successfully")
            else:
                print("Failed to delete camera")
    
    def exit_application(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
