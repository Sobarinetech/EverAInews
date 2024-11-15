import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
import textwrap
from gtts import gTTS
import moviepy.editor as mp

# Function to create the video from the text
def create_video_with_audio(script, avatar_image_path):
    # 1. Generate the audio
    audio_file = generate_audio(script)

    # 2. Create video frames with subtitles
    frames = add_subtitles_to_frames(script, avatar_image_path)

    # 3. Combine audio and video into a final output video
    video_file = combine_audio_and_video(frames, audio_file)

    return video_file

# Function to generate audio from the text using gTTS
def generate_audio(script):
    audio_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

    # Using gTTS to convert text to speech
    tts = gTTS(text=script, lang='en')
    tts.save(audio_file_path)

    return audio_file_path

# Function to add subtitles to video frames
def add_subtitles_to_frames(script, avatar_image_path):
    frames = []
    avatar_image = Image.open(avatar_image_path)
    font = ImageFont.load_default()  # Use default font for simplicity

    for i, line in enumerate(script.splitlines()):
        # Create a new image for each frame
        img = avatar_image.copy()  # Use the avatar image for the frame
        draw = ImageDraw.Draw(img)

        # Wrap text to fit the frame
        wrapped_text = textwrap.fill(line, width=50)
        w, h = draw.textsize(wrapped_text, font=font)

        # Position the text at the bottom of the frame
        text_position = ((img.width - w) // 2, img.height - h - 20)
        draw.text(text_position, wrapped_text, font=font, fill="white")

        # Save frame as a temporary image file
        frame_path = f"frame_{i}.png"
        img.save(frame_path)
        frames.append(frame_path)

    return frames

# Function to combine audio and video into a final video file
def combine_audio_and_video(frames, audio_file):
    # Create a list of video clips
    clips = []
    for frame in frames:
        clip = mp.ImageClip(frame, duration=2)  # Each frame lasts 2 seconds
        clips.append(clip)

    # Concatenate clips into a video
    video = mp.concatenate_videoclips(clips, method="compose")

    # Set audio for the video
    audio = mp.AudioFileClip(audio_file)
    video = video.set_audio(audio)

    # Save final video
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    video.write_videofile(output_file.name, fps=24)

    # Clean up frame images
    for frame in frames:
        os.remove(frame)

    return output_file.name

# Streamlit UI
def run_streamlit_app():
    st.title("Text-to-Video with Avatar and Subtitles")

    # Input text (script)
    script = st.text_area("Enter the script for the video:", height=300)

    # Upload avatar image
    avatar_image = st.file_uploader("Upload an avatar image:", type=["png", "jpg", "jpeg"])

    if script and avatar_image:
        avatar_image_path = save_uploaded_file(avatar_image)

        # Create video with audio and avatar
        video_file = create_video_with_audio(script, avatar_image_path)

        st.video(video_file)

# Function to save uploaded file to temporary directory
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name

# Run Streamlit app
if __name__ == "__main__":
    run_streamlit_app()
