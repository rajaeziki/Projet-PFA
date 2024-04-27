
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import os
import face_recognition as fr
import cvzone
cred=credentials.Certificate("C:\\Users\\ULTRA PC\\Downloads\\pfa1-3687a-firebase-adminsdk-hkao1-2db974ef46.json")

firebase_admin.initialize_app(cred,{
    'storageBucket': 'pfa1-3687a.appspot.com',
    'databaseURL': 'https://pfa1-3687a-default-rtdb.europe-west1.firebasedatabase.app/'})

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
MyFoldimg='C:\\Users\\ULTRA PC\\source\\repos\\myFirstPyProject\\images\\'
imgpathlist=os.listdir(MyFoldimg)
MyfoldList=[]
for el in imgpathlist:
    MyfoldList.append(cv2.imread(os.path.join(MyFoldimg,el)))
print('load encoding file')
file=open('EncodeFile.p','rb')
enKnownANDNames=pickle.load(file)
file.close()
enKnown,MyfoldListName=enKnownANDNames
print('end load encoding file')
print(len(MyfoldList))
print(MyfoldListName)
while True:
    success,img=cap.read()
    imgS=cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    faceCurFrame=fr.face_locations(imgS)
    encodeCurFrame=fr.face_encodings(imgS,faceCurFrame)
    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        print("bla")
        print("encodeFace shape:", encodeFace.shape) 
        encodeFace = encodeFace.flatten()
        matches=fr.compare_faces(enKnown,encodeFace)
        faceDis=fr.face_distance(enKnown,encodeFace)
        print("matches: ", matches)
        print("faceDis: ", faceDis)
        y1,x2,y2,x1= faceLoc
        y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
        bbox = (x1 - 10, y1 - 10, x2-x1, y2-y1)
        img=cvzone.cornerRect(img,bbox,rt=0)
    cv2.imshow("webcam",img)
    cv2.waitKey(1)