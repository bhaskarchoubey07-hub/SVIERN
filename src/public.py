import streamlit as st
from src.database import get_vehicle_by_number, log_scan
from src.utils import simulate_location, get_whatsapp_link
from src.styles import glass_card

def show_public_profile(v_num):
    vehicle = get_vehicle_by_number(v_num)
    
    if not vehicle:
        st.error("Vehicle information not found.")
        return

    # Log the scan automatically (simulated location)
    if 'scanned' not in st.session_state:
        loc = simulate_location()
        log_scan(vehicle['id'], loc['lat'], loc['lon'], loc['name'])
        st.session_state['scanned'] = True

    st.markdown(f"""
        <div style='text-align: center; margin-top: 20px;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0;'>{v_num}</h1>
            <p style='color: #94a3b8; font-size: 1rem;'>Certified Vehicle Identity</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <h3>👤 Owner Information</h3>
            <p style="margin:0;"><strong>Name:</strong> {vehicle['owner_name']}</p>
            <p style="margin:0;"><strong>Contact:</strong> {vehicle['phone']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Call Button
        st.markdown(f"""
            <a href="tel:{vehicle['phone']}" style="text-decoration:none;">
                <div style="background: #10b981; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:bold; margin-bottom:20px;">
                    📞 CALL OWNER
                </div>
            </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <h3>🏥 Medical Info</h3>
            <p style="color: #ef4444; font-weight: bold;">{vehicle['medical_info'] or 'None provided'}</p>
        </div>
        """, unsafe_allow_html=True)

    # SOS Section
    st.markdown('<div class="glass-card" style="border: 2px solid #ef4444; text-align: center;">', unsafe_allow_html=True)
    st.markdown("## EMERGENCY SOS")
    st.markdown("Click the button below to alert family and emergency services with your current location.")
    
    if st.button("🚨 TRIGGER SOS ALERT", key="sos_btn", help="Send location alert"):
        loc = simulate_location()
        sos_msg = f"EMERGENCY! Vehicle {v_num} involves an accident. Location: {loc['name']} ({loc['lat']}, {loc['lon']}). Please respond immediately!"
        
        wa_link = get_whatsapp_link(vehicle['emergency_contact'], sos_msg)
        
        st.markdown(f"""
            <div style="margin-top:20px;">
                <a href="{wa_link}" target="_blank" style="text-decoration:none;">
                    <div style="background: #25D366; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:bold; margin-bottom:10px;">
                        📲 SEND WHATSAPP ALERT
                    </div>
                </a>
                <a href="tel:112" style="text-decoration:none;">
                    <div style="background: #ef4444; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:bold;">
                        ☎️ CALL POLICE (112)
                    </div>
                </a>
            </div>
        """, unsafe_allow_html=True)
        st.error("ALERT TRIGGERED: Information Sent to Emergency Contacts")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("Your location has been logged for security purposes.")
