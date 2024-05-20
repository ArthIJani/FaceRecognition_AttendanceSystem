# import face_recognition
# import os
# import pickle
#
# # Path to the folder containing known face images
# known_faces_dir = "images"
#
# known_faces = []
# known_names = []
#
# # Loop through each image in the known_faces folder
# for filename in os.listdir(known_faces_dir):
#     image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
#     # Convert image to RGB format (required by face_recognition)
#     image_rgb = image[:, :, ::-1]
#
#     # Get face encoding for the current image
#     face_encoding = face_recognition.face_encodings(image_rgb)[0]
#
#     # Extract name from filename (assuming filename format: name.jpg)
#     known_names.append(os.path.splitext(filename)[0])
#     known_faces.append(face_encoding)

# Save encoded faces and names to a pickle file
# with open("known_faces.pkl", "wb") as f:
#     pickle.dump((known_faces, known_names), f)
#
# print("Encoding complete and saved to known_faces.pkl!")

import face_recognition
import os
import pickle

# Path to the folder containing known face images
known_faces_dir = "../data/images"

known_faces = []
known_names = []

# Loop through each image in the known_faces folder
for filename in os.listdir(known_faces_dir):
    name, extension = os.path.splitext(filename)  # Separate name and extension
    # Split name and number (assuming format: name_number)
    if "_" in name:
        person_name, _ = name.split("_")
    else:
        # Handle filenames without numbers (e.g., just a name.jpg)
        person_name = name

    image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
    # Convert image to RGB format (required by face_recognition)
    image_rgb = image[:, :, ::-1]

    # Get face encoding for the current image
    face_encoding = face_recognition.face_encodings(image_rgb)[0]

    # Append encoding and name considering multiple images per person
    known_names.append(person_name)
    known_faces.append(face_encoding)

# Save encoded faces and names to a pickle file
try:
    with open("../data/known_faces.pkl", "wb") as f:
        pickle.dump((known_faces, known_names), f)
    print("Encoding complete and saved to known_faces.pkl!")
except Exception as e:
    print(f"Error saving known faces file: {e}")

