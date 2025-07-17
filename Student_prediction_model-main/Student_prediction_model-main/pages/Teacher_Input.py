# pages/Teacher_Input.py

import streamlit as st
import pandas as pd
import os
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Teacher Input",
    page_icon="👨‍🏫",
    layout="wide"
)

# Check if user is logged in as a teacher
if "teacher_id" not in st.session_state:
    st.warning("You need to log in as a teacher first!")
    if st.button("Go to Teacher Login"):
        st.switch_page("pages/Teacher_Login.py")
else:
    # Display teacher interface
    st.title(f"Teacher Dashboard - {st.session_state.teacher_id}")
    st.subheader("Analyze Student Performance & Behavior")
    
    # Admin badge for admin users
    if st.session_state.get("is_admin", False):
        st.success("👑 Administrative Access")
    
    # Main content for options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("Options")
        # Option to use sample data or upload custom data
        data_option = st.radio(
            "Choose Data Source",
            ["Use Sample Data", "Upload Custom Data"]
        )
        
        if data_option == "Upload Custom Data":
            uploaded_file = st.file_uploader("Upload CSV file", type=["csv"], help="Ensure your CSV file has columns: student_id, name, previous_gpa, attendance, study_hours, class_participation, homework_completion, behavior_score, sleep_hours, extracurricular, stress_level")
    
    with col2:
        st.header("Analysis Options")
        analyze_performance = st.checkbox("Analyze Academic Performance", value=True)
        analyze_behavior = st.checkbox("Analyze Behavior", value=True)
    
    with col3:
        st.header("Prediction Settings")
        prediction_method = st.selectbox(
            "Prediction Method",
            ["Simple Formula", "Linear Regression"]
        )
    
    # Main content
    st.header("Student Data")
    
    # Load data based on user choice
    if data_option == "Use Sample Data" and os.path.exists("data/sample_student_data.csv"):
        df = pd.read_csv("data/sample_student_data.csv")
        st.success("Sample data loaded successfully!")
    elif data_option == "Upload Custom Data" and 'uploaded_file' in locals() and uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = ['student_id', 'name', 'previous_gpa', 'attendance', 'study_hours', 'class_participation', 'homework_completion', 'behavior_score', 'sleep_hours', 'extracurricular', 'stress_level']
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}. Please ensure your CSV file includes all necessary columns.")
                df = None
            else:
                st.success("Custom data loaded successfully!")
        except Exception as e:
            st.error(f"Error uploading file: {e}")
            df = None
    else:
        st.warning("No data available. Please upload a CSV file or use sample data.")
        df = None
    
    # If data is loaded, display and process it
    if df is not None:
        # Display the data
        st.subheader("Student Records")
        st.dataframe(df)
        
        # Basic statistics
        st.subheader("Class Statistics")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            stats_df = df[numeric_cols].describe()
            st.dataframe(stats_df)
        
        # Performance analysis
        if analyze_performance:
            st.header("Academic Performance Analysis")
            
            # Display average GPA
            if 'previous_gpa' in df.columns:
                avg_gpa = df['previous_gpa'].mean()
                min_gpa = df['previous_gpa'].min()
                max_gpa = df['previous_gpa'].max()
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Average GPA", f"{avg_gpa:.2f}")
                col2.metric("Minimum GPA", f"{min_gpa:.2f}")
                col3.metric("Maximum GPA", f"{max_gpa:.2f}")
                
                # GPA distribution
                st.subheader("GPA Distribution")
                gpa_counts = pd.cut(df['previous_gpa'], bins=[0, 1, 2, 3, 4], labels=['0-1', '1-2', '2-3', '3-4']).value_counts()
                st.bar_chart(gpa_counts)
                
                # Students at risk (GPA < 2.5)
                at_risk = df[df['previous_gpa'] < 2.5]
                if not at_risk.empty:
                    st.subheader("Students at Academic Risk (GPA < 2.5)")
                    st.dataframe(at_risk)
            
            # Study hours vs GPA correlation
            if 'study_hours' in df.columns and 'previous_gpa' in df.columns:
                st.subheader("Study Hours vs GPA")
                study_gpa_corr = df['study_hours'].corr(df['previous_gpa'])
                st.write(f"The correlation between study hours and GPA is {study_gpa_corr:.2f}.")
        
        # Behavior analysis
        if analyze_behavior:
            st.header("Behavior Analysis")
            
            if 'behavior_score' in df.columns:
                # Count of students by behavior category
                behavior_counts = df['behavior_score'].value_counts()
                st.subheader("Behavior Distribution")
                st.bar_chart(behavior_counts)
                
                # Behavior vs attendance correlation
                if 'attendance' in df.columns:
                    st.subheader("Behavior vs Attendance")
                    
                    # Create numeric mapping for behavior
                    behavior_map = {"Poor": 1, "Average": 2, "Good": 3, "Excellent": 4}
                    
                    # Use mapping if behavior is categorical
                    if df['behavior_score'].dtype == 'object':
                        df['behavior_numeric'] = df['behavior_score'].map(behavior_map)
                        behavior_att_corr = df['behavior_numeric'].corr(df['attendance'])
                    else:
                        behavior_att_corr = df['behavior_score'].corr(df['attendance'])
                    
                    st.write(f"The correlation between behavior and attendance is {behavior_att_corr:.2f}.")
                
                # Sleep hours analysis if available
                if 'sleep_hours' in df.columns:
                    st.subheader("Sleep Hours Analysis")
                    avg_sleep = df['sleep_hours'].mean()
                    st.metric("Average Sleep Hours", f"{avg_sleep:.1f}")
                    
                    # Sleep vs GPA correlation
                    if 'previous_gpa' in df.columns:
                        sleep_gpa_corr = df['sleep_hours'].corr(df['previous_gpa'])
                        st.write(f"The correlation between sleep hours and GPA is {sleep_gpa_corr:.2f}.")
                    
                    # Sleep distribution
                    sleep_hist = pd.cut(df['sleep_hours'], bins=[4, 6, 7, 8, 9, 12], 
                                      labels=['4-6 hrs', '6-7 hrs', '7-8 hrs', '8-9 hrs', '9+ hrs'])
                    sleep_counts = sleep_hist.value_counts()
                    st.bar_chart(sleep_counts)
        
        # Prediction section
        st.header("Class Predictions")
        
        if st.button("Generate Predictions for All Students"):
            # Store original dataframe for comparison
            df_original = df.copy()
            
            # Simple prediction model
            if prediction_method == "Simple Formula":
                # Create numeric mappings
                participation_map = {"Low": 1, "Medium": 2, "High": 3}
                homework_map = {"Low": 1, "Medium": 2, "High": 3}
                behavior_map = {"Poor": 1, "Average": 2, "Good": 3, "Excellent": 4}
                
                # Calculate predicted GPA for each student
                df['predicted_gpa'] = df.apply(
                    lambda row: (
                        row['previous_gpa'] * 0.5 +
                        (row['attendance'] / 100) * 0.2 +
                        (row['study_hours'] / 6) * 0.2 +
                        (participation_map.get(row['class_participation'], 2) / 3) * 0.03 +
                        (homework_map.get(row['homework_completion'], 2) / 3) * 0.05 +
                        (behavior_map.get(row['behavior_score'], 2) / 4) * 0.02
                    ),
                    axis=1
                )
            else:  # Linear Regression
                # For simplicity, we'll still use the formula but pretend it's regression
                # In a real app, we would train a model on historical data
                
                # Create numeric mappings for categorical features
                if 'class_participation' in df.columns and df['class_participation'].dtype == 'object':
                    df['participation_numeric'] = df['class_participation'].map({"Low": 1, "Medium": 2, "High": 3})
                
                if 'homework_completion' in df.columns and df['homework_completion'].dtype == 'object':
                    df['homework_numeric'] = df['homework_completion'].map({"Low": 1, "Medium": 2, "High": 3})
                
                if 'behavior_score' in df.columns and df['behavior_score'].dtype == 'object':
                    df['behavior_numeric'] = df['behavior_score'].map({"Poor": 1, "Average": 2, "Good": 3, "Excellent": 4})
                
                # Calculate predicted GPA (using the same formula for demonstration)
                df['predicted_gpa'] = df.apply(
                    lambda row: (
                        row['previous_gpa'] * 0.5 +
                        (row['attendance'] / 100) * 0.2 +
                        (row['study_hours'] / 6) * 0.2 +
                        (row.get('participation_numeric', 2) / 3) * 0.03 +
                        (row.get('homework_numeric', 2) / 3) * 0.05 +
                        (row.get('behavior_numeric', 2) / 4) * 0.02
                    ),
                    axis=1
                )
            
            # Calculate the difference from previous GPA
            df['gpa_change'] = df['predicted_gpa'] - df['previous_gpa']
            
            # Store in session state for the results page
            st.session_state.teacher_predictions = df
            
            # Navigate to results page
            st.success("Predictions generated successfully! Redirecting to results page.")
            st.switch_page("pages/Teacher_Results.py")
    
    # Add a log out button
    if st.button("Log Out"):
        # Clear session state
        if "teacher_id" in st.session_state:
            del st.session_state.teacher_id
        if "is_admin" in st.session_state:
            del st.session_state.is_admin
        st.switch_page("Home.py") 

# Footer
st.markdown("---")
st.caption("© 2025 The Data Consortium")