import os
import textwrap
import pyttsx3
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
import numpy as np

# Initialize pyttsx3
engine = pyttsx3.init()

# Function to convert text to speech
def text_to_speech(script, audio_file='output_audio.mp3'):
    engine.save_to_file(script, audio_file)
    engine.runAndWait()

# Function to create image frames with text
def create_image_from_text(text, frame_num):
    width, height = 800, 600  # Set the size of the image
    img = Image.new('RGB', (width, height), color=(255, 255, 255))  # Create a blank white image
    draw = ImageDraw.Draw(img)
    
    # Load a default font (no need for paths or custom fonts)
    try:
        font = ImageFont.load_default()  # Use the default font available in PIL
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if not available
    
    # Wrap the text to fit within the image width
    wrapped_text = textwrap.fill(text, width=60)
    
    # Positioning and drawing text in the center
    w, h = draw.textsize(wrapped_text, font=font)
    text_position = ((width - w) // 2, (height - h) // 2)
    draw.text(text_position, wrapped_text, fill="black", font=font)
    
    # Save the image frame
    img.save(f"frame_{frame_num}.png")

# Function to add subtitles to frames
def add_subtitles_to_frames(script):
    frames = []
    for i, line in enumerate(script.splitlines()):
        create_image_from_text(line, i)
        frames.append(f"frame_{i}.png")
    
    return frames

# Function to create video with audio and subtitles
def create_video_with_audio(script, audio_file='output_audio.mp3', output_video='output_video.mp4'):
    # Generate the audio file from the script
    text_to_speech(script, audio_file)
    
    # Create frames for the video with subtitles
    frames = add_subtitles_to_frames(script)
    
    # Create video clip from frames
    clips = [mp.ImageClip(frame).set_duration(2) for frame in frames]
    video = mp.concatenate_videoclips(clips, method="compose")
    
    # Add audio to the video
    audio = mp.AudioFileClip(audio_file)
    video = video.set_audio(audio)
    
    # Write the final video to a file
    video.write_videofile(output_video, fps=24)

    # Clean up the frame images
    for frame in frames:
        os.remove(frame)

# Example script (you can replace this with your own script)
script = """
Welcome to the video!
This is an example script.
Enjoy the video and have fun.
"""

# Create video from the script
create_video_with_audio(script)
