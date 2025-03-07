import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI API
genai.configure(api_key=api_key)

st.title("AI-Powered Interview Question Generator")
st.write("Generate interview questions based on role, skills, and difficulty level.")

# User Inputs
job_role = st.text_input("Enter Job Role (e.g., Software Developer)")
skill = st.text_input("Enter Skill/Topic (e.g., Python, DSA)")
difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
format_type = st.selectbox("Select Question Format", ["MCQ", "Coding", "Theory"])

if st.button("Generate Questions"):
    if job_role and skill:
        prompt = f"Generate 5 {difficulty} {format_type} interview questions for a {job_role} role focusing on {skill}."

        try:
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(prompt)
            questions = response.text

            st.subheader("Generated Questions:")
            questions_list = [q.strip() for q in questions.split("\n") if q.strip()]  # Remove empty lines
            for idx, question in enumerate(questions_list, start=1):
                     st.markdown(f"**{idx}.** {question}")


            # Save questions to a file
            with open("questions.txt", "w") as f:
                f.write(questions)
            st.download_button("Download Questions", data=questions, file_name="questions.txt")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both Job Role and Skill.")
