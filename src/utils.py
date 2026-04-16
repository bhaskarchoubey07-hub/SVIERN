import qrcode
from PIL import Image
import os
import io
import base64
from datetime import datetime
import streamlit as st

def generate_qr(vehicle_number, base_url="http://localhost:8501"):
    # Create the URL for the QR code
    public_url = f"{base_url}/?v={vehicle_number}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(public_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Save to a byte stream
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    return byte_im

def get_image_base64(byte_data):
    return base64.b64encode(byte_data).decode()

def simulate_location():
    # Randomly simulate common Indian city locations or global ones
    import random
    locations = [
        {"name": "Mumbai Central", "lat": 18.9696, "lon": 72.8193},
        {"name": "Delhi Airport", "lat": 28.5562, "lon": 77.1000},
        {"name": "Bangalore IT Park", "lat": 12.9716, "lon": 77.5946},
        {"name": "Chennai Marina", "lat": 13.0418, "lon": 80.2850},
        {"name": "Kolkata Bridge", "lat": 22.5726, "lon": 88.3639}
    ]
    return random.choice(locations)

def get_whatsapp_link(phone, msg):
    # Encode message for URL
    import urllib.parse
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{phone}?text={encoded_msg}"

def format_time(ts):
    if isinstance(ts, str):
        ts = datetime.fromisoformat(ts)
    return ts.strftime("%d %b, %H:%M")
