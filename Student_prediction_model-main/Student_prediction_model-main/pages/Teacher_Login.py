# pages/Teacher_Login.py

import streamlit as st

st.set_page_config(
    page_title="Teacher Login",
    page_icon="👨‍🏫",
    layout="wide"
)

st.title("Teacher Login")

with st.form("teacher_login_form"):
    teacher_id = st.text_input("Teacher ID")
    password = st.text_input("Password", type="password")
    school_code = st.text_input("School Code")
    login_button = st.form_submit_button("Login")
    
    if login_button:
        if teacher_id and password and school_code:
            # Simple validation for prototype
            if teacher_id.startswith('T') and len(password) >= 6 and school_code == "DEMO2023":
                st.success("Login successful!")
                st.session_state.teacher_id = teacher_id
                st.session_state.is_admin = teacher_id in ["T001", "T002", "T003"]  # Example admin users
                # Navigate to teacher dashboard upon successful login
                st.switch_page("pages/Teacher_Input.py")
            else:
                st.error("Invalid credentials. Please check your ID, password, and school code.")
        else:
            st.error("Please enter Teacher ID, Password, and School Code.")

# Display demo credentials
with st.expander("Demo Credentials (For Testing)"):
    st.code("""
    Teacher ID: T12345
    Password: teacher123
    School Code: DEMO2023
    """)

# Navigation buttons outside the form
if "teacher_id" in st.session_state:
    if st.button("Go to Teacher Dashboard"):
        st.switch_page("pages/Teacher_Input.py")

if st.button("Return to Home"):
    st.switch_page("Home.py")