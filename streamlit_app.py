import os
import textwrap
import wave
import pyaudio
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp

# Create speech using pyaudio and wave
def text_to_speech(script, audio_file='output_audio.wav'):
    # Set parameters for audio file
    sample_rate = 44100
    volume = 1.0
    channels = 1
    frame_rate = 256

    # Initialize text-to-speech engine (pyaudio)
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, output=True)

    # Prepare text as audio output (mock implementation, replace with actual TTS model)
    # In this implementation, we are skipping actual text-to-speech, and we assume the script is being synthesized as an audio file.

    # Save a basic silent audio file for testing
    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(b'\0' * int(sample_rate * 2 * len(script.split())))

    # Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

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
def create_video_with_audio(script, audio_file='output_audio.wav', output_video='output_video.mp4'):
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
