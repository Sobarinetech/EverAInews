import streamlit as st
import PyPDF2
from PIL import Image
from gtts import gTTS
import pygame
import os

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
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('news.mp3')
    pygame.mixer.music.play()

def show_slideshow(slides):
    slide_index = 0
    while slide_index < len(slides):
        slide = Image.open(slides[slide_index])
        slide.thumbnail((400, 400))  # Resize image
        st.image(slide)
        slide_index += 1
        if slide_index < len(slides):
            if st.button('Next Slide'):
                pass

def main():
    st.title("News Anchor")

    pdf_file = select_pdf()
    avatar_file = select_avatar()
    slides_dir = select_slides()

    if pdf_file and avatar_file and slides_dir:
        st.markdown("## News Anchor")
        avatar = Image.open(avatar_file)
        avatar.thumbnail((150, 150))  # Resize avatar image
        st.image(avatar, caption='News Anchor')

        news_text = extract_text(pdf_file)
        st.write(news_text)

        play_button = st.button('Play News')
        if play_button:
            play_news(news_text)
            show_slideshow(slides_dir)

if __name__ == "__main__":
    main()
