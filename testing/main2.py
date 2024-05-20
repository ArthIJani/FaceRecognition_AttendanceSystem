import os
import cv2
import csv
import json
import time
import pickle
import datetime
# import numpy as np
# import pandas as pd
# import requests
# from PIL import Image
import face_recognition
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

DATA_FILE = "../data/data.json"

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://faceattendancerealtime-4d7bd-default-rtdb.firebaseio.com/",
#     'storageBucket': "faceattendancerealtime-4d7bd.appspot.com"
# })
#
# bucket = storage.bucket()

st.set_page_config(page_title="Attendance System", page_icon=":student:", layout="wide")


# ---------------------------------------- Loading Animation ----------------------------------------------------
def load_lottie_file(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)


# ---- LOAD ASSETS ----
lottie_coding = load_lottie_file("../lottie_files/face_recognition.json")


# ---------------------------------------------- Save Data --------------------------------------------------------
def save_student_data(name, enrollment_no, class_name, image):
    # Prepare student data
    student_data = {
        "name": name,
        "enrollment_no": enrollment_no,
        "class": class_name,
        "image_filename": f"{name.replace(' ', '')}.jpg",  # Use student name for image filename
        "attendance": 0,
    }

    # Load existing data or initialize empty list
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        data = []

    # Check for duplicate enrollment number
    enrollment_numbers = [student["enrollment_no"] for student in data]
    if enrollment_no in enrollment_numbers:
        st.warning(f"Enrollment number {enrollment_no} already exists. Please use a different enrollment number.")
        return

    # Save image to 'images' folder with student name as filename
    if not os.path.exists("../data/images"):
        os.makedirs("../data/images")
    image_path = os.path.join("../data/images", f"{name.replace(' ', '')}.jpg")
    with open(image_path, "wb") as img_file:
        img_file.write(image.getvalue())

    # Append new student data to the list
    data.append(student_data)

    # Save updated data back to the JSON file
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    st.success("Student data saved successfully!")


# ---------------------------------------------- Encode Data --------------------------------------------------------
def update_known_faces(image_data):
    known_faces_dir = "../data/images"

    known_faces = []
    known_names = []

    # Loop through each image in the known_faces folder
    for filename in os.listdir(known_faces_dir):
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
        # Convert image to RGB format (required by face_recognition)
        image_rgb = image[:, :, ::-1]

        # Get face encoding for the current image
        face_encoding = face_recognition.face_encodings(image_rgb)[0]

        # Extract name from filename (assuming filename format: name.jpg)
        known_names.append(os.path.splitext(filename)[0])
        known_faces.append(face_encoding)

    # Save encoded faces and names to a pickle file
    try:
        with open("../data/known_faces.pkl", "wb") as f:
            pickle.dump((known_faces, known_names), f)
        print("Encoding complete and saved to known_faces.pkl!")
    except Exception as e:
        print(f"Error saving known faces file: {e}")


# def load_known_faces():
#     """Loads known face encodings and names from a pickle file."""
#     try:
#         with open("known_faces.pkl", "rb") as f:
#             known_faces, known_names = pickle.load(f)
#         return known_faces, known_names
#     except FileNotFoundError:
#         st.error("Error: 'known_faces.pkl' file not found. Please generate it first.")
#         return None, None


#  ---------------------------------------- Navigation Bar -----------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["Home", "Add Details", "Attendance System", "Contact Us"],
    icons=["house", "cloud-upload", "person-bounding-box", "telephone"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px"},
        "nav-link-selected": {"background-color": "blue"},
    }
)

# --------------------------------------------  Home Page  -----------------------------------------------------------
if selected == "Home":
    with st.container():
        # st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.write("## Face Recognition Attendance System")
            st.write("""
            Welcome to our Face Recognition Attendance System!
            This application allows you to manage attendance using face recognition technology.
            """)
            st.markdown(
                """## How it Works

1. **Upload Images** : Upload images of individuals whose attendance you want to track.
2. **Recognition** : The system will recognize faces in uploaded images.
3. **Attendance Tracking** : Match recognized faces with known individuals to mark attendance."""
            )
            st.write("""
            ## Instructions

    1. **Upload Images**:
       - Click on the upload button to select images.
       - Ensure images are clear and include only one face per image.

    2. **Attendance Monitoring**:
       - After uploading, the system will process the images.
       - It will compare recognized faces with known individuals.

    3. **View Attendance**:
       - Attendance records will be displayed once processing is complete.
       - Check attendance status and export reports if needed.
            """)
        with right_column:
            st_lottie(lottie_coding, height=700, key="coding")

    st.write("---")
    footer = """<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: lightblue;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: white;
    text-align: center;
    }
    </style>
    """
    st.markdown(footer, unsafe_allow_html=True)
    hide_st_style = """
    <div class="footer">
    <p>Developed by 
    <a style=' text-align: center;' href="https://github.com/ArthIJani" target="_blank">Arth I Jani </a>
    </p>
    </div>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

# ----------------------------------------- Add Details Page -------------------------------------------------------

if selected == "Add Details":
    st.title("Student Information")

    # Input fields
    name = st.text_input("Name")
    enrollment_no = st.text_input("Enrollment Number")
    class_name = st.text_input("Class")
    image = st.file_uploader("Upload Student Image", type=["jpg", "jpeg", "png"])

    if st.button("Submit"):
        if name and enrollment_no and class_name and image:
            save_student_data(name, enrollment_no, class_name, image)
            update_known_faces(image.read())  # Pass image data to update function
        else:
            st.warning("Please fill in all the fields and upload an image.")

# -------------------------------------- Attendance Page --------------------------------------------------------------
if selected == "Attendance System":
    st.title("Attendance System")

    selected = option_menu(
        menu_title=None,
        options=["Using Image", "Using Webcam"],
        icons=["images", "webcam"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "blue"},
        }
    )

    if selected == "Using Webcam":
        # Title and caption for the app
        st.title("Webcam Display with Face Detection")
        st.caption("Powered by OpenCV, Streamlit & face_recognition")

        # Load known face encodings and names from pickle file
        with open("../data/known_faces.pkl", "rb") as f:
            known_faces, known_names = pickle.load(f)

        # Capture video from webcam
        cap = cv2.VideoCapture(0)

        # Initialize variables for attendance data and last save time
        attendance_data = []
        last_save_time = time.time()

        last_attendance_time = None

        # Placeholder to display the frame with detected faces
        frame_placeholder = st.empty()

        # Button to stop the app
        stop_button_pressed = st.button("Stop")

        # Initial attendance capture upon opening camera
        ret, frame = cap.read()
        # Convert frame to RGB format
        # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

            # Draw rectangles around detected faces (red color)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with known face encodings
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                    # Check for new attendance within 5-minute window
                    current_time = datetime.datetime.now()
                    print(name, datetime.datetime.now())

                    if last_attendance_time is None or (
                            current_time - datetime.timedelta(minutes=5)) > last_attendance_time:
                        attendance_data.append([name, current_time.strftime("%Y-%m-%d %H:%M:%S")])
                        last_attendance_time = current_time  # Update last attendance time

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Red color (BGR)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the frame with detected faces (already RGB format)
            frame_placeholder.image(frame, channels="RGB")

            # Exit on 'q' key press or button click
            if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
                break

            # Save attendance data every 5 minutes
            if time.time() - last_save_time >= 300:  # Check every 5 minutes
                if attendance_data:
                    with open("attendance_data.csv", "a") as f:  # Append mode
                        writer = csv.writer(f)
                        writer.writerows(attendance_data)
                    attendance_data = []  # Clear data for next 5-minute window
                    last_save_time = time.time()

        # Release capture and destroy windows
        cap.release()
        cv2.destroyAllWindows()

    if selected == "Using Image":
        st.title("Face Recognition using Image")

# -------------------------------------- Contact Us Page --------------------------------------------------------------
if selected == "Contact Us":
    st.header(":mailbox: Get In Touch With Me!")

    contact_form = """
    <form action="https://formsubmit.co/zyan.zqusd11@gmail.com" method="POST">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Your name" required>
         <input type="email" name="email" placeholder="Your email" required>
         <textarea name="message" placeholder="Your message here"></textarea>
         <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)


# ---------------------------------------- Use Local CSS File -------------------------------------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("../style/style.css")
