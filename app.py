import streamlit as st
import pyrebase
import firebase_admin
import firebase_admin 
import credentials, auth

# Page configuration
st.set_page_config(
    page_title="Brainrot Chat Bot",
    page_icon="🧠",
    layout="wide",
)

#Firebase Configuration
from config import firebaseConfig

#Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
            color: black;
            font-family: 'Comic Sans MS', 'Arial', sans-serif;
        }
        .main-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 20px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #8e44ad;
            text-align: center;
        }
        .chat-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
        }
        .chat-bubble {
            background: #85C1E9;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            max-width: 70%;
            color: white;
        }
        .chat-input {
            margin-top: 10px;
        }
        .top-right-card, .top-left-card {
            border-radius: 10px;
            padding: 15px;
            background: #F7DC6F;
            color: black;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Top bar cards
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("<div class='top-left-card'><b>Leaderboard</b></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='top-left-card'><b>Friends</b></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='top-right-card'><b>Sign Up</b></div>", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>Brainrot Chat Bot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your study companion</div>", unsafe_allow_html=True)

# Chatbox
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)

# Placeholder for chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.markdown(
        f"<div class='chat-bubble'>{msg}</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Input for the chatbox
with st.form(key="chat_form"):
    user_input = st.text_input("Let's study, buddy! B)", key="chat_input")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    st.session_state["messages"].append(user_input)
    st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)

