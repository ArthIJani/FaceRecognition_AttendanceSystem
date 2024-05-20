import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def add_data_to_firebase(data, path):
  # Initialize Firebase app with credentials
  cred = credentials.Certificate('serviceAccountKey.json')  # Replace with your credentials file path
  firebase_admin.initialize_app(cred, {
      'databaseURL': 'https://your-firebase-project.firebaseio.com'  # Replace with your project URL
  })

  # Get a database reference
  ref = database.reference(path)


