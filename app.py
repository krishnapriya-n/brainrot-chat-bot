import os
import streamlit as st
import pyrebase
import requests
from config import firebaseConfig
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner.script_runner import RerunData

# Page configuration
st.set_page_config(
    page_title="Brainrot Chat Bot",
    page_icon="🧠",
    layout="wide",
)

#Pybase setup
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def login():
    try:
        email = st.session_state.login_email_main
        password = st.session_state.login_password_main
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state.user = user
        st.success('Login successful!')

    except Exception as e:
        st.error('Error logging in')

def signup():
    try:
        email = st.session_state.signup_email_main
        password = st.session_state.signup_password_main
        user = auth.create_user_with_email_and_password(email, password)
        st.session_state.user = user
        st.success('Account created successfully!')
    except Exception as e:
        st.error(f'Error creating account: {str(e)}')

def google_login():
    try:
       redirect_uri = "http://localhost:8501"
       client_id = firebaseConfig.get('clientId')
       
       auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            "response_type=code&"
            "scope=openid%20email%20profile&"
            "access_type=offline&"
            "state=state_parameter_passthrough_value&"
            "include_granted_scopes=true&"
            "prompt=consent"         
        )
       
        # Creating Google Sign in Styling
       st.markdown(f"""
            <a href="{auth_url}" target="_self">
                <button style="
                    background-color: white;
                    color: #757575;
                    padding: 10px 20px;
                    border: 1px solid #757575;
                    border-radius: 5px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    width: 100%;
                    justify-content: center;
                    margin: 5px 0;">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" height="18">
                    Sign in with Google
                </button>
            </a>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f'Error setting up Google Login: {str(e)}')

def handle_google_callback():
    try:
        query_params = st.query_params
        if 'code' in query_params:
            try:
                st.session_state.user = {'auth_code': query_params['code'][0]}
                st.success('Successfully logged in with Google!')
                st.query_params.clear()
                return True
            except Exception as e:
                st.error(f'Error processing Google login: {str(e)}')
                return False    
        return False
    except Exception as e:
       st.error(f'Error handling Google callback: {str(e)}')
       return False

# Load CSS file and apply dark mode if enabled
with open("style.css") as css:
    css_content = css.read()
    if st.session_state.dark_mode:
        css_content += """
        /* Dark mode styles */
        .main {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        .auth-container, .auth-box, .chat-container, .mode-description, .welcome-text {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        .welcome-text h2, .auth-box h3 {
            color: #ffffff !important;
        }
        .welcome-text {
            background: linear-gradient(45deg, #2d2d2d, #1a1a1a) !important;
        }
        .chat-bubble.bot-message {
            background: #3d3d3d;
            color: #ffffff;
        }
        .stTextInput > div > div {
            background-color: #3d3d3d !important;
            color: #ffffff !important;
        }
        .top-card {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        """
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Top Bar Section
col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
with col1:
    st.markdown("<div class='top-card'>Leaderboard</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='top-card'>Friends</div>", unsafe_allow_html=True)
with col3:
    if handle_google_callback():
        st.rerun()

    if st.session_state.user:
        st.markdown("<div class='top-right-card'><b>Welcome!</b></div>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state['logout_trigger'] = True
            raise RerunException(RerunData(None))

with col4:
    toggle_container = st.container()
    with toggle_container:
        col_left, col_toggle, col_right = st.columns([1, 2, 1])
        with col_left:
            st.image("static/assets/moon.png", width=30)
        with col_toggle:
            dark_mode = st.checkbox('', value=st.session_state.dark_mode, key='dark_mode_toggle', on_change=toggle_dark_mode)
        with col_right:
            st.image("static/assets/light.png", width=30)

# Title Section
st.markdown("<div class='title'>Brainrot Chat Bot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your Favorite Study Buddy</div>", unsafe_allow_html=True)

# Main Content Section
if not st.session_state.user:
    # Authentication container
    auth_container = st.container()
    with auth_container:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        
        # Welcome message
        st.markdown("""
            <div class='welcome-text'>
                <h2>Welcome to Your AI Study Companion! 📚</h2>
                <p>Join us to start your interactive learning journey with our intelligent tutoring system.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Two-column layout for login and signup
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
            st.markdown("<h3>Login</h3>", unsafe_allow_html=True)
            with st.form("login_form_main"):
                st.text_input("Email", key="login_email_main", placeholder="Enter your email")
                st.text_input("Password", type="password", key="login_password_main", placeholder="Enter your password")
                if st.form_submit_button("Login", use_container_width=True):
                    login()
            st.markdown("<div class='separator'>OR</div>", unsafe_allow_html=True)
            google_login()
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
            st.markdown("<h3>Sign Up</h3>", unsafe_allow_html=True)
            with st.form("signup_form"):
                st.text_input("Email", key="signup_email_main", placeholder="Enter your email")
                st.text_input("Password", type="password", key="signup_password_main", placeholder="Choose a password")
                if st.form_submit_button("Sign Up", use_container_width=True):
                    signup()
            st.markdown("<div class='separator'>OR</div>", unsafe_allow_html=True)
            google_login()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Chat Interface
    if "chat_mode" not in st.session_state:
        st.session_state.chat_mode = "tutor"

    # Mode Selection
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("<div class='mode-selector'>", unsafe_allow_html=True)
        st.session_state.chat_mode = st.selectbox(
            "Study Mode",
            ["tutor", "rubber_duck"],
            format_func=lambda x: "👩‍🏫 Tutor Mode" if x == "tutor" else "🦆 Rubber Duck Mode"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Mode description
    if st.session_state.chat_mode == "rubber_duck":
        st.markdown("""
            <div class='mode-description duck'>
                🦆 <strong>Rubber Duck Mode:</strong> Teach me about any topic! I'll ask questions to help deepen your understanding.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='mode-description tutor'>
                👩‍🏫 <strong>Tutor Mode:</strong> I'll help explain concepts in a fun and engaging way!
            </div>
        """, unsafe_allow_html=True)

    
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Render messages using Streamlit's native components with custom HTML
for msg in st.session_state["messages"]:
    if msg.startswith("You: "):
        message_content = msg[4:]
        st.markdown(f'<div class="chat-bubble user-message">{message_content}</div>', unsafe_allow_html=True)
    elif msg.startswith("Bot: "):
        message_content = msg[4:]
        st.markdown(f'<div class="chat-bubble bot-message">{message_content}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Chat Input
with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_button = st.columns([6, 1])
    with col_input:
        user_input = st.text_input(
            "Type your message...",
            key="chat_input",
            placeholder="Share your knowledge or ask a question..."
        )
    with col_button:
        submit_button = st.form_submit_button("Send 📤")

    if submit_button and user_input:
        st.session_state["messages"].append(f"You: {user_input}")
        
        try:
            response = requests.post(
                "http://localhost:5000/chat",
                json={
                    "message": user_input,
                    "history": st.session_state["messages"],
                    "mode": st.session_state.chat_mode
                }
            )
            
            if response.status_code == 200:
                bot_response = response.json()["response"]
                st.session_state["messages"].append(f"Bot: {bot_response}")
            else:
                st.error("Failed to get response from the bot. Please try again.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.rerun()
