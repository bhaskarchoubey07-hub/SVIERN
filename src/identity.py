import streamlit as st
from src.database import get_owner_vehicles
from src.utils import generate_qr
from src.components import section_header
from src.styles import glass_card

def show_identity_hub():
    section_header("Identity Hub", "Generate and download QR identity cards")
    
    user_id = st.session_state['user']['id']
    vehicles_df = get_owner_vehicles(user_id)
    
    if vehicles_df.empty:
        st.info("Please register a vehicle in the Fleet Manager first.")
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        selected_v = st.selectbox("Select Vehicle", vehicles_df['vehicle_number'].tolist())
    with c2:
        # Allow user to specify the deployment URL for the QR code
        base_url = st.text_input("Deployment URL", value="https://sviern.streamlit.app", help="The URL where this app is hosted (e.g., your streamlit.app domain)")
    
    if selected_v:
        qr_bytes = generate_qr(selected_v, base_url)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.image(qr_bytes, caption=f"QR Identity for {selected_v}", use_container_width=True)
            st.download_button(
                label="Download QR Code",
                data=qr_bytes,
                file_name=f"QR_{selected_v}.png",
                mime="image/png"
            )
            
        with col2:
            st.markdown(f"""
            <div style="background: white; color: black; padding: 20px; border-radius: 15px; border: 2px solid #a855f7;">
                <h3 style="margin-top:0; color:#a855f7;">SVIERN IDENTITY CARD</h3>
                <hr style="border: 1px solid #eee;">
                <p><strong>VEHICLE:</strong> {selected_v}</p>
                <p><strong>OWNER:</strong> {vehicles_df[vehicles_df['vehicle_number'] == selected_v]['owner_name'].values[0]}</p>
                <p style="font-size: 0.8rem; color: #666; margin-top: 20px;">
                    Scan this QR code in case of emergency or for vehicle information.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
