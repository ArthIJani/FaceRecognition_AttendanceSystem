from streamlit_option_menu import option_menu


def create_navigation_bar():
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
    return selected

# selected_page = create_navigation_bar()
