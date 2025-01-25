import streamlit as st
import pyrebase
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

#Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None


def login():
    try:
        email = st.session_state.login_email
        password = st.session_state.login_password
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state.user = user
        st.success('Login sucessful!')

    except Exception as e:
        st.error('Error loggin in')

def signup():
    try:
        email = st.session_state.signup_email
        password = st.session_state.signup_password
        user = auth.create_user_with_email_and_password(email, password)
        st.session_state.user = user
        st.success('Account created sucessfully!')
    except Exception as e:
        st.error(f'Error creating account: {str(e)}')

def google_login():
    try:
       provider_id = 'google.com'

       auth_url = (
            f"https://{firebaseConfig['authDomain']}/__/auth/handler?"
            f"apiKey={firebaseConfig['apiKey']}&providerId={provider_id}&"
            f"redirect_uri=http://localhost:8501&response_type=token&prompt=select_account"
       )

        #Creating Google Sign in Styling
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
        st.error(f'Error setting up Google Login : {str(e)}')


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
            st.button("Sign Up", on_click=signup)
            st.markdown('---')
            google_login()

    if 'logout_trigger' in st.session_state and st.session_state['logout_trigger']:
        # Reset the state or clear user data as needed
        del st.session_state['logout_trigger']
        st.experimental_rerun()  # Ensures rerun

    else:
        st.markdown("<div class='top-right-card'><b>Welcome!</b></div>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.user = None  # Clear user session
            raise RerunException(RerunData(None))

        
# Title
st.markdown("<div class='title'>Brainrot Chat Bot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your study companion</div>", unsafe_allow_html=True)

# Chatbox
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)

# Only show chat interface if user is logged in
if st.session_state.user:
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
else:
    st.info('Please log in to continue!')

