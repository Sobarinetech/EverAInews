import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

# Function to create a basic 3D-like avatar
def draw_avatar(mouth_state="closed"):
    # Create a figure
    fig, ax = plt.subplots(figsize=(4, 6))

    # Draw the head
    head = Ellipse((0.5, 0.75), width=0.6, height=0.8, color="peachpuff", zorder=1)
    ax.add_patch(head)

    # Draw the eyes
    left_eye = Ellipse((0.35, 0.85), width=0.1, height=0.2, color="white", zorder=2)
    right_eye = Ellipse((0.65, 0.85), width=0.1, height=0.2, color="white", zorder=2)
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)

    # Draw pupils
    left_pupil = Ellipse((0.35, 0.85), width=0.05, height=0.1, color="black", zorder=3)
    right_pupil = Ellipse((0.65, 0.85), width=0.05, height=0.1, color="black", zorder=3)
    ax.add_patch(left_pupil)
    ax.add_patch(right_pupil)

    # Draw the nose
    nose = Rectangle((0.475, 0.7), width=0.05, height=0.1, color="sienna", zorder=4)
    ax.add_patch(nose)

    # Draw the mouth
    if mouth_state == "open":
        mouth = Ellipse((0.5, 0.6), width=0.3, height=0.1, color="red", zorder=5)
    else:  # Closed mouth
        mouth = Rectangle((0.35, 0.59), width=0.3, height=0.05, color="red", zorder=5)
    ax.add_patch(mouth)

    # Draw the body
    body = Rectangle((0.25, 0.1), width=0.5, height=0.5, color="navy", zorder=1)
    ax.add_patch(body)

    # Set up the plot
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    ax.axis("off")
    plt.close(fig)  # Close the plot to prevent duplicate rendering
    return fig

# Function to animate the avatar based on the news script
def animate_avatar(script_text):
    st.markdown("## Animation in Progress")
    if not script_text.strip():
        st.warning("Please provide a valid news script to start the animation.")
        return

    # Loop through the script text and animate mouth movement
    for i, char in enumerate(script_text):
        mouth_state = "open" if i % 2 == 0 else "closed"  # Alternate mouth state
        fig = draw_avatar(mouth_state)
        st.pyplot(fig)  # Render the avatar
        time.sleep(0.1)  # Adjust animation speed

# Main application function
def main():
    st.title("News Anchor 3D Avatar Simulation")
    st.markdown(
        """
        This app simulates a 3D-like avatar reading a script with animated mouth movements.
        Type or paste your news script below to start the animation.
        """
    )

    # Input for the news script
    news_script = st.text_area("Type or Paste the News Script Below:")

    # Button to start the animation
    if st.button("Start Animation"):
        animate_avatar(news_script)

# Entry point of the script
if __name__ == "__main__":
    main()
