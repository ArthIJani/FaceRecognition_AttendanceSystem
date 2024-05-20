import pickle
import datetime
import cv2
import face_recognition
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate('/Users/arthjani/Desktop/CP4-FaceRec'
                                              '/Final_FaceRecognition_AttendanceSystem/serviceAccountKey.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecattenedancesystemfinal-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'facerecattenedancesystemfinal.appspot.com'
})


ref = db.reference('Students')


def display_webcam_attendance(debug_mode=False):
    st.title("Attendance System")
    st.caption("Powered by OpenCV, Streamlit & face_recognition")

    # Load known face encodings and names from pickle file
    with open("data/EncodeFile.p", "rb") as f:
        known_faces, known_id = pickle.load(f)

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

    # Find all faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

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

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding with known face encodings
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                id = known_id[first_match_index]
                print(id)
                # studentInfo = None
                studentInfo = db.reference(f'Students/{known_id[first_match_index]}').get()
                print(studentInfo)

                # Update data of attendance
                datetimeObject = datetime.datetime.fromisoformat(studentInfo['last_attendance_time'])
                secondsElapsed = (datetime.datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    # Connect to Firebase
                    ref = db.reference(f'Students/{known_id[first_match_index]}')
                    # Update attendance data
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    st.write("Marked : ")
                    st.dataframe(studentInfo)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, f"{id}", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        frame_placeholder.image(frame, channels="BGR")

    # Release capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()
