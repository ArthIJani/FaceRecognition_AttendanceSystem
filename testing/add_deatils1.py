import firebase_admin
import streamlit as st
import pyrebase

# # Replace with your Firebase configuration
# cred = firebase_admin.credentials.Certificate('serviceAccountKey.json')
# firebaseConfig = firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://facerecattenedancesystemfinal-default-rtdb.asia-southeast1.firebasedatabase.app/',
#     'storageBucket': 'facerecattenedancesystemfinal.appspot.com'
# })
#
# # Initialize Firebase app
# firebase = pyrebase.initialize_app(firebaseConfig)
# db = firebase.database()
# storage = firebase.storage()


# Function to upload image to Firebase Storage
def upload_image(image_file):
    storage_ref = storage.reference(child=f"images/{image_file.name}")
    storage_ref.put(image_file)
    return storage_ref.get_download_url()


def register_student():
    name = st.text_input("Name")
    enrollment_no = st.text_input("Enrollment No.")
    class_selection = st.selectbox("Class", ["Select Class", "Class 1", "Class 2", "..."])  # Add more options

    uploaded_image = st.file_uploader("Upload Image (Optional)", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        try:
            image_url = upload_image(uploaded_image)
        except Exception as e:
            st.error(f"Error uploading image: {e}")
            image_url = None  # Set to None to prevent errors in storing data
    else:
        image_url = None  # No image uploaded

    if name and enrollment_no and class_selection != "Select Class":
        data = {
            "name": name,
            "enrollment_no": enrollment_no,
            "class": class_selection,
            "image_url": image_url if image_url else "",  # Include image URL if uploaded
        }
        try:
            # Add a unique identifier (e.g., timestamp) to prevent overwriting
            new_student_ref = db.reference('students').push(data)
            st.success(f"Student {name} registered successfully! (ID: {new_student_ref.key})")
        except Exception as e:
            st.error(f"Error storing data: {e}")
    else:
        st.error("Please fill in all required fields!")


st.title("Student Registration App")
register_student()
