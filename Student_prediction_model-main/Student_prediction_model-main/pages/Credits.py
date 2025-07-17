# pages/About_Our_Team.py

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About Our Team",
    page_icon="👥",
    layout="wide"
)

st.title("Meet Our Development Team")
st.markdown("---")

# Return to home button
if st.button("🏠 Return to Home"):
    st.switch_page("Home.py")

st.write("""
## About This Project
The Student Performance Prediction System is a Streamlit-based web application designed to help 
teachers track student performance and predict academic outcomes. The system uses machine learning 
techniques to analyze various factors that influence student success.
""")

# Team member data
team_members = [
    {
        "name": "Saugat Odari",
        "role": "Team Leader",
        "image": "data/Sau.jpg",
        "linkedin": "https://www.linkedin.com/in/saugatodari/",
    },
    {
        "name": "Priyanshu Sarkar",
        "role": "Streamlit Designer",
        "image": "data/Pri.jpg",
        "linkedin": "https://www.linkedin.com/in/priyanshu-sarkar-04b3a4348?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
    },
    {
        "name": "Ankita Roy",
        "role": "Data Science",
        "image": "data/Ankita.jpg",
        "linkedin": "https://www.linkedin.com/in/ankita-roy-03a61b309?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
    },
    {
        "name": "Sujoy Kumar Saha",
        "role": "Software Developer",
        "image": "data/Sujoy.jpg",
        "linkedin": "https://www.linkedin.com/in/sujoy-saha-7a33a7348?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
    }
]

# Display team members in a grid
st.markdown("## Our Team")
st.markdown("---")

# Create two rows with two team members each
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# First row
with row1_col1:
    st.subheader(team_members[0]["name"])
    st.image(team_members[0]["image"], width=150)
    st.write(f"*Role:* {team_members[0]['role']}")
    st.markdown(f"[LinkedIn]({team_members[0]['linkedin']})")

with row1_col2:
    st.subheader(team_members[1]["name"])
    st.image(team_members[1]["image"], width=150)
    st.write(f"*Role:* {team_members[1]['role']}")
    st.markdown(f"[LinkedIn]({team_members[1]['linkedin']})")

# Second row
with row2_col1:
    st.subheader(team_members[2]["name"])
    st.image(team_members[2]["image"], width=150)
    st.write(f"*Role:* {team_members[2]['role']}")
    st.markdown(f"[LinkedIn]({team_members[2]['linkedin']})")

with row2_col2:
    st.subheader(team_members[3]["name"])
    st.image(team_members[3]["image"], width=150)
    st.write(f"*Role:* {team_members[3]['role']}")
    st.markdown(f"[LinkedIn]({team_members[3]['linkedin']})")

# Contact section
st.markdown("---")
st.header("Get in Touch")
st.write("""
Have questions or feedback about our application? 
Feel free to reach out to any of our team members through LinkedIn.
""")

# Footer
st.markdown("---")
st.caption("© 2025 The Data Consortium")