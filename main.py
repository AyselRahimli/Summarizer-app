import streamlit as st
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from transformers import pipeline
import pyttsx3
import PyPDF2
from pytube import YouTube
import os

# Load summarization model
summarizer = pipeline("summarization")

# Functions for each page
def video_from_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename="temp_audio.mp4")
    return "temp_audio.mp4"

def video_to_text(video_path):
    clip = VideoFileClip(video_path)
    audio_path = "audio.wav"
    clip.audio.write_audiofile(audio_path)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    return text

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def summarize_pdf(text):
    return summarize_text(text)

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'output_audio.mp3')
    engine.runAndWait()

# Streamlit Interface
st.set_page_config(page_title="Media Summarizer", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Home", "Video Summarizer", "PDF Summarizer", "PDF to Voice"])

if page == "Home":
    st.title("Welcome to Media Summarizer!")
    st.markdown("""
    ## Introduction
    This project is designed to help users summarize videos and convert PDF content to audio.  
    **Why this project?**  
    In today’s world, we are constantly processing large amounts of media.  
    With the growing importance of time management, our goal is to provide tools that can make it easier for people to access essential information quickly.
    ### Features:
    1. **Video Summarizer**: Upload a YouTube video link, extract its audio, transcribe the audio, and get a concise summary.
    2. **PDF Summarizer**: Upload a PDF and get a summarized version of its text content.
    3. **PDF to Voice**: Upload a PDF, convert its text to speech, and listen to it in audio format.
    """)
    st.markdown("""
    ### Project Motivation:
    - **Time-Saving**: People can easily consume large amounts of information in less time.
    - **Accessibility**: Making content more accessible to everyone, including those with disabilities.
    - **Efficient Learning**: Summarizing long videos or PDFs helps users focus on the most relevant points.
    """)

elif page == "Video Summarizer":
    st.title("Video Summarizer")
    video_url = st.text_input("Enter YouTube Video URL")

    if video_url:
        try:
            st.write("Downloading and processing your video... Please wait.")
            video_path = video_from_youtube(video_url)
            text = video_to_text(video_path)
            summary = summarize_text(text)
            st.write("### Video Summary: ", summary)
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif page == "PDF Summarizer":
    st.title("PDF Summarizer")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        with open("temp_pdf.pdf", "wb") as f:
            f.write(uploaded_pdf.read())
        
        st.write("Processing your PDF... Please wait.")
        text = pdf_to_text("temp_pdf.pdf")
        summary = summarize_pdf(text)
        st.write("### PDF Summary: ", summary)

elif page == "PDF to Voice":
    st.title("PDF to Voice")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        with open("temp_pdf.pdf", "wb") as f:
            f.write(uploaded_pdf.read())
        
        st.write("Processing your PDF... Please wait.")
        text = pdf_to_text("temp_pdf.pdf")
        text_to_speech(text)
        st.audio('output_audio.mp3', format='audio/mp3')
