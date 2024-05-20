# import os
# import cv2
# import face_recognition
# import pickle
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage
#
# cred = firebase_admin.credentials.Certificate('serviceAccountKey.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://facerecattenedancesystemfinal-default-rtdb.asia-southeast1.firebasedatabase.app/',
#     'storageBucket': 'facerecattenedancesystemfinal.appspot.com'
# })
#
# # Importing student images
# folderPath = 'data/images'
# pathList = os.listdir(folderPath)
# print(pathList)
# imgList = []
# studentIds = []
# for path in pathList:
#     imgList.append(cv2.imread(os.path.join(folderPath, path)))
#     studentIds.append(os.path.splitext(path)[0])
#     # print(os.path.splitext(path)[0])
#
#     fileName = f'{folderPath}/{path}'
#     bucket = storage.bucket()
#     blob = bucket.blob(fileName)
#     blob.upload_from_filename(fileName)