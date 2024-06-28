import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import os
import face_recognition as fr
import cvzone
import pywhatkit
from datetime import datetime
import time

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
os.environ['num'] = '+212658773297'
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
print(enKnown)

def capture_image():
    ret, frame = cap.read()
    if ret:
        # Convert the image frame to JPEG format in memory
        _, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()
        
        # Initialize Firebase Storage client
        bucket = storage.bucket()
        
        # Generate a filename based on current timestamp
        timestamp = int(time.time())
        filename = f"image_{timestamp}.jpg"
        
        # Upload the image data to Firebase Storage
        blob = bucket.blob(filename)
        blob.upload_from_string(image_data, content_type='image/jpeg')
        '''
        _, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()
        bucket = storage.bucket()
        timestamp = int(time.time())
        filename = f"image_{timestamp}.jpg"
        blob = bucket.blob(filename)
        blob.upload_from_string(image_data)
        '''
    else:
        print("Failed to capture image")
    
    

    
while True:
    success,img=cap.read()
    if not success:
        print("Failed to capture frame from webcam.")
        continue
    imgS=cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    faceCurFrame=fr.face_locations(imgS)
    encodeCurFrame=fr.face_encodings(imgS,faceCurFrame)
    matches= False
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
        if True in matches:
            matches_found = True
    
    if not matches:
        now=datetime.now()
        hr=int(now.strftime("%H"))
        min=int(now.strftime("%M"))
        num=os.environ.get('num')
        #pywhatkit.sendwhatmsg_instantly(num, "Hi maj, an unknown person is here")
        try:
            pywhatkit.sendwhatmsg_instantly(num, "Hi maj, an unknown person is here")
            print("msg sent successfully!")
            '''img_path = '''
            capture_image()
           # if img_path:
                
                # Send the captured image via WhatsApp
                #pywhatkit.send_image(img_path, num, "Hi maj, an unknown person is here")
                
                # Delete the temporary image file
                #os.remove(img_path)
        except Exception as e:
            #print(f"Error sending image: {e}")
            print(f"Error sending msg")
            time.sleep(10)
        
    cv2.imshow("webcam",img)
    cv2.waitKey(1)