import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
import pyttsx3
import tempfile

# Function to convert text to speech and save as audio file
def text_to_speech(script, audio_file_path):
    engine = pyttsx3.init()
    engine.save_to_file(script, audio_file_path)
    engine.runAndWait()

# Function to add subtitles on frames
def add_subtitles_to_frames(frames, script):
    subtitle_frames = []
    font_size = 24
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    for i, frame_path in enumerate(frames):
        img = Image.open(frame_path)
        draw = ImageDraw.Draw(img)
        text = script[:i + 1]  # Show incremental text
        w, h = font.getsize(text)  # Calculate text width and height
        
        # Draw background for subtitle and the text itself
        draw.rectangle([0, img.height - 40, img.width, img.height], fill="black")
        draw.text(((img.width - w) // 2, img.height - 35), text, fill="white", font=font)
        
        subtitle_frame_path = f"subtitle_frame_{i}.png"
        img.save(subtitle_frame_path)
        subtitle_frames.append(subtitle_frame_path)
    
    return subtitle_frames

# Function to generate video from frames
def generate_video_from_frames(frames, video_file_path, fps=24):
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(video_file_path, codec="libx264")

# Main function to generate video with text-to-speech and subtitles
def create_video_with_script(script, video_file_path):
    # Step 1: Create temporary directory to store frames
    temp_dir = tempfile.mkdtemp()

    # Step 2: Convert script to audio and save
    audio_file_path = os.path.join(temp_dir, "output_audio.mp3")
    text_to_speech(script, audio_file_path)

    # Step 3: Generate frames for video (for simplicity, use a static image as a placeholder)
    frames = []
    for i in range(len(script)):
        # Create a placeholder image for each frame (this could be any image)
        img = Image.new('RGB', (640, 480), color='blue')
        frames.append(os.path.join(temp_dir, f"frame_{i}.png"))
        img.save(frames[i])

    # Step 4: Add subtitles to the frames
    subtitle_frames = add_subtitles_to_frames(frames, script)

    # Step 5: Generate the video from the subtitle frames
    generate_video_from_frames(subtitle_frames, video_file_path)

    # Clean up temporary files
    for frame in subtitle_frames:
        os.remove(frame)
    for frame in frames:
        os.remove(frame)

    print(f"Video saved to {video_file_path}")

# Example usage:
script = "This is an example script for the video. It will generate text-to-speech and subtitles for each frame."
video_file_path = "final_video.mp4"
create_video_with_script(script, video_file_path)
