import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import base64
import pdf2image
import io
from PIL import Image
pdf2image


# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini API
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Prompt Template for data science, data analyst, AI/ML engineer, DevOps, and MLOps roles
input_prompt = """
You are an experienced Application Tracking System (ATS) with expertise in evaluating resumes
for roles in data science, data analysis, AI/ML engineering, DevOps, and MLOps. Your task is to 
assess the candidate's suitability for the role based on the provided job description.

Please assign a percentage match based on how well the resume aligns with the job description 
and highlight any missing keywords with high accuracy.

Key areas to evaluate:
- Technical skills related to data science and analysis (e.g., Python, R, SQL, data visualization)
- Experience with machine learning algorithms and frameworks (e.g., TensorFlow, PyTorch)
- Knowledge of cloud platforms and tools (e.g., AWS, Azure, GCP)
- Proficiency in DevOps practices (e.g., Docker, Kubernetes) and CI/CD pipelines
- Skills in MLOps and model deployment (e.g., MLflow, Kubeflow)
- Familiarity with Agile methodologies and collaborative tools (e.g., JIRA, Confluence)

resume: {text}
job_description: {job_description}

I want the response in a structured format:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit App
st.set_page_config(page_title="Resume Evaluation Assistant")
st.title("Resume Evaluation Assistant")

# Text area for job description input
job_description = st.text_area("Paste the Job Description:")

# File uploader for resume (PDF) input
uploaded_file = st.file_uploader("Upload Your Resume (PDF)...", type=["pdf"])

# Submit button for processing the resume and job description
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        try:
            # Extract text from PDF
            resume_text = input_pdf_text(uploaded_file)
            
            # Prepare prompt with extracted resume text and job description
            input_prompt_filled = input_prompt.format(text=resume_text, job_description=job_description)
            
            # Get response from Gemini API
            response = get_gemini_response(input_prompt_filled)
            
            # Display the Gemini Response in a block format
            st.markdown("### Gemini Response:")
            st.code(response, language='json')
            
            # Calculate percentage match (you can refine this logic as per your requirements)
            # For demonstration, we assume a simple percentage calculation
            # Replace this with your actual logic for calculating percentage match
            percentage_match = 85  # Example value, replace with actual calculation
            
            st.markdown("### Percentage Match:")
            st.write(f"{percentage_match}%")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload a resume.")
