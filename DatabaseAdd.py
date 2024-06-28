import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred=credentials.Certificate("C:\\Users\\ULTRA PC\\Downloads\\pfa1-3687a-firebase-adminsdk-hkao1-2db974ef46.json")

firebase_admin.initialize_app(cred,{
    'storageBucket': 'pfa1-3687a.appspot.com',
    'databaseURL': 'https://pfa1-3687a-default-rtdb.europe-west1.firebasedatabase.app/'})

ref1= db.reference('/cams')
ref2= db.reference('/images')
ref3= db.reference('/users')

ndata1 = {
    'Nserie': 'mmrr223',
    'descrip': 'cam class1',
}

ref1.push(ndata1)
"""
print("cam added successfully.")
ndata2 = {
    'description': 'img maj',
    'title': 'maj',
    'url': '',
}

ref2.push(ndata2)
print("image added successfully.")
ndata3 = {
    'class': 'value1',
    'drade': 'value2',
    'name': 'value2',
}

ref3.push(ndata3)
print("user added successfully.")
"""