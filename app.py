from flask import Flask,request,jsonify
import google.generativeai as genai
from google.generativeai import GenerationConfig
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY not found in Streamlit secrets.")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model=genai.GenerativeModel("gemini-1.5-flash")
generate_config=GenerationConfig(temperature=0.4)

st.title("Gemini problem solver")
st.write("Give an error message or problem you're facing, and get multiple ways to solve it!")
user_input = st.text_area("🔍 What's the error or problem?", height=150)

if st.button("solve"):
    if user_input:
        with st.spinner("Analyzing problem and generating solutions..."):
             # Define roles
            roles = {
                "Engineer": "Provide a quick, fix-oriented response to this issue.",
                "Scientist": "Explain the root cause of the issue in a logical, analytical way.",
                "Teacher": "Explain this issue in simple, beginner-friendly steps.",
                "Beginner": "Pretend you're a student who just learned this and is trying to explain it to a friend.",
                "AI Expert": "Suggest the most efficient and advanced solution to fix or improve this problem."
            }
            responses={}
            for role in roles :
                prompt = f"""
                You are an {role} who helps people solve errors or task problems.
                Given this problem or error: "{user_input}", suggest unique way to solve it.
                Your answers should be detailed and consider different perspectives like debugging, tools, and resources.
                """
                suggestions=model.generate_content(prompt,generation_config=generate_config)
                responses[role] = suggestions.candidates[0].content.parts[0].text.strip()
            for role,solution in responses.items():
                st.subheader(f"{role}")
                st.markdown(f"> {solution}")
