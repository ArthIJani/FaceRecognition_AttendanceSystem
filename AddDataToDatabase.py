import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import firebase_init
_initialized = False


def set_student_data_from_json(json_file_path):
    global _initialized

    # Read data from JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Initialize Firebase app only if not already done
    if not _initialized:
        firebase_init.initialize_app()
        _initialized = True

    # Get a reference to the Students node
    ref = db.reference('Students')

    # Iterate through all student data in the list
    for student_entry in data:
        # Handle potential non-dictionary entries (e.g., empty list)
        if not isinstance(student_entry, dict):
            continue

        for student_id, student_details in student_entry.items():
            ref.child(student_id).set(student_details)


# # Example usage
# json_file_path = "data/data.json"
# set_student_data_from_json(json_file_path)
