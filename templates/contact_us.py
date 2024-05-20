import streamlit as st


def display_contact_us():
    """
  Displays a contact form for users to reach out.
  """
    st.header(":mailbox: Get In Touch With Me!")
    contact_form = """
      <form action="https://formsubmit.co/your_email@example.com" method="POST">
           <input type="hidden" name="_captcha" value="false">
           <input type="text" name="name" placeholder="Your name" required>
           <input type="email" name="email" placeholder="Your email" required>
           <textarea name="message" placeholder="Your message here"></textarea>
           <button type="submit">Send</button>
      </form>
      """
    st.markdown(contact_form, unsafe_allow_html=True)


