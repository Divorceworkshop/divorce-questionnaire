import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from PIL import Image
from io import BytesIO
from questionnaire import get_questionnaire_sections
from analyzer import calculate_scores, generate_feedback, generate_improvement_suggestions
from email_sender import send_results_email
from utils import create_report_html
from database import save_assessment_result
import time

# Function to load and display car image
def get_car_image_base64():
    # Placeholder base64 image - this simulates the car image
    return """
    iVBORw0KGgoAAAANSUhEUgAAASwAAACoCAMAAABt9SM9AAAAA1BMVEX/XgA92nntAAAAR0lEQVR4nO3BAQEAAACCIP+vbkhAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO8GxYgAAb0jQ/cAAAAASUVORK5CYII=
    """

# Page configuration
st.set_page_config(
    page_title="Divorce Strategy Profiler",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state variables
if 'current_section' not in st.session_state:
    st.session_state.current_section = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

# Get questionnaire sections
sections = get_questionnaire_sections()
total_sections = len(sections)

# Header will be created with custom style below

# Create a yellow box with car image and white text
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

.car-header {
    background-color: #FFD700;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
    position: relative;
}
.car-header h1 {
    font-family: 'Roboto', sans-serif;
    font-weight: 700;
    color: white;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    position: relative;
    z-index: 2;
    font-size: 3.75em; /* Updated to 3.75em as requested */
    margin-bottom: 15px;
    line-height: 1.2;
}
.car-header h2 {
    font-family: 'Roboto', sans-serif;
    font-weight: 700;
    color: white;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    position: relative;
    z-index: 2;
    font-size: 2.25em; /* Updated to 2.25em as requested */
    margin-top: -0.1em; /* Moved upward to have minimal spacing */
    line-height: 1.3;
}
.car-header h3 {
    color: white;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    position: relative;
    z-index: 2;
    margin-top: 30px;
    font-size: 1.1em; /* Updated to 1.1em as requested */
}
.car-background {
    background-image: url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4QO2aHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA1LjYtYzE0NSA3OS4xNjM0OTksIDIwMTgvMDgvMTMtMTY6NDA6MjIgICAgICAgICI+CiAgIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgICAgIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICAgICAgICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgICAgICAgICAgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiPgogICAgICAgICA8ZGM6c3ViamVjdD4KICAgICAgICAgICAgPHJkZjpCYWcvPgogICAgICAgICA8L2RjOnN1YmplY3Q+CiAgICAgICAgIDx4bXA6TW9kaWZ5RGF0ZT4yMDE5LTAyLTI2VDIyOjI4OjUzLTA1OjAwPC94bXA6TW9kaWZ5RGF0ZT4KICAgICAgICAgPHhtcDpDcmVhdG9yVG9vbD5BZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoTWFjaW50b3NoKTwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOjI2QUIwN0I3QTUxMzExRTk5MTEyQTQyMTk0QTI5MkYwPC94bXBNTTpJbnN0YW5jZUlEPgogICAgICAgICA8eG1wTU06RG9jdW1lbnRJRD54bXAuZGlkOjI2QUIwN0I4QTUxMzExRTk5MTEyQTQyMTk0QTI5MkYwPC94bXBNTTpEb2N1bWVudElEPgogICAgICAgICA8eG1wTU06RGVyaXZlZEZyb20gcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICA8c3RSZWY6aW5zdGFuY2VJRD54bXAuaWlkOjI2QUIwN0I1QTUxMzExRTk5MTEyQTQyMTk0QTI5MkYwPC9zdFJlZjppbnN0YW5jZUlEPgogICAgICAgICAgICA8c3RSZWY6ZG9jdW1lbnRJRD54bXAuZGlkOjI2QUIwN0I2QTUxMzExRTk5MTEyQTQyMTk0QTI5MkYwPC9zdFJlZjpkb2N1bWVudElEPgogICAgICAgICA8L3htcE1NOkRlcml2ZWRGcm9tPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KPD94cGFja2V0IGVuZD0iciI/Pv/tAKBQaG90b3Nob3AgMy4wADhCSU0EBAAAAAAAWBwCUAAMSlVTVCBTRVBBUkFURUQcAngAH0EgUG9kY2FzdCBmb3IgRGl2b3JjZSAmIFNlcGFyYXRpb24cAnwAGHdpdGggS2FyZW4gT21hbmQsIEIuQS5Tb2M4QklNBCUAAAAAABAZOVXq9NoAr98TKk0xh0lc/+IMWElDQ19QUk9GSUxFAAEBAAAMSExpbm8CEAAAbW50clJHQiBYWVogB84AAgAJAAYAMQAAYWNzcE1TRlQAAAAASUVDIHNSR0IAAAAAAAAAAAAAAAAAAPbWAAEAAAAA0y1IUCAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARY3BydAAAAVAAAAAzZGVzYwAAAYQAAABsd3RwdAAAAfAAAAAUYmtwdAAAAgQAAAAUclhZWgAAAhgAAAAUZ1hZWgAAAiwAAAAUYlhZWgAAAkAAAAAUZG1uZAAAAlQAAABwZG1kZAAAAsQAAACIdnVlZAAAA0wAAACGdmlldwAAA9QAAAAkbHVtaQAAA/gAAAAUbWVhcwAABAwAAAAkdGVjaAAABDAAAAAMclRSQwAABDwAAAgMZ1RSQwAABDwAAAgMYlRSQwAABDwAAAgMdGV4dAAAAABDb3B5cmlnaHQgKGMpIDE5OTggSGV3bGV0dC1QYWNrYXJkIENvbXBhbnkAAGRlc2MAAAAAAAAAEnNSR0IgSUVDNjE5NjYtMi4xAAAAAAAAAAAAAAASc1JHQiBJRUM2MTk2Ni0yLjEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAAAAAAAADzUQABAAAAARbMWFlaIAAAAAAAAAAAAAAAAAAAAABYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9kZXNjAAAAAAAAABZJRUMgaHR0cDovL3d3dy5pZWMuY2gAAAAAAAAAAAAAABZJRUMgaHR0cDovL3d3dy5pZWMuY2gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZGVzYwAAAAAAAAAuSUVDIDYxOTY2LTIuMSBEZWZhdWx0IFJHQiBjb2xvdXIgc3BhY2UgLSBzUkdCAAAAAAAAAAAAAAAuSUVDIDYxOTY2LTIuMSBEZWZhdWx0IFJHQiBjb2xvdXIgc3BhY2UgLSBzUkdCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGRlc2MAAAAAAAAALFJlZmVyZW5jZSBWaWV3aW5nIENvbmRpdGlvbiBpbiBJRUM2MTk2Ni0yLjEAAAAAAAAAAAAAACxSZWZlcmVuY2UgVmlld2luZyBDb25kaXRpb24gaW4gSUVDNjE5NjYtMi4xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB2aWV3AAAAAAATpP4AFF8uABDPFAAD7cwABBMLAANcngAAAAFYWVogAAAAAABMCVYAUAAAAFcf521lYXMAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAKPAAAAAnNpZyAAAAAAQ1JUIGN1cnYAAAAAAAAEAAAAAAUACgAPABQAGQAeACMAKAAtADIANwA7AEAARQBKAE8AVABZAF4AYwBoAG0AcgB3AHwAgQCGAIsAkACVAJoAnwCkAKkArgCyALcAvADBAMYAywDQANUA2wDgAOUA6wDwAPYA+wEBAQcBDQETARkBHwElASsBMgE4AT4BRQFMAVIBWQFgAWcBbgF1AXwBgwGLAZIBmgGhAakBsQG5AcEByQHRAdkB4QHpAfIB+gIDAgwCFAIdAiYCLwI4AkECSwJUAl0CZwJxAnoChAKOApgCogKsArYCwQLLAtUC4ALrAvUDAAMLAxYDIQMtAzgDQwNPA1oDZgNyA34DigOWA6IDrgO6A8cD0wPgA+wD+QQGBBMEIAQtBDsESARVBGMEcQR+BIwEmgSoBLYExATTBOEE8AT+BQ0FHAUrBToFSQVYBWcFdwWGBZYFpgW1BcUF1QXlBfYGBgYWBicGNwZIBlkGagZ7BowGnQavBsAG0QbjBvUHBwcZBysHPQdPB2EHdAeGB5kHrAe/B9IH5Qf4CAsIHwgyCEYIWghuCIIIlgiqCL4I0gjnCPsJEAklCToJTwlkCXkJjwmkCboJzwnlCfsKEQonCj0KVApqCoEKmAquCsUK3ArzCwsLIgs5C1ELaQuAC5gLsAvIC+EL+QwSDCoMQwxcDHUMjgynDMAM2QzzDQ0NJg1ADVoNdA2ODakNww3eDfgOEw4uDkkOZA5/DpsOtg7SDu4PCQ8lD0EPXg96D5YPsw/PD+wQCRAmEEMQYRB+EJsQuRDXEPURExExEU8RbRGMEaoRyRHoEgcSJhJFEmQShBKjEsMS4xMDEyMTQxNjE4MTpBPFE+UUBhQnFEkUahSLFK0UzhTwFRIVNBVWFXgVmxW9FeAWAxYmFkkWbBaPFrIW1hb6Fx0XQRdlF4kXrhfSF/cYGxhAGGUYihivGNUY+hkgGUUZaxmRGbcZ3RoEGioaURp3Gp4axRrsGxQbOxtjG4obshvaHAIcKhxSHHscoxzMHPUdHh1HHXAdmR3DHeweFh5AHmoelB6+HukfEx8+H2kflB+/H+ogFSBBIGwgmCDEIPAhHCFIIXUhoSHOIfsiJyJVIoIiryLdIwojOCNmI5QjwiPwJB8kTSR8JKsk2iUJJTglaCWXJccl9yYnJlcmhya3JugnGCdJJ3onqyfcKA0oPyhxKKIo1CkGKTgpaymdKdAqAio1KmgqmyrPKwIrNitpK50r0SwFLDksbiyiLNctDC1BLXYtqy3hLhYuTC6CLrcu7i8kL1ovkS/HL/4wNTBsMKQw2zESMUoxgjG6MfIyKjJjMpsy1DMNM0YzfzO4M/E0KzRlNJ402DUTNU01hzXCNf02NzZyNq426TckN2A3nDfXOBQ4UDiMOMg5BTlCOX85vDn5OjY6dDqyOu87LTtrO6o76DwnPGU8pDzjPSI9YT2hPeA+ID5gPqA+4D8hP2E/oj/iQCNAZECmQOdBKUFqQaxB7kIwQnJCtUL3QzpDfUPARANER0SKRM5FEkVVRZpF3kYiRmdGq0bwRzVHe0fASAVIS0iRSNdJHUljSalJ8Eo3Sn1KxEsMS1NLmkviTCpMcky6TQJNSk2TTdxOJU5uTrdPAE9JT5NP3VAnUHFQu1EGUVBRm1HmUjFSfFLHUxNTX1OqU/ZUQlSPVNtVKFV1VcJWD1ZcVqlW91dEV5JX4FgvWH1Yy1kaWWlZuFoHWlZaplr1W0VblVvlXDVchlzWXSddeF3JXhpebF69Xw9fYV+zYAVgV2CqYPxhT2GiYfViSWKcYvBjQ2OXY+tkQGSUZOllPWWSZedmPWaSZuhnPWeTZ+loP2iWaOxpQ2maafFqSGqfavdrT2una/9sV2yvbQhtYG25bhJua27Ebx5veG/RcCtwhnDgcTpxlXHwcktypnMBc11zuHQUdHB0zHUodYV14XY+dpt2+HdWd7N4EXhueMx5KnmJeed6RnqlewR7Y3vCfCF8gXzhfUF9oX4BfmJ+wn8jf4R/5YBHgKiBCoFrgc2CMIKSgvSDV4O6hB2EgITjhUeFq4YOhnKG14c7h5+IBIhpiM6JM4mZif6KZIrKizCLlov8jGOMyo0xjZiN/45mjs6PNo+ekAaQbpDWkT+RqJIRknqS45NNk7aUIJSKlPSVX5XJljSWn5cKl3WX4JhMmLiZJJmQmfyaaJrVm0Kbr5wcnImc951kndKeQJ6unx2fi5/6oGmg2KFHobaiJqKWowajdqPmpFakx6U4pammGqaLpv2nbqfgqFKoxKk3qamqHKqPqwKrdavprFys0K1ErbiuLa6hrxavi7AAsHWw6rFgsdayS7LCszizrrQltJy1E7WKtgG2ebbwt2i34LhZuNG5SrnCuju6tbsuu6e8IbypvQW9j74KvoS+/796v/XAcMDswWfB48JfwtvDWMPUxFHEzsVLxcjGRsbDx0HHv8g9yLzJOsm5yjjKt8s2y7bMNcy1zTXNtc42zrbPN8+40DnQutE80b7SP9LB00TTxtRJ1MvVTtXR1lXW2Ndc1+DYZNjo2WzZ8dp22vvbgNwF3IrdEN2W3hzeot8p36/gNuC94UThzOJT4tvjY+Pr5HPk/OWE5g3mlucf56noMui86Ubp0Opb6uXrcOv77IbtEe2c7ijutO9A78zwWPDl8XLx//KM8xnzp/Q09ML1UPXe9m32+/eK+Bn4qPk4+cf6V/rn+3f8B/yY/Sn9uv5L/tz/bf//');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    opacity: 0.8;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
}
</style>

<div class="car-header">
    <div class="car-background"></div>
    <h1>Do You Know Your Divorce Strategy?</h1>
    <h2>And Is It Helping or Just Costing You Money?</h2>
    <h3>Copyright - Divorceworkshop.ca</h3>
</div>
""", unsafe_allow_html=True)

if st.session_state.email_sent:
    # Custom branded success message
    st.markdown("""
    <div style="text-align: center; padding: 30px; background-color: #FFD700; border-radius: 10px; margin: 20px 0; border: 2px solid #000;">
        <i class="fas fa-envelope" style="font-size: 48px; color: #000;"></i>
        <h2 style="color: #000;">Your Results Have Been Sent</h2>
        <p style="font-size: 18px; color: #000;">We've sent your personalized strategy profile to your email address.</p>
        <p style="font-size: 16px; color: #000;">Please check your inbox (and spam folder if necessary) for an email with the subject:</p>
        <p style="font-weight: bold; color: #000;">"Your Divorce Strategy Profile Results"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional information with matching branding
    st.markdown("""
    <div style="padding: 20px; background-color: #fff; border: 2px solid #FFD700; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: #000;">What's Included in Your Results:</h3>
        <ul style="color: #000;">
            <li>Your dominant divorce negotiation strategy</li>
            <li>Analysis of your strategy's strengths and watch-out points</li>
            <li>How your strategy interacts with different ex-partner approaches</li>
            <li>Personalized recommendations for your specific situation</li>
            <li>Resources to support your divorce process</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Restart button with matching style
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Take the Assessment Again", key="restart_btn"):
            st.session_state.current_section = 0
            st.session_state.responses = {}
            st.session_state.email_sent = False
            st.rerun()
    
else:
    # Display branded introduction
    if st.session_state.current_section == 0:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px; padding: 15px; background-color: #fff; border: 2px solid #FFD700; border-radius: 10px;">
            <p style="color: #000; font-size: 18px;">This questionnaire will help identify your divorce negotiation strategy and provide personalized recommendations. Upon completion, you'll receive detailed results via email.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Removed the icons and text as requested
            
    # Progress bar
    progress = st.session_state.current_section / total_sections
    st.progress(progress)
    st.write(f"Section {st.session_state.current_section + 1} of {total_sections}")

    # Display current section
    current_section = sections[st.session_state.current_section]
    st.header(current_section['title'])
    
    # Form for the current section
    with st.form(key=f"section_{st.session_state.current_section}"):
        responses = {}
        
        for question in current_section['questions']:
            question_id = question['id']
            question_text = question['text']
            question_type = question['type']
            
            if question_type == 'open_ended':
                response = st.text_area(question_text, key=question_id)
                responses[question_id] = response
            
            elif question_type == 'single_choice':
                options = question['options']
                response = st.radio(question_text, options, key=question_id)
                responses[question_id] = response
            
            elif question_type == 'multiple_choice':
                options = question['options']
                st.write(question_text)
                for option in options:
                    responses[f"{question_id}_{option}"] = st.checkbox(option, key=f"{question_id}_{option}")
            
            elif question_type == 'rating':
                options = question['options']
                response = st.select_slider(question_text, options=options, key=question_id)
                responses[question_id] = response
            
            elif question_type == 'conditional':
                main_question = question['main_question']
                main_options = question['main_options']
                follow_up = question['follow_up']
                
                main_response = st.radio(main_question, main_options, key=f"{question_id}_main")
                responses[f"{question_id}_main"] = main_response
                
                if main_response == follow_up['condition']:
                    follow_up_response = st.text_area(follow_up['text'], key=f"{question_id}_follow_up")
                    responses[f"{question_id}_follow_up"] = follow_up_response
            
            elif question_type == 'email':
                response = st.text_input(question_text, key=question_id)
                responses[question_id] = response
                
            st.markdown("---")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        # Initialize button variables to avoid unbound variable errors
        prev_button = False
        next_button = False
        submit_button = False
        
        with col1:
            if st.session_state.current_section > 0:
                prev_button = st.form_submit_button("Previous")
        with col2:
            if st.session_state.current_section < total_sections - 1:
                next_button = st.form_submit_button("Next")
            else:
                submit_button = st.form_submit_button("Submit")
        
        # Handle form submission
        if next_button:
            # Save responses and move to next section
            st.session_state.responses.update(responses)
            st.session_state.current_section += 1
            st.rerun()
            
        elif prev_button:
            # Move to previous section
            st.session_state.current_section -= 1
            st.rerun()
            
        elif submit_button:
            # Validate email at submission
            email = responses.get('email', '').strip()
            if not email or '@' not in email or '.' not in email:
                st.error("Please enter a valid email address to receive your results.")
            else:
                # Save final responses
                st.session_state.responses.update(responses)
                
                # Show processing message
                with st.spinner("Analyzing your strategy profile and preparing your personalized report..."):
                    # Calculate scores
                    scores = calculate_scores(st.session_state.responses)
                    
                    # Generate feedback
                    feedback = generate_feedback(scores, st.session_state.responses)
                    
                    # Generate improvement suggestions
                    suggestions = generate_improvement_suggestions(scores, st.session_state.responses)
                    
                    # Create HTML report
                    html_report = create_report_html(scores, feedback, suggestions, st.session_state.responses)
                    
                    # Save results to database
                    try:
                        # Adapt the existing database save function to work with our new data format
                        db_result = save_assessment_result(
                            email, 
                            {
                                'overall': scores['overall'],
                                'dominant_strategy': scores['dominant_strategy'],
                                # Leave these as 0 since they're not used in the new assessment
                                'legal_score': 0,
                                'emotional_score': 0,
                                'financial_score': 0,
                                'children_score': 0,
                                'recovery_score': 0
                            }, 
                            st.session_state.responses
                        )
                        if db_result:
                            st.session_state.db_saved = True
                    except Exception as e:
                        print(f"Database error: {str(e)}")
                        # Don't show error to user, just continue to send email
                    
                    # Send email with results
                    success = send_results_email(email, html_report, scores)
                    
                    if success:
                        st.session_state.email_sent = True
                        time.sleep(1)  # Brief pause for transition
                        st.rerun()
                    else:
                        st.error("There was an issue sending your results. Please try again.")

# Add CSS for Font Awesome icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
    .stProgress > div > div > div > div {
        background-color: #4a90e2;
    }
</style>
""", unsafe_allow_html=True)
