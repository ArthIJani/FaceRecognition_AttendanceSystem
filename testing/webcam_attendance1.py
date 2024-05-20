import pickle
from datetime import datetime
import cv2
import face_recognition
import numpy as np
import streamlit as st
import firebase_admin
from firebase_admin import db
from firebase_admin import storage

from testing.AddImageToDatabase import studentIds

cred = firebase_admin.credentials.Certificate('/Users/arthjani/Desktop/CP4-FaceRec'
                                              '/Final_FaceRecognition_AttendanceSystem/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecattenedancesystemfinal-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'facerecattenedancesystemfinal.appspot.com'
})
bucket = storage.bucket()


def display_webcam_attendance(debug_mode=False):
    counter = -1
    st.title("Attendance System")
    st.caption("Powered by OpenCV, Streamlit & face_recognition")

    # Load known face encodings and names from pickle file
    with open("../data/EncodeFile.p", "rb") as f:
        known_faces, known_names = pickle.load(f)

    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    # Placeholder to display the frame with detected faces
    frame_placeholder = st.empty()

    # Button to stop the app
    stop_button_pressed = st.button("Stop")

    # Initial attendance capture upon opening camera
    ret, frame = cap.read()
    # Convert frame to RGB format
    rgb_frame = frame[:, :, ::-1]

    while cap.isOpened() and not stop_button_pressed:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame capture failed
        if not ret:
            st.write("Video Capture Ended")
            break

        # Convert frame to RGB format
        rgb_frame = frame[:, :, ::-1]

        # Find all faces and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_locations:
            # Draw rectangles around detected faces (red color)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with known face encodings
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                faceDis = face_recognition.face_distance(known_faces, face_encoding)

                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(studentIds[matchIndex])
                    y1, x2, y2, x1 = top, right, bottom, left
                    id = studentIds[matchIndex]

                    if counter == 0:
                        counter = 1
            if counter != 0:
                if counter == 1:
                    # Get the Data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)

                    # Update data of attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        counter = 0
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Red color (BGR)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, f"{name}", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            frame_placeholder.image(frame, channels="BGR")









