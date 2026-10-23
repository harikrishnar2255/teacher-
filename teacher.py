import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables (for local development)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Teacher Chatbot",
    page_icon="👨‍🏫",
    layout="centered"
)

# Fetch API key: checks Streamlit Secrets first (for cloud deployment), then local .env variable 'x'
groq_api_key = st.secrets.get("x") if "x" in st.secrets else os.environ.get("x")

if not groq_api_key:
    st.error("API Key not found. Please set 'x' in your .env file or Streamlit Secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=groq_api_key)
MODEL = "openai/gpt-oss-120b"

# Header UI
st.title("👨‍🏫 AI Teacher Assistant")
st.caption("Ask any question or pick a subject to learn today!")

# Define Teacher Persona System Prompt
TEACHER_SYSTEM_PROMPT = (
    "You are a friendly, encouraging, and knowledgeable school teacher. "
    "Your goal is to help students learn effectively. "
    "Explain complex concepts in simple, easy-to-understand language using clear examples or real-world analogies. "
    "Be patient, supportive, and structured in your explanations. "
    "At the end of your response, ask a light follow-up question or present a simple short exercise to check if the student understood."
)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": TEACHER_SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello there! I'm your AI teacher today. 🎓 What topic or subject would you like to explore?"}
    ]

# Display existing messages (skip system message)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👨‍🏫" if msg["role"] == "assistant" else "🧑‍🎓"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# User input field
if user_prompt := st.chat_input("Ask your teacher a question..."):
    # Display user input
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_prompt)
    
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate response
    with st.chat_message("assistant", avatar="👨‍🏫"):
        with st.spinner("Teacher is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages
                )
                teacher_response = response.choices[0].message.content
                st.markdown(teacher_response)
                
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": teacher_response})
            except Exception as e:
                st.error(f"An error occurred: {e}")