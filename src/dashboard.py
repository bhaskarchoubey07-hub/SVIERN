import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import get_stats, get_all_scans, get_all_alerts
from src.components import metric_card, section_header
from src.utils import format_time

def show_dashboard():
    section_header("Command Center", "Real-time analytics and system monitoring")
    
    stats = get_stats()
    
    # Metrics Row
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Total Registered", stats['total_vehicles'], "12% Monthly")
    with c2:
        metric_card("Identity Scans", stats['total_scans'], "24% Weekly")
    with c3:
        metric_card("Active Alerts", stats['active_alerts'])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col_l, col_r = st.columns([2, 1])
    
    scans_df = get_all_scans()
    
    with col_l:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Scan Activity Trends")
        if not scans_df.empty:
            scans_df['scan_time'] = pd.to_datetime(scans_df['scan_time'])
            # Group by hour for the chart
            chart_data = scans_df.resample('h', on='scan_time').size().reset_index(name='scans')
            fig = px.area(chart_data, x="scan_time", y="scans", 
                          template="plotly_dark", 
                          color_discrete_sequence=['#a855f7'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="",
                yaxis_title="Total Scans",
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No scan data available yet.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔔 Live Alerts")
        alerts_df = get_all_alerts()
        if not alerts_df.empty:
            for _, alert in alerts_df.head(5).iterrows():
                st.markdown(f"""
                <div style="border-left: 3px solid #ef4444; padding-left: 10px; margin-bottom: 15px;">
                    <p style="margin:0; font-weight:bold; color:#ef4444;">{alert['alert_type']}</p>
                    <p style="margin:0; font-size:0.8rem; color:#94a3b8;">Vehicle: {alert['vehicle_number']}</p>
                    <p style="margin:0; font-size:0.7rem; color:#64748b;">{format_time(alert['alert_time'])}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("All systems clear.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Activity Feed
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📑 Recent Activity")
    if not scans_df.empty:
        st.dataframe(scans_df[['vehicle_number', 'scan_time', 'location_name']].head(10), 
                     use_container_width=True)
    else:
        st.write("No recent activity logs.")
    st.markdown('</div>', unsafe_allow_html=True)
