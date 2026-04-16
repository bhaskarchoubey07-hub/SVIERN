import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime
import streamlit as st

# Load database URL from secrets
def get_db_url():
    try:
        return st.secrets["database"]["url"]
    except Exception:
        return None

DB_URL = get_db_url()

def get_connection():
    if not DB_URL:
        st.error("🚫 **Database Connection Failed**: Database URL not found in secrets.")
        st.info("💡 **Fix**: If you are on Streamlit Cloud, go to **Settings > Secrets** and paste your `.streamlit/secrets.toml` content there.")
        st.stop()
    return psycopg2.connect(DB_URL)

def init_db():
    try:
        conn = get_connection()
        c = conn.cursor()
    
    # Use standard Postgres SQL
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT
    );
    CREATE TABLE IF NOT EXISTS vehicles (
        id SERIAL PRIMARY KEY,
        owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        vehicle_number TEXT UNIQUE NOT NULL,
        owner_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        emergency_contact TEXT,
        medical_info TEXT
    );
    CREATE TABLE IF NOT EXISTS scans (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
        scan_time TIMESTAMP DEFAULT NOW(),
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        location_name TEXT
    );
    CREATE TABLE IF NOT EXISTS alerts (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
        alert_type TEXT NOT NULL,
        alert_time TIMESTAMP DEFAULT NOW(),
        message TEXT,
        is_resolved BOOLEAN DEFAULT FALSE
    );
    """)
    conn.commit()
    conn.close()

# --- USER OPERATIONS ---
def create_user(username, password, email):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                  (username, password, email))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        conn.close()

def get_user(username):
    try:
        conn = get_connection()
        c = conn.cursor(cursor_factory=RealDictCursor)
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = c.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        conn.close()

# --- VEHICLE OPERATIONS ---
def add_vehicle(owner_id, v_num, owner_name, phone, e_contact, medical):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""INSERT INTO vehicles (owner_id, vehicle_number, owner_name, phone, emergency_contact, medical_info) 
                     VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""", 
                  (owner_id, v_num, owner_name, phone, e_contact, medical))
        new_id = c.fetchone()[0]
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Error adding vehicle: {e}")
        return None
    finally:
        conn.close()

def get_owner_vehicles(owner_id):
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM vehicles WHERE owner_id = %s", conn, params=(owner_id,))
        return df
    except Exception as e:
        print(f"Error getting fleet: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_vehicle_by_number(v_num):
    try:
        conn = get_connection()
        c = conn.cursor(cursor_factory=RealDictCursor)
        c.execute("SELECT * FROM vehicles WHERE vehicle_number = %s", (v_num,))
        vehicle = c.fetchone()
        return dict(vehicle) if vehicle else None
    except Exception as e:
        print(f"Error getting vehicle: {e}")
        return None
    finally:
        conn.close()

def delete_vehicle(vehicle_id):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting vehicle: {e}")
        return False
    finally:
        conn.close()

# --- SCAN & ALERT OPERATIONS ---
def log_scan(vehicle_id, lat, lon, loc_name="Unknown"):
    try:
        conn = get_connection()
        c = conn.cursor()
        scan_time = datetime.now()
        c.execute("INSERT INTO scans (vehicle_id, scan_time, latitude, longitude, location_name) VALUES (%s, %s, %s, %s, %s)",
                  (vehicle_id, scan_time, lat, lon, loc_name))
        
        # Simple AI Alert Detection
        c.execute("SELECT COUNT(*) FROM scans WHERE vehicle_id = %s AND scan_time > NOW() - INTERVAL '5 minutes'", (vehicle_id,))
        recent_scans = c.fetchone()[0]
        
        if recent_scans > 3:
            c.execute("INSERT INTO alerts (vehicle_id, alert_type, alert_time, message) VALUES (%s, %s, %s, %s)",
                      (vehicle_id, "Suspicious Activity", scan_time, "Multiple scans detected in under 5 minutes."))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error logging scan: {e}")
        return False
    finally:
        conn.close()

def get_all_scans():
    try:
        conn = get_connection()
        query = """
        SELECT s.*, v.vehicle_number 
        FROM scans s 
        JOIN vehicles v ON s.vehicle_id = v.id 
        ORDER BY s.scan_time DESC
        """
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error getting scans: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_all_alerts():
    try:
        conn = get_connection()
        query = """
        SELECT a.*, v.vehicle_number 
        FROM alerts a 
        JOIN vehicles v ON a.vehicle_id = v.id 
        ORDER BY a.alert_time DESC
        """
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_stats():
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM vehicles")
        v_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM scans")
        s_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM alerts WHERE is_resolved = FALSE")
        a_count = c.fetchone()[0]
        
        return {
            "total_vehicles": v_count,
            "total_scans": s_count,
            "active_alerts": a_count
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {"total_vehicles": 0, "total_scans": 0, "active_alerts": 0}
    finally:
        conn.close()
