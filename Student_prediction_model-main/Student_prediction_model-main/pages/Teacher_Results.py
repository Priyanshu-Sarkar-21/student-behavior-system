# pages/Teacher_Results.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Teacher Results",
    page_icon="📈",
    layout="wide"
)

st.title("Prediction Results Dashboard")

# Check if prediction exists in session state
if "teacher_predictions" not in st.session_state:
    st.warning("No prediction data found. Please generate predictions first.")
    if st.button("Go to Teacher Input"):
        st.switch_page("pages/Teacher_Input.py")
else:
    # Get the prediction data
    df = st.session_state.teacher_predictions
    
    # Overview section
    st.header("Class Overview")
    st.write("Here's a summary of the class performance predictions:")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_pred_gpa = df['predicted_gpa'].mean()
        st.metric("Average Predicted GPA", f"{avg_pred_gpa:.2f}")
    
    with col2:
        avg_change = df['gpa_change'].mean()
        st.metric("Average GPA Change", f"{avg_change:.2f}", delta=f"{avg_change:.2f}")
    
    with col3:
        improved = len(df[df['gpa_change'] > 0])
        total = len(df)
        st.metric("Students Expected to Improve", f"{improved} ({improved/total*100:.1f}%)")
    
    # GPA Distribution chart
    st.subheader("Predicted GPA Distribution")
    st.write("This chart compares the distribution of current and predicted GPAs:")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create histogram with both current and predicted GPA
    sns.histplot(data=df, x='previous_gpa', color='blue', alpha=0.5, label='Current GPA', bins=20, kde=True)
    sns.histplot(data=df, x='predicted_gpa', color='orange', alpha=0.5, label='Predicted GPA', bins=20, kde=True)
    
    ax.set_xlabel('GPA')
    ax.set_ylabel('Number of Students')
    ax.set_title('GPA Distribution Comparison')
    ax.legend()
    
    st.pyplot(fig)
    
    # Detailed student predictions
    st.header("Individual Student Predictions")
    st.write("Below is a detailed view of each student's predicted performance:")
    
    # Display dataframe with the most relevant columns
    display_cols = ['student_id', 'name', 'previous_gpa', 'predicted_gpa', 'gpa_change']
    
    # Make sure all columns exist
    valid_cols = [col for col in display_cols if col in df.columns]
    
    if valid_cols:
        # Sort by GPA change
        sorted_df = df[valid_cols].sort_values(by='gpa_change', ascending=False)
        st.dataframe(sorted_df)
    
    # Students needing attention
    st.header("Students Needing Attention")
    st.write("This section highlights students whose performance might require intervention:")
    
    # Students with declining performance
    declining = df[df['gpa_change'] < -0.1].copy()
    if not declining.empty:
        st.subheader("Declining Performance")
        st.dataframe(declining[valid_cols])
        
        # Create recommendations
        st.subheader("Intervention Recommendations")
        st.write("Based on the predicted decline in GPA, here are some recommendations:")
        
        # Group students by how much intervention they need
        declining['intervention_level'] = pd.cut(
            declining['gpa_change'], 
            bins=[-1, -0.5, -0.3, -0.1, 0], 
            labels=['Urgent', 'High', 'Medium', 'Low']
        )
        
        for level in ['Urgent', 'High', 'Medium', 'Low']:
            level_students = declining[declining['intervention_level'] == level]
            if not level_students.empty:
                st.write(f"**{level} Intervention Needed:**")
                
                if level == 'Urgent':
                    st.error("These students need immediate attention:")
                    for _, student in level_students.iterrows():
                        st.write(f"- **{student['name']}**: Schedule a parent-teacher conference and consider tutoring.")
                elif level == 'High':
                    st.warning("These students need additional support:")
                    for _, student in level_students.iterrows():
                        st.write(f"- **{student['name']}**: Regular check-ins and study plan review are recommended.")
                else:
                    st.info(f"These students need monitoring:")
                    student_list = ", ".join(level_students['name'].tolist())
                    st.write(f"- {student_list}")
    else:
        st.success("No students show significant decline in performance.")
    
    # Analysis of factors
    st.header("Factor Analysis")
    st.write("This analysis shows which factors have the most influence on GPA predictions:")
    
    # Correlation between factors and predicted GPA
    numeric_df = df.select_dtypes(include=[np.number])
    corr_cols = [col for col in numeric_df.columns if col != 'predicted_gpa' and col != 'gpa_change']
    
    if corr_cols:
        correlations = []
        for col in corr_cols:
            corr = numeric_df['predicted_gpa'].corr(numeric_df[col])
            correlations.append({'Factor': col, 'Correlation': corr})
        
        corr_df = pd.DataFrame(correlations)
        corr_df = corr_df.sort_values('Correlation', ascending=False)
        
        st.subheader("Factors Influencing GPA Predictions")
        st.write("The following chart shows the correlation of various factors with the predicted GPA:")
        
        # Create a horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Correlation', y='Factor', data=corr_df, ax=ax, palette="viridis")
        ax.set_xlabel('Correlation with Predicted GPA')
        ax.set_title('Impact of Different Factors on GPA')
        
        st.pyplot(fig)
        
        # Key insights based on correlations
        st.subheader("Key Insights")
        top_factor = corr_df.iloc[0]['Factor']
        top_corr = corr_df.iloc[0]['Correlation']
        
        st.write(f"- **{top_factor}** has the strongest correlation ({top_corr:.2f}) with predicted GPA")
        st.write("- Based on this analysis, consider focusing improvement efforts on:")
        
        for _, row in corr_df.head(3).iterrows():
            st.write(f"  - **{row['Factor']}** (correlation: {row['Correlation']:.2f})")
    
    # Export options
    st.header("Export Results")
    st.write("You can download the prediction results for further analysis:")
    
    # Create a CSV download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Predictions as CSV",
        data=csv,
        file_name="student_predictions.csv",
        mime="text/csv"
    )
    
    # Navigation buttons
    col4, col5 = st.columns(2)
    
    with col4:
        if st.button("Return to Teacher Input"):
            st.switch_page("pages/Teacher_Input.py")
    
    with col5:
        if st.button("Return to Home"):
            st.switch_page("Home.py") 

# Footer
st.markdown("---")
st.caption("© 2025 The Data Consortium")