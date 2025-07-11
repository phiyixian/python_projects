import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon="page", layout="centered")

#Streamlit can auto handle redering any visual items or we tell it how to write it
st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

#st variables are like booleans, can be true/false
uploaded_file = st.file_uploader("Upload yoru resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targetting (optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_Reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_Reader.pages:
        text += page.extract_text() + "\n"
    return text

#assume LLM cannot accept file
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        #convert the read information into byte object to be sent to function above
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    #if not pdf file just read like normal text
    return uploaded_file.read().decode("utf-8")

#if button pressed
if analyze and uploaded_file:
    #st.write("Button pressed")
    try:
        file_content = extract_text_from_file(uploaded_file)

        #if file has content
        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()
        prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}

        Please provide your analysis in a clear, structured format with specific recommendations."""

        client = OpenAI(api_key=OPEN_API_KEY)
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role": "system", "content": "You are an expert resume reviewer with years of experience."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occured: {str(e)}")