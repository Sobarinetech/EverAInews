import streamlit as st
import PyPDF2
from PIL import Image
import pygame
import os
import cv2
import numpy as np
import librosa
import wave
import contextlib

# Select PDF for news
def select_pdf():
    st.markdown("## Upload News PDF")
    pdf_file = st.file_uploader("Select PDF file", type=['pdf'])
    return pdf_file

# Select Avatar
def select_avatar():
    st.markdown("## Upload Anchor Avatar")
    avatar_file = st.file_uploader("Select anchor avatar image", type=['jpg', 'png'])
    return avatar_file

# Select Slideshow Images
def select_slides():
    st.markdown("## Upload Slideshow Images")
    slides_dir = st.file_uploader("Select slideshow images", type=['jpg', 'png'], accept_multiple_files=True)
    return slides_dir

# Extract text from PDF
def extract_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    news_text = ''
    for page in pdf_reader.pages:
        news_text += page.extract_text()
    return news_text

# Play News
def play_news(news_text):
    tts = gTTS(text=news_text, lang='en')
    tts.save('news.mp3')
    st.audio('news.mp3')

# Lip-sync simulation without dlib
def animate_mouth(avatar_img, audio_file):
    # Load the avatar image
    avatar = Image.open(avatar_img)
    avatar = avatar.convert("RGBA")
    
    # Load the audio file
    audio, sr = librosa.load(audio_file)
    
    # Calculate the duration of the audio
    with contextlib.closing(wave.open(audio_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    
    # Here, you could simulate mouth movement based on audio length.
    # For simplicity, let's animate mouth with a basic shape.
    
    for i in range(int(duration * 10)):  # simulate mouth for the audio's duration
        frame = avatar.copy()
        frame = frame.convert("RGBA")

        # Simple simulation: Modify mouth shape based on time (simulating lip-sync)
        if i % 2 == 0:  # Create a "mouth open" effect every other frame
            mouth = Image.open("mouth_open.png").resize((100, 30))  # Custom mouth shape image
        else:
            mouth = Image.open("mouth_closed.png").resize((100, 30))  # Custom closed mouth image
        
        # Place mouth on the avatar
        frame.paste(mouth, (60, 120), mouth)  # Adjust (60, 120) based on avatar

        # Show the current frame (lip sync effect)
        st.image(frame)

# Slideshow of images
def show_slideshow(slides):
    slide_index = 0
    while slide_index < len(slides):
        slide = Image.open(slides[slide_index])
        slide.thumbnail((400, 400))
        st.image(slide)
        slide_index += 1
        if slide_index < len(slides):
            next_slide_button = st.button('Next Slide', key='next_slide_button')
            if next_slide_button:
                pass

# Main
def main():
    st.title("News Anchor")

    pdf_file = select_pdf()
    avatar_file = select_avatar()
    slides_dir = select_slides()

    if pdf_file and avatar_file and slides_dir:
        st.markdown("## News Anchor")
        avatar = Image.open(avatar_file)
        avatar.thumbnail((150, 150))
        st.image(avatar, caption='News Anchor')

        news_text = extract_text(pdf_file)
        st.write(news_text)

        play_button = st.button('Play News', key='play_news_button')
        if play_button:
            play_news(news_text)
            animate_mouth(avatar_file, 'news.mp3')
            show_slideshow(slides_dir)

if __name__ == "__main__":
    main()
