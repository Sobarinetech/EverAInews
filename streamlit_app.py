import streamlit as st
import PyPDF2
from PIL import Image
from gtts import gTTS
import pygame
import os

def select_pdf():
    pdf_file = st.file_uploader("Select PDF file", type=['pdf'])
    return pdf_file

def extract_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    news_text = ''
    for page in pdf_reader.pages:
        news_text += page.extract_text()
    return news_text

def initialize_slideshow():
    slide_dir = 'slides'
    slides = []
    for filename in os.listdir(slide_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            slides.append(os.path.join(slide_dir, filename))
    return slides

def play_news(news_text):
    tts = gTTS(text=news_text, lang='en')
    tts.save('news.mp3')
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('news.mp3')
    pygame.mixer.music.play()

def show_slideshow(slides):
    slide_index = 0
    while slide_index < len(slides):
        slide_path = slides[slide_index]
        slide = Image.open(slide_path)
        slide.thumbnail((400, 400))  # Resize image
        st.image(slide)
        slide_index += 1
        if slide_index < len(slides):
            if st.button('Next Slide'):
                pass

def main():
    st.title("News Anchor")
    anchor_avatar = Image.open('anchor_avatar.jpg')  # Replace with your avatar image
    anchor_avatar.thumbnail((150, 150))  # Resize avatar image
    st.image(anchor_avatar, caption='News Anchor')

    pdf_file = select_pdf()
    if pdf_file:
        news_text = extract_text(pdf_file)
        st.write(news_text)
        slides = initialize_slideshow()
        play_button = st.button('Play News')
        if play_button:
            play_news(news_text)
            show_slideshow(slides)

if __name__ == "__main__":
    main()
