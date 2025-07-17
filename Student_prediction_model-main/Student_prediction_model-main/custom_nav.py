# custom_nav.py

import streamlit as st

def main():
    # Define your pages manually or detect from /pages folder
    pages = {
        "Home": "Home.py",
        "Student Input": "pages/Student_Input.py",
        "Student Results": "pages/Student_Results.py",
        "Teacher Input": "pages/Teacher_Input.py",
        "Teacher Results": "pages/Teacher_Results.py",
        "About Our Team": "pages/About_Our_Team.py"
    }

    # Since the sidebar is hidden in Home.py, we'll use a different approach for navigation
    # You might want to consider a different UI element if you want to keep navigation visible
    with st.sidebar:
        st.title("Navigation")
        choice = st.radio("Go to", list(pages.keys()))

    # Set query parameters using the modern API
    st.query_params.update({"page": choice})

    # Navigate to selected page
    st.switch_page(pages[choice])

if __name__ == "__main__":
    main()