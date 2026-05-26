import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="मां प्रॉपर्टी ऐप 2026", layout="wide")

# Custom CSS for Premium look
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
        padding: 20px;
        border-radius: 8px;
        border: 2px dashed #000000;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Database
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": "PROP-101", "name": "साईं रेजीडेंसी", "type": "प्लॉट (Plot)", "area": "1200 SqFt", "rate": "2500000", "location": "Sector 15, Lucknow", "owner": "राम कुमार"},
        {"id": "PROP-102", "name": "गोकुल विला", "type": "मकान (House)", "area": "3 BHK", "rate": "6500000", "location": "Gomti Nagar", "owner": "S. K. Khan"}
    ]

st.title("🏠 मां प्रॉपर्टी डिजिटल ऐप 2026")
st.write("---")

tab1, tab2, tab3 = st.tabs(["🔍 लाइव स्क्रीन (View)", "➕ नई प्रॉपर्टी जोड़ें", "💰 बिलिंग पैनल (Billing)"])

# TAB 1: VIEW
with tab1:
    st.markdown("### 📱 लाइव प्रॉपर्टीज की सूची")
    for p in st.session_state.properties:
        st.markdown(f"""
        <div class="card">
            <h4>🏢 नाम: {p['name']} ({p['id']})</h4>
            <p>📁 प्रकार: {p['type']} | 📍 लोकेशन: {p['location']}</p>
            <p>📐 एरिया: {p['area']} | 💰 कीमत: ₹{int(p['rate']):,}</p>
            <p>👤 मालिक: {p['owner']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        msg = f"नमस्ते, मुझे प्रॉपर्टी {p['name']} (ID: {p['id']}) में इंटरेस्ट है।"
        wa_url = f"https://wa.me/919999999999?text={msg.replace(' ', '%20')}"
        st.markdown(f"[💬 WhatsApp पर भेजें]({wa_url})")
        st.write("---")

# TAB 2: ADD
with tab2:
    st.markdown("### ➕ नई प्रॉपर्टी एंट्री")
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("प्रॉपर्टी का नाम")
        t = st.selectbox("प्रकार", ["प्लॉट (Plot)", "मकान (House)", "दुकान (Shop)", "खेत (Agriculture)"])
        a = st.text_input("एरिया (जैसे: 1200 SqFt)")
        r = st.text_input("कुल कीमत (सिर्फ नंबर लिखें जैसे: 2500000)")
        l = st.text_input("लोकेशन / पता")
        o = st.text_input("मालिक का नाम")
        
        btn = st.form_submit_button("सुरक्षित सेव करें")
        if btn:
            if n and r:
                new_id = f"PROP-{random.randint(103, 999)}"
                st.session_state.properties.append({"id": new_id, "name": n, "type": t, "area": a, "rate": r, "location": l, "owner": o})
                st.success("🎉 प्रॉपर्टी सफलतापूर्वक सेव हो गई!")
                st.balloons()
            else:
                st.error("नाम और कीमत भरना जरूरी है!")

# TAB 3: BILLING
with tab3:
    st.markdown("### 💰 डिजिटल बिल बनाएं")
    p_list = [f"{p['id']} - {p['name']}" for p in st.session_state.properties]
    sel = st.selectbox("प्रॉपर्टी चुनें", p_list)
    
    sel_id = sel.split(" - ")[0]
    p_data = next(item for item in st.session_state.properties if item["id"] == sel_id)
    
    c_name = st.text_input("कस्टमर का नाम")
    c_phone = st.text_input("कस्टमर का मोबाइल")
    
    base = float(p_data['rate'])
    st.write(f"💵 मूल कीमत: ₹{base:,}")
    
    disc = st.number_input("छूट / Discount (₹)", value=0)
    adv = st.number_input("एडवांस पेमेंट (₹)", value=0)
    
    final = base - disc
    pending = final - adv
    
    if st.button("🖨️ रसीद जनरेट करें"):
        st.markdown(f"""
        <div class="bill-box">
            <h2 style="text-align: center;"><b>मां प्रॉपर्टी रसीद</b></h2>
            <p style="text-align: center;">तारीख: {datetime.now().strftime('%d-%m-%Y')}</p>
            <hr>
            <p><b>प्रॉपर्टी:</b> {p_data['name']} ({p_data['id']})</p>
            <p><b>लोकेशन:</b> {p_data['location']}</p>
            <hr>
            <p><b>कस्टमर:</b> {c_name} | <b>मोबाइल:</b> {c_phone}</p>
            <hr>
            <p>मूल कीमत: ₹{base:,}</p>
            <p>छूट: ₹{disc:,}</p>
            <p style="color: green;"><b>कुल सौदा: ₹{final:,}</b></p>
            <p style="color: blue;"><b>जमा एडवांस: ₹{adv:,}</b></p>
            <hr>
            <h3 style="color: red;"><b>बकाया राशि: ₹{pending:,}</b></h3>
        </div>
        """, unsafe_allow_html=True)
