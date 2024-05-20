import os
import json
import pickle

import cv2
import face_recognition


folderPath = 'data/images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    # print(os.path.splitext(path)[0])
    fileName = f'{folderPath}/{path}'

print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


def save_student_data(name, enrollment_no, class_name, year, image):
    # Prepare student data dictionary with desired format
    student_data = {
        enrollment_no: {
            "name": name,
            "class": class_name,
            "total_attendance": 0,
            "year": year,  # Include the year in the dictionary
            "last_attendance_time": None,  # Initialize last attendance time
            "image": f"{enrollment_no}.jpg",  # Use enrollment number for image filename
        }
    }

    # Load existing data or create an empty dictionary if file doesn't exist
    if os.path.exists("data/data.json"):
        with open("data/data.json", "r") as file:
            data = json.load(file)
    else:
        data = {}

    # Check for duplicate enrollment number
    if enrollment_no in data:
        return False  # Handle duplicate error elsewhere

    # Save image to 'images' folder with enrollment number as filename
    if not os.path.exists("data/Images"):
        os.makedirs("data/Images")
    image_path = os.path.join("data/Images", f"{enrollment_no}.jpg")
    with open(image_path, "wb") as img_file:
        img_file.write(image.getvalue())

    # Update the data dictionary with the new student information
    data.update(student_data)

    # Save updated data back to the JSON file
    with open("data/data.json", "w") as file:
        json.dump(data, file, indent=4)

    # Add data to Firebase (assuming appropriate setup using firebase_admin)
    # db.reference(f"students/{enrollment_no}").set(student_data[enrollment_no])
    return True  # Indicate successful save


def update_known_faces():
    print("Encoding Started...")
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Complete")

    file = open("data/EncodeFile.p", "wb")
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File Saved")


update_known_faces()
