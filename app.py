import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(
    page_title="मां प्रॉपर्टी डिजिटल ऐप 2026",
    page_icon="🏠",
    layout="wide"
)

# --- THEME STYLING ---
st.markdown("""
<style>
    .main { background-color: #0f0f11; color: #ffffff; }
    .card {
        background-color: #1e1e24;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #d4af37;
        margin-bottom: 15px;
    }
    .bill-box {
        background-color: #ffffff;
        color: #000000;
        padding: 25px;
        border-radius: 8px;
        border: 2px dashed #000000;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL DATA CLOUD STORAGE (SESSION STATE) ---
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-1001", "name": "कृष्णा ग्रीन प्लॉट", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500", "status": "Available", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-1002", "name": "खान विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "status": "Available", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]
if 'bills' not in st.session_state:
    st.session_state.bills = []

st.title("🏠 मां प्रॉपर्टी डिजिटल ऐप 2026")
st.subheader("Cloud Sync & Real-time Billing Enabled")
st.write("---")

# --- TABS SYSTEM ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 प्रॉपर्टी खोजें और देखें (Live Screen)", 
    "➕ नई प्रॉपर्टी जोड़ें (Save to Cloud)", 
    "💰 डिजिटल बिलिंग (Billing Panel)",
    "📊 स्मार्ट डैशबोर्ड"
])

# --- TAB 1: SEARCH & LIVE VIEW ---
with tab1:
    st.markdown("### 📱 आपकी स्क्रीन पर लाइव प्रॉपर्टीज (Live Database)")
    f_type = st.selectbox("कैटेगरी फिल्टर (Category)", ["All", "प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
    
    filtered = st.session_state.properties
    if f_type != "All":
        filtered = [p for p in filtered if p['type'] == f_type]
        
    if len(filtered) == 0:
        st.info("कोई प्रॉपर्टी नहीं मिली।")
        
    for p in filtered:
        st.markdown(f"""
        <div class="card">
            <h4>🏢 नाम: {p['name']} ({p['id']})</h4>
            <p>📁 <b>प्रकार:</b> {p['type']} | 📍 <b>लोकेशन:</b> {p['location']}</p>
            <p>📐 <b>एरिया:</b> {p['area']} | 💰 <b>कीमत/रेट:</b> ₹{int(p['rate']):,}</p>
            <p>👤 <b>मालिक (Owner):</b> {p['owner']} | 🟢 <b>स्टेटस:</b> {p['status']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # WhatsApp Button
        msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी '{p['name']}' (ID: {p['id']}) में इंटरेस्ट है जो {p['location']} में है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर ग्राहक को भेजें]({wa_url})")
        st.write("---")

# --- TAB 2: ADD PROPERTY (SAVING TO CLOUD AND SCREEN) ---
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री (Save to Screen & Cloud)")
    with st.form("property_form", clear_on_submit=True):
        p_name = st.text_input("प्रॉपर्टी का नाम (Property Name)", placeholder="जैसे: साईं रेजीडेंसी प्लॉट नं 5")
        p_type = st.selectbox("प्रॉपर्टी प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        p_area = st.text_input("एरिया (Area - जैसे: 1500 SqFt / 2 बीघा)")
        p_rate = st.text_input("कुल कीमत या रेट प्रति SqFt (सिर्फ नंबर लिखें)")
        p_loc = st.text_input("लोकेशन / पता (Address)")
        p_owner = st.text_input("मालिक का नाम (Owner Name)")
        
        submitted = st.form_submit_button("☁️ सुरक्षित रूप से क्लाउड और स्क्रीन पर सेव करें")
        
        if submitted:
            if p_name and p_rate:
                new_id = f"PROP-{random.randint(1003, 9999)}"
                # डेटाबेस में नया रिकॉर्ड जोड़ना
                new_prop = {
                    "id": new_id, 
                    "name": p_name,
                    "type": p_type, 
                    "area": p_area, 
                    "rate": p_rate, 
                    "status": "Available", 
                    "location": p_loc, 
                    "owner": p_owner
                }
                st.session_state.properties.append(new_prop)
                st.success(f"
    
