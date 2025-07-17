import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Student Results",
    page_icon="📊",
    layout="wide"
)

st.title("Your Prediction Results")

# Check if prediction exists in session state
if "student_prediction" not in st.session_state:
    st.warning("No prediction data found. Please complete the student input form first.")
    if st.button("Go to Student Input"):
        st.switch_page("pages/Student_Input.py")
else:
    # Get the prediction data
    data = st.session_state.student_prediction
    
    # Display student info
    st.subheader("Student Information")
    st.write(f"**Name:** {data['name']}")
    st.write(f"**Age:** {data['age']}")
    
    # Display prediction results
    st.subheader("Prediction Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # GPA Prediction
        st.metric(
            label="Predicted GPA", 
            value=f"{data['predicted_gpa']:.2f}", 
            delta=f"{data['predicted_gpa'] - data['previous_gpa']:.2f}"
        )
        
        # Create a gauge chart for GPA
        fig1, ax1 = plt.subplots(figsize=(4, 0.3))
        gpa_range = np.linspace(0, 4, 100)
        ax1.barh(0, 4, color='lightgray', height=0.2)
        ax1.barh(0, data['predicted_gpa'], color='blue', height=0.2)
        ax1.set_xlim(0, 4)
        ax1.set_yticks([])
        ax1.set_xticks([0, 1, 2, 3, 4])
        ax1.set_xticklabels(['0', '1', '2', '3', '4'])
        ax1.set_title('GPA Scale')
        st.pyplot(fig1)
        
        # Recommendations based on GPA
        st.subheader("Academic Recommendations")
        if data['predicted_gpa'] < 2.0:
            st.error("Your predicted GPA is concerning. Consider these immediate actions:")
            st.write("- Establish a regular study schedule")
            st.write("- Meet with a tutor or teacher for extra help")
            st.write("- Reduce distractions during study time")
        elif data['predicted_gpa'] < 3.0:
            st.warning("Your predicted GPA could be improved with:")
            st.write("- Increase daily study hours")
            st.write("- Participate more actively in class")
            st.write("- Complete all homework assignments")
        else:
            st.success("Great job! To maintain your strong performance:")
            st.write("- Continue your current study habits")
            st.write("- Consider challenging yourself with advanced materials")
            st.write("- Help peers who may be struggling")
    
    with col2:
        # Behavior Prediction
        st.metric(
            label="Behavior Score", 
            value=f"{data['predicted_behavior']:.1f}/10"
        )
        
        # Create a gauge chart for behavior
        fig2, ax2 = plt.subplots(figsize=(4, 0.3))
        behavior_range = np.linspace(0, 10, 100)
        ax2.barh(0, 10, color='lightgray', height=0.2)
        ax2.barh(0, data['predicted_behavior'], color='green', height=0.2)
        ax2.set_xlim(0, 10)
        ax2.set_yticks([])
        ax2.set_xticks([0, 2, 4, 6, 8, 10])
        ax2.set_title('Behavior Scale')
        st.pyplot(fig2)
        
        # Behavior recommendations
        st.subheader("Behavior Recommendations")
        if data['predicted_behavior'] < 5:
            st.error("Your behavior score needs improvement:")
            st.write("- Work on better classroom etiquette")
            st.write("- Improve attendance and punctuality")
            st.write("- Show more respect to teachers and peers")
        elif data['predicted_behavior'] < 7.5:
            st.warning("Consider these behavior improvements:")
            st.write("- Participate more actively in discussions")
            st.write("- Turn in assignments on time")
            st.write("- Be more helpful to classmates")
        else:
            st.success("Excellent behavior! Keep up the good work:")
            st.write("- Continue being a positive role model")
            st.write("- Consider mentoring other students")
            st.write("- Your positive attitude contributes to a better learning environment")
    
    # Factors that influenced the prediction
    st.subheader("Key Factors Influencing Your Prediction")
    
    # Create a bar chart of factors
    factors = ['Previous GPA', 'Attendance', 'Study Hours', 'Participation', 'Homework', 'Behavior']
    
    # Normalize values to 0-1 scale for comparison
    factor_values = [
        data['previous_gpa'] / 4,
        data['attendance'] / 100,
        data['study_hours'] / 6,
        {"Low": 0.33, "Medium": 0.66, "High": 1}[data['class_participation']],
        {"Low": 0.33, "Medium": 0.66, "High": 1}[data['homework_completion']],
        {"Poor": 0.25, "Average": 0.5, "Good": 0.75, "Excellent": 1}[data['behavior_score']]
    ]
    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    bars = ax3.bar(factors, factor_values, color=['blue', 'green', 'orange', 'red', 'purple', 'brown'])
    ax3.set_ylim(0, 1)
    ax3.set_ylabel('Normalized Score')
    ax3.set_title('Your Performance Factors')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{height:.2f}', ha='center', va='bottom')
    
    st.pyplot(fig3)
    
    # Navigation buttons
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("Return to Student Input"):
            st.switch_page("pages/Student_Input.py")
    
    with col4:
        if st.button("Return to Home"):
            st.switch_page("Home.py") 

# Footer
st.markdown("---")
st.caption("© 2025 The Data Consortium") 