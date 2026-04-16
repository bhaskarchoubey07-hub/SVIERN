import streamlit as st
from src.styles import glass_card

def sidebar_nav():
    with st.sidebar:
        st.markdown('<h1 style="text-align: center; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SVIERN</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: -15px;">Smart Vehicle Identity System</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation
        menu = ["🏠 Dashboard", "🚗 Fleet Manager", "🪪 Identity Hub", "🛰️ Emergency Monitor", "⚙️ Settings"]
        choice = st.radio("", menu)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
    return choice

def metric_card(label, value, delta=None):
    html = f"""
    <div class="glass-card" style="text-align: center; padding: 1.5rem;">
        <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">{label}</p>
        <h2 style="margin: 0.5rem 0; font-size: 2.5rem;">{value}</h2>
        {f'<p style="color: #10b981; font-size: 0.8rem; margin: 0;">↑ {delta}</p>' if delta else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def section_header(title, subtitle):
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0.2rem;">{title}</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def alert_toast(message, type="warning"):
    colors = {"warning": "#f59e0b", "error": "#ef4444", "success": "#10b981"}
    color = colors.get(type, "#6366f1")
    st.markdown(f"""
    <div style="padding: 1rem; border-left: 5px solid {color}; background: rgba(255,255,255,0.05); border-radius: 5px; margin-bottom: 1rem;">
        <span style="color: {color}; font-weight: bold;">{type.upper()}:</span> {message}
    </div>
    """, unsafe_allow_html=True)
