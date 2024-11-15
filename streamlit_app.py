import streamlit as st
import PyPDF2
from PIL import Image
from gtts import gTTS
import pygame
import os
import cv2
import numpy as np
import librosa
import tempfile
import wave
import struct

# Function to select PDF file
def select_pdf():
    st.markdown("## Upload News PDF")
    pdf_file = st.file_uploader("Select PDF file", type=['pdf'])
    return pdf_file

# Function to select Avatar Image
def select_avatar():
    st.markdown("## Upload Anchor Avatar")
    avatar_file = st.file_uploader("Select anchor avatar image", type=['jpg', 'png'])
    return avatar_file

# Function to select Slideshow Images
def select_slides():
    st.markdown("## Upload Slideshow Images")
    slides_dir = st.file_uploader("Select slideshow images", type=['jpg', 'png'], accept_multiple_files=True)
    return slides_dir

# Function to extract text from PDF
def extract_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    news_text = ''
    for page in pdf_reader.pages:
        news_text += page.extract_text()
    return news_text

# Function to play news using TTS
def play_news(news_text):
    tts = gTTS(text=news_text, lang='en')
    tts.save('news.mp3')
    st.audio('news.mp3')

# Function to animate the avatar with simplified mouth movement
def animate_mouth_simple(audio_file, avatar_img):
    # Simulate basic mouth movements based on audio length
    audio, sr = librosa.load(audio_file)
    # Determine how many "mouth frames" we should show based on the length of the audio
    duration = librosa.get_duration(y=audio, sr=sr)
    num_frames = int(duration * 10)  # 10 frames per second of audio
    mouth_images = ['mouth_open.png', 'mouth_closed.png']  # Predefined mouth images
    
    # Load the avatar image and simulate lip-sync by switching between mouth images
    avatar = Image.open(avatar_img)
    avatar.thumbnail((150, 150))
    st.image(avatar, caption='News Anchor')
    
    for i in range(num_frames):
        # Alternate between mouth open and closed
        mouth_frame = mouth_images[i % len(mouth_images)]
        mouth_img = Image.open(mouth_frame)
        mouth_img = mouth_img.resize((50, 50))  # Resize the mouth image to fit the avatar
        avatar.paste(mouth_img, (50, 100), mouth_img)  # Paste mouth image on avatar

        st.image(avatar, caption=f'News Anchor Frame {i+1}')
        
    # Play the news audio again (for sync with visual)
    st.audio(audio_file)

# Function to show slideshow images
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

# Main function to execute the app
def main():
    st.title("News Anchor")

    pdf_file = select_pdf()
    avatar_file = select_avatar()
    slides_dir = select_slides()

    if pdf_file and avatar_file and slides_dir:
        # Display Avatar
        avatar = Image.open(avatar_file)
        avatar.thumbnail((150, 150))
        st.image(avatar, caption='News Anchor')

        # Extract Text from PDF
        news_text = extract_text(pdf_file)
        st.write(news_text)

        # Play News Audio
        play_button = st.button('Play News', key='play_news_button')
        if play_button:
            play_news(news_text)
            
            # Simulate simple mouth animation and Display Slideshow
            animate_mouth_simple('news.mp3', avatar_file)
            show_slideshow(slides_dir)

if __name__ == "__main__":
    main()
