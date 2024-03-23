import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Check if Firebase Admin SDK has already been initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('/Users/syntichemusawu/Desktop/IntrotoSFE/introtosfe-035c966fdaea.json')
    firebase_admin.initialize_app(cred)

def app():
    st.title('Welcome to:violet[]')
    choice = st.selectbox('Login/Signup',['Login','Sign Up'])

    if choice == 'Login':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            try:
                user = auth.get_user_by_email(email)
                # Assuming you have a way to verify the password here
                # For demonstration, let's assume the password is correct
                st.success('Login Successful')
            except:
                st.warning('Login failed')
    else:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input('Enter your unique username')
        if st.button('create my account'):
            user = auth.create_user(email=email, password=password, uid=username)
            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()

# Call the app function
app()
