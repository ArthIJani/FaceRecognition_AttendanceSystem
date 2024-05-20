import streamlit as st


def apply_local_css(file_name):
    """
    Applies custom CSS styling to the Streamlit app (for older Streamlit versions).

    Args:
        file_name (str): Path to the CSS file containing styling rules.
    """
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Example usage (assuming style.css is in the same directory)
apply_local_css("style/style.css")
