import streamlit as st
import numpy as np
import cv2
import random
from gtts import gTTS
import os
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image
import time

# Function to create a cool cartoon avatar with basic animations
def create_animated_avatar(script_text):
    frames = []
    for i in range(len(script_text)):
        avatar_canvas = np.ones((500, 500, 3), dtype=np.uint8) * 255  # White background canvas

        # Draw face with random position and size
        face_x = random.randint(150, 350)
        face_y = random.randint(100, 300)
        face_radius = random.randint(50, 150)
        cv2.circle(avatar_canvas, (face_x, face_y), face_radius, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), -1)  # Face

        # Draw eyes with random position and size
        eye1_x = face_x - random.randint(20, 50)
        eye1_y = face_y - random.randint(20, 50)
        eye2_x = face_x + random.randint(20, 50)
        eye2_y = face_y - random.randint(20, 50)
        cv2.circle(avatar_canvas, (eye1_x, eye1_y), random.randint(5, 15), (0, 0, 0), -1)  # Left eye
        cv2.circle(avatar_canvas, (eye2_x, eye2_y), random.randint(5, 15), (0, 0, 0), -1)  # Right eye

        # Draw mouth with random position and size
        mouth_x = face_x
        mouth_y = face_y + random.randint(20, 50)
        mouth_width = random.randint(20, 50)
        mouth_height = random.randint(5, 15)
        cv2.rectangle(avatar_canvas, (mouth_x - mouth_width//2, mouth_y), (mouth_x + mouth_width//2, mouth_y + mouth_height), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), -1)

        # Add crazy animations
        if random.random() < 0.5:  # 50% chance of animation
            # Randomly change the background color
            avatar_canvas[:, :, :] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

            # Randomly draw a hat
            hat_x = face_x
            hat_y = face_y - face_radius - random.randint(10, 50)
            hat_width = random.randint(50, 100)
            hat_height = random.randint(10, 50)
            cv2.rectangle(avatar_canvas, (hat_x - hat_width//2, hat_y), (hat_x + hat_width//2, hat_y + hat_height), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), -1)

            # Randomly draw glasses
            glass_x = face_x
            glass_y = eye1_y + random.randint(10, 30)
            glass_width = random.randint(50, 100)
            glass_height = random.randint(5, 15)
            cv2.rectangle(avatar_canvas, (glass_x - glass_width//2, glass_y), (glass_x + glass_width//2, glass_y + glass_height), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), -1)

        # Add the current frame to the list of frames
        frame_path = f"frame_{i}.png"
        cv2.imwrite(frame_path, avatar_canvas)
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
    st.markdown("### Type your news script below:")
    
    # Input box for user to input script text
    script_text = st.text_area("Enter Script Here:", "Welcome to the news channel. Here's today's update...")

    if st.button("Generate Animated Video"):
        if script_text:
            with st.spinner('Creating animated video...'):
                # Generate animated avatar frames
                frames = create_animated_avatar(script_text)
                
                # Generate audio for the script
                audio_path = generate_audio(script_text)

                # Create video with the generated frames and audio
                video_path = create_video(frames, audio_path)
                
                st.success("Video Created Successfully!")

                # Display video
                video_file = open(video_path, "rb")
                video_bytes = video_file.read()
                st.video(video_bytes)
                
                # Clean up temporary files
                for frame in frames:
                    os.remove(frame)
                os.remove(audio_path)
                os.remove(video_path)
        else:
            st.error("Please enter a script text!")

if __name__ == "__main__":
    main()
