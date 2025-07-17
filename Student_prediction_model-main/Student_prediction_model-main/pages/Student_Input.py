# pages/Student_Input.py

import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression

# Page configuration
st.set_page_config(
    page_title="Student Input",
    page_icon="👨‍🎓",
    layout="wide"
)

# Check if user is logged in
if "student_id" not in st.session_state or "student_name" not in st.session_state:
    st.warning("You need to log in first!")
    if st.button("Go to Login Page"):
        st.switch_page("pages/Student_Login.py")
else:
    # User is logged in, show the student input form
    st.title(f"Welcome, {st.session_state.student_name}")
    st.subheader("Enter your information to get a prediction")
    
    # Try to pre-fill some data based on student ID
    student_data = None
    if os.path.exists("data/sample_student_data.csv"):
        try:
            df = pd.read_csv("data/sample_student_data.csv")
            student_record = df[df['student_id'].astype(str) == st.session_state.student_id]
            if not student_record.empty:
                student_data = student_record.iloc[0]
        except Exception as e:
            st.error(f"Error reading sample data: {e}")
    
    # Create a simple form for student inputs
    with st.form("student_form"):
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.student_name)
            age = st.number_input("Age", min_value=14, max_value=26, value=student_data['age'] if student_data is not None else 18)
            gender = st.selectbox("Gender", options=["Male", "Female", "Other"], 
                               index=0 if student_data is None else (0 if student_data['gender'] == 'M' else 1 if student_data['gender'] == 'F' else 2))
        
        with col2:
            attendance = st.slider("Attendance Percentage", min_value=0, max_value=100, 
                                value=student_data['attendance'] if student_data is not None else 85)
            study_hours = st.slider("Daily Study Hours (outside class)", min_value=0.0, max_value=6.0, value=student_data['study_hours'] if student_data is not None else 2.0, step=0.5)
            prev_gpa = st.slider("Previous GPA", min_value=0.0, max_value=4.0, value=student_data['previous_gpa'] if student_data is not None else 3.0, step=0.1)
        
        # Additional factors
        st.subheader("Additional Factors")
        
        col3, col4 = st.columns(2)
        
        part_options = ["Low", "Medium", "High"]
        hw_options = ["Low", "Medium", "High"]
        behav_options = ["Poor", "Average", "Good", "Excellent"]
        extra_options = ["None", "Limited", "Moderate", "Extensive"]
        stress_options = ["Very Low", "Low", "Medium", "High", "Very High"]
        
        with col3:
            participation = st.selectbox("Class Participation", options=part_options,
                                      index=part_options.index(student_data['class_participation']) if student_data is not None and 'class_participation' in student_data else 1)
            homework = st.selectbox("Homework Completion", options=hw_options,
                                 index=hw_options.index(student_data['homework_completion']) if student_data is not None and 'homework_completion' in student_data else 1)
            sleep_hours = st.slider("Average Sleep Hours per Night", min_value=4, max_value=12, 
                                  value=student_data['sleep_hours'] if student_data is not None and 'sleep_hours' in student_data else 7, step=1)
            
        with col4:
            behavior = st.selectbox("Behavior in Class", options=behav_options,
                                 index=behav_options.index(student_data['behavior_score']) if student_data is not None and 'behavior_score' in student_data else 1)
            extracurricular = st.selectbox("Extracurricular Activities", options=extra_options,
                                        index=extra_options.index(student_data['extracurricular']) if student_data is not None and 'extracurricular' in student_data else 1)
            stress_level = st.select_slider("Stress Level", options=stress_options,
                                         value=student_data['stress_level'] if student_data is not None and 'stress_level' in student_data else "Medium")
        
        submitted = st.form_submit_button("Predict My Performance")
    
    # Process the form and make predictions when submitted
    if submitted:
        # Create a dict of student data
        student_data = {
            "name": name,
            "age": age,
            "gender": "M" if gender == "Male" else "F" if gender == "Female" else "O",
            "attendance": attendance,
            "study_hours": study_hours,
            "previous_gpa": prev_gpa,
            "class_participation": participation,
            "homework_completion": homework,
            "behavior_score": behavior,
            "sleep_hours": sleep_hours,
            "extracurricular": extracurricular,
            "stress_level": stress_level
        }
        
        # Convert categorical variables to numeric
        participation_map = {"Low": 1, "Medium": 2, "High": 3}
        homework_map = {"Low": 1, "Medium": 2, "High": 3}
        behavior_map = {"Poor": 1, "Average": 2, "Good": 3, "Excellent": 4}
        extracurricular_map = {"None": 0, "Limited": 1, "Moderate": 2, "Extensive": 3}
        stress_map = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
        
        # Calculate normalized scores (0-1 scale) for each factor
        attendance_norm = attendance / 100
        study_norm = study_hours / 6
        part_norm = participation_map.get(participation, 2) / 3
        homework_norm = homework_map.get(homework, 2) / 3
        behavior_norm = behavior_map.get(behavior, 2) / 4
        extracurricular_norm = extracurricular_map.get(extracurricular, 0) / 3
        
        # Sleep hours has an optimal range (7-9 hours), convert to 0-1 scale
        if 7 <= sleep_hours <= 9:
            sleep_norm = 1.0
        else:
            sleep_norm = 1.0 - min(abs(sleep_hours - 8), 4) / 4
        
        # Stress has negative impact, invert the scale (higher stress = lower score)
        stress_norm = 1.0 - (stress_map.get(stress_level, 3) - 1) / 4
        
        # Advanced weighted model for GPA prediction
        # Different weight combinations based on previous GPA range
        if prev_gpa >= 3.5:
            # High achievers - attendance and homework completion are most critical
            predicted_gpa = min(4.0, (
                prev_gpa * 0.45 +
                attendance_norm * 0.15 +
                study_norm * 0.10 +
                part_norm * 0.05 +
                homework_norm * 0.10 +
                behavior_norm * 0.05 +
                sleep_norm * 0.05 + 
                extracurricular_norm * 0.02 +
                stress_norm * 0.03
            ))
        elif prev_gpa >= 2.5:
            # Average students - study hours and participation become more important
            predicted_gpa = min(4.0, (
                prev_gpa * 0.40 +
                attendance_norm * 0.15 +
                study_norm * 0.15 +
                part_norm * 0.10 +
                homework_norm * 0.10 +
                behavior_norm * 0.02 +
                sleep_norm * 0.03 + 
                extracurricular_norm * 0.02 +
                stress_norm * 0.03
            ))
        else:
            # Struggling students - study hours and attendance are critical
            predicted_gpa = min(4.0, (
                prev_gpa * 0.30 +
                attendance_norm * 0.20 +
                study_norm * 0.20 +
                part_norm * 0.10 +
                homework_norm * 0.10 +
                behavior_norm * 0.02 +
                sleep_norm * 0.03 + 
                extracurricular_norm * 0.02 +
                stress_norm * 0.03
            ))
        
        # Adjust prediction based on age - older students tend to be more consistent
        age_adjustment = min(0.1, (age - 14) * 0.01)
        predicted_gpa = min(4.0, predicted_gpa * (1 + age_adjustment))
        
        # Calculate behavior score with improved weighting and additional factors
        behavior_score = min(10, (
            behavior_norm * 4.0 +
            attendance_norm * 2.0 +
            part_norm * 1.5 +
            sleep_norm * 1.0 +
            stress_norm * 1.5
        ))
        
        # Store results for the results page
        student_data["predicted_gpa"] = predicted_gpa
        student_data["predicted_behavior"] = behavior_score
        
        # Save the results to a session state for access in the results page
        st.session_state.student_prediction = student_data
        
        # Navigate to results page
        st.success("Prediction completed! View your results.")
        if st.button("View My Results"):
            st.switch_page("pages/Student_Results.py")
    
    # Add a logout button
    if st.button("Log Out"):
        # Clear session state
        if "student_id" in st.session_state:
            del st.session_state.student_id
        if "student_name" in st.session_state:
            del st.session_state.student_name
        st.switch_page("Home.py")