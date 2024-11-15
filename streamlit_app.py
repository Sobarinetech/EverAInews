import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Polygon
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
from PIL import Image

# Function to create a realistic avatar frame
def draw_avatar(mouth_state="closed"):
    fig, ax = plt.subplots(figsize=(4, 6))

    # Face shape (more rounded)
    face = Ellipse((0.5, 0.75), width=0.65, height=0.85, color="peachpuff", zorder=1, edgecolor="brown", lw=2)
    ax.add_patch(face)

    # Eyes (more realistic)
    left_eye = Ellipse((0.35, 0.85), width=0.12, height=0.18, color="white", zorder=2, edgecolor="black", lw=1)
    right_eye = Ellipse((0.65, 0.85), width=0.12, height=0.18, color="white", zorder=2, edgecolor="black", lw=1)
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Pupils (slightly bigger for realism)
    left_pupil = Ellipse((0.35, 0.85), width=0.06, height=0.08, color="black", zorder=3)
    right_pupil = Ellipse((0.65, 0.85), width=0.06, height=0.08, color="black", zorder=3)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)

    # Nose (more defined)
    nose = Polygon([(0.475, 0.7), (0.525, 0.7), (0.5, 0.65)], color="sienna", zorder=4)
    ax.add_patch(nose)

    # Mouth (more expressive)
    if mouth_state == "open":
        mouth = Ellipse((0.5, 0.6), width=0.3, height=0.1, color="red", zorder=5)
    else:
        mouth = Ellipse((0.5, 0.58), width=0.28, height=0.06, color="red", zorder=5)
    ax.add_patch(mouth)

    # Body (remains unchanged)
    body = Rectangle((0.25, 0.1), width=0.5, height=0.5, color="navy", zorder=1)
    ax.add_patch(body)

    # Plot adjustments
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    ax.axis("off")
    plt.close(fig)

    # Save the figure as an image
    img_path = f"frame_{mouth_state}.png"
    fig.savefig(img_path, bbox_inches="tight", dpi=100)
    return img_path

# Function to generate frames for video (remains the same)
def generate_frames(script_text):
    frames = []
    for i, char in enumerate(script_text):
        mouth_state = "open" if i % 2 == 0 else "closed"
        frame_path = draw_avatar(mouth_state)
        frames.append(frame_path)
    return frames

# Function to generate TTS audio (remains the same)
def generate_audio(script_text, audio_path="news_audio.mp3"):
    tts = gTTS(script_text, lang="en")
    tts.save(audio_path)
    return audio_path

# Function to create the video (remains the same)
def create_video(frames, audio_path, output_video_path="news_video.mp4"):
    # Load frames into a clip
    clip = ImageSequenceClip(frames, fps=10)
    
    # Add audio to the clip
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Streamlit app main function (remains the same)
def main():
    st.title("News Anchor Avatar with Video Generation")
    st.markdown("### Paste your news script below to generate an avatar video with narration!")
    
    # Input for news script
    news_script = st.text_area("Type or Paste News Script Below:")
    
    # Generate video button
    if st.button("Generate Video"):
        if not news_script.strip():
            st.warning("Please provide a valid script to generate the video!")
            return

        # Generate frames
        st.info("Generating avatar frames...")
        frames = generate_frames(news_script)
        
        # Generate audio
        st.info("Generating TTS audio...")
        audio_path = generate_audio(news_script)
        
        # Create video
        st.info("Creating video...")
        video_path = create_video(frames, audio_path)

        st.success("Video created successfully!")
        st.video(video_path)

# Run the Streamlit app
if __name__ == "__main__":
    main()
