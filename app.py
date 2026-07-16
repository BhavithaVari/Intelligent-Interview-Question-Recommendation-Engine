import streamlit as st
import requests
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Interview Question Generator",
    page_icon=":dart:",
    layout="wide"
)

# Title and description
st.title("Intelligent Interview Question Generator")
st.markdown("Upload a resume and job description to generate structured interview questions")

# Create two columns for upload
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Resume")
    resume_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx'],
        help="Upload candidate's resume in PDF or DOCX format"
    )
    if resume_file:
        st.success(f"Uploaded: {resume_file.name}")

with col2:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the job description here..."
    )

# Generate button
if st.button("Generate Questions", type="primary", use_container_width=True):
    if not resume_file or not job_description:
        st.error("Please upload a resume and enter a job description")
    else:
        with st.spinner("Analyzing and generating questions..."):
            try:
                # Prepare files for API
                files = {
                    'resume': (resume_file.name, resume_file.getvalue(), resume_file.type)
                }
                data = {
                    'job_description': job_description
                }
                
                # Call backend API
                response = requests.post(
                    'http://127.0.0.1:8000/generate-questions',
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'questions' in result and result['questions']:
                        # Display analysis summary
                        st.success("Questions generated successfully!")
                        
                        # Show questions
                        st.subheader("Generated Interview Questions")
                        
                        # Create tabs for different views
                        tab1, tab2, tab3 = st.tabs(["All Questions", "Approved", "Rejected"])
                        
                        with tab1:
                            for i, q in enumerate(result['questions'], 1):
                                with st.expander(f"Question {i}: {q.get('difficulty', 'Medium')} - {q.get('question', 'No question')[:50]}..."):
                                    col_a, col_b = st.columns([3, 1])
                                    with col_a:
                                        st.markdown(f"**Question:** {q.get('question', 'N/A')}")
                                        st.markdown(f"**Difficulty:** `{q.get('difficulty', 'Medium')}`")
                                        st.markdown(f"**Expected Answer Points:**")
                                        for point in q.get('expected_answer_points', []):
                                            st.markdown(f"- {point}")
                                        st.markdown(f"**Reason:** {q.get('reason', 'N/A')}")
                                    with col_b:
                                        # Approve/Reject buttons
                                        if 'status' not in q:
                                            q['status'] = 'pending'
                                        
                                        if q['status'] == 'approved':
                                            st.button("Approved", key=f"approved_{i}", disabled=True)
                                        elif q['status'] == 'rejected':
                                            st.button("Rejected", key=f"rejected_{i}", disabled=True)
                                        else:
                                            col_btn1, col_btn2 = st.columns(2)
                                            with col_btn1:
                                                if st.button("Approve", key=f"approve_{i}"):
                                                    q['status'] = 'approved'
                                                    st.rerun()
                                            with col_btn2:
                                                if st.button("Reject", key=f"reject_{i}"):
                                                    q['status'] = 'rejected'
                                                    st.rerun()
                        
                        with tab2:
                            approved = [q for q in result['questions'] if q.get('status') == 'approved']
                            if approved:
                                for q in approved:
                                    st.markdown(f"{q.get('question', 'N/A')}")
                            else:
                                st.info("No approved questions yet")
                        
                        with tab3:
                            rejected = [q for q in result['questions'] if q.get('status') == 'rejected']
                            if rejected:
                                for q in rejected:
                                    st.markdown(f"{q.get('question', 'N/A')}")
                            else:
                                st.info("No rejected questions yet")
                    else:
                        st.warning("No questions were generated. Please check the input.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Please make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Tip:** Make sure your backend is running with `uvicorn main:app --reload`")