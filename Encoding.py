import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import os
import face_recognition as fr
import pickle

cred=credentials.Certificate("C:\\Users\\ULTRA PC\\Downloads\\pfa1-3687a-firebase-adminsdk-hkao1-2db974ef46.json")

firebase_admin.initialize_app(cred,{
    'storageBucket': 'pfa1-3687a.appspot.com',
    'databaseURL': 'https://pfa1-3687a-default-rtdb.europe-west1.firebasedatabase.app/'})


MyFoldimg='C:\\Users\\ULTRA PC\\source\\repos\\myFirstPyProject\\images\\'
imgpathlist=os.listdir(MyFoldimg)
MyfoldListName=[]
MyfoldList=[]
bucket = storage.bucket()
blobs = bucket.list_blobs()
for blob in blobs:
    filename = blob.name
    file_path = os.path.join(MyFoldimg, filename)
    blob.download_to_filename(file_path)
imgpathlist = os.listdir(MyFoldimg)
print(imgpathlist)
MyfoldListName = []
MyfoldList = []
for el in imgpathlist:
    filename = os.path.join(MyFoldimg, el)
    MyfoldList.append(cv2.imread(filename))
    MyfoldListName.append(os.path.splitext(el)[0])

print(MyfoldList)
print(MyfoldListName)
print(imgpathlist)


def findEn(List):
    enList=[]
    for img in List:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        en=fr.face_encodings(img)[0]
        enList.append(en)
    return enList

print("start Encoding")
enKnown=findEn(MyfoldList)
print(enKnown)
print("end Encoding")
enKnownANDNames=[enKnown,MyfoldListName]
file=open("EncodeFile.p",'wb')
pickle.dump(enKnownANDNames, file)
file.close()
print("file saved")
