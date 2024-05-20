# import os
# import cv2
# import face_recognition
# import pickle
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage
#
#
# def update_known_faces(folder_path="data/images"):
#     """
#   This function updates the known faces data structure by encoding images in a folder
#   and uploading them to Firebase Storage (optional).
#
#   Args:
#       folder_path (str, optional): Path to the folder containing student images. Defaults to "data/images".
#   """
#
#     # Initialize Firebase if not already done (assuming credentials are configured)
#     try:
#         cred = credentials.Certificate("serviceAccountKey.json")
#         firebase_admin.initialize_app(cred, {
#             'databaseURL': "https://facerecattenedancesystemfinal-default-rtdb.asia-southeast1.firebasedatabase.app/",
#             'storageBucket': "facerecattenedancesystemfinal.appspot.com"
#         })
#     except ValueError:
#         pass  # Firebase app already initialized
#
#     # Importing student images
#     pathList = os.listdir(folder_path)
#     imgList = []
#     studentIds = []
#     for path in pathList:
#         img = cv2.imread(os.path.join(folder_path, path))
#         imgList.append(img)
#         studentIds.append(os.path.splitext(path)[0])
#
#         # Optional: Upload image to Firebase Storage
#         # fileName = f'{folderPath}/{path}'
#         # bucket = storage.bucket()
#         # blob = bucket.blob(fileName)
#         # blob.upload_from_filename(fileName)
#
#     print(studentIds)
#
#     def find_encodings(images_list):
#         encode_list = []
#         for img in images_list:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB format
#             encode = face_recognition.face_encodings(img)[0]
#             encode_list.append(encode)
#         return encode_list
#
#     # Load existing encoded faces and names (if available)
#     known_faces_path = "../data/known_faces.pkl"
#     if os.path.exists(known_faces_path):
#         with open(known_faces_path, "rb") as f:
#             encodeListKnown, studentIds = pickle.load(f)
#     else:
#         encodeListKnown, studentIds = [], []
#
#     # Encode the newly imported images from the folder
#     print("Encoding newly imported images...")
#     new_encodeListKnown = find_encodings(imgList)
#     encodeListKnown.extend(new_encodeListKnown)  # Combine existing and new encodings
#     studentIds.extend([path.split(".")[0] for path in pathList])  # Add student IDs from filenames
#
#     # Save the updated encoded faces and names
#     with open(known_faces_path, "wb") as f:
#         pickle.dump((encodeListKnown, studentIds), f)
#     print("Encoding complete and saved to known_faces.pkl!")
#
#
# # Example usage in a Streamlit app
# if __name__ == "__main__":
#     import streamlit as st
#
#     st.title("Update Known Faces")
#     if st.button("Update Faces"):
#         update_known_faces()
#         st.success("Known faces updated successfully!")
