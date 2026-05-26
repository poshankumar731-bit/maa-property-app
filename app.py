import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page Configuration for Professional Real-Estate System
st.set_page_config(page_title="मां प्रॉपर्टी डिजिटल ऐप 2026", layout="wide")

# Premium High-Contrast Styling & Print Layout Rules
st.markdown("""
<style>
    .main { background-color: #0f111a; color: #e1e1e6; }
    .stTabs [data-baseweb="tab"] { color: #a0a5b5; font-weight: bold; font-size: 16px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00ffcc; border-bottom-color: #00ffcc; }
    
    /* Clean, Professional Invoice Box Style matching your paper print photo */
    .invoice-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border: 2px solid #000000;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
        max-width: 600px;
        margin: 20px auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .invoice-card h2, .invoice-card h4, .invoice-card p, .invoice-card td, .invoice-card th {
        color: #000000 !important;
    }
    
    /* CSS rule to isolate only the receipt for clean printing */
    @media print {
        body * { visibility: hidden; background: white !important; }
        .printable-receipt, .printable-receipt * { visibility: visible; color: black !important; }
        .printable-receipt { position: absolute; left: 0; top: 0; width: 100%; box-shadow: none !important; border: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# Persistent Database Store Simulation using Streamlit Session State
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"},
        {"id": "PROP-356", "name": "chatarkhar", "type": "प्लॉट (Plot)", "area": "87200", "rate": "1600", "location": "chatarkhar", "owner": "Self Owner"}
    ]

if 'bill_records' not in st.session_state:
    st.session_state.bill_records = []

# Application Title Header
st.title("⚡ मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🔍 लाइव स्क्रीन (View Database)", 
    "➕ नई प्रॉपर्टी जोड़ें", 
    "💳 डिजिटल बिलिंग (Billing)"
])

# TAB 1: LIVE DATABASE WITH DELETE OPTION
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    st.write("यहाँ से आप प्रॉपर्टी देख सकते हैं, WhatsApp पर भेज सकते हैं या डिलीट कर सकते हैं:")
    st.write("---")
    
    # Loop backward to prevent index shifting bugs during deletion
    for index, p in enumerate(st.session_state.properties):
        col_data, col_action = st.columns([4, 1])
        
        with col_data:
            st.info(f"🏢 नाम: {p['name']} | ID: {p['id']} | प्रकार: {p['type']}")
            st.write(f"📍 लोकेशन: {p['location']} | 📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}")
            st.write(f"👤 मालिक: {p['owner']}")
            
            # WhatsApp Integration Link
            msg = f"नमस्ते, मुझे आपकी प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
            wa_url = f"https://wa.me/918109471091?text={msg.replace(' ', '%20')}"
            st.markdown(f"[💬 WhatsApp पर ग्राहक को विवरण भेजें]({wa_url})")
            
        with col_action:
            st.write(" ")
            st.write(" ")
            # Unique key for each delete button using property ID
            if st.button(f"❌ डिलीट करें", key=f"del_{p['id']}_{index}"):
                st.session_state.properties.pop(index)
                st.warning(f"🗑️ {p['name']} को डेटाबेस से डिलीट कर दिया गया है!")
                st.rerun()
                
        st.write("---")

# TAB 2: ADD NEW PROPERTY
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री फॉर्म")
    with st.form("add_property_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें, जैसे: 2500000)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        btn = st.form_submit_button("☁️ सुरक्षित लाइव सेव करें")
        if btn:
            if n and r:
                try:
                    rate_val = int(r)
                except ValueError:
                    rate_val = 0
                new_id = f"PROP-{random.randint(400, 999)}"
                st.session_state.properties.append({
                    "id": new_id, "name": n, "type": t, "area": a, "rate": str(rate_val), "location": l, "owner": o
                })
                st.success(f"🎉 नई प्रॉपर्टी '{n}' सफलतापूर्वक लाइव स्क्रीन पर सेव हो गई! ID: {new_id}")
                st.balloons()
                st.rerun()
            else:
                st.error("प्रॉपर्टी का नाम और कीमत भरना अनिवार्य है!")

# TAB 3: BILLING & PAPER PRINT ENGINE
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    st.write("डिटेल्स भरें और नीचे रसीद पेपर प्रिंट आउट निकालें:")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        b_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value="maa proprey")
        b_loc = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value="chatarkhar")
        c_name = st.text_input("3. ग्राहक (Buyer) का name", value="umasankar")
        c_phone = st.text_input("4. ग्राहक का मोबाइल नंबर", value="8109471091")

    with col_right:
        base_price = st.number_input("5. मूल सौदा राशि (₹)", min_value=0, value=20000000, step=1000)
        disc = st.number_input("6. डिस्काउंट / छूट (₹)", min_value=0, value=0, step=500)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=100000, step=1000)

    # Computations
    final_total = base_price - disc
    pending_amount = final_total - adv
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_time = datetime.now().strftime('%H:%M')
    
    st.write("---")
    
    # Process invoice calculation
    if 'current_receipt' not in st.session_state:
        st.session_state.current_receipt = None

    if st.button("✨ डिजिटल रसीद तैयार करें"):
        if b_name == "":
            st.error("कृपया बिल बनाने के लिए प्रॉपर्टी का नाम लिखें!")
        else:
            invoice_id = f"INV-{random.randint(3000, 3999)}"
            
            # Save receipt layout inside a standard variable session state
            st.session_state.current_receipt = {
                "id": invoice_id, "date": current_date, "time": current_time,
                "b_name": b_name, "b_loc": b_loc, "c_name": c_name, "c_phone": c_phone,
                "base": base_price, "disc": disc, "total": final_total, "adv": adv, "due": pending_amount
            }
            
            # Append to history ledger
            st.session_state.bill_records.append({
                "रसीद ID": invoice_id, "तारीख": current_date, "प्रॉपर्टी": b_name,
                "कस्टमर": c_name, "फाइनल सौदा": final_total, "बकाया राशि": pending_amount
            })
            st.success("✅ रसीद सफलतापूर्वक तैयार हो गई है! नीचे प्रिंट ऑप्शन देखें।")

    # If receipt generated, show print option and standard layout look
    if st.session_state.current_receipt:
        rc = st.session_state.current_receipt
        
        # JAVASCRIPT PRINT TRIGGER BUTTON
        st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
                <button onclick="window.print()" style="
                    background-color: #00ffcc; 
                    color: #000000; 
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 12px 35px; 
                    border: none; 
                    border-radius: 5px; 
                    cursor: pointer;
                    box-shadow: 0 4px 10px rgba(0,255,204,0.3);
                ">🖨️ Print Receipt (रसीद प्रिंट आउट निकालें)</button>
            </div>
        """, unsafe_allow_html=True)
        
        # Display Exact Invoice matching your paper screenshot layout
        st.markdown(f"""
        <div class="invoice-card printable-receipt">
            <div style="text-align: center; border-bottom: 2px solid #000000; padding-bottom: 5px; margin-bottom: 12px;">
                <h2 style="margin: 0; font-size: 22px; letter-spacing: 1px;"><b>|| माँ प्रॉपर्टीज डिजिटल इनवॉइस ||</b></h2>
                <p style="margin: 3px 0 0 0; font-size: 12px;">तारीख: {rc['date']} | समय: {rc['time']}</p>
            </div>
            
            <table style="width: 100%; font-size: 14px; margin-bottom: 10px; line-height: 1.8;">
                <tr><td style="width: 35%;"><b>🏢 प्रॉपर्टी नाम:</b></td><td><b>{rc['b_name']}</b></td></tr>
                <tr><td><b>📍 लोकेशन:</b></td><td>{rc['b_loc']}</td></tr>
                <tr><td><b>👤 ग्राहक:</b></td><td>{rc['c_name']}</td></tr>
