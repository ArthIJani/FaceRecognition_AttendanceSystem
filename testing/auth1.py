# import pyrebase
#
# firebaseConfig = {
#     'apiKey': "AIzaSyDVUusGLqXzeIqbko4O17zkiLVmCbmU9pc",
#     'authDomain': "faceattendanceauth.firebaseapp.com",
#     'projectId': "faceattendanceauth",
#     'storageBucket': "faceattendanceauth.appspot.com",
#     'messagingSenderId': "267254041884",
#     'appId': "1:267254041884:web:03ded6d99cb00abc78fed9",
#     'measurementId': "G-M3CQD37X4E"
# }
#
# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()
#
#
# # Login function
# def login():
#     print("Log in...")
#     email = input("Enter email: ")
#     password = input("Enter password: ")
#     try:
#         login = auth.sign_in_with_email_and_password(email, password)
#         print("Successfully logged in!")
#         # print(auth.get_account_info(login['idToken']))
#     # email = auth.get_account_info(login['idToken'])['users'][0]['email']
#     # print(email)
#     except:
#         print("Invalid email or password")
#     return
#
#
# # Signup Function
#
# def signup():
#     print("Sign up...")
#     email = input("Enter email: ")
#     password = input("Enter password: ")
#     try:
#         user = auth.create_user_with_email_and_password(email, password)
#         ask = input("Do you want to login?[y/n]")
#         if ask == 'y':
#             login()
#     except:
#         print("Email already exists")
#     return
#
#
# # Main
#
# ans = input("Are you a new user?[y/n]")
#
# if ans == 'n':
#     login()
# elif ans == 'y':
#     signup()
