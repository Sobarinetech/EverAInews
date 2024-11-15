import streamlit as st
import numpy as np
import cv2
from gtts import gTTS
import os
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image
import random
import time

# Function to create a cool cartoon avatar with basic animations
def create_animated_anchor(script_text):
    # Create a blank canvas for the avatar
    avatar_canvas = np.ones((500, 500, 3), dtype=np.uint8) * 255  # White background canvas

    # Create a simple cartoon avatar (face, eyes, and mouth)
    # Draw face
    cv2.circle(avatar_canvas, (250, 200), 100, (200, 200, 255), -1)  # Face (light skin)

    # Draw eyes
    cv2.circle(avatar_canvas, (210, 170), 15, (0, 0, 0), -1)  # Left eye
    cv2.circle(avatar_canvas, (290, 170), 15, (0, 0, 0), -1)  # Right eye
    
    # Draw the mouth (closed by default)
    mouth_position = (220, 250, 280, 270)  # Rectangular mouth
    cv2.rectangle(avatar_canvas, (mouth_position[0], mouth_position[1]), (mouth_position[2], mouth_position[3]), (0, 0, 255), -1)

    # Generate frames with animation (mouth opening/closing, eyes blinking)
    frames = []
    for i in range(len(script_text)):
        frame = avatar_canvas.copy()

        # Simulate mouth opening/closing
        mouth_opening = random.choice([True, False])
        mouth_position = (220, 250, 280, 270) if mouth_opening else (220, 260, 280, 275)
        cv2.rectangle(frame, (mouth_position[0], mouth_position[1]), (mouth_position[2], mouth_position[3]), (0, 0, 255), -1)
        
        # Simulate eye blinking
        blink = random.choice([True, False])
        if blink:
            cv2.circle(frame, (210, 170), 15, (255, 255, 255), -1)  # Left eye blink
            cv2.circle(frame, (290, 170), 15, (255, 255, 255), -1)  # Right eye blink
        else:
            cv2.circle(frame, (210, 170), 15, (0, 0, 0), -1)  # Left eye open
            cv2.circle(frame, (290, 170), 15, (0, 0, 0), -1)  # Right eye open
        
        # Add the current frame to the list of frames
        frame_path = f"frame_{i}.png"
        cv2.imwrite(frame_path, frame)
        frames.append(frame_path)
    
    return frames

# Function to generate TTS audio
def generate_audio(script_text, audio_path="news_audio.mp3"):
    tts = gTTS(script_text, lang="en")
    tts.save(audio_path)
    return audio_path

# Function to create the video from frames and audio
def create_video(frames, audio_path, output_video_path="news_video.mp4"):
    # Load frames into a video clip
    clip = ImageSequenceClip(frames, fps=10)
    
    # Add audio to the video
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    
    # Write the video to output file
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Main Streamlit function
def main():
    st.title("Cool Animated Anchor")
    st.markdown("### Type your news script below to generate an animated anchor!")

    # Input for news script
    news_script = st.text_area("Type or Paste News Script Below:")

    # Generate video button
    if st.button("Generate Video"):
        if not news_script.strip():
            st.warning("Please provide a valid script to generate the video!")
            return

        # Generate frames for the avatar with animations
        st.info("Generating avatar frames...")
        frames = create_animated_anchor(news_script)
        
        # Generate audio from the script
        st.info("Generating TTS audio...")
        audio_path = generate_audio(news_script)
        
        # Create video from frames and audio
        st.info("Creating video...")
        video_path = create_video(frames, audio_path)

        st.success("Video created successfully!")
        st.video(video_path)

# Run the Streamlit app
if __name__ == "__main__":
    main()
