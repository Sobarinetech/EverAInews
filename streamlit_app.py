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
def create_animated_avatar(script_text, uploaded_image):
    # Load the uploaded image (resize to fit the avatar body)
    img = Image.open(uploaded_image)
    img = img.resize((300, 300))  # Resize to avatar size

    # Avatar base (blank canvas)
    avatar_canvas = np.ones((500, 500, 3), dtype=np.uint8) * 255  # White background canvas
    
    # Add the uploaded face to the canvas
    avatar_canvas[100:400, 100:400] = np.array(img)
    
    # Add basic animations (mouth opening, eyes blinking, etc.)
    frames = []
    for i in range(len(script_text)):
        frame = avatar_canvas.copy()
        
        # Randomize mouth opening/closing for a cool effect
        mouth_opening = random.choice([True, False])
        mouth_position = (300, 350, 350, 380) if mouth_opening else (300, 360, 350, 370)
        
        # Draw mouth
        cv2.rectangle(frame, (mouth_position[0], mouth_position[1]), (mouth_position[2], mouth_position[3]), (0, 0, 255), -1)
        
        # Random eye movement for a cool animated effect
        eye_position_left = (230, 230) if random.choice([True, False]) else (240, 230)
        eye_position_right = (270, 230) if random.choice([True, False]) else (260, 230)
        
        cv2.circle(frame, eye_position_left, 10, (0, 0, 0), -1)  # Left eye
        cv2.circle(frame, eye_position_right, 10, (0, 0, 0), -1)  # Right eye
        
        # Add the current frame to the frames list
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
    st.title("Cool Animated Avatar with News Script")
    st.markdown("### Upload your image and paste your news script below to generate an animated avatar!")

    # Image upload option
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        # Display uploaded image
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Input for news script
        news_script = st.text_area("Type or Paste News Script Below:")
        
        # Generate video button
        if st.button("Generate Video"):
            if not news_script.strip():
                st.warning("Please provide a valid script to generate the video!")
                return

            # Generate frames for the avatar with animations
            st.info("Generating avatar frames...")
            frames = create_animated_avatar(news_script, uploaded_image)
            
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
