import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
import numpy as np
import pyttsx3
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import ImageSequenceClip, AudioFileClip
import streamlit as st

# Step 1: Function to draw a human-like avatar with mouth animation
def draw_avatar(mouth_state="closed"):
    fig, ax = plt.subplots(figsize=(4, 6))

    # Head
    head = Ellipse((0.5, 0.75), width=0.6, height=0.8, color="peachpuff", zorder=1)
    ax.add_patch(head)

    # Eyes (simple circular eyes)
    left_eye = Ellipse((0.35, 0.85), width=0.1, height=0.2, color="white", zorder=2)
    right_eye = Ellipse((0.65, 0.85), width=0.1, height=0.2, color="white", zorder=2)
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Pupils
    left_pupil = Ellipse((0.35, 0.85), width=0.05, height=0.1, color="black", zorder=3)
    right_pupil = Ellipse((0.65, 0.85), width=0.05, height=0.1, color="black", zorder=3)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)

    # Nose (simplified)
    nose = Rectangle((0.475, 0.7), width=0.05, height=0.1, color="sienna", zorder=4)
    ax.add_patch(nose)

    # Mouth (open or closed)
    if mouth_state == "open":
        mouth = Ellipse((0.5, 0.6), width=0.3, height=0.1, color="red", zorder=5)
    else:
        mouth = Rectangle((0.35, 0.59), width=0.3, height=0.05, color="red", zorder=5)
    ax.add_patch(mouth)

    # Body
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

# Step 2: Function to generate audio using TTS
def generate_audio(script_text, audio_path="news_audio.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(script_text, audio_path)
    engine.runAndWait()
    return audio_path

# Step 3: Function to get phonemes from the audio
def get_phonemes_from_audio(audio_path):
    recognizer = sr.Recognizer()
    sound = AudioSegment.from_mp3(audio_path)

    # Split audio into phoneme-level segments (or approximate)
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio = recognizer.record(source)
        phonemes = recognizer.recognize_google(audio, show_all=True)
    
    return phonemes

# Step 4: Function to generate frames for the avatar based on phonemes
def generate_frames(script_text, phonemes):
    frames = []
    for i, phoneme in enumerate(phonemes):
        mouth_state = "open" if phoneme in ['A', 'E', 'O'] else "closed"
        frame_path = draw_avatar(mouth_state)
        frames.append(frame_path)
    return frames

# Step 5: Function to create a video using the frames and audio
def create_video(frames, audio_path, output_video_path="news_video.mp4"):
    # Load frames into a clip
    clip = ImageSequenceClip(frames, fps=10)
    
    # Add audio to the clip
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Streamlit integration to build the web interface
def main():
    st.title("Realistic Human-like News Anchor with Video Generation")
    st.markdown("### Paste your news script below to generate an avatar video with narration!")

    news_script = st.text_area("Type or Paste News Script Below:")

    if st.button("Generate Video"):
        if not news_script.strip():
            st.warning("Please provide a valid script to generate the video!")
            return

        # Step 6: Generate TTS audio
        st.info("Generating TTS audio...")
        audio_path = generate_audio(news_script)

        # Step 7: Generate phonemes for lip-syncing
        phonemes = get_phonemes_from_audio(audio_path)

        # Step 8: Generate frames based on phonemes
        st.info("Generating avatar frames...")
        frames = generate_frames(news_script, phonemes)
        
        # Step 9: Create video
        st.info("Creating video...")
        video_path = create_video(frames, audio_path)

        st.success("Video created successfully!")
        st.video(video_path)

if __name__ == "__main__":
    main()
