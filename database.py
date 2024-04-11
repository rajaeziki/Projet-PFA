import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# try:
#     import firebase_admin
#     print("Firebase Admin SDK is installed.")
# except ImportError:
#     print("Firebase Admin SDK is not installed.")
cred = credentials.Certificate("path/to/websitepython-b4984-firebase-adminsdk-zveq3-d650097ae7.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
data = {
    'id'=''
    'status'=
}
try: 
    import firebase_admin
    print("Firebase Admin SDK is installed.")
except ImportError:
    print("Firebase Admin SDK is not installed.")