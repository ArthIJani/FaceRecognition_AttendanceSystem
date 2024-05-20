import json
import streamlit as st
from streamlit_lottie import st_lottie


def display_home_page():
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
            lottie_coding = load_lottie_file("lottie_files/face_recognition.json")
            st_lottie(lottie_coding, height=700, key="coding")

    st.write("---")


def load_lottie_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)



