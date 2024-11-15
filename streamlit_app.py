import streamlit as st
import numpy as np
import cv2
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image
import os

# Function to generate audio using gTTS (Google Text-to-Speech)
def generate_audio(script_text, audio_path="news_audio.mp3"):
    tts = gTTS(script_text, lang="en")
    tts.save(audio_path)
    return audio_path

# Function to animate mouth based on phonemes (simplified mapping)
def get_mouth_shape(phoneme):
    # Mapping phonemes to basic mouth shapes
    if phoneme in ['a', 'e', 'o', 'u']:
        return "open"
    elif phoneme in ['b', 'p', 'm']:
        return "closed"
    else:
        return "neutral"

# Function to generate human avatar frames based on input text
def generate_human_avatar_frames(script_text, face_image_path="human_face.jpg"):
    frames = []
    face_img = cv2.imread(face_image_path)
    
    # Phoneme simulation based on input text (simple version, actual phoneme recognition would be better)
    script_phonemes = [word for word in script_text.split()]  # Breaking into words for simplicity
    
    # Iterate through the script and animate the mouth for each phoneme (for simplicity, treating words as phonemes)
    for i, word in enumerate(script_phonemes):
        mouth_state = get_mouth_shape(word[0].lower())  # Using the first letter as a simple phoneme
        
        if mouth_state == "open":
            cv2.ellipse(face_img, (250, 300), (50, 20), 0, 0, 180, (0, 0, 255), -1)  # Open mouth
        elif mouth_state == "closed":
            cv2.rectangle(face_img, (230, 290), (270, 310), (0, 0, 255), -1)  # Closed mouth
        else:
            # Neutral mouth
            cv2.line(face_img, (230, 300), (270, 300), (0, 0, 255), 2)
        
        # Save each frame
        frame_path = f"frame_{i}.jpg"
        cv2.imwrite(frame_path, face_img)
        frames.append(frame_path)
    
    return frames

# Function to create a video with frames and audio
def create_video(frames, audio_path, output_video_path="news_video.mp4"):
    # Load frames into a video clip
    clip = ImageSequenceClip(frames, fps=10)
    
    # Add audio to the video
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    
    # Save the video
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Streamlit app main function
def main():
    st.title("Human-Like News Anchor Video Generator")
    st.markdown("### Paste your news script below to generate a human-like avatar video with narration!")
    
    # Input for news script
    news_script = st.text_area("Type or Paste News Script Below:")
    
    # Generate video button
    if st.button("Generate Video"):
        if not news_script.strip():
            st.warning("Please provide a valid script to generate the video!")
            return

        # Generate audio
        st.info("Generating TTS audio...")
        audio_path = generate_audio(news_script)
        
        # Generate avatar frames
        st.info("Generating avatar frames...")
        frames = generate_human_avatar_frames(news_script)
        
        # Create video
        st.info("Creating video...")
        video_path = create_video(frames, audio_path)

        st.success("Video created successfully!")
        st.video(video_path)

# Run the Streamlit app
if __name__ == "__main__":
    main()
