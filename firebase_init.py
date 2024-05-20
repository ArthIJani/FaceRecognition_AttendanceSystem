import firebase_admin
from firebase_admin import credentials


def initialize_app():
    # Initialize Firebase app (replace with your credentials)
    cred = firebase_admin.credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://facerecattenedancesystemfinal-default-rtdb.asia-southeast1.firebasedatabase.app/',
        'storageBucket': 'facerecattenedancesystemfinal.appspot.com'
    }, name='store_data')




