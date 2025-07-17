import streamlit as st
import os
from custom_nav import main as custom_nav_main

# Configure the page
st.set_page_config(
    page_title="Student Prediction System",
    page_icon="📚",
    layout="centered"
)

# Hide the default sidebar and the navigation icon
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        display: none;
    }
    div[data-testid="stDecoration"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display logo if available
if os.path.exists("data/logo.png"):
    st.image("data/logo.png", width=200, use_container_width=False)
    
# Main title
st.title("Student Prediction System")

# App description
st.write("This application predicts student performance and behavior. Choose your role to start:")

# Role selection section
col1, col2 = st.columns(2)

with col1:
    if st.button("Student Login"):
        st.switch_page("pages/Student_Login.py")

with col2:
    if st.button("Teacher Login"):
        st.switch_page("pages/Teacher_Login.py")

# Footer
st.markdown("---")
st.caption("© 2025 The Data Consortium")

# Run custom navigation
custom_nav_main()