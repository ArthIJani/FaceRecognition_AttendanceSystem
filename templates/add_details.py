import streamlit as st
import json
import os
from datetime import datetime
from AddDataToDatabase import set_student_data_from_json
from data_utils import update_known_faces


def save_image(image_file, id, image_folder):
    try:
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Use enrollment number (ID) as the filename
        filename = f"{id}.{image_file.name.split('.')[-1]}"

        with open(os.path.join(image_folder, filename), "wb") as f:
            f.write(image_file.read())
        return filename
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None


# Function to save data to JSON file (modify file path)
def save_data(data, data_file):
    try:
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")


def app():

    # Data file paths (modify as needed)
    data_file = "/Users/arthjani/Desktop/CP4-FaceRec/Final_FaceRecognition_AttendanceSystem/data/data.json"
    image_folder = "/Users/arthjani/Desktop/CP4-FaceRec/Final_FaceRecognition_AttendanceSystem/data/images"

    # Load existing data (handle potential errors)
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Create empty list if file doesn't exist or has invalid format

    # Streamlit app layout
    # st.title("Data Collection App")

    # User input fields
    id = st.text_input("Enrollment Number:", key="id")
    name = st.text_input("Name:", key="name")
    class_ = st.text_input("Class (e.g., IPL):", key="class")
    year = st.text_input("Year:", key="year")
    image_file = st.file_uploader("Upload Image (JPG, PNG):", type=["jpg", "png"], key="image")
    last_attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Submit button
    submitted = st.button("Submit Data")

    # Process data on submit
    if submitted:
        if id and name and class_ and year and image_file:
            # Check for duplicate ID
            duplicate_found = False
            for entry in data:
                if id in entry:
                    duplicate_found = True
                    break

            if not duplicate_found:
                # Save uploaded image (handle errors)
                image_filename = save_image(image_file, id, image_folder)
                if image_filename:
                    data_entry = {id: {
                        "name": name,
                        "class": class_,
                        "total_attendance": 0,
                        "year": year,
                        "last_attendance_time": last_attendance_time,
                        "image": image_filename
                    }}
                    data.append(data_entry)
                    save_data(data, data_file)  # Save updated data
                    st.success("Data saved successfully!")
                    json_file_path = "data/data.json"
                    set_student_data_from_json(json_file_path)
                    update_known_faces()
                    # load_and_upload_student_images(FOLDER_PATH)
                else:
                    st.error("Error saving image. Please try again.")
            else:
                st.error("Enrollment number already exists. Please use a unique ID.")
        else:
            st.error("Please fill in all required fields and upload a valid image.")
