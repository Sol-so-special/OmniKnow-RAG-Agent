import streamlit as st
import html
from io import BytesIO
import base64
from PIL import Image, ImageSequence
from pathlib import Path

@st.cache_data
def slow_down_gif(gif_path: str) -> str:
    """Slows down a GIF animation by increasing frame duration."""
    
    img = Image.open(gif_path)
    frames = []
    durations = []
    factor = 50  # Slowdown factor

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.copy())
        durations.append(frame.info.get("duration", 100) * factor)

    # Write slowed GIF to memory
    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2
    )
    buffer.seek(0)

    # Encode to base64
    gif_b64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/gif;base64,{gif_b64}"

def apply_styling():
    """Injects custom CSS for UI styling."""
    
    # Get GIF path
    gif_path = Path(__file__).parent / "background.gif"
    
    if gif_path.exists():
        slowed_gif = slow_down_gif(str(gif_path))
    else:
        slowed_gif = ""
    
    st.markdown(
        f"""
        <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: #001a0f !important;
        }}

        /* Background GIF */
        .stApp {{
            background-image: url('{slowed_gif}') !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
            background-size: cover !important;
        }}

        /* Transparent chat container */
        [data-testid="stChatMessageContainer"] {{
            background: transparent !important;
        }}

        /* User message bubble */
        .user-box {{
            background-color: #2f2f2f;
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            margin-left: 10%;
            margin-right: 5px;
            text-align: left;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }}

        /* AI message bubble */
        .ai-box {{
            background-color: #1a1a1a;
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            margin-right: 10%;
            margin-left: 5px;
            text-align: left;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }}

        /* Message header */
        .chat-header {{
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 8px;
            color: #4CAF50;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True
    )

def render_user_message(message: str):
    """Render user chat bubble."""
    st.markdown(
        f"""
        <div class="user-box">
            <div class="chat-header">👤 USER</div>
            {html.escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_ai_message(message: str):
    """Render AI chat bubble."""
    st.markdown(
        f"""
        <div class="ai-box">
            <div class="chat-header">🤖 OmniKnow</div>
            {html.escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )