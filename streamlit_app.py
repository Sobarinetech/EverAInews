import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip
import os

# Function to draw an avatar frame
def draw_avatar(mouth_state="closed", eye_state="open"):
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
    
    # Body
    ax.add_patch(Rectangle((0.25, 0.1), 0.5, 0.5, color="navy"))
    
    # Adjust plot
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    plt.close(fig)
    
    # Save the frame image
    img_path = f"frame_{mouth_state}_{eye_state}.png"
    fig.savefig(img_path, dpi=100)
    return img_path

# Function to generate avatar frames
def generate_frames(script):
    frames = []
    for i, char in enumerate(script):
        mouth_state = "open" if i % 2 == 0 else "closed"
        eye_state = "open" if i % 5 != 0 else "closed"
        frame_path = draw_avatar(mouth_state, eye_state)
        frames.append(frame_path)
    return frames

# Function to create a video with subtitles
def create_video(frames, script, output_video="news_video.mp4", fps=10):
    clip = ImageSequenceClip(frames, fps=fps)
    text_clip = TextClip(script, fontsize=24, color="white", bg_color="black", size=(800, 100)).set_duration(clip.duration)
    video = CompositeVideoClip([clip, text_clip.set_position(("center", "bottom"))])
    video.write_videofile(output_video, codec="libx264")
    return output_video

# Main function for Streamlit app
def main():
    st.title("Avatar News Video Generator")
    st.write("Create a dynamic news avatar video with subtitles.")

    # Input: News script
    script = st.text_area("Enter the news script here:", "")
    
    # Input: FPS slider
    fps = st.slider("Frames per second (FPS):", 5, 30, 10)

    # Generate video button
    if st.button("Generate Video"):
        if not script.strip():
            st.warning("Please enter a valid script.")
            return
        
        # Generate avatar frames
        st.info("Generating avatar frames...")
        frames = generate_frames(script)

        # Create video
        st.info("Creating video...")
        video_path = create_video(frames, script, fps=fps)

        # Display video
        st.success("Video generated successfully!")
        st.video(video_path)

        # Cleanup: Remove generated frame images
        for frame in frames:
            os.remove(frame)

# Run the Streamlit app
if __name__ == "__main__":
    main()
