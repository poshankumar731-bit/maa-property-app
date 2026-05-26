import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="मां प्रॉपर्टी ऐप 2026", layout="wide")

# Premium Cyber/Digital Dark Theme Styling
st.markdown("""
<style>
    .main { background-color: #0b0c10; color: #c5c6c7; }
    .card {
        background-color: #1f2833;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4682b4;
        margin-bottom: 15px;
    }
    .digital-bill {
        background-color: #111111;
        color: #00ffcc;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #00ffcc;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Live Cloud Database Simulation
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]

st.title("⚡ मां प्रॉपर्टी डिजिटल क्लाउड ऐप 2026")
st.write("---")

tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (View Database)", "➕ नई प्रॉपर्टी जोड़ें", "💳 डिजिटल बिलिंग पैनल (Billing)"])

# TAB 1: LIVE VIEW SCREEN
with tab1:
    st.markdown("### 📱 आपकी लाइव स्क्रीन पर प्रॉपर्टीज")
    for p in st.session_state.properties:
        st.markdown(f"""
        <div class="card">
            <h4 style="color: #66fcf1;">🏢 नाम: {p['name']} ({p['id']})</h4>
            <p>📁 प्रकार: {p['type']} | 📍 लोकेशन: {p['location']}</p>
            <p>📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}</p>
            <p>👤 मालिक: {p['owner']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        msg = f"नमस्ते, मुझे प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर ग्राहक को भेजें]({wa_url})")
        st.write("---")

# TAB 2: ADD PROPERTY TO CLOUD & SCREEN
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री (Save to Cloud)")
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (যেমন: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें जैसे: 2500000)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        btn = st.form_submit_button("☁️ क्लाउड और स्क्रीन पर सुरक्षित सेव करें")
        if btn:
            if n and r:
                new_id = f"PROP-{random.randint(103, 999)}"
                st.session_state.properties.append({"id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o})
                st.success("🎉 प्रॉपर्टी सफलतापूर्वक सेव हो गई! अब यह लाइव स्क्रीन टैब में दिख रही है।")
                st.balloons()
            else:
                st.error("नाम और कीमत भरना जरूरी है!")

# TAB 3: DIGITAL BILLING PANEL (ALL FIELDS BLANK & HI-TECH LOOK)
with tab3:
    st.markdown("### 💳 न्यू डिजिटल इनवॉइस जनरेटर")
    st.info("💡 नीचे दी गई सभी फील्ड्स को खली रखा गया है, आप अपनी मर्ज़ी से नया डेटा भर सकते हैं।")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        b_prop_name = st.text_input("1. प्रॉपर्टी / रेजीडेंसी का नाम", value="", placeholder="जैसे: साईं रेजीडेंसी प्लॉट नं 12")
        b_location = st.text_input("2. प्रॉपर्टी की लोकेशन/पता", value="", placeholder="जैसे: गोमती नगर, लखनऊ")
        c_name = st.text_input("3. कस्टमर (Buyer) का नाम", value="", placeholder="खरीदार का नाम लिखें")
        c_phone = st.text_input("4. कस्टमर का मोबाइल नंबर", value="", placeholder="9999xxxxxx")

    with col_b:
        base_price = st.number_input("5. कुल तय कीमत / सौदा राशि (₹)", min_value=0, value=0, step=1000)
        disc = st.number_input("6. डिजिटल डिस्काउंट / छूट (₹)", min_value=0, value=0, step=500)
        adv = st.number_input("7. एडवांस पेमेंट / बयाना (₹)", min_value=0, value=0, step=1000)

    # Live Real-time Calculation
    final_total = base_price - disc
    pending_amount = final_total - adv
    
    st.write("---")
    generate_bill = st.button("🖨️ जेनरेट हाई-टेक डिजिटल रसीद")
    
    if generate_bill:
        if b_prop_name == "":
            st.warning("कृपया बिल बनाने के लिए प्रॉपर्टी का नाम ज़रूर टाइप करें!")
        else:
            st.markdown("#### ⚡ LIVE DIGITAL INVOICE GENERATED:")
            st.markdown(f"""
            <div class="digital-bill">
                <h2 style="text-align: center; color: #00ffcc; margin: 0;"><b>|| माँ प्रॉपर्टीज डिजिटल रसीद ||</b></h2>
                <p style="text-align: center; font-size: 12px; color: #888;">CLOUD SYNC ID: {random.randint(100000, 999999)} | DATE: {datetime.now().strftime('%d-%m-%Y')} </p>
                <p style="text-align: center; font-size: 12px; color: #888;">TIME: {datetime.now().strftime('%H:%M:%S')} IST</p>
                <hr style="border-top: 1px dashed #00ffcc;">
                
                <p><b>🏢 प्रॉपर्टी नाम :</b> {b_prop_name}</p>
                <p><b>📍 पता / लोकेशन :</b> {b_location}</p>
                <hr style="border-top: 1px dashed #444;">
                
                <p><b>👤 ग्राहक का नाम :</b> {c_name}</p>
                <p><b>📞 मोबाइल नंबर :</b> {c_phone}</p>
                <hr style="border-top: 1px dashed #00ffcc;">
                
                <p style="color: #ffffff;">💵 मूल सौदा राशि (
                
