import os
import random
import textwrap
from gtts import gTTS  # Google Text-to-Speech (no external dependencies needed)
from moviepy.editor import ImageSequenceClip, concatenate_videoclips, TextClip
from PIL import Image, ImageDraw, ImageFont

# Path where you want to store images and video
output_path = './output/'
os.makedirs(output_path, exist_ok=True)

def text_to_speech(script, audio_file_path):
    """
    Convert text to speech and save it as an audio file.
    """
    tts = gTTS(text=script, lang='en')
    tts.save(audio_file_path)

def create_image_from_text(text, frame_num, font_path=None):
    """
    Create an image with the given text overlay for each video frame.
    """
    width, height = 800, 600  # Set the size of the image
    img = Image.new('RGB', (width, height), color=(255, 255, 255))  # Create a blank white image
    draw = ImageDraw.Draw(img)
    
    # Load a font or use default if not specified
    try:
        font = ImageFont.truetype(font_path, 24)
    except IOError:
        font = ImageFont.load_default()  # Use default font if custom one is unavailable
    
    # Wrap the text to fit within the image width
    wrapped_text = textwrap.fill(text, width=60)
    
    # Positioning and drawing text in the center
    w, h = draw.textsize(wrapped_text, font=font)
    text_position = ((width - w) // 2, (height - h) // 2)
    draw.text(text_position, wrapped_text, fill="black", font=font)
    
    # Save the image frame
    img.save(os.path.join(output_path, f"frame_{frame_num}.png"))

def generate_video_from_frames(script, frame_rate=1, video_output="final_video.mp4"):
    """
    Generate a video from the list of images with subtitles from the script.
    """
    # Create frames from the script
    frames = []
    for i, word in enumerate(script.split()):
        frame_text = ' '.join(script.split()[:i + 1])  # Show incremental text
        create_image_from_text(frame_text, i)
        frames.append(os.path.join(output_path, f"frame_{i}.png"))

    # Create the video using the frames
    clip = ImageSequenceClip(frames, fps=frame_rate)
    clip.write_videofile(video_output, codec="libx264")

    # Optionally, clean up frame images
    for frame in frames:
        os.remove(frame)

def main():
    # Example script to use
    script = "This is an example script for generating a video with text-to-speech narration."
    
    # Step 1: Convert the script to speech
    audio_file_path = os.path.join(output_path, 'output_audio.mp3')
    text_to_speech(script, audio_file_path)

    # Step 2: Generate video from the script
    generate_video_from_frames(script, frame_rate=1)

    print(f"Video and audio have been generated successfully: {audio_file_path}")

if __name__ == '__main__':
    main()
