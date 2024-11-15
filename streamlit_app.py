import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
from PIL import Image

# Function to create an avatar frame with customizable features
def draw_avatar(mouth_state="closed", hair_color="brown", eye_shape="round", clothing_color="navy"):
    fig, ax = plt.subplots(figsize=(4, 6))
    
    # Head
    head = Ellipse((0.5, 0.75), width=0.6, height=0.8, color="peachpuff", zorder=1)
    ax.add_patch(head)

    # Hair
    hair = Ellipse((0.5, 1.05), width=0.6, height=0.2, color=hair_color, zorder=2)
    ax.add_patch(hair)

    # Eyes with customizable shape
    if eye_shape == "round":
        left_eye = Ellipse((0.35, 0.85), width=0.1, height=0.2, color="white", zorder=3)
        right_eye = Ellipse((0.65, 0.85), width=0.1, height=0.2, color="white", zorder=3)
    else:
        left_eye = Ellipse((0.35, 0.85), width=0.15, height=0.1, color="white", zorder=3)
        right_eye = Ellipse((0.65, 0.85), width=0.15, height=0.1, color="white", zorder=3)
    
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Pupils
    left_pupil = Ellipse((0.35, 0.85), width=0.05, height=0.1, color="black", zorder=4)
    right_pupil = Ellipse((0.65, 0.85), width=0.05, height=0.1, color="black", zorder=4)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)

    # Nose
    nose = Rectangle((0.475, 0.7), width=0.05, height=0.1, color="sienna", zorder=5)
    ax.add_patch(nose)

    # Mouth
    if mouth_state == "open":
        mouth = Ellipse((0.5, 0.6), width=0.3, height=0.1, color="red", zorder=6)
    else:
        mouth = Rectangle((0.35, 0.59), width=0.3, height=0.05, color="red", zorder=6)
    ax.add_patch(mouth)

    # Body with customizable clothing
    body = Rectangle((0.25, 0.1), width=0.5, height=0.5, color=clothing_color, zorder=1)
    ax.add_patch(body)

    # Plot adjustments
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    ax.axis("off")
    plt.close(fig)

    # Save the figure as an image
    img_path = f"frame_{mouth_state}_{hair_color}_{eye_shape}_{clothing_color}.png"
    fig.savefig(img_path, bbox_inches="tight", dpi=100)
    return img_path

# Function to generate frames for video
def generate_frames(script_text, hair_color, eye_shape, clothing_color):
    frames = []
    for i, char in enumerate(script_text):
        mouth_state = "open" if i % 2 == 0 else "closed"
        frame_path = draw_avatar(mouth_state, hair_color, eye_shape, clothing_color)
        frames.append(frame_path)
    return frames

# Function to generate TTS audio with gender/accent options
def generate_audio(script_text, gender="female", audio_path="news_audio.mp3"):
    tts = gTTS(script_text, lang="en", slow=False, tld='com' if gender == "female" else 'co.uk')
    tts.save(audio_path)
    return audio_path

# Function to create the video with adjustable speed
def create_video(frames, audio_path, video_speed=1, output_video_path="news_video.mp4"):
    # Load frames into a clip
    clip = ImageSequenceClip(frames, fps=10 * video_speed)
    
    # Add audio to the clip
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Streamlit app main function
def main():
    st.title("News Anchor Avatar with Video Generation")
    st.markdown("### Paste your news script below to generate an avatar video with narration!")
    
    # Input for news script
    news_script = st.text_area("Type or Paste News Script Below:")
    
    # Avatar customization options
    hair_color = st.selectbox("Select Hair Color", ["brown", "black", "blonde", "red", "grey"])
    eye_shape = st.selectbox("Select Eye Shape", ["round", "oval"])
    clothing_color = st.selectbox("Select Clothing Color", ["navy", "red", "green", "blue"])
    
    # TTS options
    gender = st.selectbox("Select Voice Gender", ["female", "male"])
    
    # Video speed option
    video_speed = st.slider("Select Video Speed", min_value=0.5, max_value=2.0, value=1.0)
    
    # Background music option
    bg_music = st.checkbox("Add Background Music")
    
    # Generate video button
    if st.button("Generate Video"):
        if not news_script.strip():
            st.warning("Please provide a valid script to generate the video!")
            return

        # Generate frames
        with st.spinner("Generating avatar frames..."):
            frames = generate_frames(news_script, hair_color, eye_shape, clothing_color)
        
        # Generate audio
        with st.spinner("Generating TTS audio..."):
            audio_path = generate_audio(news_script, gender)
        
        # Optionally, add background music
        if bg_music:
            # Placeholder: Add your logic for background music here
            st.info("Background music feature is under development.")
        
        # Create video
        with st.spinner("Creating video..."):
            video_path = create_video(frames, audio_path, video_speed)

        st.success("Video created successfully!")
        st.video(video_path)
        
        # Allow video download
        with open(video_path, "rb") as file:
            st.download_button("Download Video", file, file_name="generated_video.mp4", mime="video/mp4")

# Run the Streamlit app
if __name__ == "__main__":
    main()
