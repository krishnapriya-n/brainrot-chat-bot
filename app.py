import os
import streamlit as st
import pyrebase
import requests
from config import firebaseConfig
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner.script_runner import RerunData

# Page configuration
st.set_page_config(
    page_title="Brainrot Chat Bot",  # Set the page title displayed in the browser tab
    page_icon="🧠",  # Set the page icon
    layout="wide",  # Set the layout to 'wide' to use the available space
)
#Pybase setup
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def login():
    try:
        email = st.session_state.login_email
        password = st.session_state.login_password
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state.user = user
        st.success('Login successful!')

    except Exception as e:
        st.error('Error logging in')

def signup():
    try:
        email = st.session_state.signup_email
        password = st.session_state.signup_password
        user = auth.create_user_with_email_and_password(email, password)
        st.session_state.user = user
        st.success('Account created successfully!')
        st.markdown("Already have an account? [Login here](#)", unsafe_allow_html=True)  # Added link to login
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
            "scope=openid%20email%20profile&"  # Added openid scope
            "access_type=offline&"
            "state=state_parameter_passthrough_value&"  # Added state parameter
            "include_granted_scopes=true&"  # Added include_granted_scopes
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

# Load CSS file to style the app (make sure to have a 'style.css' file in your project directory)
with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Top Bar Section: This section contains links or buttons for the app's main features
# Using st.columns to create columns for each element in the top bar
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
with col1:
    # Display the "Leaderboard" link/card
    st.markdown("<div class='top-card'>Leaderboard</div>", unsafe_allow_html=True)
with col2:
    # Display the "Friends" link/card
    st.markdown("<div class='top-card'>Friends</div>", unsafe_allow_html=True)
with col3:
    if handle_google_callback():
        st.rerun()

    if not st.session_state.user:
        with st.expander("Login"):
            st.text_input("Email", key="login_email")
            st.text_input("Password", type="password", key="login_password")
            st.button("Login", on_click=login)
            st.markdown('---')
            google_login()
        
        with st.expander("Sign Up"):
            st.text_input("Email", key="signup_email")
            st.text_input("Password", type="password", key="signup_password")
            st.button("Sign Up", key="signup_button", on_click=signup)
            st.markdown("Already have an account? [Click on the login section](#)", unsafe_allow_html=True)  # Moved link to login
            st.markdown('---')
            google_login()

    if 'logout_trigger' in st.session_state and st.session_state['logout_trigger']:
        del st.session_state['logout_trigger']
        st.rerun()  # Ensures rerun

    else:
        st.markdown("<div class='top-right-card'><b>Welcome!</b></div>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.user = None  # Clear user session
            st.session_state['logout_trigger'] = True
            raise RerunException(RerunData(None)) 

with col4:
    # Create a container with left and right images (moon for dark mode and sun for light mode)
    toggle_container = st.container()
    with toggle_container:
        col_left, col_toggle, col_right = st.columns([1, 2, 1])  # Adjusted width for columns
        with col_left:
            st.image("static/assets/moon.png", width=30)  # Moon image
        with col_toggle:
            # Toggle switch HTML for switching between dark and light mode
            st.markdown(""" 
                <label class="switch">
                    <input type="checkbox" id="dark-mode-toggle">
                    <span class="slider round"></span>
                </label>
            """, unsafe_allow_html=True)
        with col_right:
            st.image("static/assets/light.png", width=30)  # Sun image
with col5:
    # Display the "Sign Up" link/card and redirect to the sign up page
    if st.button("Sign Up"):
        st.session_state.page = "signup"

# Title Section: This section contains the main heading for the app
st.markdown("<div class='title'>Brainrot Chat Bot</div>", unsafe_allow_html=True)

# Subtitle Section: A smaller text under the title that describes the purpose of the app
st.markdown("<div class='subtitle'>Your Favorite Study Buddy</div>", unsafe_allow_html=True)

# Chatbox Section: The section where users can interact with the chatbot
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Placeholder for chat messages: If no messages exist in the session state, initialize an empty list
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Loop through and display all previous chat messages stored in session state
for msg in st.session_state["messages"]:
    st.markdown(f"<div class='chat-bubble'>{msg}</div>", unsafe_allow_html=True)

# Input section: A form where users can type their message to send to the bot
with st.form(key="chat_form"):
    col_input, col_button = st.columns([4, 1])  # Adjust column sizes for input box and button
    with col_input:
        user_input = st.text_input("Enter prompt here", key="chat_input")  # Text input for the user message
    with col_button:
        submit_button = st.form_submit_button("Send")  # Button to send the message

# If the user has submitted a message, send it to the backend and display the response
if submit_button and user_input:
    # Display user message
    st.session_state["messages"].append(f"You: {user_input}")
    
    try:
        # Send request to Flask backend
        response = requests.post(
            "http://localhost:5000/chat",
            json={
                "message": user_input,
                "history": st.session_state["messages"]
            }
        )
        
        if response.status_code == 200:
            bot_response = response.json()["response"]
            st.session_state["messages"].append(f"Bot: {bot_response}")
        else:
            st.error("Failed to get response from the bot. Please try again.")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    # Force a rerun to display the new messages
    st.experimental_rerun()

# Check for navigation to the Sign Up page
if "page" in st.session_state and st.session_state.page == "signup":
    # Importing and running signup.py from within the app
    st.session_state.page = None  # Reset the page state after redirecting
    os.system("streamlit run signup.py")  # Open the signup.py script in a new Streamlit process