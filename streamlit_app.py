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
    cap = cv2.VideoCapture('output.mp4')
    audio, sr = librosa.load(audio_file)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            mouth_points = landmarks.parts()[48:68]
            mouth_img = np.zeros_like(frame)
            cv2.fillPoly(mouth_img, [np.array([point.x, point.y] for point in mouth_points)], (255, 255, 255))
            frame = cv2.addWeighted(frame, 1, mouth_img, 0.5, 0)

        cv2.imshow('Avatar', frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()

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
