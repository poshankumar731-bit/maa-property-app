import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page configuration for a professional layout
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल क्लाउड ऐप 2026", layout="wide")

# Modern Tech/Corporate Styling
st.markdown("""
<style>
    .main { background-color: #0f111a; color: #ffffff; }
    .stTabs [data-baseweb="tab"] { color: #8a99ad; font-weight: bold; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00ffcc; border-bottom-color: #00ffcc; }
    
    /* Premium Invoice Styles for Screen & Print */
    .print-box {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border: 2px solid #000000;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        max-width: 600px;
        margin: 20px auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .print-box h2, .print-box h3, .print-box p, .print-box td {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Databases in Session Memory (Simulated Cloud Backend)
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = []

# Top App Banner
st.title("⚡ माँ प्रॉपर्टीज डिजिटल क्लाउड मैनेजमेंट")
st.write("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🔍 लाइव स्क्रीन (View Database)", 
    "➕ नई प्रॉपर्टी जोड़ें", 
    "💳 डिजिटल बिलिंग और रिकॉर्ड्स (Billing Panel)"
])

# TAB 1: LIVE DATABASE VIEW SCREEN
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    for p in st.session_state.properties:
        st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
        st.write(f"📍 लोकेशन: {p['location']} | 📐エリア: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}")
        st.write(f"👤 मालिक: {p['owner']}")
        
        msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर विवरण भेजें]({wa_url})")
        st.write("---")

# TAB 2: ADD NEW PROPERTY TO CLOUD
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("add_property_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        btn = st.form_submit_button("☁️ सुरक्षित लाइव सेव करें")
        if btn:
            if n and r:
                new_id = f"PROP-{random.randint(103, 999)}"
                st.session_state.properties.append({"id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o})
                st.success(f"🎉 प्रॉपर्टी सफलतापूर्वक लाइव स्क्रीन पर सेव हो गई! ID: {new_id}")
                st.balloons()
            else:
                st.error("नाम और कीमत भरना जरूरी है!")

# TAB 3: BILLING PANEL WITH HISTORY STORAGE & FIXED HTML PRINT SYSTEM
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    st.write("विवरण दर्ज करें और रसीद तुरंत प्रिंट या नीचे रिकॉर्ड रजिस्टर में सुरक्षित करें:")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value="", placeholder="जैसे: साईं रेजीडेंसी")
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value="", placeholder="जैसे: गोमती नगर, लखनऊ")
        c_name = st.text_input("3. ग्राहक (Buyer) का नाम", value="")
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value="")

    with col_right:
        base_price = st.number_input("5. कुल सौदा राशि (₹)", min_value=0, value=0, step=5000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=0, step=1000)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=0, step=5000)

    # Automated Live Calculations
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write("---")
    
    # Process Button
    if st.form_submit_button if 'form' in locals() else st.button("🖨️ डिजिटल रसीद जनरेट और रिकॉर्ड में सेव करें"):
        if b_name == "":
            st.warning("कृपया बिल बनाने के लिए प्रॉपर्टी का नाम अवश्य लिखें!")
        else:
            invoice_id = f"INV-{random.randint(1000, 9999)}"
            
            # Save to history ledger dictionary safely
            saved_record = {
                "इनवॉइस ID": invoice_id,
                "तاريخ": current_date,
                "प्रॉपर्टी": b_name,
                "कस्टमर": c_name,
                "मोबाइल": c_phone,
                "मूल सौदा (₹)": base_price,
                "छूट (₹)": disc,
                "फाइनल डील (₹)": final_total,
                "एडवांस प्राप्त (₹)": adv,
                "बकाया राशि (₹)": pending_amount
            }
            st.session_state.bill_records.append(saved_record)
            st.success(f"✅ इनवॉइस {invoice_id} सफलतापूर्वक क्लाउड रिकॉर्ड में रजिस्टर हो गया है!")
            
            # FIXED: HTML Rendering enabled via unsafe_allow_html=True
            st.markdown(f"""
            <div class="print-box">
                <div style="text-align: center; border-bottom: 2px solid #000000; padding-bottom: 8px; margin-bottom: 15
    
