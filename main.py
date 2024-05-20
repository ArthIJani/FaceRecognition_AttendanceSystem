import streamlit as st

st.set_page_config(
    page_title="Attendance System",
    page_icon=":student:",
    layout="wide"
)

# Import modules for navigation and content display
from templates.home_page import display_home_page
from templates.add_details import app
from templates.navigation import create_navigation_bar
from templates.webcam_attendance import display_webcam_attendance
from templates.contact_us import display_contact_us
from style.style import apply_local_css

# Navigation bar
selected_page = create_navigation_bar()

try:
    if selected_page == "Home":
        display_home_page()
    elif selected_page == "Add Details":
        app()
    elif selected_page == "Attendance System":
        display_webcam_attendance()
    elif selected_page == "Contact Us":
        display_contact_us()
    else:
        st.error(f"Invalid page selection: {selected_page}")
except Exception as e:
    # Handle errors during content display
    st.error(f"An error occurred: {e}")


# Apply local CSS for styling (optional)
apply_local_css("style/style.css")
