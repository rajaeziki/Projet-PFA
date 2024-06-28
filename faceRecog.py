import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
cred=credentials.Certificate("C:\\Users\\ULTRA PC\\Downloads\\pfa1-3687a-firebase-adminsdk-hkao1-2db974ef46.json")

firebase_admin.initialize_app(cred,{
    'storageBucket': 'pfa1-3687a.appspot.com',
    'databaseURL': 'https://pfa1-3687a-default-rtdb.europe-west1.firebasedatabase.app/'})

cap=cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
while True:
    success,img=cap.read()
    cv2.imshow("Maj",img)
    cv2.waitkey(1)
