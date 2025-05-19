import streamlit as st
import pandas as pd
from database import get_assessment_results
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Divorce Assessment Admin",
    page_icon="📊",
    layout="wide"
)

# Admin password protection
def check_password():
    """Returns `True` if the user had the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.title("Divorce Assessment Admin Panel")
    password = st.text_input("Enter password", type="password")
    
    # Replace with a secure password in production
    if password == "admin1234":
        st.session_state.password_correct = True
        return True
    else:
        if password:  # Only show error if they've actually tried
            st.error("😕 Incorrect password")
        return False

if check_password():
    st.title("Divorce Assessment Admin Dashboard")
    st.markdown("View and analyze all assessment results")
    
    # Get all results from database
    results = get_assessment_results()
    
    if not results:
        st.info("No assessment results found in the database.")
    else:
        # Convert results to DataFrame for easier analysis
        data = []
        for result in results:
            data.append({
                'id': result.id,
                'email': result.email,
                'age': result.age,
                'divorce_stage': result.divorce_stage,
                'overall_score': result.overall_score,
                'legal_score': result.legal_score,
                'emotional_score': result.emotional_score,
                'financial_score': result.financial_score,
                'children_score': result.children_score,
                'recovery_score': result.recovery_score,
                'created_at': result.created_at
            })
        
        df = pd.DataFrame(data)
        
        # Dashboard metrics
        st.subheader("Dashboard Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assessments", len(df))
        with col2:
            st.metric("Average Overall Score", f"{df['overall_score'].mean():.1f}")
        with col3:
            st.metric("Recent Submissions", len(df[df['created_at'] > pd.Timestamp.now() - pd.Timedelta(days=7)]))
        
        # Charts and visualizations
        st.subheader("Assessment Score Distribution")
        
        # Distribution of overall scores
        fig1 = px.histogram(
            df,
            x="overall_score",
            nbins=20,
            title="Distribution of Overall Scores",
            labels={"overall_score": "Overall Score"},
            color_discrete_sequence=["#4a90e2"]
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Average category scores
        categories = ['legal_score', 'emotional_score', 'financial_score', 'children_score', 'recovery_score']
        category_labels = {
            'legal_score': 'Legal',
            'emotional_score': 'Emotional',
            'financial_score': 'Financial',
            'children_score': 'Children',
            'recovery_score': 'Recovery'
        }
        
        category_means = {category_labels[col]: df[col].mean() for col in categories}
        
        fig2 = px.bar(
            x=list(category_means.keys()),
            y=list(category_means.values()),
            labels={'x': 'Category', 'y': 'Average Score'},
            title="Average Scores by Category",
            color=list(category_means.values()),
            color_continuous_scale=['red', 'yellow', 'green'],
            range_color=[0, 100]
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Distribution by divorce stage
        if df['divorce_stage'].notna().any():
            stage_counts = df['divorce_stage'].value_counts().reset_index()
            stage_counts.columns = ['Divorce Stage', 'Count']
            
            fig3 = px.pie(
                stage_counts,
                values='Count',
                names='Divorce Stage',
                title="Assessment Distribution by Divorce Stage",
                hole=0.4
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Raw data table (with option to download)
        st.subheader("Raw Assessment Data")
        
        # Create downloadable CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Data as CSV",
            csv,
            "divorce_assessment_data.csv",
            "text/csv",
            key='download-csv'
        )
        
        # Display the data table
        st.dataframe(df)
