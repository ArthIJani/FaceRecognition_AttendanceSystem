# import streamlit as st
# import pyrebase
#
# firebaseConfig = {
#     'apiKey': "AIzaSyDVUusGLqXzeIqbko4O17zkiLVmCbmU9pc",
#     'authDomain': "faceattendanceauth.firebaseapp.com",
#     'projectId': "faceattendanceauth",
#     'storageBucket': "faceattendanceauth.appspot.com",
#     'messagingSenderId': "267254041884",
#     'appId': "1:267254041884:web:03ded6d99cb00abc78fed9",
#     'measurementId': "G-M3CQD37X4E",
#     'databaseURL': "https://faceattendanceauth-default-rtdb.asia-southeast1.firebasedatabase.app/"
# }
#
# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()
#
#
# def login():
#     """Performs user login and displays a success/error message."""
#     email = st.text_input("Enter email:", key="email_input")
#     password = st.text_input("Enter password:", type="password", key="password_input")
#
#     if st.button("Login"):
#         try:
#             login = auth.sign_in_with_email_and_password(email, password)
#             st.success("Successfully logged in!", class_="text-green-500")
#         except Exception as e:
#             st.error(f"Invalid email or password: {e}", class_="text-red-500")
#
#
# def signup():
#     """Performs user signup and prompts for login."""
#     email = st.text_input("Enter email:", key="signup_email_input")
#     password = st.text_input("Enter password:", type="password", key="signup_password_input")
#
#     if st.button("Sign Up"):
#         try:
#             user = auth.create_user_with_email_and_password(email, password)
#             st.success("Account created successfully!", class_="text-green-500")
#
#             ask = st.selectbox("Do you want to login now?", ("Yes", "No"))
#             if ask == "Yes":
#                 login()
#         except Exception as e:
#             st.error(f"Email already exists or other error: {e}", class_="text-red-500")
#
#
# def main():
#     """Displays the main interface for user selection (login or signup)."""
#     st.set_page_config(page_title="Firebase Auth", page_icon=":lock:")  # Set page title and icon
#
#     # Container for logo (replace 'logo.png' with your image path)
#     logo_container = st.container()
#     with logo_container:
#         st.image('login.png', width=200)  # Use st.image for the logo (no class_)
#         logo_text = st.empty()  # Empty container for text with class
#
#         logo_text.markdown(f"""<p class="text-center">Your App Name</p>""",
#                            unsafe_allow_html=True)  # Text with Tailwind CSS class
#
#     # Container for login/signup choice
#     choice_container = st.container()
#     with choice_container:
#         st.title("Firebase Authentication with Streamlit")
#         choice = st.selectbox("New User?", ("No (Login)", "Yes (Signup)"), class_="text-xl font-bold mb-4")
#
#     # Login/Signup based on user choice
#     if choice == "No (Login)":
#         login()
#
