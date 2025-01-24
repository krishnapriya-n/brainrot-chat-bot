import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Brainrot Chat Bot - Sign Up",
    page_icon="🧠",
    layout="wide",
)

# Title
st.markdown("<h1 style='text-align: center;'>Welcome to Brainrot Chat Bot</h1>", unsafe_allow_html=True)

# Fun message
st.markdown("""
    <p style='text-align: center;'>
        I see you have decided to try out <i>studying</i> this time. Let's see if you are up for the challenge 😉
    </p>
    <h2 style='text-align: center;'>Sign up today!</h2>
""", unsafe_allow_html=True)

# Sign-up form
with st.form(key="signup_form"):
    user = st.text_input("User", "user")  # Default username "user"
    password = st.text_input("Password", "password123", type="password")  # Default password "password123"
    
    submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        # Check dummy credentials (This is just for the mockup)
        if user == "user" and password == "password123":
            st.success("Sign Up Successful! 🎉")
        else:
            st.error("Invalid credentials! Please try again.")

# Option to go back to main page or dashboard (as a placeholder)
st.markdown("""
    <p style='text-align: center;'>
        Already have an account? <a href='#' style='color: blue;'>Log in here</a>.
    </p>
""", unsafe_allow_html=True)
