import streamlit as st
import numpy as np
import cv2
import random
from gtts import gTTS
import os
from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image
import time

# Function to create a refined and realistic cartoon avatar with advanced features and animations
def create_animated_avatar(script_text):
    frames = []
    for i in range(len(script_text)):
        avatar_canvas = np.ones((500, 500, 3), dtype=np.uint8) * 255  # White background canvas

        # Draw face
        face_x = random.randint(150, 350)
        face_y = random.randint(100, 300)
        face_radius = random.randint(60, 120)
        cv2.circle(avatar_canvas, (face_x, face_y), face_radius, (random.randint(150, 255), random.randint(100, 200), 255), -1)  # Basic face

        # Draw eyes with random movement
        eye1_x = face_x - random.randint(30, 50)
        eye1_y = face_y - random.randint(10, 20)
        eye2_x = face_x + random.randint(30, 50)
        eye2_y = face_y - random.randint(10, 20)
        cv2.ellipse(avatar_canvas, (eye1_x, eye1_y), (15, 10), 0, 0, 360, (0, 0, 0), -1)  # Left eye
        cv2.ellipse(avatar_canvas, (eye2_x, eye2_y), (15, 10), 0, 0, 360, (0, 0, 0), -1)  # Right eye

        # Draw mouth with slight movement based on script
        mouth_x = face_x
        mouth_y = face_y + random.randint(30, 50)
        mouth_width = random.randint(30, 60)
        mouth_height = random.randint(8, 15)
        cv2.ellipse(avatar_canvas, (mouth_x, mouth_y), (mouth_width, mouth_height), 0, 0, 180, (random.randint(0, 100), random.randint(0, 100), random.randint(100, 255)), -1)

        # Add random blink effect (Eye animation)
        if random.random() < 0.1:  # 10% chance of blink
            cv2.ellipse(avatar_canvas, (eye1_x, eye1_y), (15, 5), 0, 0, 180, (0, 0, 0), -1)  # Blink left eye
            cv2.ellipse(avatar_canvas, (eye2_x, eye2_y), (15, 5), 0, 0, 180, (0, 0, 0), -1)  # Blink right eye

        # Hand gesture (Simple animation)
        if random.random() < 0.05:  # 5% chance to show hand gestures
            hand_x = random.randint(50, 450)
            hand_y = random.randint(350, 450)
            cv2.rectangle(avatar_canvas, (hand_x - 20, hand_y - 20), (hand_x + 20, hand_y + 20), (0, 0, 255), -1)

        # Adding accessories (random)
        if random.random() < 0.3:  # 30% chance of adding accessories like glasses or hats
            # Add hat
            hat_x = face_x
            hat_y = face_y - face_radius - random.randint(10, 30)
            hat_width = random.randint(60, 120)
            hat_height = random.randint(20, 50)
            cv2.ellipse(avatar_canvas, (hat_x, hat_y), (hat_width, hat_height), 0, 0, 360, (random.randint(100, 200), random.randint(0, 100), random.randint(0, 255)), -1)

            # Add glasses
            glass_x = face_x
            glass_y = face_y - random.randint(20, 40)
            glass_width = random.randint(40, 80)
            glass_height = random.randint(10, 20)
            cv2.ellipse(avatar_canvas, (glass_x, glass_y), (glass_width, glass_height), 0, 0, 360, (random.randint(0, 50), random.randint(0, 100), random.randint(0, 150)), -1)

        # Add some background effects (random weather, colors, etc.)
        if random.random() < 0.1:  # 10% chance of weather effect
            avatar_canvas[:, :, :] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color background
            if random.random() < 0.5:
                avatar_canvas = cv2.putText(avatar_canvas, "Rainy", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

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
                st.video(video_path)

                # Clean up generated files
                for frame in frames:
                    os.remove(frame)
                os.remove(audio_path)

        else:
            st.warning("Please enter a script to generate the video.")

if __name__ == "__main__":
    main()
