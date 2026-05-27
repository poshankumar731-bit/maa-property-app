import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Maa Property 2026", layout="wide")

# प्रिंट के लिए एकदम सटीक CSS
st.markdown("""
<style>
    /* प्रिंट करते समय पूरी स्क्रीन और प्रिंटिंग एरिया के लिए सेटिंग */
    @media print {
        .no-print, .no-print * { display: none !important; }
        .print-only { 
            display: block !important; 
            width: 100% !important; 
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        @page { size: A4 portrait; margin: 5mm; }
        body { margin: 0; padding: 0; }
    }
    
    /* स्क्रीन के लिए रसीद का स्टाइल */
    .print-only { 
        width: 100%; max-width: 450px; border: 2px solid #000; 
        padding: 20px; margin: 10px auto; font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# लॉगिन सिस्टम
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    u = st.text_input("यूजर आईडी")
    p = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if u == "admin" and p == "12345": st.session_state.logged_in = True; st.rerun()
    st.stop()

if 'bills' not in st.session_state: st.session_state.bills = []

st.title("⚡ MAA PROPERTIES MUNGELI")

# 'no-print' सेक्शन: जो प्रिंट में नहीं आएगा
st.markdown('<div class="no-print">', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📄 बिल जनरेट करें", "📜 बिल हिस्ट्री"])
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        b_name = st.text_input("प्रॉपर्टी का नाम")
        khasra = st.text_input("खसरा नंबर")
        area = st.text_input("एरिया (SqFt)")
    with c2:
        c_name = st.text_input("खरीदार का नाम")
        c_phone = st.text_input("खरीदार मोबाइल", value="6264024293")
        base = st.number_input("कुल राशि", value=0)
        adv = st.number_input("एडवांस", value=0)
    
    if st.button("✅ रसीद तैयार करें"):
        st.session_state.active_bill = {
            "id": random.randint(1000, 9999), "b_name": b_name.upper(), "khasra": khasra,
            "area": area, "c_name": c_name.upper(), "c_phone": c_phone, 
            "base": base, "due": base - adv, "date": datetime.now().strftime('%d-%m-%Y')
        }
        st.session_state.bills.append(st.session_state.active_bill)

with tab2:
    for i, b in enumerate(st.session_state.bills):
        c1, c2 = st.columns([4, 1])
        c1.write(f"🆔 {b['id']} | 👤 {b['c_name']}")
        if c2.button("🗑️", key=f"del_{i}"):
            st.session_state.bills.pop(i); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# केवल बिल वाला हिस्सा (print-only)
if 'active_bill' in st.session_state:
    rb = st.session_state.active_bill
    st.markdown(f"""
    <div class="print-only">
        <h1 style="text-align:center; font-size: 24px; margin: 0;">MAA PROPERTIES</h1>
        <p style="text-align:center; margin: 0;"><b>MUNGELI | Contact: 6264024293</b></p>
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0;"><b>Invoice No:</b> {rb['id']} &nbsp;&nbsp; <b>Date:</b> {rb['date']}</p>
        <p style="margin: 5px 0;"><b>Property:</b> {rb['b_name']} (Khasra: {rb['khasra']})</p>
        <p style="margin: 5px 0;"><b>Area:</b> {rb['area']} SqFt</p>
        <p style="margin: 5px 0;"><b>Buyer:</b> {rb['c_name']}</p>
        <p style="margin: 5px 0; font-size:18px;"><b>Total:</b> ₹{rb['base']:,} | <b>Due:</b> ₹{rb['due']:,}</p>
        <br>
        <div style="display:flex; justify-content: space-between; margin-top: 20px;">
            <div>_______<br>Buyer</div><div>_______<br>Seller</div>
        </div>
        <p style="text-align:center; margin-top:20px; font-weight:bold;">Proprietor: VISHAL GUPTA</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🖨️ प्रिंट करने के लिए Ctrl + P दबाएं।")
