import streamlit as st
import bcrypt
from src.database import create_user, get_user
from src.styles import glass_card

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_page():
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; margin-bottom: 30px;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 0;'>SVIERN</h1>
            <p style='color: #94a3b8; font-size: 1.2rem;'>Secure Vehicle Identity & Emergency Response Network</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                user = get_user(username)
                if user and check_password(password, user['password']):
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = user
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
                    
        with tab2:
            new_user = st.text_input("Choose Username", key="reg_user")
            new_email = st.text_input("Email", key="reg_email")
            new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register"):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    hashed = hash_password(new_pass)
                    if create_user(new_user, hashed, new_email):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username already exists")
