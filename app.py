import streamlit as st
import os

# Page Config must be first
st.set_page_config(
    page_title="SVIERN | Smart Vehicle Identity",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.database import init_db
from src.styles import apply_styles
from src.auth import login_page
from src.components import sidebar_nav
from src.dashboard import show_dashboard
from src.fleet import show_fleet
from src.identity import show_identity_hub
from src.map import show_map
from src.public import show_public_profile

# Initialize DB
if not os.path.exists("sviern_data.db"):
    init_db()

# Apply Global Styling
apply_styles()

def main():
    # Session state initialization
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Check for public URL parameter (QR scan)
    query_params = st.query_params
    if "v" in query_params:
        show_public_profile(query_params["v"])
        return

    # User flows
    if not st.session_state['logged_in']:
        login_page()
    else:
        # User is logged in, show main app navigation
        choice = sidebar_nav()
        
        if choice == "🏠 Dashboard":
            show_dashboard()
        elif choice == "🚗 Fleet Manager":
            show_fleet()
        elif choice == "🪪 Identity Hub":
            show_identity_hub()
        elif choice == "🛰️ Emergency Monitor":
            show_map()
        elif choice == "⚙️ Settings":
            st.title("Settings")
            st.info("System configuration options coming soon.")

if __name__ == "__main__":
    main()
