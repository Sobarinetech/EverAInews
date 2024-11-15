import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from moviepy.editor import ImageSequenceClip, AudioFileClip, TextClip, CompositeVideoClip
from gtts import gTTS
from PIL import Image

# Function to create a customizable avatar frame
def draw_avatar(mouth_state="closed", face_color="peachpuff", eye_color="white", pupil_color="black", clothing_color="navy"):
    fig, ax = plt.subplots(figsize=(4, 6))
    
    # Head
    head = Ellipse((0.5, 0.75), width=0.6, height=0.8, color=face_color, zorder=1)
    ax.add_patch(head)

    # Eyes
    left_eye = Ellipse((0.35, 0.85), width=0.1, height=0.2, color=eye_color, zorder=2)
    right_eye = Ellipse((0.65, 0.85), width=0.1, height=0.2, color=eye_color, zorder=2)
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Pupils
    left_pupil = Ellipse((0.35, 0.85), width=0.05, height=0.1, color=pupil_color, zorder=3)
    right_pupil = Ellipse((0.65, 0.85), width=0.05, height=0.1, color=pupil_color, zorder=3)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)

    # Nose
    nose = Rectangle((0.475, 0.7), width=0.05, height=0.1, color="sienna", zorder=4)
    ax.add_patch(nose)

    # Mouth
    if mouth_state == "open":
        mouth = Ellipse((0.5, 0.6), width=0.3, height=0.1, color="red", zorder=5)
    else:
        mouth = Rectangle((0.35, 0.59), width=0.3, height=0.05, color="red", zorder=5)
    ax.add_patch(mouth)

    # Body
    body = Rectangle((0.25, 0.1), width=0.5, height=0.5, color=clothing_color, zorder=1)
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

# Function to generate frames for video
def generate_frames(script_text, face_color, eye_color, pupil_color, clothing_color):
    frames = []
    for i, char in enumerate(script_text):
        mouth_state = "open" if i % 2 == 0 else "closed"
        frame_path = draw_avatar(mouth_state, face_color, eye_color, pupil_color, clothing_color)
        frames.append(frame_path)
    return frames

# Function to generate TTS audio
def generate_audio(script_text, audio_path="news_audio.mp3", lang="en", speed=1.0):
    tts = gTTS(script_text, lang=lang)
    tts.save(audio_path)
    return audio_path

# Function to create video with subtitles
def create_video(frames, audio_path, script_text, output_video_path="news_video.mp4", fps=10):
    # Load frames into a clip
    clip = ImageSequenceClip(frames, fps=fps)

    # Add audio to the clip
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)

    # Add subtitles
    subtitle = TextClip(script_text, fontsize=24, color='white', bg_color="black", size=clip.size).set_duration(audio.duration)
    final_video = CompositeVideoClip([video, subtitle.set_position(("center", "bottom"))])

    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Streamlit app main function
def main():
    st.title("Dynamic News Avatar Video Generator")
    st.markdown("### Customize your news-reading avatar and generate engaging videos!")

    # Input for news script
    news_script = st.text_area("Type or Paste News Script Below:")

    # Avatar customization options
    st.markdown("#### Avatar Customization")
    face_color = st.color_picker("Choose Face Color", "#FFDAB9")
    eye_color = st.color_picker("Choose Eye Color", "#FFFFFF")
    pupil_color = st.color_picker("Choose Pupil Color", "#000000")
    clothing_color = st.color_picker("Choose Clothing Color", "#000080")

    # TTS customization options
    st.markdown("#### TTS Customization")
    lang = st.selectbox("Select Language", ["en", "es", "fr", "de", "hi"])
    speed = st.slider("Select Speech Speed", 0.5, 2.0, 1.0)

    # Video customization
    st.markdown("#### Video Customization")
    fps = st.slider("Frames per Second (FPS)", 5, 30, 10)

    # Background upload
    bg_image = st.file_uploader("Upload Background Image (Optional)", type=["jpg", "png"])

    # Generate video button
    if st.button("Generate Video"):
        if not news_script.strip():
            st.warning("Please provide a valid script to generate the video!")
            return

        # Generate frames
        st.info("Generating avatar frames...")
        frames = generate_frames(news_script, face_color, eye_color, pupil_color, clothing_color)

        # Generate audio
        st.info("Generating TTS audio...")
        audio_path = generate_audio(news_script, lang=lang, speed=speed)

        # Create video
        st.info("Creating video...")
        video_path = create_video(frames, audio_path, news_script, fps=fps)

        st.success("Video created successfully!")
        st.video(video_path)

# Run the Streamlit app
if __name__ == "__main__":
    main()
