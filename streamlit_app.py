import streamlit as st
import PyPDF2
from PIL import Image
from gtts import gTTS
import pygame
import os
import cv2
import numpy as np
import librosa
import dlib

def select_pdf():
    st.markdown("## Upload News PDF")
    pdf_file = st.file_uploader("Select PDF file", type=['pdf'])
    return pdf_file

def select_avatar():
    st.markdown("## Upload Anchor Avatar")
    avatar_file = st.file_uploader("Select anchor avatar image", type=['jpg', 'png'])
    return avatar_file

def select_slides():
    st.markdown("## Upload Slideshow Images")
    slides_dir = st.file_uploader("Select slideshow images", type=['jpg', 'png'], accept_multiple_files=True)
    return slides_dir

def extract_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    news_text = ''
    for page in pdf_reader.pages:
        news_text += page.extract_text()
    return news_text

def play_news(news_text):
    tts = gTTS(text=news_text, lang='en')
    tts.save('news.mp3')
    st.audio('news.mp3')

def animate_mouth(avatar_img, audio_file):
    # Load the avatar image
    avatar = Image.open(avatar_img)
    avatar = avatar.convert("RGBA")

    # Load the audio file
    audio, sr = librosa.load(audio_file, sr=None)

    # Extract features from the audio to simulate lip movement
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)

    # Normalize onset energy
    normalized_onset = (onset_env - np.min(onset_env)) / (np.max(onset_env) - np.min(onset_env))

    # Initialize a pygame window for displaying the avatar
    pygame.init()
    screen = pygame.display.set_mode(avatar.size)
    clock = pygame.time.Clock()

    # Main loop for animating the mouth
    for i, energy in enumerate(normalized_onset):
        avatar_copy = avatar.copy()
        # Simulate mouth opening based on audio energy
        mouth_height = int(energy * 10)
        avatar_copy = simulate_mouth_opening(avatar_copy, mouth_height)

        # Display the avatar on screen
        screen.fill((255, 255, 255))  # Clear the screen
        avatar_copy_surface = pygame.image.fromstring(avatar_copy.tobytes(), avatar_copy.size, avatar_copy.mode)
        screen.blit(avatar_copy_surface, (0, 0))
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()

def simulate_mouth_opening(avatar, mouth_height):
    # This is a simple way of simulating the mouth movement. You could use more sophisticated methods here.
    avatar_array = np.array(avatar)
    # Simple mouth-opening simulation by modifying pixel rows at the bottom of the image
    avatar_array[-mouth_height:, :] = [255, 0, 0, 255]  # Change bottom pixels (simulated mouth open)
    return Image.fromarray(avatar_array)

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
