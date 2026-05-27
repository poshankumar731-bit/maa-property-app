import streamlit as st
import random
from datetime import datetime
import json
import os

# पेज सेटअप
st.set_page_config(page_title="Maa Property 2026", layout="wide")

# डेटा को फाइल में सेव करने का फंक्शन (ताकि डेटा कभी न कटे)
DATA_FILE = "bills_history.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# हिस्ट्री लोड करें
if 'bills' not in st.session_state:
    st.session_state.bills = load_data()

# प्रिंटिंग CSS
st.markdown("""
<style>
    @media print {
        .no-print, .no-print * { display: none !important; }
        .print-only { display: block !important; width: 100% !important; margin: 0 !important; }
        @page { size: A4 portrait; margin: 10mm; }
    }
    .print-only { width: 100%; max-width: 480px; border: 2px solid #000; padding: 25px; margin: 10px auto; font-family: 'Arial', sans-serif; }
</style>
""", unsafe_allow_html=True)

# लॉगिन
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    u = st.text_input("यूजर आईडी")
    p = st.text_input("पासवर्ड", type="password")
    if st.button("लॉगिन"):
        if u == "admin" and p == "12345": st.session_state.logged_in = True; st.rerun()
    st.stop()

st.title("⚡ MAA PROPERTY DEALING MUNGELI")

st.markdown('<div class="no-print">', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📄 बिल जनरेट करें", "📜 बिल हिस्ट्री"])

with tab1:
    st.subheader("📝 नई रसीद")
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
    
    if st.button("✅ रसीद सुरक्षित करें"):
        new_bill = {
            "id": random.randint(1000, 9999), "b_name": b_name.upper(), "khasra": khasra,
            "area": area, "c_name": c_name.upper(), "c_phone": c_phone, 
            "base": base, "due": base - adv, "date": datetime.now().strftime('%d-%m-%Y')
        }
        st.session_state.bills.append(new_bill)
        save_data(st.session_state.bills) # फाइल में सेव किया
        st.session_state.active_bill = new_bill
        st.success("रसीद सुरक्षित हो गई है!")

with tab2:
    st.subheader("📜 परमानेंट बिल हिस्ट्री")
    for i, b in enumerate(st.session_state.bills):
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"🆔 {b['id']} | 👤 {b['c_name']}")
        if c2.button("👁️ देखें", key=f"view_{i}"):
            st.session_state.active_bill = b
        if c3.button("🗑️ डिलीट", key=f"del_{i}"):
            st.session_state.bills.pop(i)
            save_data(st.session_state.bills) # अपडेटेड लिस्ट सेव की
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# प्रिंट वाला हिस्सा
if 'active_bill' in st.session_state:
    rb = st.session_state.active_bill
    st.markdown(f"""
    <div class="print-only">
        <h1 style="text-align:center; font-size: 24px; margin: 0;">MAA PROPERTY DEALING</h1>
        <h2 style="text-align:center; font-size: 18px; margin: 0;">MUNGELI</h2>
        <p style="text-align:center; margin: 5px 0;"><b>Contact: 6264024293</b></p>
        <hr style="border-top: 2px solid #000; margin: 10px 0;">
        <p style="margin: 5px 0;"><b>Invoice No:</b> {rb['id']} &nbsp;&nbsp; <b>Date:</b> {rb['date']}</p>
        <p style="margin: 5px 0;"><b>Property:</b> {rb['b_name']} | <b>Khasra:</b> {rb['khasra']}</p>
        <p style="margin: 5px 0;"><b>Area:</b> {rb['area']} SqFt | <b>Buyer:</b> {rb['c_name']}</p>
        <p style="margin: 5px 0; font-size:18px;"><b>Total:</b> ₹{rb['base']:,} | <b>Due:</b> ₹{rb['due']:,}</p>
        <br>
        <div style="display:flex; justify-content: space-between; margin-top: 30px;">
            <div style="text-align:center;">_______<br>Buyer</div>
            <div style="text-align:center;">_______<br>Seller</div>
        </div>
        <p style="text-align:center; margin-top:30px; font-weight:bold;">Proprietor: VISHAL GUPTA</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🖨️ प्रिंट के लिए Ctrl + P दबाएं।")
