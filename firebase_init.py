import firebase_admin
from firebase_admin import credentials


def initialize_app():
    # Initialize Firebase app (replace with your credentials)
    cred = firebase_admin.credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'FIREBASE_DATABASEURL',
        'storageBucket': 'FIREBASE_STORAGEBUCKET'
    }, name='store_data')




