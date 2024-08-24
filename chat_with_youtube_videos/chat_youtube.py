# Import the required libraries
import tempfile
import streamlit as st
from embedchain import App
import os
from dotenv import load_dotenv
import openai
from langchain_groq import ChatGroq
# Define the embedchain_bot function
# Initialize the app
app = App()
def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4-turbo", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

# Create Streamlit app
st.title("Chat with YouTube Video 📺")
st.caption("This app allows you to chat with a YouTube video using OpenAI API")
ChatGroq.api_key= os.getenv('GROQ_API_KEY')
# Get OpenAI API key from user
openai_access_token = st.text_input(ChatGroq.api_key, type="password")

# If OpenAI API key is provided, create an instance of App
if openai_access_token:
    # Create a temporary directory to store the database
    db_path = tempfile.mkdtemp()
    # Create an instance of Embedchain App
    app = embedchain_bot(db_path, openai_access_token)
    # Get the YouTube video URL from the user
    #video_url = st.text_input("https://www.youtube.com/watch?v=dQw4w9WgXcQ", type="default")
    video_url = st.text_input("Enter YouTube video URL", "https://www.youtube.com/watch?v=3JZ_D3ELwOQ")
    # Add the video to the knowledge base
    if video_url:
        app.add(video_url, data_type="youtube_video")
        st.success(f"Added {video_url} to knowledge base!")
        # Ask a question about the video
        prompt = st.text_input("Ask any question about the YouTube Video")
        # Chat with the video
        if prompt:
            answer = app.chat(prompt)
            st.write(answer)

        