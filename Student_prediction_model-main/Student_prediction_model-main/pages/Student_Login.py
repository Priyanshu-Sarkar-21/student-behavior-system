# pages/Student_Login.py

import streamlit as st

st.set_page_config(
    page_title="Student Login",
    page_icon="👨‍🎓",
    layout="wide"
)

st.title("Student Login")

with st.form("student_login_form"):
    student_id = st.text_input("Student ID")
    password = st.text_input("Password", type="password")
    school_code = st.text_input("School Code")
    login_button = st.form_submit_button("Login")
    
    if login_button:
        if student_id and password and school_code:
            # Simple validation for prototype with a set password
            if student_id.isdigit() and password == "student123" and school_code == "DEMO2023":
                st.success("Login successful!")
                st.session_state.student_id = student_id
                st.session_state.student_name = "John Doe"  # Placeholder name
                # Since we can't use st.button() here, we'll navigate directly
                st.switch_page("pages/Student_Input.py")
            else:
                st.error("Invalid credentials. Please check your ID, password, and school code.")
        else:
            st.error("Please enter Student ID, Password, and School Code.")

# Display demo credentials
with st.expander("Demo Credentials (For Testing)"):
    st.code("""
    Student ID: 12345
    Password: student123
    School Code: DEMO2023
    """)

# Navigation buttons outside the form
if "student_id" in st.session_state and "student_name" in st.session_state:
    if st.button("Go to Student Input"):
        st.switch_page("pages/Student_Input.py")

if st.button("Return to Home"):
    st.switch_page("Home.py")