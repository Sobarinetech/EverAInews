import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip
import pyttsx3
import os
import random

# Function to draw a simple avatar frame
def draw_avatar(mouth_state="closed", eye_state="open", hair_color="black", clothes_color="blue"):
    fig, ax = plt.subplots(figsize=(4, 6))
    # Head
    ax.add_patch(Ellipse((0.5, 0.75), width=0.6, height=0.8, color="peachpuff"))
    # Eyes
    eye_y = 0.85
    if eye_state == "closed":
        ax.plot([0.35, 0.45], [eye_y, eye_y], color="black", lw=2)
        ax.plot([0.55, 0.65], [eye_y, eye_y], color="black", lw=2)
    else:
        ax.add_patch(Ellipse((0.35, 0.85), width=0.1, height=0.2, color="white"))
        ax.add_patch(Ellipse((0.65, 0.85), width=0.1, height=0.2, color="white"))
        ax.add_patch(Ellipse((0.35, 0.85), width=0.05, height=0.1, color="black"))
        ax.add_patch(Ellipse((0.65, 0.85), width=0.05, height=0.1, color="black"))
    # Mouth
    if mouth_state == "open":
        ax.add_patch(Ellipse((0.5, 0.6), width=0.3, height=0.1, color="red"))
    else:
        ax.add_patch(Rectangle((0.35, 0.58), 0.3, 0.05, color="red"))
    # Hair
    ax.add_patch(Rectangle((0.25, 0.9), 0.5, 0.2, color=hair_color))
    # Clothes
    ax.add_patch(Rectangle((0.25, 0.1), 0.5, 0.5, color=clothes_color))
    # Adjust plot
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    plt.close(fig)
    img_path = f"frame_{mouth_state}_{eye_state}_{hair_color}_{clothes_color}.png"
    fig.savefig(img_path, dpi=100)
    return img_path

# Generate frames based on the script
def generate_frames(script, hair_color, clothes_color):
    frames = []
    for i, char in enumerate(script):
        mouth_state = "open" if i % 2 == 0 else "closed"
        eye_state = "open" if i % 5 != 0 else "closed"
        frame_path = draw_avatar(mouth_state, eye_state, hair_color, clothes_color)
        frames.append(frame_path)
    return frames

# Generate audio using pyttsx3
def generate_audio(script, audio_path="news_audio.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(script, audio_path)
    engine.runAndWait()
    return audio_path

# Create video with subtitles
def create_video(frames, audio_path, script, output_video="news_video.mp4", fps=10):
    clip = ImageSequenceClip(frames, fps=fps)
    text_clip = TextClip(script, fontsize=24, color="white", bg_color="black", size=(800, 100)).set_duration(clip.duration)
    video = CompositeVideoClip([clip, text_clip.set_position(("center", "bottom"))])
    video.write_videofile(output_video, codec="libx264", audio_codec="aac")
    return output_video

# Streamlit app main function
def main():
    st.title("News Avatar Video Generator")
    st.write("Generate a dynamic news avatar video with audio narration.")
    
    # Input script
    script = st.text_area("Enter the news script here:", "")
    fps = st.slider("Frames per second (FPS):", 5, 30, 10)
    hair_color = st.color_picker("Select hair color")
    clothes_color = st.color_picker("Select clothes color")
    
    # Generate video button
    if st.button("Generate Video"):
        if not script.strip():
            st.warning("Please enter a valid script.")
            return
        
        # Generate frames
        st.info("Generating frames...")
        frames = generate_frames(script, hair_color, clothes_color)
        
        # Generate audio
        st.info("Generating audio
