import streamlit as st
import folium
from streamlit_folium import st_folium
from src.database import get_all_scans
from src.components import section_header

def show_map():
    section_header("Emergency Monitor", "Geospatial analysis of scan activity and incidents")
    
    scans_df = get_all_scans()
    
    if scans_df.empty:
        st.info("No geospatial data available yet.")
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Create center point
    avg_lat = scans_df['latitude'].mean()
    avg_lon = scans_df['longitude'].mean()
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5, control_scale=True, tiles="cartodb dark_matter")
    
    for _, row in scans_df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            popup=f"Vehicle: {row['vehicle_number']}<br>Time: {row['scan_time']}",
            color="#a855f7",
            fill=True,
            fill_color="#a855f7"
        ).add_to(m)
        
    st_folium(m, width=900, height=500)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📍 Recent Locations")
    st.table(scans_df[['vehicle_number', 'location_name', 'scan_time']].head(10))
    st.markdown('</div>', unsafe_allow_html=True)
