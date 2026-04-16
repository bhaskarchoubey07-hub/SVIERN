import streamlit as st
import pandas as pd
from src.database import add_vehicle, get_owner_vehicles, delete_vehicle
from src.components import section_header, alert_toast
from src.styles import glass_card

def show_fleet():
    section_header("Fleet Manager", "Manage your registered vehicles and profiles")
    
    user_id = st.session_state['user']['id']
    
    tab1, tab2 = st.tabs(["Register Vehicle", "All Vehicles"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("add_vehicle_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                v_num = st.text_input("Vehicle Number (e.g., MH12AB1234)")
                owner_name = st.text_input("Owner Name")
                phone = st.text_input("Contact Number")
            with col2:
                e_contact = st.text_input("Emergency Contact Number")
                medical_info = st.text_area("Medical Information (Allergies, Blood Group, etc.)")
            
            submitted = st.form_submit_button("Register Vehicle")
            if submitted:
                if v_num and owner_name and phone:
                    vid = add_vehicle(user_id, v_num.upper(), owner_name, phone, e_contact, medical_info)
                    if vid:
                        st.success(f"Vehicle {v_num} registered successfully!")
                    else:
                        st.error("Error: Vehicle number might already exist.")
                else:
                    st.warning("Please fill in all mandatory fields.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        df = get_owner_vehicles(user_id)
        if not df.empty:
            for _, row in df.iterrows():
                with st.expander(f"🚗 {row['vehicle_number']} - {row['owner_name']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Phone:** {row['phone']}")
                        st.write(f"**Emergency Contact:** {row['emergency_contact']}")
                    with col_b:
                        st.write(f"**Medical Info:** {row['medical_info']}")
                    
                    if st.button(f"Delete Vehicle", key=f"del_{row['id']}"):
                        delete_vehicle(row['id'])
                        st.success("Vehicle removed")
                        st.rerun()
        else:
            st.info("No vehicles registered yet.")
