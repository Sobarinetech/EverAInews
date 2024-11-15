import streamlit as st
import PyPDF2
from PIL import Image
from gtts import gTTS
import pygame
import os

# Function to select PDF file
def select_pdf():
    pdf_file = st.file_uploader("Select PDF file", type=['pdf'])
    return pdf_file

# Extract text from PDF
def extract_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    news_text = ''
    for page in pdf_reader.pages:
        news_text += page.extract_text()
    return news_text

# Initialize slideshow
def initialize_slideshow():
    slide_dir = 'slides'
    slides = []
    for filename in os.listdir(slide_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            slides.append(os.path.join(slide_dir, filename))
    return slides

# Play news audio
def play_news(news_text):
    tts = gTTS(text=news_text, lang='en')
    tts.save('news.mp3')
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('news.mp3')
    pygame.mixer.music.play()

# Display slideshow
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

# Main function
def main():
    st.title("News Anchor")

    # Display anchor avatar
    anchor_url = "https://raw.githubusercontent.com/your-username/your-repo/main/anchor_avatar.jpg"
    anchor_avatar = Image.open(st.cache_data(anchor_url))
    anchor_avatar.thumbnail((150, 150))  # Resize avatar image
    st.image(anchor_avatar, caption='News Anchor')

    # Select PDF file
    pdf_file = select_pdf()
    if pdf_file:
        # Extract text from PDF
        news_text = extract_text(pdf_file)
        st.write(news_text)

        # Initialize slideshow
        slides = initialize_slideshow()

        # Play news audio and display slideshow
        play_button = st.button('Play News')
        if play_button:
            play_news(news_text)
            show_slideshow(slides)

# Run application
if __name__ == "__main__":
    main()
